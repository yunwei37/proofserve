#!/usr/bin/env python3
"""Linux per-task retired-instruction counters, including inherited threads.
Uses the kernel perf_event_attr ABI and sysfs PMU descriptors; no sampling.
"""
import ctypes
import os
from pathlib import Path
import struct

LIBC=ctypes.CDLL(None,use_errno=True)
PERF_EVENT_OPEN=298  # x86-64; checked before use
class Attr(ctypes.Structure):
    _fields_=[("type",ctypes.c_uint32),("size",ctypes.c_uint32),
              ("config",ctypes.c_uint64),("sample_period",ctypes.c_uint64),
              ("sample_type",ctypes.c_uint64),("read_format",ctypes.c_uint64),
              ("flags",ctypes.c_uint64),("wakeup_events",ctypes.c_uint32),
              ("bp_type",ctypes.c_uint32),("config1",ctypes.c_uint64),
              ("config2",ctypes.c_uint64),("branch_sample_type",ctypes.c_uint64),
              ("sample_regs_user",ctypes.c_uint64),("sample_stack_user",ctypes.c_uint32),
              ("clockid",ctypes.c_int32),("sample_regs_intr",ctypes.c_uint64),
              ("aux_watermark",ctypes.c_uint32),("sample_max_stack",ctypes.c_uint16),
              ("reserved",ctypes.c_uint16),("aux_sample_size",ctypes.c_uint32),
              ("reserved3",ctypes.c_uint32),("sig_data",ctypes.c_uint64)]
def pmus():
    if os.uname().machine!="x86_64":raise RuntimeError("this control uses x86-64 syscall ABI")
    result={}
    for name in ("cpu_core","cpu_atom"):
        base=Path("/sys/bus/event_source/devices")/name
        event=(base/"events/instructions").read_text().strip()
        if event!="event=0xc0":raise RuntimeError("unhandled native instruction descriptor "+event)
        result[name]={"type":int((base/"type").read_text()),"config":0xc0,
                      "event":event,"cpus":(base/"cpus").read_text().strip()}
    return result
def open_counters(pid):
    counters={}
    try:
        for name,desc in pmus().items():
            for mode in ("user","kernel"):
                a=Attr();a.size=ctypes.sizeof(a);a.type=desc["type"];a.config=desc["config"]
                a.read_format=3 # PERF_FORMAT_TOTAL_TIME_ENABLED | TOTAL_TIME_RUNNING
                # disabled, inherit, exclude_hv, enable_on_exec. All task threads
                # inherit from this pre-exec task; the read includes exited children.
                a.flags=(1<<0)|(1<<1)|(1<<6)|(1<<12)
                a.flags|=(1<<5) if mode=="user" else (1<<4)
                fd=LIBC.syscall(PERF_EVENT_OPEN,ctypes.byref(a),pid,-1,-1,8)
                if fd<0:raise OSError(ctypes.get_errno(),os.strerror(ctypes.get_errno()))
                counters[name+"_"+mode]=fd
        return counters
    except BaseException:
        for fd in counters.values():os.close(fd)
        raise
def read_counters(counters):
    result={}
    try:
        for name,fd in counters.items():
            value,enabled,running=struct.unpack("QQQ",os.read(fd,24))
            result[name]={"instructions":value,"enabled_ns":enabled,"running_ns":running,
                          "coverage":running/enabled if enabled else None}
        return result
    finally:
        for fd in counters.values():os.close(fd)
