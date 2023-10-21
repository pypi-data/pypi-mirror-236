import ctypes
import datetime

from . import util


class ShmTime(ctypes.Structure):
    """Structure for NTP's shared memory segment

    See https://docs.ntpsec.org/latest/driver_shm.html

    Fields renamed slightly.
    """

    _fields_ = (
        ("mode", ctypes.c_int),
        ("count", ctypes.c_int),  # volatile
        ("clock_time_sec", ctypes.c_int64),  # time_t
        ("clock_time_usec", ctypes.c_int),
        ("receive_time_sec", ctypes.c_int64),  # time_t
        ("receive_time_usec", ctypes.c_int),
        ("leap", ctypes.c_int),
        ("precision", ctypes.c_int),
        ("nsamples", ctypes.c_int),
        ("valid", ctypes.c_int),  # volatile
        ("clock_time_nsec", ctypes.c_uint),
        ("receive_time_nsec", ctypes.c_uint),
        ("_dummy", ctypes.c_int * 8),
    )

    @property
    def clock_dt(self) -> datetime.datetime:
        """Datetime representation of the clock time.

        Note that python datetime does not support nanosecond precision."""
        return util.ns_to_datetime(self.clock_ns)

    @property
    def clock_ns(self) -> int:
        """Clock time in integer nanoseconds"""
        return util.tuple_to_ns(self.clock_time_sec, self.clock_time_usec, self.clock_time_nsec)

    @clock_ns.setter
    def clock_ns(self, time_ns: int) -> None:
        """Clock time in integer nanoseconds"""
        time_sec, time_usec, time_nsec = util.ns_to_tuple(time_ns)
        self.clock_time_sec = time_sec
        self.clock_time_usec = time_usec
        self.clock_time_nsec = time_nsec

    @property
    def receive_dt(self) -> datetime.datetime:
        """Datetime representation of the receive time.

        Note that python datetime does not support nanosecond precision."""
        return util.ns_to_datetime(self.receive_ns)

    @property
    def receive_ns(self) -> int:
        """Receive time in integer nanoseconds."""
        return util.tuple_to_ns(self.receive_time_sec, self.receive_time_usec, self.receive_time_nsec)

    @receive_ns.setter
    def receive_ns(self, time_ns: int) -> None:
        """Clock time in integer nanoseconds"""
        time_sec, time_usec, time_nsec = util.ns_to_tuple(time_ns)
        self.receive_time_sec = time_sec
        self.receive_time_usec = time_usec
        self.receive_time_nsec = time_nsec
