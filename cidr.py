import bisect
import ipaddress
import pathlib
import sys


def get_country(ranges, ip):
    i = bisect.bisect_right(ranges, ip)
    if i > len(ranges) - 1:
        return ranges[-1]
    else:
        return ranges[i-1]


def file_paths_in_dir(dir_path_name):
    file_paths = []
    for entry in pathlib.Path(dir_path_name).iterdir():
        if entry.is_file():
            file_paths.append(entry)
    return file_paths


def pull_ranges_from_dir(dir_path):
    """ Grab IP ranges per country from a data set, return a list of each
    block's staring address, in ascending order.
    
    Expects the data set to be a directory of all countries in the format
    `<2 letter country code>.cidr`. The files should list the ip blocks in CIDR
    format, one per line. """

    ranges = []
    for path in file_paths_in_dir(dir_path):
        country_code = path.name.replace(".cidr", "")
        with open(path, "r") as f:
            for line in f.readlines():
                ip_address = ipaddress.IPv4Network(line.strip()).network_address
                ranges.append((ip_address, country_code))

    return sorted(ranges, key=lambda tup: ipaddress.IPv4Address(tup[0]))


ranges = pull_ranges_from_dir("./ipv4")
while True:
    ip = input("New IP: ")
    country = get_country(ranges, (ipaddress.IPv4Address(ip), ))
    print(country)
