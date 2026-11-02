/* Pinned Lean4.34.1 checked-frontier commit adapter.
 * Mathematical checking remains lean_add_decl, before token construction.
 * This is trusted coordination glue, not a new type checker.
 */
#include <lean/lean.h>
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
