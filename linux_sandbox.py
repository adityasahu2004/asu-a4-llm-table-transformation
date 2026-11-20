"""Linux coursework guard: kernel network/process filter plus Python file audit.

The generated program is also subject to execution.check_code. This layered guard
is intended for the assignment's constrained pandas programs, not arbitrary native
hostile code. It fails closed when the kernel filter cannot be installed.
"""
import ctypes
import errno
import os
from pathlib import Path
import platform
import sys


class SandboxUnavailable(RuntimeError):
    pass


def install(work):
    work = Path(work).resolve()
    machine = platform.machine().lower()
    if machine in {'x86_64', 'amd64'}:
        arch = 0xc000003e
        denied = list(range(41, 60)) + [101, 155, 165, 166, 272, 288, 299,
            303, 304, 307, 308, 310, 311, 321, 322, 435, 438]
    elif machine in {'aarch64', 'arm64'}:
        arch = 0xc00000b7
        denied = list(range(198, 213)) + [39, 40, 41, 97, 117, 220, 221,
            242, 243, 264, 265, 268, 269, 270, 271, 280, 281, 435, 438]
    else:
        raise SandboxUnavailable('Unsupported Linux architecture: ' + machine)

    class Filter(ctypes.Structure):
        _fields_ = [('code', ctypes.c_ushort), ('jt', ctypes.c_ubyte),
                    ('jf', ctypes.c_ubyte), ('k', ctypes.c_uint)]

    class Program(ctypes.Structure):
        _fields_ = [('len', ctypes.c_ushort), ('filter', ctypes.POINTER(Filter))]

    # Architecture mismatch is fatal; denied syscalls return EPERM.
    instructions = [(0x20, 0, 0, 4), (0x15, 1, 0, arch),
                    (0x06, 0, 0, 0x80000000), (0x20, 0, 0, 0)]
    for number in sorted(set(denied)):
        instructions.extend([(0x15, 0, 1, number), (0x06, 0, 0, 0x00050000 | errno.EPERM)])
    instructions.append((0x06, 0, 0, 0x7fff0000))
    filters = (Filter * len(instructions))(*(Filter(*row) for row in instructions))
    program = Program(len(filters), filters)
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(38, 1, 0, 0, 0) or libc.prctl(22, 2, ctypes.byref(program), 0, 0):
        raise SandboxUnavailable('Linux seccomp unavailable: errno ' + str(ctypes.get_errno()))

    roots = [Path(sys.base_prefix).resolve(), Path(sys.prefix).resolve(),
             Path('/usr/share/zoneinfo'), Path('/usr/lib/locale')]
    files = {Path('/etc/localtime'), Path('/etc/locale.alias'), Path('/dev/null')}

    def permitted(path, writing=False):
        if not isinstance(path, (str, bytes, os.PathLike)):
            return False
        path = Path(os.fsdecode(path)).resolve()
        if path == work or work in path.parents:
            return True
        return not writing and (path in files or any(path == r or r in path.parents for r in roots))

    def audit(event, args):
        if event == 'open':
            path, mode, flags = args
            writing = bool((flags or 0) & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            if not permitted(path, writing):
                raise PermissionError('Sandbox denied file access')
        elif event in {'os.listdir', 'os.scandir', 'os.chdir'}:
            if not permitted(args[0]):
                raise PermissionError('Sandbox denied directory access')
        elif event in {'os.remove', 'os.rmdir', 'os.mkdir', 'os.chmod', 'os.truncate'}:
            if not permitted(args[0], True):
                raise PermissionError('Sandbox denied file mutation')
        elif event in {'os.rename', 'os.link', 'os.symlink'}:
            if not all(permitted(p, True) for p in args[:2]):
                raise PermissionError('Sandbox denied file mutation')
        elif event.startswith(('socket.', 'subprocess.')) or event in {
                'os.system', 'os.fork', 'os.forkpty', 'os.posix_spawn', 'os.exec'}:
            raise PermissionError('Sandbox denied network/process access')

    sys.addaudithook(audit)
