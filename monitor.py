""" Monitor the ssh authlog file on OpenBSD.
Determine the likely origin country of new failed logins, then:
- Store this information in an SQLite database, and
- Send an IPC signal to the web framework that the data has changed.

May not catch the last few lines before a log file rollover.
"""

import re
import sqlite3
import time

#import openbsd


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

cursor_position = 0
turn_over_timestamp = ""
while True:
    with open(AUTHLOG_PATH) as f:
        new_entries, cursor_position, turn_over_timestamp = process_new_entries(f, turn_over_timestamp, cursor_position)
    for e in new_entries:
        print(e)
    print(cursor_position)
    print("===============")
    time.sleep(10)
