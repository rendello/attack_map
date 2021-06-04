""" Run-once script to install SSH_Map program. """

import sqlite3
import os

import constants


def create_sqlite_db():
    con = sqlite3.connect(constants.DB_PATH)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE ssh_password_violations(
            timestamp   REAL,
            ip          TEXT,
            username    TEXT,
            nation      TEXT
        )
        """
    )
    con.commit()
    con.close()

create_sqlite_db()
