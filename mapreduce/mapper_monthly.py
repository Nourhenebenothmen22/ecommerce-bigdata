#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    parts = line.split(",")
    if parts[0] == "order_id":
        continue
    try:
        date = parts[1]
        month = date[:7]  # 2023-01
        total = parts[6]
        print(f"{month}\t{total}")
    except:
        continue