
#include <lean/lean.h>
#include <stdint.h>
#include <time.h>
LEAN_EXPORT lean_obj_res ps_pool_spin(uint64_t duration, lean_obj_arg w) {
 struct timespec t;clock_gettime(CLOCK_THREAD_CPUTIME_ID,&t);
 uint64_t start=(uint64_t)t.tv_sec*1000000000ULL+t.tv_nsec, now=start,v=1;
 do { for(unsigned i=0;i<2048;i++) v=v*6364136223846793005ULL+1;
 clock_gettime(CLOCK_THREAD_CPUTIME_ID,&t);now=(uint64_t)t.tv_sec*1000000000ULL+t.tv_nsec;
 } while(now-start<duration);
 return lean_io_result_mk_ok(lean_box_uint64(v));
}
