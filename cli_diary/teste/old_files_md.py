"""

"""
import os
import pickle
import random

import snoop
from pynput.mouse import Button, Controller

# import subprocess
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def packs():
    """
    De forma a que cada post tenha umas coordenadas que o
    possam identificar, criamos coordenadas ao acaso, mas
    dentro dos limites do ecrã do terminal. Juntamo-los,
    também de forma randomizada a cada uma dos posts.
    """
    mouse = Controller()

    mdfolder = "/home/mic/python/cli_diary/cli_diary/md_posts"
    mdfiles = os.listdir(mdfolder)

    length = random.sample(range(0, 3440), 53)
    height = random.sample(range(0, 1440), 53)
    coords = [(random.choice(length), random.choice(height)) for _ in range(53)]
    packs = [(random.choice(mdfiles), random.choice(coords)) for _ in range(53)]

    with open("packs.bin", "wb") as f:
        pickle.dump(packs, f)


if __name__ == "__main__":
    packs()
