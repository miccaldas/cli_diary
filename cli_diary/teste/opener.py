"""
Module Docstring
"""
import snoop
from snoop import pp
from contextlib import suppress
import sys

# from configs.config import Efs, tput_config
# import os
import subprocess
from dotenv import load_dotenv
from pynput import mouse


sys.tracebacklimit = 0


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


@snoop
def on_click(x, y, button, pressed):
    """"""
    if pressed:
        coords = (x, y)
        print(coords)
        if coords == (1195, 1380):
            cmd = "frogmouth teste.md"
            subprocess.run(cmd, shell=True)
        if coords == (1173, 1344):
            cmd = "frogmouth teste1.md"
            subprocess.run(cmd, shell=True)
        if button == mouse.Button.right:
            return False
        # with suppress(TypeError):
        #     raise SystemExit


with mouse.Listener(on_click=on_click) as listener:
    listener.join()
