from unittest import TestCase
from somni_log.constants import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL


class Test_Loglevel(TestCase):
    def test_notset(self):
        self.assertEqual(0, NOTSET.INT)
        self.assertEqual('NOTSET', NOTSET.STRING)

    def test_debug(self):
        self.assertEqual(10, DEBUG.INT)
        self.assertEqual('DEBUG', DEBUG.STRING)

    def test_info(self):
        self.assertEqual(20, INFO.INT)
        self.assertEqual('INFO', INFO.STRING)

    def test_warning(self):
        self.assertEqual(30, WARNING.INT)
        self.assertEqual('WARNING', WARNING.STRING)

    def test_error(self):
        self.assertEqual(40, ERROR.INT)
        self.assertEqual('ERROR', ERROR.STRING)

    def test_critical(self):
        self.assertEqual(50, CRITICAL.INT)
        self.assertEqual('CRITICAL', CRITICAL.STRING)
