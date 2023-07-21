"""Where all functions are called by the user."""
import subprocess

import questionary

# import snoop
from questionary import Separator, Style

from delete import delete
from edit import edit
from new import new_main
from search import search_main
from see import see_main
from update import update
from view import view_main

# from snoop import pp


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def main():
    """
    We'll create a dropdown with Questionary for
    the user to access all modules. We'll call
    the ones the user chooses.
    The 'view markdown post', has a 'pynput'
    observer object that makes it impossible to
    use it through import. We'll used by subprocess.
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
        "What do you want to do?",
        qmark=" [X]",
        pointer="»»",
        use_indicator=True,
        style=custom_style_diary,
        choices=[
            "View HTML Post",
            "View Markdown Post",
            "Create Post",
            "Edit Post",
            "Search Posts",
            "Delete Post",
            "Update Post",
            "See Posts",
            Separator(),
            "Exit",
        ],
    ).ask()

    if selection == "Exit":
        raise SystemExit
    if selection == "View HTML Post":
        view_main()
    if selection == "View Markdown Post":
        cmd = "/usr/bin/python /home/mic/python/cli_diary/cli_diary/choicemd.py"
        subprocess.run(cmd, shell=True)
    if selection == "Create Post":
        new_main()
    if selection == "Edit Post":
        edit()
    if selection == "Search Posts":
        search_main()
    if selection == "Delete Post":
        delete()
    if selection == "Update Post":
        update()
    if selection == "See Posts":
        see_main()


if __name__ == "__main__":
    main()
