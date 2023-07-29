"""
MySQL module, to be shared by all modules.
"""
from mysql.connector import Error, connect


def dbdata(query, data, answers=None):
    """
    Collects list of posts on the db.
    We'll use this function as a template,
    letting the functions that call on it
    to define its structure. That being
    the query and if using .fetchall()
    or .commit()
    This permits writing just one db function
    per module.
    """
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="cli_diary",
        )
        cur = conn.cursor()
        if answers:
            cur.execute(query, answers)
        else:
            cur.execute(query)
        if data == "fetch":
            data = cur.fetchall()
        if data == "commit":
            data = conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data
