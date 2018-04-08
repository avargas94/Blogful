import os
import unittest
import datetime


if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"


from blog import app
from blog.filters import *


class FilterTests(unittest.TestCase):
    def test_date_format(self):
        date = datetime.date(2018, 12, 31)
        formatted = dateformat(date, "%m/%d/%y")
        self.assertEqual(formatted, '12/31/18')

    def test_date_format_none(self):
        formatted = dateformat(None, "%m/%d/%y")
        self.assertEqual(formatted, None)


if __name__ == "__main__":
    unittest.main()
