"""
Shows content of the database and opens chosen
markdown file in less.
"""
import os
import pickle
import subprocess

# import snoop
from mysql.connector import Error, connect
from rich import box, print
from rich.console import Console

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
def dbcall():
    """
    Gets all information from the db.
    """
    query = "SELECT id, title, k1, k2, time FROM cli_diary ORDER BY time"
    data = dbdata(query, "fetch")

    with open("data.bin", "wb") as f:
        pickle.dump(data, f)


# @snoop
def see():
    """
    Shows posts in markdown using frogmouth.
    """
    with open("data.bin", "rb") as f:
        data = pickle.load(f)

    console = Console()
    for entry in data:
        date = f"{entry[4].strftime('%Y-%m-%d %H:%M')}"
        console.print(
            f"[bold #B2B8A3]{entry[0]}[/]",
            f"[bold #fff2cc]{entry[1]}.md[/]",
            f"[bold #96ceb4]{entry[2]}[/]",
            f"[bold #ffcc5c]{entry[3]}[/]",
            f"[bold #5E8B7E]{date}[/]",
            justify="full",
        )
    print("\n")
    choice = console.input("[bold #dd9245]/[*] - What is the ID of the post you want to read? [/]")
    query = f"SELECT title FROM cli_diary WHERE id = {choice}"
    title = dbdata(query, "fetch")
    tit = title[0][0]
    filename = f"{tit}.md"
    cmd = f"frogmouth md_posts/{filename}"
    subprocess.run(cmd, cwd=os.getcwd(), shell=True)


# @snoop
def see_main():
    """
    Initiates all functions in the module.
    """
    dbcall()
    see()

    os.remove("data.bin")


if __name__ == "__main__":
    see_main()
