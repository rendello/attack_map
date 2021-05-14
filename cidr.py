import bisect
import ipaddress
import pathlib
import platform
import signal
import sys

import appdirs
import toml


# =============================================================================

def file_paths_in_dir(dir_path_name):
    file_paths = []
    for entry in pathlib.Path(dir_path_name).iterdir():
        if entry.is_file():
            file_paths.append(entry)
    return file_paths


def pull_ranges_from_dir(base_dir_path, ip_version):
    """ Grab IP ranges per country from a data set, return a list of every
    block's starting address in ascending order.
    
    Expects the base folder to have the subdirectories "ipv4" and "ipv6", each
    of which will contain files for all countries in the format "XX.cidr",
    where XX is the country code. The files should list the ip blocks in CIDR
    format, one per line. """

    global info

    version_dir_path = f"{base_dir_path}/ipv{ip_version}"
    if ip_version == 4:
        IPNetwork = ipaddress.IPv4Network
        IPAddress = ipaddress.IPv4Address
    elif ip_version == 6:
        IPNetwork = ipaddress.IPv6Network
        IPAddress = ipaddress.IPv6Address

    ranges = []
    for path in file_paths_in_dir(version_dir_path):
        country_code = path.name.replace(".cidr", "")
        info = f"Loading {country_code} IPv{ip_version} blocks."
        with open(path, "r") as f:
            for line in f.readlines():
                ip_address = IPNetwork(line.strip()).network_address
                ranges.append((ip_address, country_code))

    return sorted(ranges, key=lambda tup: IPAddress(tup[0]))


def get_country(ranges, ip):
    i = bisect.bisect_right(ranges, ip)
    if i > len(ranges) - 1:
        return ranges[-1]
    else:
        return ranges[i-1]


# =============================================================================

IS_OPENBSD = (platform.system() == "OpenBSD")

if IS_OPENBSD:
    import openbsd

    def siginfo_handler(signal_number, frame):
        """ Handle the non-standard SIGINFO signal on OpenBSD by returning
        information about the program. Allows user to see information with
        "ctrl+t". """

        global info
        try:
            print(info)
        except NameError:
            pass

    signal.signal(signal.SIGINFO, siginfo_handler)


config_file = pathlib.Path(appdirs.user_config_dir("SSH_Map")).joinpath("config.toml")
with open(config_file, "r") as f:
    config = toml.load(f)


info = ""  # Process information for OpenBSD SIGINFO.
ipv4_ranges = pull_ranges_from_dir(config["country_ip_blocks"], 4)
ipv6_ranges = pull_ranges_from_dir(config["country_ip_blocks"], 6)

while True:
    ip = input("New IP: ")
    if "." in ip:
        country = get_country(ipv4_ranges, (ipaddress.IPv4Address(ip), ))
    else:
        country = get_country(ipv6_ranges, (ipaddress.IPv6Address(ip), ))
    print(country)
