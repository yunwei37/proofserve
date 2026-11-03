#define _GNU_SOURCE
#include <lean/lean.h>
#include <sched.h>
#include <pthread.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/syscall.h>
typedef unsigned long long U;
typedef struct { uint64_t a,b,cpu; size_t index; } Interval;
typedef struct {
 long tid;
 uint64_t wall0,cpu0; int core0;
 uint64_t count[24], cpu[24], hb[24], narrow[24], narrow_hb[24];
 uint64_t max_job, migrations;
 size_t job_index;
 Interval *v; size_t len,cap;
} Local;
static Local *registry[128];
static size_t registry_n;
static pthread_mutex_t registry_lock=PTHREAD_MUTEX_INITIALIZER;
static _Thread_local Local *local;
static _Thread_local int bound_core=-1;
static int cpus[24],cpu_n,coordinator_cpu;
static cpu_set_t original_allowed;
static int have_allowed;
static atomic_int wave_slot;
static uint64_t wave0,wavecpu0,union_sum,batch_sum,batch_cpu_sum,wave_max_sum,waves;
static size_t wave_jobs;

static FILE *tracefile;
static int trace_configured;
static uint64_t phase_ns[6],wave_id;
static void configure_trace(void) {
 if(trace_configured)return;
 trace_configured=1;const char *p=getenv("PARALLEL_WALL_TRACE");
 if(p && *p){tracefile=fopen(p,"ax");if(!tracefile)abort();}
}
LEAN_EXPORT lean_obj_res ps_trace_enabled(lean_obj_arg w) {
 configure_trace();return lean_io_result_mk_ok(lean_box(tracefile!=NULL));
}
LEAN_EXPORT lean_obj_res ps_trace_plan(b_lean_obj_arg text,lean_obj_arg w) {
 configure_trace();if(tracefile){fputs(lean_string_cstr(text),tracefile);fputc(10,tracefile);fflush(tracefile);}
 return lean_io_result_mk_ok(lean_box(0));
}
static uint64_t ns(clockid_t id) {struct timespec t;clock_gettime(id,&t);return (uint64_t)t.tv_sec*1000000000+t.tv_nsec;}
static lean_obj_res ok(void) {return lean_io_result_mk_ok(lean_box(0));}
static Local *getlocal(void) {
 if(local)return local;
 local=calloc(1,sizeof(Local));if(!local)abort();
 local->tid=(long)syscall(SYS_gettid);
 pthread_mutex_lock(&registry_lock);
 if(registry_n==128)abort();
 registry[registry_n++]=local;pthread_mutex_unlock(&registry_lock);
 return local;
}
static int bindcpu(int cpu) {
 if(bound_core==cpu)return 0;
 cpu_set_t mask;CPU_ZERO(&mask);CPU_SET(cpu,&mask);
 int rc=sched_setaffinity(0,sizeof(mask),&mask);if(!rc)bound_core=cpu;return rc;
}
LEAN_EXPORT lean_obj_res ps_configure_placement(b_lean_obj_arg text,size_t coor,lean_obj_arg w) {
 const char *s=lean_string_cstr(text);int selected[24],n=0;
 if(!have_allowed){if(sched_getaffinity(0,sizeof(original_allowed),&original_allowed))return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("cannot read initial affinity")));have_allowed=1;}
 while(*s) {
  const char *end=s;long x=0;
  while(*end>='0'&&*end<='9'){x=x*10+(*end-'0');end++;if(x>=24)break;}
  if(end==s||x<0||x>=24||n==24||!CPU_ISSET(x,&original_allowed))return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("invalid worker CPU map")));
  for(int i=0;i<n;i++)if(selected[i]==x)return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("duplicate worker core")));
  selected[n++]=(int)x;s=end;if(*s==',')s++;else if(*s) return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("invalid CPU separator")));
 }
 if(n && (coor>=24||!CPU_ISSET(coor,&original_allowed)))return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("invalid coordinator CPU")));
 for(int i=0;i<n;i++)cpus[i]=selected[i];
 cpu_n=n;coordinator_cpu=(int)coor;atomic_store(&wave_slot,0);

 if(n && bindcpu(coordinator_cpu))return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("coordinator affinity denied")));
 return ok();
}
LEAN_EXPORT lean_obj_res ps_bind_coordinator(lean_obj_arg w) {
 if(cpu_n && bindcpu(coordinator_cpu))return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("coordinator binding denied")));
 return ok();
}
LEAN_EXPORT lean_obj_res ps_bind_worker(lean_obj_arg w) {
 if(!cpu_n)return ok();
 int slot=atomic_fetch_add(&wave_slot,1);
 if(slot>=cpu_n)return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("active wave exceeds distinct CPU pins")));
 if(bindcpu(cpus[slot]))return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("worker binding denied")));
 return ok();
}
LEAN_EXPORT lean_obj_res ps_trace_job(size_t index,lean_obj_arg w) {
 getlocal()->job_index=index;return ok();
}
LEAN_EXPORT lean_obj_res ps_trace_phase(size_t phase,lean_obj_arg w) {
 if(phase<6)phase_ns[phase]=ns(CLOCK_MONOTONIC);return ok();
}
LEAN_EXPORT lean_obj_res ps_wave_begin(size_t jobs,lean_obj_arg w) {
 atomic_store(&wave_slot,0);wave_jobs=jobs;wave0=ns(CLOCK_MONOTONIC);phase_ns[0]=wave0;wavecpu0=ns(CLOCK_PROCESS_CPUTIME_ID);return ok();
}
LEAN_EXPORT lean_obj_res ps_profile_begin(lean_obj_arg w) {
 Local *l=getlocal();l->core0=sched_getcpu();l->wall0=ns(CLOCK_MONOTONIC);l->cpu0=ns(CLOCK_THREAD_CPUTIME_ID);return ok();
}
LEAN_EXPORT lean_obj_res ps_profile_end(uint64_t hb,lean_obj_arg w) {
 uint64_t cpu1=ns(CLOCK_THREAD_CPUTIME_ID),wall1=ns(CLOCK_MONOTONIC);Local *l=local;
 int core=l->core0;
 if(core<0||core>=24)abort();
 if(sched_getcpu()!=core)l->migrations++;
 uint64_t cost=cpu1-l->cpu0;l->count[core]++;l->cpu[core]+=cost;l->hb[core]+=hb;
 if(wave_jobs<=8){l->narrow[core]++;l->narrow_hb[core]+=hb;}
 if(cost>l->max_job)l->max_job=cost;
 if(l->len==l->cap){l->cap=l->cap?2*l->cap:64;l->v=realloc(l->v,l->cap*sizeof(Interval));if(!l->v)abort();}
 l->v[l->len++]=(Interval){l->wall0,wall1,cost,l->job_index};return ok();
}
static int by_start(const void*a,const void*b){const Interval*x=a,*y=b;return x->a<y->a?-1:x->a>y->a?1:0;}
LEAN_EXPORT lean_obj_res ps_wave_finish(lean_obj_arg w) {
 size_t n=0;uint64_t maxjob=0;
 for(size_t i=0;i<registry_n;i++){n+=registry[i]->len;if(registry[i]->max_job>maxjob)maxjob=registry[i]->max_job;}
 Interval *all=n?malloc(n*sizeof(Interval)):NULL;size_t k=0;
 for(size_t i=0;i<registry_n;i++){Local*l=registry[i];if(l->len)memcpy(all+k,l->v,l->len*sizeof(Interval));k+=l->len;l->len=0;l->max_job=0;}
 configure_trace();
 if(tracefile) {
  fprintf(tracefile,"{\"event\":\"wave\",\"id\":%llu,\"width\":%zu,\"phase_ns\":[",
   (U)wave_id++,wave_jobs);
  for(unsigned i=0;i<6;i++)fprintf(tracefile,"%s%llu",i?",":"",(U)phase_ns[i]);
  fprintf(tracefile,"],\"jobs\":[");
  for(size_t i=0;i<n;i++)fprintf(tracefile,"%s[%zu,%llu,%llu,%llu]",i?",":"",
   all[i].index,(U)all[i].a,(U)all[i].b,(U)all[i].cpu);
  fprintf(tracefile,"]}");fputc(10,tracefile);fflush(tracefile);
 }
 if(n){qsort(all,n,sizeof(Interval),by_start);uint64_t a=all[0].a,b=all[0].b;
  for(size_t i=1;i<n;i++){if(all[i].a<=b){if(all[i].b>b)b=all[i].b;}else{union_sum+=b-a;a=all[i].a;b=all[i].b;}}union_sum+=b-a;}
 free(all);wave_max_sum+=maxjob;waves++;
 batch_sum+=ns(CLOCK_MONOTONIC)-wave0;batch_cpu_sum+=ns(CLOCK_PROCESS_CPUTIME_ID)-wavecpu0;
 return ok();
}
LEAN_EXPORT lean_obj_res ps_profile_summary(lean_obj_arg w) {
 size_t cap=1024*1024,pos=0;char*buf=malloc(cap);if(!buf)abort();
 #define ADD(...) do{int z=snprintf(buf+pos,cap-pos,__VA_ARGS__);if(z<0||(size_t)z>=cap-pos)abort();pos+=z;}while(0)
 uint64_t totalcpu=0,totalhb=0,checks=0;
 for(size_t i=0;i<registry_n;i++)for(int c=0;c<24;c++){totalcpu+=registry[i]->cpu[c];totalhb+=registry[i]->hb[c];checks+=registry[i]->count[c];}
 ADD("{\"kernel_union_ns\":%llu,\"batch_wall_ns\":%llu,\"batch_cpu_ns\":%llu,\"kernel_cpu_ns\":%llu,\"raw_HB\":%llu,\"checks\":%llu,\"waves\":%llu,\"sum_wave_max_cpu_ns\":%llu,\"workers\":[",(U)union_sum,(U)batch_sum,(U)batch_cpu_sum,(U)totalcpu,(U)totalhb,(U)checks,(U)waves,(U)wave_max_sum);
 int first=1;
 for(size_t i=0;i<registry_n;i++)for(int c=0;c<24;c++)if(registry[i]->count[c]){
  Local*l=registry[i];if(!first)ADD(",");first=0;
  ADD("{\"tid\":%ld,\"cpu\":%d,\"checks\":%llu,\"cpu_ns\":%llu,\"raw_HB\":%llu,\"narrow_checks\":%llu,\"narrow_HB\":%llu,\"within_check_migrations\":%llu}",l->tid,c,(U)l->count[c],(U)l->cpu[c],(U)l->hb[c],(U)l->narrow[c],(U)l->narrow_hb[c],(U)l->migrations);
 }
 ADD("]}");
 for(size_t i=0;i<registry_n;i++){Local*l=registry[i];memset(l->count,0,sizeof(l->count));memset(l->cpu,0,sizeof(l->cpu));memset(l->hb,0,sizeof(l->hb));memset(l->narrow,0,sizeof(l->narrow));memset(l->narrow_hb,0,sizeof(l->narrow_hb));l->migrations=0;}
 union_sum=batch_sum=batch_cpu_sum=wave_max_sum=waves=0;
 lean_object*out=lean_mk_string(buf);free(buf);return lean_io_result_mk_ok(out);
 #undef ADD
}
LEAN_EXPORT lean_obj_res ps_cpu_id(lean_obj_arg w){return lean_io_result_mk_ok(lean_box_uint32((uint32_t)sched_getcpu()));}
