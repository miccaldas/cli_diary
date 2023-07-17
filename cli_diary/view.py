"""
Opens a table view of the post files that can be accessed by clicking them.
"""
import os
import pickle
from datetime import datetime

# import snoop
from mysql.connector import Error, connect
from rich import box
from rich.console import Console
from rich.table import Table

# from snoop import pp


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
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
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="cli_diary",
        )
        cur = conn.cursor()
        cur.execute(query)
        if data == "fetch":
            data = cur.fetchall()
        if data == "commit":
            data = conn.commit()
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data


# @snoop
def dbcall():
    """
    Calls the db to get date and title data.
    """
    query = "SELECT title, time FROM cli_diary ORDER BY title"
    datelink = dbdata(query, "fetch")

    with open("datelink.bin", "wb") as f:
        pickle.dump(datelink, f)


# @snoop
def view():
    """
    Gets information from the database, the html files and makdown files.
    The first supplies the datetime values and titles, the other link to
    the html version and the latter is used as a preview.
    """

    with open("datelink.bin", "rb") as f:
        datelink = pickle.load(f)

    htmlfolder = f"{os.getcwd()}/html_posts"
    mdfolder = f"{os.getcwd()}/md_posts"

    table = Table(
        box=box.HEAVY_EDGE,
        padding=1,
        highlight=True,
        show_lines=True,
        style="#69a297",
        header_style="bold #f5e8e0",
    )
    table.add_column("Datetime", vertical="middle", justify="center")
    table.add_column("Link", vertical="middle", justify="center")
    table.add_column("Preview", justify="full", style="#fff2cc", max_width=80)

    for entry in datelink:
        # The title kept in the db is the same used in naming the files.
        filename = entry[0]
        # These turn a filename in a real title.
        tspace = filename.replace("_", " ")
        upper = tspace.title()
        # Datetime data in human format.
        date = f"{entry[1].strftime('%Y-%m-%d %H:%M')}"
        # From the md file we take out the first 200 bytes, to serve as preview.
        with open(f"{mdfolder}/{filename}.md", "r") as g:
            mdtxt = g.readlines(200)
        mdtext = " ".join(mdtxt)
        # Loop that'll create the table with the former information.
        table.add_row(
            f"[bold #5E8B7E]{date}[/]",
            f"[bold #B2B8A3][link=file://{os.getcwd()}/html_posts/{filename}.html]{upper}[/link]",
            mdtext,
        )
    console = Console()
    console.print(table)


# @snoop
def view_main():
    """
    Calls all functions in this module.
    """
    dbcall()
    view()

    os.remove("datelink.bin")


if __name__ == "__main__":
    view_main()
