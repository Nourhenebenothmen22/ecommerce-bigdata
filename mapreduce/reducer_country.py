#!/usr/bin/env python3
import sys

current_key = None
current_sum = 0
current_count = 0

for line in sys.stdin:
    line = line.strip()
    key, value = line.split("\t")
    value = float(value)

    if key == current_key:
        current_sum += value
        current_count += 1
    else:
        if current_key:
            print(f"{current_key}\t{current_sum:.2f}\t{current_count}")
        current_key = key
        current_sum = value
        current_count = 1

if current_key:
    print(f"{current_key}\t{current_sum:.2f}\t{current_count}")