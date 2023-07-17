"""
Searches db for query. Presents results.
"""
import os
import pickle
from datetime import datetime

# import snoop
from mysql.connector import Error, connect
from rich import box
from rich.console import Console
from rich.table import Table


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
    Uses MySQL queries with fulltext to search the database.
    """
    console = Console()
    ask = console.input("[bold #5E8B7E]\[*] - What do you want to search? [/]")

    query = f"SELECT title, time FROM cli_diary WHERE MATCH(title, k1, k2) AGAINST ('{ask}')"
    srchrslt = dbdata(query, "fetch")

    with open("srchrslt.bin", "wb") as f:
        pickle.dump(srchrslt, f)


# @snoop
def search():
    """
    Gets information from the database, the html files and makdown files.
    The first supplies the datetime values and titles, the other link to
    the html version and the latter is used as a preview.
    """
    with open("srchrslt.bin", "rb") as f:
        srchrslt = pickle.load(f)

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

    for entry in srchrslt:
        # The title kept in the db is the same used in naming the files.
        filename = entry[0]
        # These turn a filename in a real title.
        tspace = filename.replace("_", " ")
        upper = tspace.title()
        # Datetime data in human format.
        date = f"{entry[1].strftime('%Y-%m-%d %H:%M')}"
        # From the md file we take out the first 500 bytes, to serve as preview.
        with open(f"{mdfolder}/{filename}.md", "r") as g:
            mdtxt = g.readlines(500)
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
def search_main():
    """
    Calls all other functions in module.
    """
    dbcall()
    search()

    os.remove("srchrslt.bin")


if __name__ == "__main__":
    search_main()
