#!/usr/bin/env python3
import sys

current_key = None
current_sum = 0

for line in sys.stdin:
    line = line.strip()
    parts = line.split("\t")
    if len(parts) != 2:
        continue
    key = parts[0]
    try:
        value = float(parts[1])
    except:
        continue

    if key == current_key:
        current_sum += value
    else:
        if current_key:
            print("%s\t%.2f" % (current_key, current_sum))
        current_key = key
        current_sum = value

if current_key:
    print("%s\t%.2f" % (current_key, current_sum))