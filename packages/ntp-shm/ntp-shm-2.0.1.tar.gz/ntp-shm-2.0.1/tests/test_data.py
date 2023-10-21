import datetime
import unittest

from ntp_shm import data


class TestData(unittest.TestCase):
    """Basic tests to ensure the special properties are working correctly"""

    DT_0 = datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    DT_1 = datetime.datetime.fromtimestamp(98765432.123456, tz=datetime.timezone.utc)
    NS_0 = 0
    NS_1 = 98765432123456000
    NS_2 = 98765432123456789

    def test_clock_dt(self):
        shm_time_0 = data.ShmTime()

        shm_time_1a = data.ShmTime(
            clock_time_sec=98765432,
            clock_time_usec=123456,
            clock_time_nsec=123456000,
        )
        shm_time_1b = data.ShmTime(
            clock_time_sec=98765432,
            clock_time_usec=123456,
            clock_time_nsec=0,
        )

        self.assertEqual(self.DT_0, shm_time_0.clock_dt)
        self.assertEqual(self.DT_1, shm_time_1a.clock_dt)
        self.assertEqual(self.DT_1, shm_time_1b.clock_dt)

    def test_clock_ns_get(self):
        shm_time_0 = data.ShmTime()

        shm_time_1a = data.ShmTime(
            clock_time_sec=98765432,
            clock_time_usec=123456,
            clock_time_nsec=123456000,
        )
        shm_time_1b = data.ShmTime(
            clock_time_sec=98765432,
            clock_time_usec=123456,
            clock_time_nsec=0,
        )
        shm_time_2 = data.ShmTime(
            clock_time_sec=98765432,
            clock_time_usec=123456,
            clock_time_nsec=123456789,
        )

        self.assertEqual(self.NS_0, shm_time_0.clock_ns)
        self.assertEqual(self.NS_1, shm_time_1a.clock_ns)
        self.assertEqual(self.NS_1, shm_time_1b.clock_ns)
        self.assertEqual(self.NS_2, shm_time_2.clock_ns)

    def test_clock_ns_set(self):
        shm_time_0 = data.ShmTime()
        shm_time_1 = data.ShmTime(
            clock_time_sec=98765432,
            clock_time_usec=123456,
            clock_time_nsec=123456000,
        )
        shm_time_2 = data.ShmTime(
            clock_time_sec=98765432,
            clock_time_usec=123456,
            clock_time_nsec=123456789,
        )

        shm_test = data.ShmTime()

        shm_test.clock_ns = self.NS_1
        self.assertEqual(bytes(shm_time_1), bytes(shm_test))

        shm_test.clock_ns = self.NS_2
        self.assertEqual(bytes(shm_time_2), bytes(shm_test))

        shm_test.clock_ns = 0
        self.assertEqual(bytes(shm_time_0), bytes(shm_test))

    def test_receive_dt(self):
        shm_time_0 = data.ShmTime()

        shm_time_1a = data.ShmTime(
            receive_time_sec=98765432,
            receive_time_usec=123456,
            receive_time_nsec=123456000,
        )
        shm_time_1b = data.ShmTime(
            receive_time_sec=98765432,
            receive_time_usec=123456,
            receive_time_nsec=0,
        )

        self.assertEqual(self.DT_0, shm_time_0.receive_dt)
        self.assertEqual(self.DT_1, shm_time_1a.receive_dt)
        self.assertEqual(self.DT_1, shm_time_1b.receive_dt)

    def test_receive_ns_get(self):
        shm_time_0 = data.ShmTime()

        shm_time_1a = data.ShmTime(
            receive_time_sec=98765432,
            receive_time_usec=123456,
            receive_time_nsec=123456000,
        )
        shm_time_1b = data.ShmTime(
            receive_time_sec=98765432,
            receive_time_usec=123456,
            receive_time_nsec=0,
        )
        shm_time_2 = data.ShmTime(
            receive_time_sec=98765432,
            receive_time_usec=123456,
            receive_time_nsec=123456789,
        )

        self.assertEqual(self.NS_0, shm_time_0.receive_ns)
        self.assertEqual(self.NS_1, shm_time_1a.receive_ns)
        self.assertEqual(self.NS_1, shm_time_1b.receive_ns)
        self.assertEqual(self.NS_2, shm_time_2.receive_ns)

    def test_receive_ns_set(self):
        shm_time_0 = data.ShmTime()
        shm_time_1 = data.ShmTime(
            receive_time_sec=98765432,
            receive_time_usec=123456,
            receive_time_nsec=123456000,
        )
        shm_time_2 = data.ShmTime(
            receive_time_sec=98765432,
            receive_time_usec=123456,
            receive_time_nsec=123456789,
        )

        shm_test = data.ShmTime()

        shm_test.receive_ns = self.NS_1
        self.assertEqual(bytes(shm_time_1), bytes(shm_test))

        shm_test.receive_ns = self.NS_2
        self.assertEqual(bytes(shm_time_2), bytes(shm_test))

        shm_test.receive_ns = 0
        self.assertEqual(bytes(shm_time_0), bytes(shm_test))
