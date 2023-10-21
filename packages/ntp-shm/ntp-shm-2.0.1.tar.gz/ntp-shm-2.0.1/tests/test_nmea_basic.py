import datetime
import unittest

from ntp_shm import nmea

TZUTC = datetime.timezone.utc


class TestNmeaBasic(unittest.TestCase):
    def test_parse_basic(self):
        line = "$TEST,FIELD1,FIELD2,FIELD3*48"
        msg, fields = nmea.parse(line)
        self.assertEqual("TEST", msg)
        self.assertEqual(["FIELD1", "FIELD2", "FIELD3"], fields)

    def test_parse_basic_empty_fields(self):
        line = "$TEST,,FIELD2,,FIELD4,FIELD5,,,*67"
        msg, fields = nmea.parse(line)
        self.assertEqual("TEST", msg)
        self.assertEqual(["", "FIELD2", "", "FIELD4", "FIELD5", "", "", ""], fields)

    def test_parse_checksum_invalid(self):
        line = "$TEST,SENTENCE*00"
        with self.assertRaisesRegex(ValueError, "Checksum error"):
            nmea.parse(line)

    def test_parse_invalid_characters(self):
        sentences = (
            "",
            "$*00",
            "XTEST,SENTENCE*00",
            "$TEST,SENTENCEX00",
            "XTEST,SENTENCEX00",
            "$TEST,SENTENCE*000",
            "$TEST,SENTENCE*00\r",
            "$TEST,SENTENCE*00\n",
        )
        for line in sentences:
            with self.assertRaisesRegex(ValueError, "Not a NMEA sentence"):
                nmea.parse(line)

    def test_gprmc_valid_minimal(self):
        lines = (
            "$GPRMC,000000,A,,,,,,,111111,,*26",
            "$GPRMC,000000,A,,,,,,,111111,,,A*4B",
            "$GPRMC,000000,A,,,,,,,111111,,,D*4E",
            "$GPRMC,000000.00,A,,,,,,,111111,,,D*60",
            "$GPRMC,000000.000,A,,,,,,,111111,,,D*50",
            "$GNRMC,000000,A,,,,,,,111111,,*38",
            "$GNRMC,000000.000,A,,,,,,,111111,,,D*4e",
        )
        expected = datetime.datetime(2011, 11, 11, 0, 00, 00, tzinfo=TZUTC)
        for line in lines:
            msg, fields = nmea.parse(line)
            actual = nmea.gprmc_time(fields)
            self.assertEqual(expected, actual)

    def test_gprmc_valid_fractional_seconds_1(self):
        line = "$GPRMC,000000.12,A,,,,,,,111111,,,D*63"
        expected = datetime.datetime(2011, 11, 11, 0, 00, 00, 120000, tzinfo=TZUTC)
        msg, fields = nmea.parse(line)
        actual = nmea.gprmc_time(fields)
        self.assertEqual(expected, actual)

    def test_gprmc_valid_fractional_seconds_2(self):
        line = "$GPRMC,000000.123,A,,,,,,,111111,,,D*50"
        expected = datetime.datetime(2011, 11, 11, 0, 00, 00, 123000, tzinfo=TZUTC)
        msg, fields = nmea.parse(line)
        actual = nmea.gprmc_time(fields)
        self.assertEqual(expected, actual)

    def test_gprmc_valid_1(self):
        line = "$GPRMC,123519,A,1234.567,N,01234.567,E,022.4,084.4,230304,003.1,W*61"
        msg, fields = nmea.parse(line)
        expected = datetime.datetime(2004, 3, 23, 12, 35, 19, tzinfo=TZUTC)
        actual = nmea.gprmc_time(fields)
        self.assertEqual(expected, actual)

    def test_gprmc_valid_2(self):
        line = "$GPRMC,004233.543,A,1234.5678,N,01234.5678,W,0.22,23.39,160921,,,D*4B"
        msg, fields = nmea.parse(line)
        expected = datetime.datetime(2021, 9, 16, 0, 42, 33, 543000, tzinfo=TZUTC)
        actual = nmea.gprmc_time(fields)
        self.assertEqual(expected, actual)

    def test_gprmc_invalid_fix(self):
        lines = (
            # No mode
            "$GPRMC,,,,,,,,,,,*67",
            "$GPRMC,,V,,,,,,,,,*31",
            # Has mode
            "$GPRMC,,,,,,,,,,,,*4B",
            "$GPRMC,,V,,,,,,,,,,*1D",
            "$GPRMC,,,,,,,,,,,,A*0A",
            "$GPRMC,,,,,,,,,,,,D*0F",
            "$GPRMC,,,,,,,,,,,,N*05",
            "$GPRMC,,V,,,,,,,,,,A*5C",
            "$GPRMC,,V,,,,,,,,,,D*59",
            "$GPRMC,,A,,,,,,,,,,E*4F",
            "$GPRMC,,A,,,,,,,,,,M*47",
            "$GPRMC,,A,,,,,,,,,,N*44",
        )
        for line in lines:
            msg, fields = nmea.parse(line)
            with self.assertRaises(nmea.InvalidFix):
                nmea.gprmc_time(fields)

    def test_gprmc_invalid_date(self):
        lines = (
            "$GPRMC,000000,A,,,,,,,,,*26",
            "$GPRMC,000000,A,,,,,,,,,,D*4E",
            "$GPRMC,000000,A,,,,,,,11111,,,D*7F",
            "$GPRMC,000000,A,,,,,,,1111111,,,D*7F",
        )
        for line in lines:
            msg, fields = nmea.parse(line)
            with self.assertRaisesRegex(ValueError, "Invalid date field"):
                nmea.gprmc_time(fields)

    def test_gprmc_invalid_time(self):
        lines = (
            # Missing
            "$GPRMC,,A,,,,,,,111111,,*26",
            "$GPRMC,,A,,,,,,,111111,,,D*4E",
            # Too many decimals
            "$GPRMC,00.00.00,A,,,,,,,111111,,,D*4E",
            # Too short
            "$GPRMC,00000,A,,,,,,,111111,,,D*7E",
            # Invalid fractional seconds
            "$GPRMC,000000.,A,,,,,,,111111,,,D*60",
            "$GPRMC,000000.0,A,,,,,,,111111,,,D*50",
            "$GPRMC,000000.0000,A,,,,,,,111111,,,D*60",
        )
        for line in lines:
            msg, fields = nmea.parse(line)
            with self.assertRaisesRegex(ValueError, "Invalid time field"):
                nmea.gprmc_time(fields)
