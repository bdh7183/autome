#!/usr/bin/env python3

import csv

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


heads = HEADER.split(",")

r = []
with open(file, newline='') as fd:
    reader = csv.DictReader(fd, delimiter=",", quoting=csv.QUOTE_MINIMAL, quotechar='"', escapechar='\\')
    for row in reader:
        r.append(row)

xdr = input("Enter a cortex XDR ID: ").strip()
print(r[0])
found = False

for i in range(len(r)-1, -1, -1):
    if r[i]["axonius_paloalto_xdr_endpoint_id"] == xdr:
        found = i

if found is False:
    print("NOT FOUND")
    exit(1)


if(not check_data(r[found])):
    print("device is already unisolated, check again")
    exit(1)

uniso = input("Enter a unisolate date (format: 2025-12-03 11:55:38): ")
comment = input("Enter a comment: ").strip()

r[found]["cortexxdr_unisolated_date"] = uniso
r[found]["cortexxdr_unisolated_comment"] = comment
r[found]["cortexxdr_unisolated_by"] = netid


with open("test.csv", "w", newline='') as outfile:
    writer = csv.DictWriter(outfile, heads, delimiter=",", quoting=csv.QUOTE_MINIMAL, quotechar='"', escapechar='\\')
    writer.writeheader()
    for i in r:
        writer.writerow(i)

print("DONE")