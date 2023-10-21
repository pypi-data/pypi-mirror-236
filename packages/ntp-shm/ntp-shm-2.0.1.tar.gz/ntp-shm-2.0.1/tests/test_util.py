import datetime
import unittest

from ntp_shm import util

TZUTC = datetime.timezone.utc


class TestUtil(unittest.TestCase):
    def test_datetime_to_ns(self):
        dt_min = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=TZUTC)
        self.assertEqual(0, util.datetime_to_ns(dt_min))

        dt_test = datetime.datetime.fromtimestamp(123.456789, tz=TZUTC)
        self.assertEqual(123456789000, util.datetime_to_ns(dt_test))

    def test_datetime_to_ns_non_utc_input(self):
        mytz = datetime.timezone(datetime.timedelta(hours=-4), "mytz")
        offset = 14400000000000

        dt_min = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=mytz)
        self.assertEqual(0 + offset, util.datetime_to_ns(dt_min))

        dt_test = datetime.datetime.utcfromtimestamp(123.456789).replace(tzinfo=mytz)
        self.assertEqual(123456789000 + offset, util.datetime_to_ns(dt_test))

    def test_ns_to_datetime(self):
        dt_min = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=TZUTC)
        self.assertEqual(dt_min, util.ns_to_datetime(0))

        dt_test = datetime.datetime.fromtimestamp(123.456789, tz=TZUTC)
        self.assertEqual(dt_test, util.ns_to_datetime(123456789000))
        self.assertEqual(dt_test, util.ns_to_datetime(123456789001))
        self.assertEqual(dt_test, util.ns_to_datetime(123456789499))
        self.assertEqual(dt_test, util.ns_to_datetime(123456788501))

    def test_ns_to_tuple(self):
        ns = 112233445566778899
        tup = (112233445, 566778, 566778899)
        result = util.ns_to_tuple(ns)
        self.assertEqual(tup, result)

    def test_tuple_to_ns(self):
        ns = 112233445566778899
        tup = (112233445, 566778, 566778899)
        result = util.tuple_to_ns(*tup)
        self.assertEqual(ns, result)

    def test_tuple_to_ns_no_nsec(self):
        ns = 112233445566778000
        tup = (112233445, 566778, 0)
        result = util.tuple_to_ns(*tup)
        self.assertEqual(ns, result)
