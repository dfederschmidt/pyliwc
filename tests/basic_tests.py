"""
Basic tests for LIWC - does not really test anything at this point.
"""
import unittest
import random
import string
import pandas as pd
from pyliwc.core import LIWC

class TestLIWC(unittest.TestCase):
    def setUp(self):
        self.liwc = LIWC("./LIWC2015.dic")

    def test_string(self):
        """Tests whether it works for a single string"""
        test_string = "I'm very angry right now - crazy stupid love!"
        res = self.liwc.process_text(test_string)

        print(res)

    def test_series(self):
        """Tests whether it works for a pandas Series"""
        series = pd.Series(["hello, you are funny", "goodbye you"])
        res = self.liwc.process_series(series)

        print(res)

    def test_series_mp(self):
        """Tests the multiprocess implementation of process_series"""
        series = pd.Series(random.choice(string.ascii_uppercase) for _ in range(100000))
        res = self.liwc.process_series_mp(series)

        print(res)

if __name__ == '__main__':
    unittest.main()
