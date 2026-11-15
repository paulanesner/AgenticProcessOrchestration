#!/usr/bin/env python3
"""Pairwise exact (positional) comparison of HTTP access logs.

For every pair of logs, walk line by line through the shorter log and compare
each entry with the entry at the same position in the longer log.

Entries:
  default    HTTP access-log lines, reduced to "METHOD PATH STATUS"
             (timestamps and client addresses always differ, so they are
             dropped; --with-size also keeps the response size, usually too
             strict for LLM-generated payloads)
  --plain    one entry per non-empty line, used verbatim; lines starting
             with '#' are ignored. Use this for manually transcribed
             orchestrator logs (one summarized logged event per line).

Match = 1 - mean(#mismatch) / mean(#log_entries)

Usage: exact_match.py [--plain | --with-size] LOG LOG [LOG ...]
"""
import argparse
import itertools
import re
import statistics
import sys

LINE_RE = re.compile(
    r'^(?P<host>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" (?P<status>\d{3}) (?P<size>\d+|-)'
)


def read_log(path, plain, with_size):
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
                continue  # skip anything that is not an access-log line
            key = f'{m["method"]} {m["path"]} {m["status"]}'
            if with_size:
                key += f' {m["size"]}'
            entries.append(key)
    return entries


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logs", nargs="+", help="log files (at least two)")
    ap.add_argument("--plain", action="store_true", help="one entry per line (transcribed orchestrator logs)")
    ap.add_argument("--with-size", action="store_true", help="also compare response sizes (access logs only)")
    args = ap.parse_args()
    if len(args.logs) < 2:
        sys.exit("need at least two log files")

    logs = {p: read_log(p, args.plain, args.with_size) for p in args.logs}
    pair_mismatches = []
    pair_rates = []

    for a, b in itertools.combinations(args.logs, 2):
        short, long_ = (a, b) if len(logs[a]) <= len(logs[b]) else (b, a)
        s, l = logs[short], logs[long_]
        print(f"=== {a} ({len(logs[a])}) vs {b} ({len(logs[b])})")

        mismatches = 0
        for i, entry in enumerate(s):
            if entry != l[i]:
                mismatches += 1
                print(f"  line {i + 1}: {short}: {entry!r}  <->  {long_}: {l[i]!r}")

        extra = len(l) - len(s)
        if extra:
            print(f"  {long_} has {extra} additional line(s) not compared:")
            for i in range(len(s), len(l)):
                print(f"    line {i + 1}: {l[i]!r}")

        rate = mismatches / len(s) if s else 0.0
        print(f"  mismatches: {mismatches} / {len(s)} compared lines ({rate:.1%})\n")
        pair_mismatches.append(mismatches)
        pair_rates.append(rate)

    lengths = [len(v) for v in logs.values()]
    mean_mm = statistics.mean(pair_mismatches)
    mean_len = statistics.mean(lengths)
    print("=== summary (EP)")
    print(f"  logs: {len(lengths)}, pairs: {len(pair_mismatches)}")
    print(f"  mean #mismatch per pair:      {mean_mm:.2f}")
    print(f"  mean mismatch rate per pair:  {statistics.mean(pair_rates):.1%}")
    print(f"  mean #log_entries:            {mean_len:.2f} (min {min(lengths)}, max {max(lengths)})")
    print(f"  Match = 1 - {mean_mm:.2f} / {mean_len:.2f} = {1 - mean_mm / mean_len:.3f}")


if __name__ == "__main__":
    main()
