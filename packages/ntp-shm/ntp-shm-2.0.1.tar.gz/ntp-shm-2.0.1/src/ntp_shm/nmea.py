import datetime
import re
from typing import Iterable, List, Tuple

from . import util

NMEA_MAX_LEN = 128  # Actually 82, but let's not be pedantic
NTP_MIN_FIX = 3

# Time jumps outside this range are invalid
MIN_DELTA = datetime.timedelta(seconds=0.5)
MAX_DELTA = datetime.timedelta(seconds=2)

US_IN_MS = 1000
US_IN_CS = 10000


class InvalidFix(RuntimeError):
    """Indicates the GPS does not have a fix"""

    pass


def _check(sentence: str, checksum: int) -> None:
    """Validate the checksum for the given NMEA sentence."""
    actual = 0
    for c in sentence:
        actual ^= ord(c)

    if actual != checksum:
        raise ValueError(f"Checksum error. Given 0x{checksum:02x}, actual 0x{actual:02x}")


def _nmea_line_gen(path: str, msg_type: str) -> Iterable[str]:
    """Generator that hides a bunch of nasty nested nastiness"""
    with open(path, "r") as f:
        while True:
            try:
                line = f.readline(NMEA_MAX_LEN)
                if not line:
                    break
                if re.match(r"^\$" + msg_type, line):
                    yield line.strip()
            except UnicodeDecodeError:
                # Ignore. Just bad data.
                pass


def parse(line: str) -> Tuple[str, List[str]]:
    """Parse a given GPS NMEA sentence, returning the message type and its fields."""
    if len(line) < 5 or not line.startswith("$") or not line[-3] == "*":
        raise ValueError("Not a NMEA sentence")

    sentence, checksum = line[1:].rsplit("*", 1)
    _check(sentence, int(checksum, 16))

    msg, rest = sentence.split(",", 1)

    return msg, rest.split(",")


def gprmc_time(fields: List[str], differential: bool = False) -> datetime.datetime:
    """Parse GPRMC time from the given array of fields

    This will only accept sentence that have a valid fix, either Autonomous or
    Differential. If differential is True, then it only accepts Differential
    mode.

    Args:
        fields: NMEA stentence fields
        differential: Only accept differential mode

    Returns:
        Datetime in UTC

    Raises:
        InvalidFix if the sentence indicates no fix
        ValueError if there's an invalid value for the date or time
    """
    utc_time = fields[0]
    valid = fields[1]
    date = fields[8]
    mode = fields[11] if len(fields) > 11 else None

    # Skip if invalid
    if valid != "A" or mode not in (None, "A", "D") or (differential and mode != "D"):
        raise InvalidFix(f"Invalid fix: {valid} | {mode}")

    # Parse the date
    if len(date) != 6:
        raise ValueError(f"Invalid date field: {date}")

    try:
        day = int(date[0:2], 10)
        month = int(date[2:4], 10)
        year = 2000 + int(date[4:6], 10)
    except ValueError:
        raise ValueError(f"Invalid date field: {date}")

    # Parse the time
    if len(utc_time) < 6:
        raise ValueError(f"Invalid time field: {utc_time}")

    try:
        hour = int(utc_time[0:2], 10)
        minute = int(utc_time[2:4], 10)
        str_sec_ms = utc_time[4:].split(".")
        second = int(str_sec_ms[0], 10)
        us = 0
        if len(str_sec_ms) > 1:
            if len(str_sec_ms[1]) == 2:
                us = int(str_sec_ms[1], 10) * US_IN_CS
            elif len(str_sec_ms[1]) == 3:
                us = int(str_sec_ms[1], 10) * US_IN_MS
            else:
                raise ValueError("Invalid fractional seconds")
    except ValueError:
        raise ValueError(f"Invalid time field: {utc_time}")

    return datetime.datetime(year, month, day, hour, minute, second, us, datetime.timezone.utc)


def nmea_time(path: str) -> Iterable[Tuple[int, int]]:
    """Fetch time from the NMEA0183 sentences at the given path

    Args:
        path: Path to the file-like device spitting out NMEA sentences

    Yields:
        A tuple of clock and received time, in nanoseconds
    """
    valid_count = 0
    last_clock_dt = None

    for line in _nmea_line_gen(path, "G.RMC"):
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        recv_ns = util.datetime_to_ns(utc_now)

        try:
            _, fields = parse(line)
            clock_dt = gprmc_time(fields)

            valid_count += 1
            if valid_count <= NTP_MIN_FIX:
                continue

            # Ensure we only step one second at a time
            if last_clock_dt:
                delta = clock_dt - last_clock_dt
                if not MIN_DELTA <= delta <= MAX_DELTA:
                    raise InvalidFix(f"Clock jump of {delta}")

            last_clock_dt = clock_dt
            clock_ns = util.datetime_to_ns(clock_dt)
            yield clock_ns, recv_ns
        except InvalidFix as ex:
            valid_count = 0
            last_clock_dt = None
            print(ex)
        except ValueError as ex:
            # Probably just a corrupted line. But warn/log...
            print(ex)
