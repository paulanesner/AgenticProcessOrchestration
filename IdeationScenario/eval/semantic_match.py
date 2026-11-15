#!/usr/bin/env python3
"""Pairwise semantic (order-independent) comparison of HTTP access logs.

For every pair of logs, count how often each endpoint ("METHOD PATH", query
string stripped) was called and compare the counts.

Mismatches of a pair = sum over all endpoints that have a different number of entries.

Entries:
  default    HTTP access-log lines, reduced to "METHOD PATH"
  --plain    one entry per non-empty line, used verbatim; lines starting
             with '#' are ignored. Use this for manually transcribed
             orchestrator logs.

Match = 1 - mean(#mismatch) / mean(#log_entries)

Usage: semantic_match.py [--plain] LOG LOG [LOG ...]
"""
import argparse
import itertools
import re
import statistics
import sys
from collections import Counter

LINE_RE = re.compile(
    r'^(?P<host>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" (?P<status>\d{3}) (?P<size>\d+|-)'
)


def read_log(path, plain):
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if plain:
                if line and not line.startswith("#"):
                    entries.append(line)
                continue
            m = LINE_RE.match(line)
            if not m:
                continue
            entries.append(f'{m["method"]} {m["path"].split("?", 1)[0]}')
    return entries


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logs", nargs="+", help="log files (at least two)")
    ap.add_argument("--plain", action="store_true", help="one entry per line (transcribed orchestrator logs)")
    args = ap.parse_args()
    if len(args.logs) < 2:
        sys.exit("need at least two log files")

    logs = {p: read_log(p, args.plain) for p in args.logs}
    counts = {p: Counter(v) for p, v in logs.items()}
    pair_mismatches = []

    for a, b in itertools.combinations(args.logs, 2):
        ca, cb = counts[a], counts[b]
        print(f"=== {a} ({len(logs[a])}) vs {b} ({len(logs[b])})")

        mismatches = 0
        for endpoint in sorted(ca.keys() | cb.keys()):
            diff = abs(ca[endpoint] - cb[endpoint])
            if diff:
                mismatches += 1
                print(f"  {endpoint}: {ca[endpoint]}x in {a}, {cb[endpoint]}x in {b}")

        print(f"  mismatches: {mismatches}\n")
        pair_mismatches.append(mismatches)

    lengths = [len(v) for v in logs.values()]
    mean_mm = statistics.mean(pair_mismatches)
    mean_len = statistics.mean(lengths)
    print("=== summary (SP)")
    print(f"  logs: {len(lengths)}, pairs: {len(pair_mismatches)}")
    print(f"  mean #mismatch per pair:  {mean_mm:.2f}")
    print(f"  mean #log_entries:        {mean_len:.2f} (min {min(lengths)}, max {max(lengths)})")
    print(f"  Match = 1 - {mean_mm:.2f} / {mean_len:.2f} = {1 - mean_mm / mean_len:.3f}")


if __name__ == "__main__":
    main()
