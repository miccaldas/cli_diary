---
title: "The Sound of Music Part2"
mainfont: Iosevka
---

A funny thing happened on my way here.  
As I said in the last post, there were things that I didn't liked on the last incarnation of the modules for the player commands:  
1. I was calling subprocess when I could solve all my needs just using [Psutil](https://psutil.readthedocs.io/en/latest/), which I was already using anyway, but not to do the search for the pid of the player's process.  
2. The bash command I was using, had some features that I copied without a critical attitude or any knowledge of what they meant. It worked just fine, but I felt that I should use a command I can thoroughly understand.  
3. The code for each command was 99% identical to the next, and divided in different modules. I thought that this could benefit from a 'tightening up'.  

When I started looking into this I found some surprises.
The old command code was built to find the ffplay process from the ffmpeg library and, as I remember, it worked fine. So at some moment in time, the player was using ffplay. Not anymore.  
Now when I tried to find a ffplay process, nothing came up. Apparently the player is working fine although not using ffplay or ffmpeg, as I couldn't find any processes by that name. The only process I found was in the name of 'python' and it referred to the player.py file.  
But, truthfully, I'm not sure anymore that these commands ever worked. I have a very hazy idea that they were written but not tested, or that I found something wrong and just forgot to correct it. I don't know. Too much time, too much drugs, everything turns to a soupy mash of days.  
But I soon realized that this mystery could be a blessing. Instead of wasting time trying to retrace my steps through alterations that I didn't document and did half-heartedly, I could start anew. A clean slate. And that is what I did.  
-------------------------------------------------------------------------------------------------------

## The Commands Module

1. Created a 'commands.py' module where I put all of the interactions with the player in a class. This is its code:  
2. Imported only psutil for the sourcing of the pid and the commands proper.
```python
import psutil
```
3. Created a class imaginatively called 'Commands'. At first I used a __init__ function, but soon discovered that it was more of a nuisance than a asset. I'm never sure if this is a very terrible thing to do (create a class without __init__) or just a venial sin, but in this case, I went without.
```python
class Commands:
```
4. Created a function to search for the pid of the python process for the player.py file.
```python
def find(self):
    """Find the process pid with psutil"""
```
5.  Create a list to house the processes output,
```python
lspid = []
```
6. the player name process is always python,
```python
name = 'python' 
```
7. for item in list of iterable processes names,
```python
for p in psutil.process_iter(['name']):
```
8. if process name is the same as python,
```python
     if p.info['name'] == name:
```
9. append to list,
```python
         lspid.append(p)
```
10. the player pid seems to be always the first on the list of processes.  As the list items are psutil.Process objects, you can add to it the pid method to return only the pid.
```python
player_pid = lspid[0].pid
```
11. Creates a psutil.Process with just the pid.
```python
 p = psutil.Process(int(player_pid))
```
12. Return the pid.
```python
return p
```
13. Function to kill the process. Importing the find() function and adding to it the kill() method from psutil. 'Mata' means kill in Portuguese.
```python
def mata(self):
    find = self.find()
    find.kill()
```
14. Function to suspend process. Same procedure as the last function.
```python
def suspend(self):
    find = self.find()
    find.suspend()
```
15. Function to resume process. More of the same.
```python
def resume(self):
    find = self.find()
    find.resume()
```

And here goes the complete code for this module:
```python
""" Module that aggregates all commands. find() gives the pid and the other functions use psutil to do various manipulations """
import psutil


class Commands:

    def find(self):
        """Find the process pid with psutil"""
        lspid = []                                  # Create a list to house the processes output
        name = 'python'                             # The player name process is always python
        for p in psutil.process_iter(['name']):     # For item in list of iterable processes names,
            if p.info['name'] == name:              # If process name is the same as python,
                lspid.append(p)                     # Append to list
        player_pid = lspid[0].pid                   # The player pid seems to be always the first on the list of processes.
        # As the list items are psutil.Process objects, you can add to it the pid method to return only the pid
        p = psutil.Process(int(player_pid))         # Creates a psutil.Process with just the pid
        return p

    def mata(self):
        find = self.find()
        find.kill()                                 # https://psutil.readthedocs.io/en/latest/

    def suspend(self):
        find = self.find()
        find.suspend()

    def resume(self):
        find = self.find()
        find.resume()
```
---------------------------------------------------------------------------------------

## The Main Module

If you read more than one post here, you already know that my memory is far from being my greatest asset. More of a hindrance really.  
So I tend to shy away from UI solutions that entail remembering commands. What I do is use prompt libraries to present the options as multiple choice questionnaire to the user, and link the choices to the respective functions.    
1. Regarding imports, I take from __future__, unicode literals. Needed for [questionary](https://questionary.readthedocs.io/en/stable/), the command line interface library; I get sys to have a sys.exit option for the user, the Commands class from the module we've talked above; the player module which houses the player, funnily enough; and finally the questionary library.
```python
from __future__ import unicode_literals
import sys
from commands import Commands
from player import player
import questionary
```
2. Create the questionary object,
```python
resposta = questionary.select(
        'What do you want do to? ',
        choices=[
            'Start the Player',
            'Stop the Player',
            'Suspend the Player',
            'Resume the Player',
            'Exit'
            ]).ask()
```
3. and link the choices to their respective functions or methods.
```python
if resposta == 'Start the Player':
    player()
if resposta == 'Stop the Player':
    com = Commands()
    com.mata()
if resposta == 'Suspend the Player':
    com = Commands()
    com.suspend()
if resposta == 'Resume the Player':
    com = Commands()
    com.resume()
if resposta == 'Exit':
    sys.exit()
```

Here's the complete code:
```python
""" Here we call the commands functions from the Commands class, and present them to the user as a multiple choice questionart """
from __future__ import unicode_literals
import sys
from commands import Commands
from player import player
import questionary

resposta = questionary.select(
        'What do you want do to? ',
        choices=[
            'Start the Player',
            'Stop the Player',
            'Suspend the Player',
            'Resume the Player',
            'Exit'
            ]).ask()

if resposta == 'Start the Player':
    player()
if resposta == 'Stop the Player':
    com = Commands()   # It is always needed to instantiate the class. Only then can you access the methods
    com.mata()
if resposta == 'Suspend the Player':
    com = Commands()
    com.suspend()
if resposta == 'Resume the Player':
    com = Commands()
    com.resume()
if resposta == 'Exit':
    sys.exit()
```
-----------------------------------------------------------------------------------------

## The Player Module

For completeness sake, here goes the player module. It uses the [Pydub](https://github.com/jiaaro/pydub/blob/master/API.markdown) library to play the music and has some folders and file manipulations to access the music.  
It also uses a threading function to be able to show a progress bar through [tqdm](https://github.com/tqdm/tqdm).  
1. These are the imports needed. os for file/folder manipulation, time to use sleep for the progress bar, threading for the reasons explained above, pydub for playing the content, tqdm for the bar and [click](https://click.palletsprojects.com/en/7.x/), for prettiness sake.
```python
""" Module to choose and reproduce music kept in the computer """
import os
from time import sleep
import threading
from pydub import AudioSegment
from pydub.playback import play
from tqdm import tqdm
import click
```
2. Define the function,
```python
def player():
    """ The program should present the content of the 'music' folder, create a prompt for the user to choose from, and reproduce the files
    with a timer."""
```
3. present the music files to the user,
```python
    # https://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
    for i in os.scandir("/home/mic/music"):
        if i.is_file():
            print(i.path)
        elif i.is_dir():
            print(i.path)
```
4. I love isometric ASCII lettering,
```python
    print(r"""
      ___           ___           ___                       ___                    ___                       ___                       ___           ___
     /\  \         /\  \         /\__\                     /\__\                  /\  \                     /\  \                     /\__\         /\  \
    |::\  \        \:\  \       /:/ _/_       ___         /:/  /                 /::\  \                   /::\  \         ___       /:/ _/_       /::\  \
    |:|:\  \        \:\  \     /:/ /\  \     /\__\       /:/  /                 /:/\:\__\                 /:/\:\  \       /|  |     /:/ /\__\     /:/\:\__\
  __|:|\:\  \   ___  \:\  \   /:/ /::\  \   /:/__/      /:/  /  ___            /:/ /:/  /  ___     ___   /:/ /::\  \     |:|  |    /:/ /:/ _/_   /:/ /:/  /
 /::::|_\:\__\ /\  \  \:\__\ /:/_/:/\:\__\ /::\  \     /:/__/  /\__\          /:/_/:/  /  /\  \   /\__\ /:/_/:/\:\__\    |:|  |   /:/_/:/ /\__\ /:/_/:/__/___
 \:\~~\  \/__/ \:\  \ /:/  / \:\/:/ /:/  / \/\:\  \__  \:\  \ /:/  /          \:\/:/  /   \:\  \ /:/  / \:\/:/  \/__/  __|:|__|   \:\/:/ /:/  / \:\/:::::/  /
  \:\  \        \:\  /:/  /   \::/ /:/  /   ~~\:\/\__\  \:\  /:/  /            \::/__/     \:\  /:/  /   \::/__/      /::::\  \    \::/_/:/  /   \::/~~/~~~~
   \:\  \        \:\/:/  /     \/_/:/  /       \::/  /   \:\/:/  /              \:\  \      \:\/:/  /     \:\  \      ~~~~\:\  \    \:\/:/  /     \:\~~\
    \:\__\        \::/  /        /:/  /        /:/  /     \::/  /                \:\__\      \::/  /       \:\__\          \:\__\    \::/  /       \:\__\
     \/__/         \/__/         \/__/         \/__/       \/__/                  \/__/       \/__/         \/__/           \/__/     \/__/         \/__/
""")
    print('\n')
```
5. ask the user to choose an album. This is done by copy/pasting one of the results in the prompt,
```python
    escolha = str(input(click.style(' » What do you want to hear? :~ ', fg='green', bold=True)))
    print('\n')
```
6. create a empty list to house the album chosen by the user.
```python
    album = []
```
7. append the individual song files to the list,
```python
    for i in os.scandir(escolha):
        if i.is_file():
            album.append(i.path)
```
8. for each song in the album list,
```python
    for song in album:
```
9. get only the music title,
```python
        musicas = os.path.basename(os.path.normpath(song))
```
10. and print it,
```python
        print(click.style(musicas, fg='bright_white', bold=True))
```
11. Create a variable to house a AudioSegment object,
```python
        sound = AudioSegment.from_file(song)
```
12. start the threading process, point it to the play function of the sound variable and start threading,
```python
        threading.get_ident()
        t = threading.Thread(target=play, args=(sound,))
        t.start()
```
13. create a variable with the song duration in seconds,
```python
        dur = sound.duration_seconds
```
14. and create the progress bar object, with percentage of time spent, elapsed and remaining, sleep for 1 second and continue
```python
        for sec in tqdm(range(int(dur)), bar_format='{desc}: {percentage:.0f}%|{bar} | {elapsed}<{remaining}'):
            sleep(1)
        print('\n')
```

Here is the full code:
```python
""" Module to choose and reproduce music kept in the computer """
import os
from time import sleep
import threading
from pydub import AudioSegment
from pydub.playback import play
from tqdm import tqdm
import click


def player():
    """ The program should present the content of the 'music' folder, create a prompt for the user to choose from, and reproduce the files
    with a timer."""
    # https://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
    for i in os.scandir("/home/mic/music"):
        if i.is_file():
            print(i.path)
        elif i.is_dir():
            print(i.path)
    print(r"""
      ___           ___           ___                       ___                    ___                       ___                       ___           ___
     /\  \         /\  \         /\__\                     /\__\                  /\  \                     /\  \                     /\__\         /\  \
    |::\  \        \:\  \       /:/ _/_       ___         /:/  /                 /::\  \                   /::\  \         ___       /:/ _/_       /::\  \
    |:|:\  \        \:\  \     /:/ /\  \     /\__\       /:/  /                 /:/\:\__\                 /:/\:\  \       /|  |     /:/ /\__\     /:/\:\__\
  __|:|\:\  \   ___  \:\  \   /:/ /::\  \   /:/__/      /:/  /  ___            /:/ /:/  /  ___     ___   /:/ /::\  \     |:|  |    /:/ /:/ _/_   /:/ /:/  /
 /::::|_\:\__\ /\  \  \:\__\ /:/_/:/\:\__\ /::\  \     /:/__/  /\__\          /:/_/:/  /  /\  \   /\__\ /:/_/:/\:\__\    |:|  |   /:/_/:/ /\__\ /:/_/:/__/___
 \:\~~\  \/__/ \:\  \ /:/  / \:\/:/ /:/  / \/\:\  \__  \:\  \ /:/  /          \:\/:/  /   \:\  \ /:/  / \:\/:/  \/__/  __|:|__|   \:\/:/ /:/  / \:\/:::::/  /
  \:\  \        \:\  /:/  /   \::/ /:/  /   ~~\:\/\__\  \:\  /:/  /            \::/__/     \:\  /:/  /   \::/__/      /::::\  \    \::/_/:/  /   \::/~~/~~~~
   \:\  \        \:\/:/  /     \/_/:/  /       \::/  /   \:\/:/  /              \:\  \      \:\/:/  /     \:\  \      ~~~~\:\  \    \:\/:/  /     \:\~~\
    \:\__\        \::/  /        /:/  /        /:/  /     \::/  /                \:\__\      \::/  /       \:\__\          \:\__\    \::/  /       \:\__\
     \/__/         \/__/         \/__/         \/__/       \/__/                  \/__/       \/__/         \/__/           \/__/     \/__/         \/__/
""")
    print('\n')
    escolha = str(input(click.style(' » What do you want to hear? :~ ', fg='green', bold=True)))
    print('\n')
    album = []
    for i in os.scandir(escolha):
        if i.is_file():
            album.append(i.path)
    for song in album:
        musicas = os.path.basename(os.path.normpath(song))
        print(click.style(musicas, fg='bright_white', bold=True))
        sound = AudioSegment.from_file(song)
        threading.get_ident()
        t = threading.Thread(target=play, args=(sound,))
        t.start()
        dur = sound.duration_seconds
        for sec in tqdm(range(int(dur)), bar_format='{desc}: {percentage:.0f}%|{bar} | {elapsed}<{remaining}'):
            sleep(1)
        print('\n')


if __name__ == '__main__':
    player()
```
