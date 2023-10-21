import ctypes
import ctypes.util
import errno

from .data import ShmTime

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

# Fix issues on 64-bit machines :(
libc.memmove.restype = ctypes.c_void_p
libc.memmove.argtypes = ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t
libc.shmat.restype = ctypes.c_void_p
libc.shmat.argtypes = ctypes.c_int, ctypes.c_void_p, ctypes.c_int
libc.shmdt.restype = ctypes.c_int
libc.shmdt.argtypes = (ctypes.c_void_p,)
libc.shmget.restype = ctypes.c_int
libc.shmget.argtypes = ctypes.c_int, ctypes.c_size_t, ctypes.c_int

NTP_SHM_KEY_BASE = 0x4E545030
IPC_CREAT = 0o1000  # Octal. Holds for most systems.

LEAP_NOWARNING = 0
LEAP_ADDSECOND = 1
LEAP_DELSECOND = 2
LEAP_NOTINSYNC = 3


class NtpShm:
    """An interface to an NTP Shared Memory time segment.

    This wraps up all the scary direct memory access.
    """

    def __init__(self, segment: int = 0, mode: int = 0o666):
        """Create a shared memory segment.

        Args:
            segment: Segment number
            mode: Permission mode to use if creating
        """
        if segment < 0:
            raise ValueError("Segment must be a non-negative integer")

        self._segment = segment

        # Get a reference
        shmid = libc.shmget(self.key, ctypes.sizeof(ShmTime), IPC_CREAT | mode)
        if shmid == -1:
            errcode = errno.errorcode[ctypes.get_errno()]
            raise OSError(f"shmget failed for segment {segment}: {errcode}")

        # Memory map
        self._seg = libc.shmat(shmid, None, 0)
        if self._seg == -1:
            errcode = errno.errorcode[ctypes.get_errno()]
            raise OSError(f"shmat failed for segment {segment}, id {shmid}: {errcode}")

    def __enter__(self) -> "NtpShm":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        libc.shmdt(self._seg)
        self._seg = 0

    @property
    def segment(self) -> int:
        return self._segment

    @property
    def key(self) -> int:
        return NTP_SHM_KEY_BASE + self._segment

    @property
    def ref(self) -> ShmTime:
        """Direct memory reference as a ShmTime object.

        Returns:
            Reference to the shared segment
        """
        return ctypes.cast(self._seg, ctypes.POINTER(ShmTime)).contents

    def read(self) -> ShmTime:
        """Get a copy of the NTP shm segment.

        Note that this is a direct copy and does not abide by any mode.

        Returns:
            Shared memory time structure
        """
        shm_time = ShmTime()
        libc.memmove(ctypes.byref(shm_time), self._seg, ctypes.sizeof(ShmTime))
        return shm_time

    def write(self, shm_time: ShmTime) -> None:
        """Write to the NTP shm segment.

        Note that this is a direct copy and does not abide by any mode.

        Args:
            shm_time: Shared memory time structure
        """
        libc.memmove(self._seg, ctypes.byref(shm_time), ctypes.sizeof(ShmTime))

    def update(self, clock_ns: int, receive_ns: int, precision: int = -1, leap: int = 0) -> None:
        """Update the shared memory segment with the given time using mode 1.

        Note that updating shared memory is rife with pitfalls. Memory barriers
        should normally be used to ensure proper memory ordering and multi-core
        cache synchronization. However, we have no such mechanism in Python.
        Cross your fingers and hope for the best.

        Precision is Log2 of the clock precision in seconds. Examples:
            -1: 0.5s (NMEA streams)
            -10: 1ms (USB PPS)
            -20: 1us (Serial or GPIO PPS)

        Leap indicates if there's a pending leap event. Examples:
            0: No warning
            1: Adding a second
            2: Deleting a second
            3: Not synchronized

        Args:
            clock_ns: Clock time (GPS clock), in ns
            receive_ns: System time when the clock time was received, in ns
            precision: Precision indicator
            leap: Leap second warning
        """
        seg = self.ref

        seg.valid = 0
        seg.mode = 1
        seg.count += 1

        seg.clock_ns = clock_ns
        seg.receive_ns = receive_ns
        seg.leap = leap
        seg.precision = precision

        seg.count += 1
        seg.valid = 1
