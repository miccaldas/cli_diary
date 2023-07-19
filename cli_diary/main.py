"""Where all functions are called by the user."""
import questionary

# import snoop
from questionary import Separator, Style

from delete import delete
from edit import edit
from new import new_main
from search import search
from see import see_main
from update import update
from view import view_main
from choicecmd import dbcall, postlist, on_press

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
            "View Markdown Posts",
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
        dbcall()
        postlist()
        on_press()
    if selection == "Create Post":
        new_main()
    if selection == "Edit Post":
        edit()
    if selection == "Search Posts":
        search()
    if selection == "Delete Post":
        delete()
    if selection == "Update Post":
        update()
    if selection == "See Posts":
        see_main()


if __name__ == "__main__":
    main()
