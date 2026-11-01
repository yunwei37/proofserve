#include <lean/lean.h>
#include <time.h>
LEAN_EXPORT lean_obj_res rv_thread_cpu_ns(lean_obj_arg w) { struct timespec t; clock_gettime(CLOCK_THREAD_CPUTIME_ID,&t); return lean_io_result_mk_ok(lean_box_uint64((uint64_t)t.tv_sec*1000000000ull+t.tv_nsec)); }
