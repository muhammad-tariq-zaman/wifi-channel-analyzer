import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import analyze


def rows(specs):
    return [{"ssid": f"n{i}", "band": b, "channel": str(c), "signal_dbm": str(s)}
            for i, (b, c, s) in enumerate(specs)]


class TestWifiAnalyzer(unittest.TestCase):
    def test_empty_channel_wins(self):
        rec = analyze(rows([("2.4GHz", 1, -40), ("2.4GHz", 1, -50), ("2.4GHz", 6, -45)]))
        self.assertEqual(rec["2.4GHz"][0], 2)

    def test_weaker_signals_preferred(self):
        rec = analyze(rows([("5GHz", 36, -30), ("5GHz", 40, -85)]))
        self.assertEqual(rec["5GHz"][0], 44)

    def test_no_data_picks_first_channel(self):
        rec = analyze([])
        self.assertEqual(rec["2.4GHz"][0], 1)
        self.assertEqual(rec["5GHz"][0], 36)
