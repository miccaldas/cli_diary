"""Deletes post from folders and database."""
import os

import click

# import snoop
from mysql.connector import Error, connect

# from snoop import pp

# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def delete():
    """
    Shows all posts' titles and id's, asks
    what is the id of the post to delete.
    Get the title of the chosen id, deletes it
    from the markdown and html folders.
    Deletes entry in the database with the
    chosen id.
    """
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = "SELECT id, title FROM cli_diary"
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            print(click.style(f"  {row[0]} - ", fg="bright_green", bold=True), click.style(row[1], fg="bright_white", bold=True))
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, e

    print("\n")
    choi = input(click.style("[*] - What is the id of the post you want to delete? ", fg="bright_green", bold=True))
    choice = int(choi)

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        answers = [choice]
        query = "SELECT title FROM cli_diary WHERE id = %s"
        cur.execute(query, (choice,))
        record = cur.fetchone()
        title_str = " "
        title = title_str.join(record)
        filename_html = f"{title}.html"
        filename_md = f"{title}.md"
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, e

    if filename_html in os.listdir("html_posts"):
        os.remove(f"html_posts/{filename_html}")
    if filename_md in os.listdir("md_posts"):
        os.remove(f"md_posts/{filename_md}")
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        answers = [choice]
        query = "DELETE FROM cli_diary WHERE id = %s"
        cur.execute(query, answers)
        conn.commit()
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg

    return filename_md, filename_html


if __name__ == "__main__":
    delete()
