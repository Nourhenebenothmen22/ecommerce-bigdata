#!/usr/bin/env python3
import sys

current_key = None
current_sum = 0

for line in sys.stdin:
    line = line.strip()
    key, value = line.split("\t")
    value = float(value)

    if key == current_key:
        current_sum += value
    else:
        if current_key:
            print(f"{current_key}\t{current_sum:.2f}")
        current_key = key
        current_sum = value

if current_key:
    print(f"{current_key}\t{current_sum:.2f}")