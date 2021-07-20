
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


@app.route("/api/ssh_attack_data.json", methods=["GET"])
def ssh_attack_new_data():
    since_query = flask.request.args.get("since") or "0"
    nation_query = flask.request.args.get("nation")
    max_items_query = flask.request.args.get("max_items") or "100"

    if since_query.isdigit():
        since = int(since_query)
    else:
        return api_error(
            "`since` value must be a positive integer representing a valid POSIX timestamp."
        )

    if max_items_query.isdigit():
        max_items = min(int(max_items_query), 100)
    else:
        return api_error("`max_items` value must be a positive integer.")

    if nation_query is not None:
        data = fetch_from_db(
            """
            SELECT timestamp, username, nation
            FROM ssh_password_violations
            WHERE timestamp > (?)
            AND nation = (?)
            ORDER BY timestamp DESC
            LIMIT (?)
            """,
            (since, nation_query, max_items)
        )
    else:
        data = fetch_from_db(
            """
            SELECT timestamp, username, nation
            FROM ssh_password_violations
            WHERE timestamp > (?)
            ORDER BY timestamp DESC
            LIMIT (?)
            """,
            (since, max_items)
        )

    data_as_dicts = []
    for datum in data:
        datum_as_dict = {
            "timestamp": datum[0],
            "username": datum[1],
            "nation": datum[2]
        }
        data_as_dicts.append(datum_as_dict)

    return flask.jsonify(data_as_dicts)


@app.route("/api/ssh_attack_top_usernames.json", methods=["GET"])
def ssh_attack_top_usernames():
    since_query = flask.request.args.get("since") or "0"
    nation_query = flask.request.args.get("nation")
    max_items_query = flask.request.args.get("max_items") or "100"

    if since_query.isdigit():
        since = int(since_query)
    else:
        return api_error(
            "`since` value must be a positive integer representing a valid POSIX timestamp."
        )

    if max_items_query.isdigit():
        max_items = min(int(max_items_query), 100)
    else:
        return api_error("`max_items` value must be a positive integer.")

    if nation_query is not None:
        data = fetch_from_db(
            """
            SELECT username, COUNT(username)
            FROM ssh_password_violations
            WHERE nation = (?)
            GROUP BY username
            ORDER BY COUNT(username) DESC
            LIMIT (?)
            """,
            (nation_query, max_items)
        )
    else:
        data = fetch_from_db(
            """
            SELECT username, COUNT(username)
            FROM ssh_password_violations
            GROUP BY username
            ORDER BY COUNT(username) DESC
            LIMIT (?)
            """,
            (max_items,)
        )

    return flask.jsonify(data)


@app.route('/', defaults={'path': ''})
def catch_all(path):
    return app.send_static_file("index.html")
