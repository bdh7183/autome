#!/usr/bin/env python3

from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone

HEADER = "axonius_aggregated_id,Host,OS,axonius_paloalto_xdr_endpoint_id,cortexxdr_isolated_date,cortexxdr_isolated_by,cortexxdr_unisolated_date,cortexxdr_unisolated_by,cortexxdr_unisolated_comment,"
FILE = "gois_asset_inventory_blocked_unsupported_operating_systems.csv"
NETID = "bdh7183"


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


def find_data(filename, eid):
    found = False
    data = []
    index = 0
    with open(filename, "r") as fd:
        for line in fd:
            data.append(line)
            if xdr in line:
                found = index
            index += 1
    return data, found


def update_file(filename, data):
    with open(filename, "w") as fd:
        for i in lines:
            fd.write(i)


def line_to_dict(s):
    heads = HEADER.split(",")
    return dict(zip(heads, s.split(",")))


def dict_to_line(data):
    return ",".join(map(str, data.values()))


heads = HEADER.split(",")


xdr = input("Enter a cortex XDR ID: ").strip()
lines, found = find_data(FILE, xdr)

if not found:
    print("NOT FOUND")
    exit(1)

timestamp = make_timestamp()

r = line_to_dict(lines[found])

if(not check_data(r)):
    print("device is already unisolated, check again")
    exit(1)

comment = input("Enter a comment: ").strip()

# update line
r["cortexxdr_unisolated_date"] = timestamp
r["cortexxdr_unisolated_comment"] = comment
r["cortexxdr_unisolated_by"] = NETID


newline = dict_to_line(r)
lines[found] = newline

print(newline)
update_file("newtest.csv", lines)

