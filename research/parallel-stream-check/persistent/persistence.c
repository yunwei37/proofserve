/* Timed official-runtime persistence ablation. Mathematical kernel unchanged. */
#define _GNU_SOURCE
#include <lean/lean.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
/* Matched SDK commit5045d005: BaseIO is erased; this official export takes one arg. */
extern lean_obj_res lean_runtime_mark_persistent(lean_obj_arg);
typedef unsigned long long U;
enum { PERSISTENT=0, ST=1, MT_ACTIVE=2, SCALAR=3, STICKY=4, KINDS=5 };
static const char *names[4]={"Nat.add","Nat.mul","c0","c1"};
static int configured,enabled,diagnostic;
typedef struct {
 uint64_t calls,wall_ns,cpu_ns;
 uint64_t before[KINDS],after[KINDS],ready[KINDS],input[KINDS];
 uint64_t ci_before[4][KINDS],ci_after[4][KINDS];
 uint64_t fields_before[4][KINDS],fields_after[4][KINDS];
} Stats;
static Stats st;
static uint64_t clockns(clockid_t id) {
 struct timespec t;clock_gettime(id,&t);
 return (uint64_t)t.tv_sec*1000000000ull+(uint64_t)t.tv_nsec;
}
static void configure(void) {
 if(configured)return;
 const char *p=getenv("PARALLEL_PERSIST_BASE");
 if(p && strcmp(p,"0") && strcmp(p,"1"))abort();
 enabled=p && !strcmp(p,"1");
 p=getenv("PARALLEL_PERSIST_DIAGNOSTIC");
 diagnostic=p && !strcmp(p,"1");configured=1;
}
static unsigned kind(b_lean_obj_arg o) {
 if(lean_is_scalar(o))return SCALAR;
 if(lean_is_persistent(o))return PERSISTENT;
 if(lean_is_st(o))return ST;
 return lean_is_unstuck_mt(o)?MT_ACTIVE:STICKY;
}
static void fields(b_lean_obj_arg base,uint64_t counts[4][KINDS]) {
 if(!diagnostic || lean_is_scalar(base) || !lean_is_ctor(base))return;
 unsigned n=lean_ctor_num_objs(base);if(n>4)n=4;
 for(unsigned i=0;i<n;i++)counts[i][kind(lean_ctor_get(base,i))]++;
}
static void cis(b_lean_obj_arg probes,uint64_t counts[4][KINDS]) {
 if(!diagnostic)return;
 for(size_t i=0;i<lean_array_size(probes);i++) {
  lean_object *pair=lean_array_uget(probes,i);
  const char *name=lean_string_cstr(lean_ctor_get(pair,0));
  lean_object *ci=lean_ctor_get(pair,1);
  for(unsigned j=0;j<4;j++)if(!strcmp(name,names[j]))counts[j][kind(ci)]++;
 }
}
LEAN_EXPORT lean_obj_res ps_persistence_frontier(lean_obj_arg base,
 b_lean_obj_arg probes,b_lean_obj_arg input,lean_obj_arg world) {
 configure();st.calls++;st.before[kind(base)]++;
 fields(base,st.fields_before);cis(probes,st.ci_before);
 if(diagnostic)for(size_t i=0;i<lean_array_size(input);i++)st.input[kind(lean_array_uget(input,i))]++;
 uint64_t w0=clockns(CLOCK_MONOTONIC),c0=clockns(CLOCK_THREAD_CPUTIME_ID);
 if(enabled)base=lean_runtime_mark_persistent(base);
 uint64_t c1=clockns(CLOCK_THREAD_CPUTIME_ID),w1=clockns(CLOCK_MONOTONIC);
 st.wall_ns+=w1-w0;st.cpu_ns+=c1-c0;
 st.after[kind(base)]++;fields(base,st.fields_after);cis(probes,st.ci_after);
 return lean_io_result_mk_ok(base);
}
LEAN_EXPORT lean_obj_res ps_persistence_ready(b_lean_obj_arg base,lean_obj_arg world) {
 configure();st.ready[kind(base)]++;
 return lean_io_result_mk_ok(lean_box(0));
}
LEAN_EXPORT lean_obj_res ps_rc_kind(b_lean_obj_arg obj,lean_obj_arg world) {
 return lean_io_result_mk_ok(lean_box(kind(obj)));
}
LEAN_EXPORT lean_obj_res ps_persistence_summary(lean_obj_arg world) {
 configure();char buf[8192];size_t pos=0;
 #define ADD(...) do{int n=snprintf(buf+pos,sizeof(buf)-pos,__VA_ARGS__);if(n<0||(size_t)n>=sizeof(buf)-pos)abort();pos+=(size_t)n;}while(0)
 #define HIST(a) ADD("[%llu,%llu,%llu,%llu,%llu]",(U)(a)[0],(U)(a)[1],(U)(a)[2],(U)(a)[3],(U)(a)[4])
 ADD("{\"enabled\":%s,\"diagnostic\":%s,\"class_order\":[\"persistent\",\"single_thread\",\"active_MT\",\"scalar\",\"sticky_frozen\"],\"calls\":%llu,\"window_wall_ns\":%llu,\"window_thread_cpu_ns\":%llu,\"base_before\":",
 enabled?"true":"false",diagnostic?"true":"false",(U)st.calls,(U)st.wall_ns,(U)st.cpu_ns);
 HIST(st.before);ADD(",\"base_after\":");HIST(st.after);
 ADD(",\"after_enqueue\":");HIST(st.ready);ADD(",\"input_ci_observations\":");HIST(st.input);
 ADD(",\"base_fields\":[");
 for(unsigned i=0;i<4;i++){if(i)ADD(",");ADD("{\"index\":%u,\"before\":",i);HIST(st.fields_before[i]);ADD(",\"after\":");HIST(st.fields_after[i]);ADD("}");}
 ADD("],\"existing_ci_probes\":[");
 for(unsigned i=0;i<4;i++){if(i)ADD(",");ADD("{\"name\":\"%s\",\"before\":",names[i]);HIST(st.ci_before[i]);ADD(",\"after\":");HIST(st.ci_after[i]);ADD("}");}
 ADD("]}");
 lean_object *text=lean_mk_string(buf);memset(&st,0,sizeof(st));
 return lean_io_result_mk_ok(text);
 #undef HIST
 #undef ADD
}
