#include <lean/lean.h>
#include <time.h>
LEAN_EXPORT lean_obj_res ck_cpu_ns(lean_obj_arg world) {
 struct timespec t; clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&t);
 return lean_io_result_mk_ok(lean_box_uint64((uint64_t)t.tv_sec*1000000000ull+t.tv_nsec));
}

LEAN_EXPORT lean_obj_res l_cpuNs(lean_obj_arg world) { return ck_cpu_ns(world); }

LEAN_EXPORT lean_obj_res ck_thread_cpu_ns(lean_obj_arg world) {
 struct timespec t; clock_gettime(CLOCK_THREAD_CPUTIME_ID,&t);
 return lean_io_result_mk_ok(lean_box_uint64((uint64_t)t.tv_sec*1000000000ull+t.tv_nsec));
}
LEAN_EXPORT lean_obj_res l_threadCpuNs(lean_obj_arg world) { return ck_thread_cpu_ns(world); }
