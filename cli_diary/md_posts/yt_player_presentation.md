---
title: "Yt Player Presentation"
date: 06/05/2022
mainfont: Iosevka
---

I created an app that searches, downloads and plays audios taken from YouTube.  
I used the libraries [youtube-search-python](https://pypi.org/project/youtube-search-python/) to search results and [Pytube](https://github.com/pytube/pytube) to download the chosen search results.  
The app is divided in the following modules:  

<h3>search.py</h3>
In short, this function asks user for a query, prepares the query string to be a folder name, asks how many results does the user wants. By default it searches 30 results. From these results it takes the values of video id, builds a youtube url with it, and the title and duration values in the search result. Returns them.  

1. This puts underscores in lieu of spaces, so as to use it as folder names.  

```python
    fldr_name = query.replace(" ", "_")
```
<br>
<br>
2. Questionary text questions returns a string, even if you input a integral. We
   need to turn it to one so as to, later, when we compare this value with an
   enumerated list of search results, they match in type.  

```python
    number_of_searches = int(lmt)
```
<br>
<br>
3. Create an instance of 'youtube-search-python'. The class 'Search', searches
   for all types of content on YouTube.  

```python
    srch = Search(query, limit=number_of_searches)
```
<br>
<br>
4. Create a variable that houses all the search results.  

```python
    results = srch.result()
```
<br>
<br>
5. Now we will loop through a named dictionary that has as value a list of
   dictionaries. Its structure is something like this:

   ```python
     results = {'result': [{'id': <some_value>, 'title': <some_value>, ...}, {'id': <some_value>, 'title': <some_value>, ...}, {...}]}
   ```

   'Duration', in some cases doesn't exist in the results, like in the case of content from playlists, for instance. We put it inside a try/except block, so as not stop the program execution. To reach the values inside the list by their key, we use this syntax:

   ```python
     for i in range(len(results["result"])):
        ident = results["result"][i]["id"]
        url = f"https://www.youtube.com/watch?v={ident}"
        tit = results["result"][i]["title"]
        try:
            dur = results["result"][i]["duration"]
        except KeyError:
            pass
   ```
<br>
<br>
6. We gather the variables we took from the search results in to a tuple
   and put them in a list.  

   ```python
     tup = (url, tit, dur)
     tup_lst.append(tup)
   ```
<br>
<br>
7. The function returns a tuple with the folder name and the list of tuples with
   the search results data. This information will be needed in the 'download.py'
   module.  

   ```python
    return fldr_name, tup_lst
   ```
<br>
<br>
<br>
Full code:

```python
  """Searches Youtube for a query."""
  import isort
  import questionary
  import snoop
  from questionary import Style
  from snoop import pp
  from youtubesearchpython import Search


  def type_watch(source, value):
      return "type({})".format(source), type(value)


  snoop.install(watch_extras=[type_watch])


  # @snoop
  def search():
    """
    Asks user for a query, prepares the query string
    to be a folder name, asks how many results does
    the user wants. By default it searches 30 results.
    From these results it takes the values of video id,
    builds a youtube url with it, and the title and
    duration values in the search result. Returns them.
    """

    custom_style_search = Style(
        [
            ("qmark", "fg:#FF5F00 bold"),
            ("question", "fg:#A2B38B bold"),
            ("answer", "fg:#F1DDBF bold"),
            ("instruction", "fg:#E4E9BE bold"),
            ("text", "fg:#F1DDBF bold"),
        ]
    )

    query = questionary.text(
        "What is your query?",
        qmark="(**)",
        style=custom_style_search,
        instruction="Choose what you'll be searching for.",
    ).ask()

    lmt = questionary.text(
        "How many results do you want?",
        qmark="(**)",
        style=custom_style_search,
        default="30",
        instruction="Choose how many search results you'll get.",
    ).ask()

    fldr_name = query.replace(" ", "_")
    number_of_searches = int(lmt)
    srch = Search(query, limit=number_of_searches)
    tup_lst = []
    results = srch.result()
    for i in range(len(results["result"])):
        ident = results["result"][i]["id"]
        url = f"https://www.youtube.com/watch?v={ident}"
        tit = results["result"][i]["title"]
        try:
            dur = results["result"][i]["duration"]
        except KeyError:
            pass
        tup = (url, tit, dur)
        tup_lst.append(tup)

    return fldr_name, tup_lst


if __name__ == "__main__":
    search()
```
<br>
<br>
<br>
<h3>download.py</h3>
The 'download' module receives query and tuple with url, title and duration of each search result, asks the user to choose what results he wants to download by choosing the id of a enumerated search results list, checks for the tuple with the corresponding id, checks if there's already a folder in 'music' with the query's name, if yes, it downloads to it, if not, it creates a folder and downloads to it.  

1. We create an instance of the 'search' function:

```python
    tups = search()
```
<br>
<br>
2. Define a list of all subfolders inside the folder 'music', where all
   downloads go. 'os.walk' returns a tuple with `(dirs, files)`, if we take only
   the first element, we get a list of folders.  

   ```python
    music_folders = [i[0] for i in os.walk("music")]
   ```
<br>
<br>
3. We print an enumerated version of the list of data we collected for each
   search result. This is so we have a way to identify each entry easily.  
   It enumerates through `tups[1]` because `tups[0]` is the folder name
   variable.  

   ```python
    for tup in enumerate(tups[1]):
        print(color(f" (**) - {tup}", fore="#A2B38B"))
   ```
<br>
<br>
4. We ask the user what are the entries he wants to download. He inputs the
   corresponding enumerate id's.  
   As the output, in case of several id's being chosen, is a string with this
   format: 'id1 id2 ...', we need to separate them into a list.  

   ```python
    entry_ids = questionary.text(
        "What ids do you want to choose?",
        qmark="(**)",
        style=custom_style_download,
        instruction="Choose the numbers of the entries you like",
    ).ask()

    lst_id = entry_ids.split(" ")
    int_id = [int(i) for i in lst_id]
   ```
<br>
<br>
5. If there's no folder with the query's name, we create it.  

   ```python
    new_fldr = f"music/{tups[0]}"
    if new_fldr not in music_folders:
        os.mkdir(new_fldr)
   ```
<br>
<br>
6. We look for the search results that correspond to the chosen id's, and use
   pytube to, from the available streams, 'get_audio_only()', which chooses the
   best quality audio stream, and we download it to the folder defined in
   'output_path'.  

   ```python
    for id in int_id:
        for tup in enumerate(tups[1]):
            if id == tup[0]:
                YouTube(tup[1][0]).streams.get_audio_only().download(output_path=new_fldr)
   ```
<br>
<br>
<br>
Full code:  

```python
"""Downloads Youtube audios."""
  import os

  import isort
  import questionary
  import snoop
  from colr import color
  from pytube import YouTube
  from questionary import Style
  from snoop import pp

  from search import search


  def type_watch(source, value):
    return "type({})".format(source), type(value)


  snoop.install(watch_extras=[type_watch])

  custom_style_download = Style(
    [
        ("qmark", "fg:#FF5F00 bold"),
        ("question", "fg:#A2B38B bold"),
        ("answer", "fg:#F1DDBF bold"),
        ("pointer", "fg:#F8CB2E bold"),
        ("highlighted", "fg:#FEFBE7 bold"),
        ("selected", "fg:#DAE5D0 bold"),
        ("instruction", "fg:#E4E9BE bold"),
        ("text", "fg:#F1DDBF bold"),
    ]
)


  # @snoop
  def download():
    """
    Receives query and tuple with url, title and duration
    of each search result, asks the user to choose what
    results he wants to download by choosing the id of a
    enumerated search results list, checks for the tuple
    with the corresponding id, checks if there's already
    a folder in 'music' with the query's name, if yes, it
    downloads to it, if not, it creates a folder and
    downloads to it.
    """

    tups = search()
    music_folders = [i[0] for i in os.walk("music")]

    print("\n")
    for tup in enumerate(tups[1]):
        print(color(f" (**) - {tup}", fore="#A2B38B"))
    print("\n")

    entry_ids = questionary.text(
        "What ids do you want to choose?",
        qmark="(**)",
        style=custom_style_download,
        instruction="Choose the numbers of the entries you like",
    ).ask()

    lst_id = entry_ids.split(" ")
    int_id = [int(i) for i in lst_id]

    new_fldr = f"music/{tups[0]}"
    if new_fldr not in music_folders:
        os.mkdir(new_fldr)

    for id in int_id:
        for tup in enumerate(tups[1]):
            if id == tup[0]:
                YouTube(tup[1][0]).streams.get_audio_only().download(output_path=new_fldr)


  if __name__ == "__main__":
      download()
```
<br>
<br>
<br>
<h3>player.py</h3>
The player module gets paths to all files and folders in 'music', puts them in a enumerated list for easy identification, asks the user the ids of the paths.  
If path is a directory, it'll play the full contents of the directory, if path is files, it'll play files.  

1. First we create a list with all subfolders and files in the 'music' folder
   and print it, questioning the user what entries he would like to play:  

   ```python
    music_lst = []
    for root, dirs, files in os.walk("music"):
        for d in dirs:
            folder = os.path.relpath(os.path.join(root, d), "music")
            music_lst.append(folder)
        for f in files:
            song = os.path.relpath(os.path.join(root, f), "music")
            music_lst.append(song)
    enum_lst = list(enumerate(music_lst))
    for music in enum_lst:
        print(color(music, fore="#A2B38B"))
    print("\n")
    music_id = questionary.text("What are the ids of the music you want to hear?", qmark="(**)", style=custom_style_player).ask()
   ```
<br>
<br>
2. We turn the answer received into a list and convert its items to integrals.  

   ```python
    id_lst = music_id.split(" ")
    int_lst = [int(i) for i in id_lst]
   ```
<br>
<br>
3. We compare the id's the user chosen now, with the id's of the search results.
   If they match we check to see if it's a directory or a file, and open the
   [mpv](https://mpv.io) player with correspondingly adequate commands.  

   ```python
    for i in int_lst:
        for e in enum_lst:
            if i == e[0]:
                if os.path.isdir(e[1]):
                    cmd1 = "mpv --no-audio-display --play-dir '{e[1]}'"
                    subprocess.run(cmd1, cwd="music", shell=True)
                else:
                    cmd2 = f"mpv --no-audio-display '{e[1]}'"
                    subprocess.run(cmd2, cwd="music", shell=True)
   ```
<br>
<br>
<br>
Full code:  

```python
"""Shows content of the 'music' folder and plays the users choice."""
import os
import subprocess

import isort
import questionary
import snoop
from colr import color
from questionary import Style
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def player():
    """
    Gets paths to all files and folders in 'music',
    puts them in a enumerated list for easy
    identification, asks the user the ids of the paths.
    If path is a directory, it'll play the full contents
    of the directory, if path is files, it'll play files.
    """

    custom_style_player = Style(
        [
            ("qmark", "fg:#FF5F00 bold"),
            ("question", "fg:#A2B38B bold"),
            ("answer", "fg:#F1DDBF bold"),
            ("instruction", "fg:#E4E9BE bold"),
            ("text", "fg:#F1DDBF bold"),
        ]
    )

    music_lst = []
    for root, dirs, files in os.walk("music"):
        for d in dirs:
            folder = os.path.relpath(os.path.join(root, d), "music")
            music_lst.append(folder)
        for f in files:
            song = os.path.relpath(os.path.join(root, f), "music")
            music_lst.append(song)
    enum_lst = list(enumerate(music_lst))
    for music in enum_lst:
        print(color(music, fore="#A2B38B"))
    print("\n")
    music_id = questionary.text("What are the ids of the music you want to hear?", qmark="(**)", style=custom_style_player).ask()
    id_lst = music_id.split(" ")
    int_lst = [int(i) for i in id_lst]
    for i in int_lst:
        for e in enum_lst:
            if i == e[0]:
                if os.path.isdir(e[1]):
                    cmd1 = "mpv --no-audio-display --play-dir '{e[1]}'"
                    subprocess.run(cmd1, cwd="music", shell=True)
                else:
                    cmd2 = f"mpv --no-audio-display '{e[1]}'"
                    subprocess.run(cmd2, cwd="music", shell=True)


if __name__ == "__main__":
    player()
```








