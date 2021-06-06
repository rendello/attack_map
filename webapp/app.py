
import sqlite3

import flask

# =============================================================================

def fetch_from_db(query, params=tuple()):
    con = sqlite3.connect("attack_data.sqlite")
    cur = con.cursor()

    cur.execute(query, params)
    data = cur.fetchall()
    con.close()

    return data


def api_error(message, code=400):
    return (flask.jsonify({"error": message}), code)


# =============================================================================

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/api/ssh_attack_summary.json", methods=["GET"])
def ssh_attack_summary():

    data_as_tuples = fetch_from_db(
        """SELECT nation, COUNT(nation) FROM ssh_password_violations
        GROUP BY nation ORDER BY COUNT(nation) DESC"""
    )
    data_as_dict = {}
    for tup in data_as_tuples:
        data_as_dict[tup[0]] = tup[1]

    return flask.jsonify(data_as_dict)


@app.route("/api/ssh_attack_data.json/", methods=["GET"])
@app.route("/api/ssh_attack_data.json/since/<since_str>", methods=["GET"])
def ssh_attack_new_data(since_str="0"):
    if since_str.isdigit():
        since = int(since_str)
    else:
        return api_error(
            "`since` value must be a positive integer representing a valid POSIX timestamp."
        )

    data = fetch_from_db(
        """ SELECT timestamp, username, nation FROM ssh_password_violations
        WHERE timestamp > (?) ORDER BY timestamp DESC LIMIT 100""",
        [since]
    )

    return flask.jsonify(data)


