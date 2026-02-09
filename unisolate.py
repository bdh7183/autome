#!/usr/bin/env python3

from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone

HEADER = "axonius_aggregated_id,Host,OS,axonius_paloalto_xdr_endpoint_id,cortexxdr_isolated_date,cortexxdr_isolated_by,cortexxdr_unisolated_date,cortexxdr_unisolated_by,cortexxdr_unisolated_comment,"
FILE = "gois_asset_inventory_blocked_unsupported_operating_systems.csv"
NETID = "bdh7183"


# Make sure host isn't already unisolated
def check_data(data):
    if (data.get("cortexxdr_unisolated_date")):
        return False
    if (data.get("cortexxdr_unisolated_comment")):
        return False
    if (data.get("cortexxdr_unisolated_by")):
        return False
    return True


# Create a timestamp of current time in Eastern timezone
def make_timestamp():
    est_offset = timezone(timedelta(hours=-5))
    now_est = datetime.now(timezone.utc).astimezone(est_offset)
    formatted_date = now_est.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


def pull_data(filename, eid):
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


# convert a line of CSV into a dictionary
def line_to_dict(s):
    heads = HEADER.split(",")
    return dict(zip(heads, s.split(",")))


# convert a dictionary to a line of CSV
def dict_to_line(data):
    return ",".join(map(str, data.values()))


def print_found_data(line):
    for val in line:
        if val and line[val]:
            print(f"{val}: {line[val]}")


if __name__ == '__main__':
    xdr = input("Enter a cortex XDR ID: ").strip()
    lines, found = pull_data(FILE, xdr)

    if not found:
        print("NOT FOUND")
        exit(1)

    timestamp = make_timestamp()

    parsedLine = line_to_dict(lines[found])

    if(not check_data(parsedLine)):
        print("device is already unisolated, check again")
        print_found_data(parsedLine)
        exit(1)

    comment = input("Enter a comment: ").strip()

    # update line
    parsedLine["cortexxdr_unisolated_date"] = timestamp
    parsedLine["cortexxdr_unisolated_comment"] = comment
    parsedLine["cortexxdr_unisolated_by"] = NETID

    # convert back to csv and replace
    newline = dict_to_line(parsedLine)
    lines[found] = newline

    print(newline)
    update_file("newtest.csv", lines)

