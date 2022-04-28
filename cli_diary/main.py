"""Where all functions are called by the user."""
import sys

import isort
import questionary
import snoop
from questionary import Separator, Style
from snoop import pp

from delete import delete
from edit import edit
from new import new
from see import see
from update import update
from view import index, show


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def main():
    """
    We'll create a dropdown with Questionary for
    the user to access all modules. We'll call
    the ones the user chooses.
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
        qmark="[X]",
        pointer="»»",
        use_indicator=True,
        style=custom_style_diary,
        choices=[
            "View Post",
            "Create Post",
            "Edit Post",
            "Delete Post",
            "Update Post",
            "See Posts",
            Separator(),
            "Exit",
        ],
    ).ask()

    if selection == "Exit":
        sys.exit()
    if selection == "View Post":
        show()
    if selection == "Create Post":
        new()
    if selection == "Edit Post":
        edit()
    if selection == "Delete Post":
        delete()
    if selection == "Update Post":
        update()
    if selection == "See Posts":
        see()


if __name__ == "__main__":
    main()
