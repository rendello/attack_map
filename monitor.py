
"""
Monitor the ssh authlog file on OpenBSD.
Determine the likely origin country of new failed logins, then:
- Store this information in an SQLite database, and
- Send an IPC signal to the web framework that the data has changed.
"""

import time
import re

#import openbsd


AUTHLOG_PATH = "/var/log/authlog"
AUTHLOG_PATH = "/home/gtgt9/Downloads/authlog"

# 1=YYYY-MM-DDTHH:MM:SS.SSS (ISO-8601, "T" is a literal "T")
LOG_TURN_OVER_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}).*logfile turned over$"
)

# 1=Month name, 2=Day of month, 3=HH:MM:SS 4=user, 5=ip, 6=port.
LOG_FAILED_PASSWORD_PATTERN = re.compile(
    r"^(\w{3,9}) {,2}(\d{,2}) (\d{2}:\d{2}:\d{2}) \w+ \w+\[\d+\]: Failed password for (\w+) from (.*) port (\d+) ssh2$",
    flags=re.MULTILINE
)


# =============================================================================

def convert_log_entry_date(turn_over_timestamp, month_name, day_of_month, time):
    """ Change date to the same YYYY-MM-DDTHH:MM:SS.SSS (ISO-8601) format
    that's used for the turn over date and that's accepted by SQLite.
    
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


# =============================================================================

with open(AUTHLOG_PATH) as f:
    s = f.readline()
    turn_over_match = re.match(LOG_TURN_OVER_PATTERN, s)

    turn_over_timestamp = turn_over_match.group(1)

    for line in f:
        entry_match = re.match(LOG_FAILED_PASSWORD_PATTERN, line)
        if entry_match is not None:
            month_name, day_of_month, time, username, ip, port = entry_match.group(1, 2, 3, 4, 5, 6)
            ISO_8601_date = convert_log_entry_date(turn_over_timestamp, month_name, day_of_month, time)



def process_new_entries():
    pass
