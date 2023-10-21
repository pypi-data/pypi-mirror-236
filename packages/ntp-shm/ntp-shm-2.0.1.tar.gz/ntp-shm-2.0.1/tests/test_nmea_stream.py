import os
import unittest

from ntp_shm import nmea


def _resource_path(name):
    return os.path.join(os.path.dirname(__file__), "resources", name)


class TestNmeaStream(unittest.TestCase):
    def test_loss_restore(self):
        path = _resource_path("loss_restore.txt")
        expected = (
            1627868857000000000,
            1627868858000000000,
            1627868874000000000,
            1627868875000000000,
        )
        actual = list(clock_ns for clock_ns, _ in nmea.nmea_time(path))
        self.assertSequenceEqual(expected, actual)

    def test_time_jump_forward(self):
        path = _resource_path("time_jump_forward.txt")
        expected = (
            1627868857000000000,
            1627868858000000000,
            1627868875000000000,
        )
        actual = list(clock_ns for clock_ns, _ in nmea.nmea_time(path))
        self.assertSequenceEqual(expected, actual)

    def test_time_jump_backward(self):
        path = _resource_path("time_jump_backward.txt")
        expected = (
            1627868874000000000,
            1627868875000000000,
            1627868858000000000,
        )
        actual = list(clock_ns for clock_ns, _ in nmea.nmea_time(path))
        self.assertSequenceEqual(expected, actual)

    def test_time_jump_duplicate(self):
        path = _resource_path("time_jump_duplicate.txt")
        expected = (
            1627868857000000000,
            1627868858000000000,
            1627868862000000000,
            1627868863000000000,
        )
        actual = list(clock_ns for clock_ns, _ in nmea.nmea_time(path))
        self.assertSequenceEqual(expected, actual)
