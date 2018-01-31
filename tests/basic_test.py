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

    def test_df(self):
        """Tests whether it works for a pandas dataframe"""
        df = pd.DataFrame([["all nice people", "mean people"], ["terrible", "awesome"]], columns=list('AB'), index=[12,3])
        res = self.liwc.process_df(df, "A")

    def test_series_mp(self):
        """Tests the multiprocess implementation of process_series"""

        df = pd.DataFrame([["all nice people", "mean people"], ["terrible", "awesome"]], columns=list('AB'), index=[12,3])
        res = self.liwc.process_df_mp(df, "A")

        print(res)

if __name__ == '__main__':
    unittest.main()
