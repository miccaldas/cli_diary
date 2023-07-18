"""
Edits an existing post.
"""
import os
import subprocess
import click

# import snoop
from mysql.connector import Error, connect

# from snoop import pp


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


def dbdata(query, data):
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
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
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


# @snoop
def dbchoices():
    """
    Collects titles and id's of posts, for the user to
    choose what it wants to edit.
    """
    query = "SELECT id, title FROM cli_diary"
    idlst = dbdata(query, "fetch")

    return idlst


# @snoop
def edit():
    """
    Shows db contents, user chooses post, we open it
    on vim. After the editing process, we delete the
    old html file and replace it with a new one.
    """
    records = dbchoices()
    for row in records:
        print(click.style(f"  {row[0]} - ", fg="bright_green", bold=True), click.style(row[1], fg="bright_white", bold=True))

    print("\n")
    choi = input(click.style("[*] - What is the id of the post you want to edit? ", fg="bright_green", bold=True))
    choice = int(choi)

    query = f"SELECT title FROM cli_diary WHERE id = {choice}"
    record = dbdata(query, "fetch")

    title_str = " "
    title = title_str.join(record)
    filename_html = f"{title}.html"
    filename_md = f"{title}.md"

    cmd = f"vim {filename_md}"
    subprocess.run(cmd, cwd="md_posts", shell=True)

    os.remove(f"html_posts/{filename_html}")

    cmd1 = f"pandoc --highlight-style=zenburn -s -o html_posts/{filename_html} md_posts/{filename_md}"
    subprocess.run(cmd1, shell=True)


if __name__ == "__main__":
    edit()
