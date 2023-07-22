"""
Module to search posts by tag.
"""
import pickle
import subprocess
import webbrowser

import questionary

# import snoop
from mysql.connector import Error, connect
from pyfzf.pyfzf import FzfPrompt
from questionary import Separator, Style

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
def file_type():
    """
    Defines what type of file he wants to see; HTML or Markdown.
    """
    custom_style_diary = Style(
        [
            ("qmark", "fg:#FF6363 bold"),
            ("question", "fg:#069A8E bold"),
            ("answer", "fg:#A1E3D8"),
            ("pointer", "fg:#F8B400 bold"),
            ("highlighted", "fg:#F7FF93 bold"),
            ("selected", "fg:#FAF5E4 bold"),
            ("separator", "fg:#069A8E"),
            ("instruction", "fg:#A1E3D8"),
            ("text", "fg:#FAF5E4 bold"),
        ]
    )

    selection = questionary.select(
        "What kind of posts do you want to see?",
        qmark=" [X]",
        pointer="»»",
        use_indicator=True,
        style=custom_style_diary,
        choices=[
            "HTML Posts",
            "Markdown Posts",
            Separator(),
            "Exit",
        ],
    ).ask()

    if selection == "Exit":
        raise SystemExit
    if selection == "HTML Posts":
        posttype = "html"
    if selection == "Markdown Posts":
        posttype = "markdown"

    with open("posttype.bin", "wb") as f:
        pickle.dump(posttype, f)


# @snoop
def dbcall():
    """
    Gets a list of all tags in the database.
    """
    query = "SELECT k1 from cli_diary UNION SELECT k2 FROM cli_diary"
    taglst = dbdata(query, "fetch")
    taglist = [i[0] for i in taglst]

    return taglist


# @snoop
def tag_search():
    """
    User chooses a search tag.
    """
    taglist = dbcall()
    fzf = FzfPrompt()

    tagchoice = fzf.prompt(
        taglist,
        '--border bold --border-label="╢Choose a Tag╟" --border-label-pos bottom',
    )

    with open("tagchoice.bin", "wb") as f:
        pickle.dump(tagchoice, f)


# @snoop
def get_titles():
    """
    List of titles in the entries that have the user's
    chosen tag.
    """
    with open("tagchoice.bin", "rb") as f:
        tagchoice = pickle.load(f)
    query = f"SELECT title FROM cli_diary WHERE k1 = '{tagchoice[0]}' OR k2 = '{tagchoice[0]}'"
    titles = dbdata(query, "fetch")

    return titles


# @snoop
def create_paths():
    """
    Create paths to post files, taking into account
    if the user chose html or markdown.
    """
    titles = get_titles()
    with open("posttype.bin", "rb") as f:
        posttype = pickle.load(f)

    htmlfolder = "/home/mic/python/cli_diary/cli_diary/html_posts"
    mdfolder = "/home/mic/python/cli_diary/cli_diary/md_posts"

    if posttype == "html":
        paths = [f"{htmlfolder}/{i[0]}.html" for i in titles]
    else:
        paths = [f"{mdfolder}/{i[0]}.md" for i in titles]

    return paths


# @snoop
def finallst():
    """
    From the paths created, the user chooses one to open.
    """
    with open("tagchoice.bin", "rb") as f:
        tagchoice = pickle.load(f)
    paths = create_paths()
    fzf = FzfPrompt()

    tagfile = fzf.prompt(
        paths,
        f'--border bold --border-label="╢Posts With the Tag {tagchoice[0].upper()}╟" --border-label-pos bottom',
    )

    return tagfile[0]


# @snoop
def open_lst():
    """
    Opens the chosen file.
    """
    tagfile = finallst()
    if tagfile.endswith(".html"):
        webbrowser.open(f"file://{tagfile}")
    if tagfile.endswith(".md"):
        cmd = f"mdless {tagfile}"
        subprocess.run(cmd, shell=True)


# @snoop
def tag_main():
    """
    Calls all previous functions.
    """
    file_type()
    tag_search()
    open_lst()


if __name__ == "__main__":
    tag_main()
