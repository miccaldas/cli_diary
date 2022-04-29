"""
Updates database entries.
"""
import click
import isort
import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def update():
    """
    Asks for column and id to make update.
    """

    column = input(click.style(" [X] - What is the column name? ", fg="bright_green", bold=True))
    value = input(click.style(" [X] - What is the alteration? ", fg="bright_green", bold=True))
    updt_id = int(input(click.style(" [X] - What is the id? ", fg="bright_green", bold=True)))

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        answers = [value, updt_id]
        query = f"UPDATE cli_diary SET {column} = %s WHERE id = %s"  # If 'column' value is a placeholder it turns to string and mysql won't accept it.
        cur.execute(query, answers)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    update()
