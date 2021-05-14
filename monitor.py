""" Monitor the authlog on OpenBSD and store failed password entries in
a database.

More precisely:
    (Setup)
    - Create a map of IP blocks to country codes.
    - Sandbox process with `pledge` and `unveil`.
    (Loop)
    - Read the new lines of the authlog,
    - Grab the failed password SSH login process_statusrmation,
    - Map the attacking IPs to their respective country codes,
    - Store the relevent attack data in the SQLite database.
    - Wait a bit; goto `Loop`.
"""

import bisect
import ipaddress
import pathlib
import platform
import re
import signal
import sqlite3
import sys
import time

import appdirs
import openbsd
import toml

# Constants ===================================================================

AUTHLOG_PATH = "/var/log/authlog"

# 1=YYYY-MM-DDTHH:MM:SS.SSS (ISO-8601, "T" is a literal "T")
LOG_TURN_OVER_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}).*logfile turned over$"
)

# 1=Month name, 2=Day of month, 3=HH:MM:SS 4=user, 5=ip.
LOG_FAILED_PASSWORD_PATTERN = re.compile(
    r"(\w{3}) {1,2}(\d{,2}) (\d{2}:\d{2}:\d{2}) \w+ \w+\[\d+\]: Failed password for (?:invalid user )?(\w+) from (.*) port \d+ ssh2",
    flags=re.MULTILINE
)


# =============================================================================

def siginfo_handler(signal_number, frame):
    """ See `process_status` definition """
    global process_status
    try:
        print(process_status)
    except NameError:
        pass


# IP-block-to-country-code functions ==========================================

def file_paths_in_dir(dir_path_name):
    file_paths = []
    for entry in pathlib.Path(dir_path_name).iterdir():
        if entry.is_file():
            file_paths.append(entry)
    return file_paths


def pull_IP_blocks_from_dir(base_dir_path, ip_version):
    """ Grab IP blocks per country from a data set, return a list of every
    block's starting address in ascending order.
    
    Expects the base folder to have the subdirectories "ipv4" and "ipv6", each
    of which will contain files for all countries in the format "XX.cidr",
    where XX is the country code. The files should list the ip blocks in CIDR
    format, one per line. """

    global process_status

    version_dir_path = f"{base_dir_path}/ipv{ip_version}"
    if ip_version == 4:
        IPNetwork = ipaddress.IPv4Network
        IPAddress = ipaddress.IPv4Address
    elif ip_version == 6:
        IPNetwork = ipaddress.IPv6Network
        IPAddress = ipaddress.IPv6Address

    blocks = []
    for path in file_paths_in_dir(version_dir_path):
        country_code = path.name.replace(".cidr", "")
        process_status = f'Loading IPv{ip_version} blocks for country: "{country_code.upper()}".'
        with open(path, "r") as f:
            for line in f.readlines():
                ip_address = IPNetwork(line.strip()).network_address
                blocks.append((ip_address, country_code))

    process_status = f'Sorting IPv{ip_version} blocks.'
    return sorted(blocks, key=lambda tup: IPAddress(tup[0]))


def get_country_from_ip(ipv4_blocks, ipv6_blocks, ip):
    """ Returns two-digit country code. """
    if "." in ip:
        blocks = ipv4_blocks
        ip_tuple = (ipaddress.IPv4Address(ip), )
    else:
        blocks = ipv6_blocks
        ip_tuple = (ipaddress.IPv6Address(ip), )

    i = bisect.bisect_right(blocks, ip_tuple)
    if i > len(blocks) - 1:
        return blocks[-1][1]
    else:
        return blocks[i-1][1]


# Logfile monitor functions ===================================================

def convert_log_entry_timestamp(turn_over_timestamp, month_name, day_of_month, time):
    """ Change date to YYYY-MM-DDTHH:MM:SS.SSS (ISO-8601) format that's
    accepted by SQLite (and used by default for the turn over timestamp).
    
    All args are strings for consistency. """

    month_num_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

    turn_over_year = int(turn_over_timestamp[0:4])
    turn_over_month = int(turn_over_timestamp[5:7])
    
    year = turn_over_year
    month = month_num_map[month_name]
    day = int(day_of_month)

    if month < turn_over_month:
        year += 1

    return f"{year}-{month:02}-{day:02}T{time}.000"


def process_new_entries(f, old_turn_over_timestamp, old_cursor_position):
    """ Return the new entries in a usable format. Only allocates/reads the
    first line and the new part of the file. """

    s = f.readline()
    turn_over_timestamp = re.match(LOG_TURN_OVER_PATTERN, s).group(1)

    if turn_over_timestamp == old_turn_over_timestamp:
        cursor_position = old_cursor_position
    else:
        cursor_position = 0

    f.seek(cursor_position)
    new_entries = []
    for entry_match in re.findall(LOG_FAILED_PASSWORD_PATTERN, f.read()):
        if entry_match is not None:
            month_name, day_of_month, time, username, ip = entry_match
            ISO_8601_date = convert_log_entry_timestamp(turn_over_timestamp, month_name, day_of_month, time)
            new_entries.append((ISO_8601_date, username, ip))

    cursor_position = f.tell()

    return new_entries, cursor_position, turn_over_timestamp


# =============================================================================
#cur.execute("create table lang (lang_name, lang_age)")
#cur.execute("CREATE TABLE password_violations (username TEXT, ip TEXT, date TEXT, nation TEXT)")

def commit_entries_to_db(entries):
    """ Open db, dump entries, close db. Despite their expense, the occasional
    opening and closing of the db allows other applications to access it. """

    con = sqlite3.connect('example.db').cursor()
    cur = con.cursor()
    for e in entries:
        cur.execute("INSERT INTO ssh VALUES (?, ?)")
    con.commit()
    con.close()

# =============================================================================



if __name__ == "__main__":

    # Information about the process' status to be returned on OpenBSD SIGINFO
    # through `siginfo_handler()`. Should be updated when any long-running action
    # is initiated.
    process_status = str()
    signal.signal(signal.SIGINFO, siginfo_handler)

    config_file = pathlib.Path(appdirs.user_config_dir("SSH_Map")).joinpath("config.toml")
    with open(config_file, "r") as f:
        config = toml.load(f)

    ipv4_blocks = pull_IP_blocks_from_dir(config["country_ip_blocks"], 4)
    ipv6_blocks = pull_IP_blocks_from_dir(config["country_ip_blocks"], 6)

    cursor_position = 0
    turn_over_timestamp = ""
    while True:
        with open(AUTHLOG_PATH) as f:
            new_entries, cursor_position, turn_over_timestamp = process_new_entries(f, turn_over_timestamp, cursor_position)
        for e in new_entries:
            print(e)
            print(get_country_from_ip(ipv4_blocks, ipv6_blocks, e[2]))
        print("===============")
        time.sleep(10)
