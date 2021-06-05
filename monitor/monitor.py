""" Monitor the authlog on OpenBSD and store failed password entries in
a database.

More precisely:
    (Setup)
    - Create a map of IP blocks to country codes,
    - Sandbox the process with `pledge` and `unveil`,
    (Loop)
    - Read the new lines of the authlog,
    - Grab the failed password SSH login information,
    - Map the attacking IPs to their respective country codes,
    - Store the relevent attack data in the SQLite database,
    - Wait a bit; goto `Loop`.

Note: Logs are sent directly to stdout, as this program is to be daemonized by
Supervisor/supervisord. """

import bisect
import collections
import datetime
import ipaddress
import pathlib
import platform
import re
import signal
import sqlite3
import sys
import time

import openbsd
import toml

import constants


# =============================================================================

# 1=YYYY-MM-DDTHH:MM:SS.SSS (ISO-8601 variant, the "T" is literal)
LOG_TURN_OVER_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}).*logfile turned over$"
)

# 1=<3-letter month name> DD HH:MM:SS 2=user, 3=ip (v4).
LOG_FAILED_PASSWORD_PATTERN = re.compile(
    (r"(\w{3} {1,2}\d{,2} \d{2}:\d{2}:\d{2}) \w+ \w+\[\d+\]: "
    +r"Failed password for (?:invalid user )?(\w+) from (.*) port \d+ ssh2"),
    flags=re.MULTILINE
)

SSHFailedEntry = collections.namedtuple("SSHFailedEntry", ("timestamp", "ip", "username", "nation"))


# =============================================================================

def siginfo_handler(signal_number, frame):
    """ See `process_status` definition. """
    global process_status
    try:
        print(process_status)
    except NameError:
        pass


# IP-block-to-country-code functions ==========================================
# IPv4 only. IPs are stored as integers in RAM to save on space.

def file_paths_in_dir(dir_path_name):
    file_paths = []
    for entry in pathlib.Path(dir_path_name).iterdir():
        if entry.is_file():
            file_paths.append(entry)
    return file_paths


def pull_IP_blocks_from_dir(base_dir_path):
    """ Grab IP blocks per country from a data set, return a list of every
    block's starting address in ascending order.
    
    Expects the base folder to have the subdirectories "ipv4" and "ipv6", each
    of which will contain files for all countries in the format "XX.cidr",
    where XX is the country code. The files should list the ip blocks in CIDR
    format, one per line. """

    global process_status

    blocks = []
    for path in file_paths_in_dir(f"{base_dir_path}/ipv4"):
        country_code = path.name.replace(".cidr", "")
        process_status = f'Loading IPv4 blocks for country: "{country_code.upper()}".'
        with open(path, "r") as f:
            for line in f.readlines():
                ip_address = int(ipaddress.IPv4Network(line.strip()).network_address)
                blocks.append((ip_address, country_code))

    process_status = f'Sorting IPv4 blocks.'
    return sorted(blocks, key=lambda tup: ipaddress.IPv4Address(tup[0]))


def get_country_from_ip(ipv4_blocks, ip):
    """ Returns two-digit country code. """

    blocks = ipv4_blocks
    ip_tuple = (int(ipaddress.IPv4Address(ip)), )

    i = bisect.bisect_right(blocks, ip_tuple)
    if i > len(blocks) - 1:
        return blocks[-1][1]
    else:
        return blocks[i-1][1]


# Logfile monitor functions ===================================================

def log_entry_timestamp_to_posix_timestamp(turn_over_timestamp, timestamp) -> float:
    """ Change log entry timestamp to floating-point POSIX timestamp.
    
    Entry dates are given in this format: "May 17 18:00:38". We rely on the
    log's turn over date (in another format, ISO 8601) to give us the year. """

    month_num_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

    turn_over_year = int(turn_over_timestamp[0:4])
    turn_over_month = int(turn_over_timestamp[5:7])

    year = turn_over_year
    month = month_num_map[timestamp[0:3]]
    day = int(timestamp[4:6])
    hour = int(timestamp[7:9])
    minute = int(timestamp[10:12])
    second = int(timestamp[13:15])

    if month < turn_over_month:
        year += 1

    return datetime.datetime(year, month, day, hour, minute, second).timestamp()


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
            non_posix_timestamp, username, ip = entry_match
            timestamp = log_entry_timestamp_to_posix_timestamp(turn_over_timestamp, non_posix_timestamp)
            nation = get_country_from_ip(ip_blocks, ip)
            new_entries.append(SSHFailedEntry(timestamp, ip, username, nation))

    cursor_position = f.tell()

    return new_entries, cursor_position, turn_over_timestamp


# =============================================================================

def commit_entries_to_db(entries, db_path):
    """ Open SQLite db, dump entries, close db. """

    con = sqlite3.connect(constants.DB_PATH)
    cur = con.cursor()

    try:
        cur.execute("SELECT MAX(timestamp) FROM ssh_password_violations")
        latest_entry_timestamp = float(cur.fetchone()[0])
    except TypeError:
        latest_entry_timestamp = float(0)

    for entry in entries:
        if entry.timestamp > latest_entry_timestamp:
            cur.execute(
                """
                INSERT INTO ssh_password_violations
                (timestamp, ip, username, nation)
                VALUES (?, ?, ?, ?)
                """,
                (entry.timestamp, entry.ip, entry.username, entry.nation)
            )

    con.commit()
    con.close()


# =============================================================================

if __name__ == "__main__":

    # Information about the process' status to be returned on OpenBSD SIGINFO
    # through `siginfo_handler()`. Should be updated when any long-running action
    # is initiated.
    process_status = str()
    signal.signal(signal.SIGINFO, siginfo_handler)

    with open(constants.CONFIG_PATH, "r") as f:
        config = toml.load(f)

    ip_blocks = pull_IP_blocks_from_dir(config["country_ip_blocks"])

    openbsd.unveil(constants.AUTHLOG_PATH, "r");
    openbsd.unveil(constants.DB_DIR_PATH, "rwc");
    openbsd.pledge("stdio flock proc rpath wpath cpath tmppath fattr");

    cursor_position = 0
    turn_over_timestamp = ""
    loop_count = 0
    while True:
        with open(constants.AUTHLOG_PATH) as f:
            new_entries, cursor_position, turn_over_timestamp = process_new_entries(f, turn_over_timestamp, cursor_position)
        for e in new_entries:
            print(e)
        print("===============")

        commit_entries_to_db(new_entries, constants.DB_PATH)

        time.sleep(10)
        loop_count += 1
        process_status = f"Monitoring log file. Loop count: {loop_count}"
