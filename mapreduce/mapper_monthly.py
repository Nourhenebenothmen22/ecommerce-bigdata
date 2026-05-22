#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    parts = line.split(",")
    if parts[0] == "order_id":
        continue
    try:
        date = parts[1]
        month = date[:7]
        total = parts[6]
        print("%s\t%s" % (month, total))
    except:
        continue