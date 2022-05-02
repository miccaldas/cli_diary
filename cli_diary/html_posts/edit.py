"""Module Docstring"""
import isort
import snoop
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def edit():
    """"""


if __name__ == "__main__":
    edit()
