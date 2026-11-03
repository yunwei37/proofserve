#define _GNU_SOURCE
/* Pinned Lean4.34.1 checked-frontier commit adapter.
 * Mathematical checking remains lean_add_decl, before token construction.
 * This is trusted coordination glue, not a new type checker.
 */
#include <lean/lean.h>
#include <stdlib.h>
#include <string.h>
extern lean_obj_res lean_environment_add(lean_obj_arg env, lean_obj_arg cinfo);

LEAN_EXPORT lean_obj_res ps_commit_checked(lean_obj_arg base, lean_obj_arg tokens,
                                          lean_obj_arg world) {
    size_t count = lean_array_size(tokens);
    /* CheckedToken layout: frontier, actual ConstantInfo, original index.
       Validate all owners before changing any destination. */
    for (size_t i = 0; i < count; ++i) {
        lean_object *token = lean_array_uget(tokens, i);
        if (lean_ctor_get(token, 0) != base) {
            lean_dec(tokens);
            lean_dec(base);
            return lean_io_result_mk_error(
                lean_mk_io_user_error(lean_mk_string("invariant: stale checked frontier")));
        }
    }
    lean_inc(base);
    lean_object *dest = base;
    for (size_t i = 0; i < count; ++i) {
        lean_object *ci = lean_ctor_get(lean_array_uget(tokens, i), 1);
        lean_inc(ci);
        dest = lean_environment_add(dest, ci); /* original upstream map insertion */
    }
    lean_dec(tokens);
    lean_dec(base);
    return lean_io_result_mk_ok(dest);
}

#include <time.h>
LEAN_EXPORT lean_obj_res ps_process_ns(lean_obj_arg world) {
 struct timespec ts; clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&ts);
 uint64_t ns=(uint64_t)ts.tv_sec*1000000000ull+(uint64_t)ts.tv_nsec;
 return lean_io_result_mk_ok(lean_box_uint64(ns));
}

LEAN_EXPORT lean_obj_res ps_thread_ns(lean_obj_arg world) {
 struct timespec ts; clock_gettime(CLOCK_THREAD_CPUTIME_ID,&ts);
 uint64_t ns=(uint64_t)ts.tv_sec*1000000000ull+(uint64_t)ts.tv_nsec;
 return lean_io_result_mk_ok(lean_box_uint64(ns));
}


/* Official primitive at an already joined frontier, no object-layout inspection. */
extern lean_obj_res lean_runtime_mark_persistent(lean_obj_arg);
LEAN_EXPORT lean_obj_res ps_persist_base(lean_obj_arg base,lean_obj_arg world) {
 const char *p=getenv("PROOFSERVE_PERSIST");
 return lean_io_result_mk_ok(p && !strcmp(p,"0") ? base : lean_runtime_mark_persistent(base));
}

#include <sched.h>
#include <unistd.h>
#include <stdio.h>
static int ps_selected(cpu_set_t *out) {
 cpu_set_t allowed; CPU_ZERO(out);
 if(sched_getaffinity(0,sizeof(allowed),&allowed))return 0;
 int count=0,has_p=0;
 for(int i=0;i<CPU_SETSIZE;i++)if(CPU_ISSET(i,&allowed)) {
  char path[180];snprintf(path,sizeof(path),"/sys/devices/system/cpu/cpu%d/topology/core_type",i);
  FILE*f=fopen(path,"r");int type=0;if(f){int ch=fgetc(f);if(ch>=48 && ch<=57)type=ch-48;fclose(f);}
  if(type==2){CPU_SET(i,out);count++;has_p=1;}
 }
 if(!has_p){*out=allowed;count=CPU_COUNT(&allowed);}
 return count;
}
LEAN_EXPORT lean_obj_res ps_default_workers(lean_obj_arg world) {
 cpu_set_t selected;int n=ps_selected(&selected);if(n<1)n=1;if(n>4)n=4;
 return lean_io_result_mk_ok(lean_box_uint32(n));
}
LEAN_EXPORT lean_obj_res ps_pin_performance(lean_obj_arg world) {
 cpu_set_t selected;int n=ps_selected(&selected);
 if(n>0 && sched_setaffinity(0,sizeof(selected),&selected))
   return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("cannot bind performance cores")));
 return lean_io_result_mk_ok(lean_box(0));
}

#include <sys/resource.h>
LEAN_EXPORT lean_obj_res ps_total_cpu_ns(lean_obj_arg world) {
 struct rusage a,b;getrusage(RUSAGE_SELF,&a);getrusage(RUSAGE_CHILDREN,&b);
 uint64_t us=(a.ru_utime.tv_sec+a.ru_stime.tv_sec+b.ru_utime.tv_sec+b.ru_stime.tv_sec)*1000000ull+
 a.ru_utime.tv_usec+a.ru_stime.tv_usec+b.ru_utime.tv_usec+b.ru_stime.tv_usec;
 return lean_io_result_mk_ok(lean_box_uint64(us*1000ull));
}

#include <sys/file.h>
#include <fcntl.h>
#include <errno.h>
LEAN_EXPORT lean_obj_res ps_checkpoint_lock(b_lean_obj_arg path,lean_obj_arg world) {
 int fd=open(lean_string_cstr(path),O_CREAT|O_RDWR|O_CLOEXEC,0600);
 if(fd<0)return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string("cannot open checkpoint lock")));
 if(flock(fd,LOCK_EX|LOCK_NB)){close(fd);return lean_io_result_mk_error(
  lean_mk_io_user_error(lean_mk_string("checkpoint directory is already in use")));}
 /* Process-lifetime descriptor: inherited exec children close it. */
 return lean_io_result_mk_ok(lean_box(0));
}
