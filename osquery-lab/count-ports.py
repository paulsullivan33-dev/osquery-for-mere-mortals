#!/usr/bin/env python3
"""Count the distinct listening ports in osqueryi's JSON output.

Reads a JSON array of rows (as produced by `osqueryi --json`) from
standard input and prints how many distinct values of the `port`
column it contains. Used in chapter 8 of the guide.

    osqueryi --json "SELECT port FROM listening_ports WHERE port > 0;" \
      | python3 count-ports.py
"""

import json
import sys


def main() -> int:
    rows = json.load(sys.stdin)
    ports = {row["port"] for row in rows}
    print(f"{len(ports)} distinct ports across {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
