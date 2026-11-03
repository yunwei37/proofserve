#include <lean/lean.h>
#include <stdint.h>
#include <time.h>

/* Observation only: the original kernel and its input terms are unchanged. */
LEAN_EXPORT lean_obj_res proofserve_process_cpu_ns(b_lean_obj_arg world) {
    struct timespec now;
    if (clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &now) != 0)
        return lean_io_result_mk_error(lean_mk_io_user_error(
            lean_mk_string("CLOCK_PROCESS_CPUTIME_ID unavailable")));
    uint64_t ns = (uint64_t)now.tv_sec * 1000000000ULL + (uint64_t)now.tv_nsec;
    return lean_io_result_mk_ok(lean_box_uint64(ns));
}
