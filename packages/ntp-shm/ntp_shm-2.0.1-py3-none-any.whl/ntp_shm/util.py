import datetime
from typing import Tuple

NSEC_IN_SEC = 1000000000
NSEC_IN_USEC = 1000


def datetime_to_ns(dt: datetime.datetime) -> int:
    """Fetch the UTC time in nanoseconds from the given datetime.

    If the datetime object is naive, the default Python behavior is to assume
    it is in the system timezone.
    """
    # Explicit conversion so we don't rely on the platform's mktime()
    timestamp = dt.astimezone(datetime.timezone.utc).timestamp()
    nsec = int(timestamp) * NSEC_IN_SEC
    nsec += dt.microsecond * NSEC_IN_USEC
    return nsec


def ns_to_datetime(time_ns: int) -> datetime.datetime:
    """Convert nanoseconds to a datetime object (UTC timezone)"""
    time_sec = time_ns / NSEC_IN_SEC
    return datetime.datetime.fromtimestamp(time_sec, datetime.timezone.utc)


def ns_to_tuple(time_ns: int) -> Tuple[int, int, int]:
    """Return a tuple of seconds, microseconds, nanoseconds from the given time.

    Note that microseconds and nanoseconds represent the same offset, just with
    different precision. That is, nanoseconds will *also* containe the value in
    microseconds.
    """
    time_sec = time_ns // NSEC_IN_SEC
    time_nsec = time_ns % NSEC_IN_SEC
    time_usec = time_nsec // NSEC_IN_USEC

    return time_sec, time_usec, time_nsec


def tuple_to_ns(time_sec: int, time_usec: int, time_nsec: int) -> int:
    """Convert a tuple of seconds, microseconds, nanoseconds, to nanoseconds."""
    time_ns = time_sec * NSEC_IN_SEC

    # In case this system does not populate properly
    if time_nsec == 0:
        time_ns += time_usec * NSEC_IN_USEC
    else:
        time_ns += time_nsec

    return time_ns
