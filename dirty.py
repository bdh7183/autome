#!/usr/bin/env python3

from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone

HEADER = "axonius_aggregated_id,Host,OS,axonius_paloalto_xdr_endpoint_id,cortexxdr_isolated_date,cortexxdr_isolated_by,cortexxdr_unisolated_date,cortexxdr_unisolated_by,cortexxdr_unisolated_comment,"
file = "gois_asset_inventory_blocked_unsupported_operating_systems.csv"
netid = "bdh7183"


def check_data(data):
    if (data.get("cortexxdr_unisolated_date")):
        return False
    if (data.get("cortexxdr_unisolated_comment")):
        return False
    if (data.get("cortexxdr_unisolated_by")):
        return False
    return True


def make_timestamp():
    est_offset = timezone(timedelta(hours=-5))
    now_est = datetime.now(timezone.utc).astimezone(est_offset)
    formatted_date = now_est.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date

heads = HEADER.split(",")


xdr = input("Enter a cortex XDR ID: ").strip()
index = 0
found = False
lines = []

with open(file, "r") as fd:
    for line in fd:
        lines.append(line)
        if xdr in line:
            found = index
        index += 1

if not found:
    print("NOT FOUND")
    exit(1)

print(lines[found])

r = dict(zip(heads, lines[found].split(",")))

if(not check_data(r)):
    print("device is already unisolated, check again")
    exit(1)

# uniso = input("Enter a unisolate date (format: 2025-12-03 11:55:38): ").strip()
comment = input("Enter a comment: ").strip()

r["cortexxdr_unisolated_date"] = make_timestamp()
r["cortexxdr_unisolated_comment"] = comment
r["cortexxdr_unisolated_by"] = netid


newline = ",".join(map(str, r.values()))
lines[found] = newline

print(newline)

with open("newtest.csv", "w") as fd:
    for i in lines:
        fd.write(i)
