"""
Searches Markdown and HTML collections, with the help of 'fzf'.
"""
import os
import subprocess

import questionary

# import snoop
from questionary import Separator, Style

# from snoop import pp


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def search():
    """
    Just calling fzf inside the md and html folders.
    To open a file, just hover it and press 'F1'.
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
        "What do you want to search?",
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

    cmd = "fzf"
    if selection == "Exit":
        raise SystemExit
    if selection == "HTML Posts":
        subprocess.run(cmd, cwd="/home/mic/python/cli_diary/cli_diary/html_posts", shell=True)
    if selection == "Markdown Posts":
        subprocess.run(cmd, cwd="/home/mic/python/cli_diary/cli_diary/md_posts", shell=True)


if __name__ == "__main__":
    search()
