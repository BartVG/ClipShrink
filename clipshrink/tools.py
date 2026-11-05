"""Finds the bundled programs and runs them without console windows."""
import ctypes, subprocess, sys
from ctypes import wintypes
from pathlib import Path

NOWIN = 0x08000000


def _base():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "vendor"
    return Path(__file__).resolve().parents[1] / "vendor"


def ffmpeg():
    return str(_base() / "ffmpeg" / "bin" / "ffmpeg.exe")


def ffprobe():
    return str(_base() / "ffmpeg" / "bin" / "ffprobe.exe")


def mpv():
    return str(_base() / "mpv" / "mpv.exe")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          stdin=subprocess.DEVNULL, creationflags=NOWIN, **kw)


_k = ctypes.WinDLL("kernel32", use_last_error=True)
_k.CreateJobObjectW.restype = wintypes.HANDLE
_k.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
_k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
_k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
_k.CreateFileW.restype = wintypes.HANDLE
_k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                           wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
_k.SetFileTime.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
_k.CloseHandle.argtypes = [wintypes.HANDLE]
_nt = ctypes.WinDLL("ntdll")
_nt.NtSuspendProcess.argtypes = [wintypes.HANDLE]
_nt.NtResumeProcess.argtypes = [wintypes.HANDLE]


class _Basic(ctypes.Structure):
    _fields_ = [("a", ctypes.c_int64), ("b", ctypes.c_int64), ("LimitFlags", wintypes.DWORD),
                ("c", ctypes.c_size_t), ("d", ctypes.c_size_t), ("e", wintypes.DWORD),
                ("f", ctypes.c_size_t), ("g", wintypes.DWORD), ("h", wintypes.DWORD)]


class _Ext(ctypes.Structure):
    _fields_ = [("basic", _Basic), ("io", ctypes.c_uint64 * 6), ("p", ctypes.c_size_t * 4)]


_job = None


def bind_to_us(proc):
    """FFmpeg dies with this app, even on a hard crash."""
    global _job
    if _job is None:
        _job = _k.CreateJobObjectW(None, None)
        info = _Ext()
        info.basic.LimitFlags = 0x2000  # KILL_ON_JOB_CLOSE
        _k.SetInformationJobObject(_job, 9, ctypes.byref(info), ctypes.sizeof(info))
    _k.AssignProcessToJobObject(_job, wintypes.HANDLE(int(proc._handle)))


def suspend(proc):
    _nt.NtSuspendProcess(wintypes.HANDLE(int(proc._handle)))


def resume(proc):
    _nt.NtResumeProcess(wintypes.HANDLE(int(proc._handle)))


def set_file_times(path, created_ns, modified_ns):
    def ft(ns):
        v = ns // 100 + 116444736000000000
        return wintypes.FILETIME(v & 0xFFFFFFFF, v >> 32)
    h = _k.CreateFileW(str(path), 0x100, 3, None, 3, 0x02000000, None)
    if h in (None, wintypes.HANDLE(-1).value):
        raise OSError(f"cannot set dates on {path}")
    try:
        a, b = ft(created_ns), ft(modified_ns)
        if not _k.SetFileTime(h, ctypes.byref(a), None, ctypes.byref(b)):
            raise OSError(f"cannot set dates on {path}")
    finally:
        _k.CloseHandle(h)


def keep_awake(on):
    """Stops Windows sleeping in the middle of a batch."""
    _k.SetThreadExecutionState(0x80000000 | (0x00000001 if on else 0))
