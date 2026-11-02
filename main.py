"""Recommend the least congested Wi-Fi channel per band from a scan CSV.

Usage: python3 main.py scan.csv
CSV columns: ssid,band,channel,signal_dbm
Score per channel: more networks and stronger signals mean more congestion;
the lowest score wins. Channels with no networks score zero.
"""
import argparse
import csv
import sys
from collections import defaultdict

KNOWN_CHANNELS = {"2.4GHz": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                  "5GHz": [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112,
                           116, 120, 124, 128, 132, 136, 140, 149, 153, 157, 161, 165]}


def analyze(rows):
    per_channel = defaultdict(list)
    for row in rows:
        per_channel[(row["band"], int(row["channel"]))].append(int(row["signal_dbm"]))
    recommendations = {}
    for band, channels in KNOWN_CHANNELS.items():
        best, best_score = None, None
        for channel in channels:
            signals = per_channel.get((band, channel), [])
            score = sum(100 + s for s in signals)
            if best_score is None or score < best_score:
                best, best_score = channel, score
        recommendations[band] = (best, best_score, len(per_channel.get((band, best), [])))
    return recommendations


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="CSV with ssid,band,channel,signal_dbm columns")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        recommendations = analyze(list(csv.DictReader(f)))
    for band in sorted(recommendations):
        channel, score, count = recommendations[band]
        print(f"{band}: use channel {channel} ({count} network(s) there, congestion score {score})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
