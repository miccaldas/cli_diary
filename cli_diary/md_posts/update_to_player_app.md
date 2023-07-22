---
title: Update to Player App
date: 21-07-2023 22:03
mainfont: Iosevka
fontsize: 15pt
---


I did some housekeeping to the *player* app. I neglected it for a while but,
needing a project, found it again.  
The major alterations were:  
   <h3>Commands.</h3>  
   The old ones were rickety and unstable, this ones, although as
   simple as they could get, are much more robust. I took notice that the
   [Blessed](https://blessed.readthedocs.io/en/latest/), the cli framework, has
   support for keyboard commands. But that is not how I got to this idea. What
   woke me up to the need for audio keyboard commands, was the fact that my
   columns stopped working and, with that, i had no easy way to, say, control
   the volume. As I use [Arch](https://archlinux.org), my audio setup is made of
   [ALSA](https://wiki.archlinux.org/title/Advanced_Linux_Sound_Architecture)
   and [PulseAudio](https://wiki.archlinux.org/title/PulseAudio). The first one
   has direct connection to the kernel and is developed by Linux. The latter is
   a sound server that works as middle layer between ALSA and client
   applications.  
   Both have rudimentary tools to manage sound streaming and, I'm very fond of
   not installing anything new if the old stuff does the job, I thought that was
   exactly what I needed. I ended up using ALSA's *alsamixer* tool to manage
   audio. The simplicity and depth of working with something at such a basic
   level, gave a feeling of confidence. I got the commands and created very
   simple shell scripts with them. Like this:  
  
   **Lowering Volume:**  
  
```console
    amixer set Master 10%- > /dev/null 2>&1  
```

   **Raising Volume:**  
  
```console
    amixer set Master 10%+ > /dev/null 2>&1
```
  
   **Mute Volume:**  

```console
    amixer set Master toggle > /dev/null 2>&1
```

   With the scripts built, it was just the case of binding them to a keyboard
   sequence. Later I created a script to stop the music player. It looks for a
   process originated by *player.py* in the *player* folder,and kills it:  
  
```console
    cd /home/mic/python/player/player/
    sudo kill -9 `pgrep -f player.py` > /dev/null 2>&1
```
  
   As my shell is [Zsh](https://zsh.sourceforge.io), I used its tool *zsh-edit*, to create the keybinds. I created these:  

   **Raising Volume - Keybind 'F6'**  
  
```console
    bind '^[[17~' ~/scripts/raisevolume.sh
```
  
   **Lowering Volume - Keybind 'F7'**  
  
```console
    bind '^[[18~' ~/scripts/lowervolumne.sh
```
  
   **Mute Sound - Keybind 'F8'**  
  
```console
    bind '^[[19~' ~/scripts/mutevolume.sh
```
  
   **Stop Player - Keybind 'Ctrl-Alt-p'**  

```shell
    bind '^[^P' ~/scripts/player_pid.sh
```
  
   To discover what codes are used by what keys, I used the very useful and
   simple [showkey](https://man7.org/linux/man-pages/man1/showkey.1.html)
   command. People will suggest other things, like Xev and what have you, but
   they tend to open unnecessary windows and superfluous information. Stick to
   showkey and you won't be led astray.  
  
   <h3>Search.</h3>  
   In the old version, to get to the music you wanted, it would get complete
   paths to each album, print them, and the user would need to copy/paste them.
   Here we tried something more friendly with a *choose.py* module.  
   We're using Blessed to prettify the output and also because it has simple
   ways of interacting with keybinds.  
   The idea is pretty simple, you're first directed to upper folder where the
   music collection is. There you choose a musician. This is glued to the rest
   of the path, now with the path for the chosen artist, and fed again to the
   *choose* module, that'll print the content of said folder; consisting mainly
   of several albums by an artist. Here the user chooses the album. And with
   that we have a complete path to a chosen album, to feed the music player.  
   The module is heavily commentated and speaks for itself. Here it is:

```python
    """
    Module to show the contents of the music folder, and collect user's choice.
    """
    import os
    import pickle

    import snoop

    from blessed import Terminal
    from snoop import pp


    def type_watch(source, value):
        return f"type({source})", type(value)


    snoop.install(out="logs", overwrite=True, watch_extras=[type_watch])


    @snoop
    def choose(content):
        """
        Presents the content of a folder. Returns an entry id.
        """
        content_list = os.listdir(content)
        # Integer with the length of the longest album name.
        longest = len(max(content_list))
        choicelst = []

        if content.endswith("music"):
            title = "CHOOSE AN ARTIST"
        else:
            title = "CHOOSE AN ALBUM"

        heights = []

        term = Terminal()
        # To center the album entries, we divide the screen width/height by two, and
        # from that number, subtract the value of 'longest' entry, for width, ang entries
        # length, for height.
        # wdth = int((term.width - longest) / 2)
        wdth = int(term.width / 4)
        # The initial height is found by first finding the number of lines of the text will
        # use. That means, the length of the list of albums, two lines for the title and its
        # separator and two lines for the exit message and its separator. We subtract this
        # from the height of the screen, if we didn't, the text would like it started too
        # low in the screen. Finally we divide the result by two.
        ht = int((term.height - (len(content_list) + 4)) / 2)
        # Calculates the title's width, it uses the block of text initial width, looks for
        # the longest line there, divides it by two and adds the halved number to the
        # initial width.
        twdth = wdth + int(longest / 2)
        # In order to define the height of each entry, we use 'enumerate' to create a
        # new list. The first element is an integer version of id, so we can use it defining
        # entry height and choosing what to play. The string version of the id serves as an
        # identifer for the user.
        albums = [[f, str(f) + " - " + "".join(i)] for f, i in enumerate(content_list)]

        # 'fullscreen' permits to restore the terminal screen to exactly how it was before
        # entering the 'player' app. Without it, the content of the app, although not
        # usable, would still be visible after exit. 'cbreak' registers individual keyboard
        # clicks. While inside this context manager, it'll log all keypresses.
        with term.fullscreen(), term.cbreak():
            # Clears, prepares, defines background/foreground colors, for the screen.
            print(term.move + term.black_on_peachpuff + term.bold + term.clear, end="")
            # The title height is the text block initial height minus one for the title and
            # one more for the seprator
            print(term.move_xy(twdth, (ht - 2)) + title)
            # To ensure that the album entries stack one after the other verticallly, we use
            # the 'idx' value, that starts at 0, and add it to the initial height of the
            # entries. We register these heights in a list called "heights".
            for album in albums:
                hght = ht + album[0]
                heights.append(hght)
                print(term.move_xy(wdth, hght) + "\n".join(term.wrap(album[1])))
            # To define the height of the exit information line, as below the the text block
            # plus a sperator line and the line proper; we get the last value in the
            # 'heights' list, corresponding to the height of the last entry, and add two.
            exitht = heights[-1] + 2
            print(term.move_xy(wdth, exitht) + "Press 'e' to exit after choosing. Press 'q' to exit this screen.")

            # Here to assure we can access 'inpt' value outside the loop.
            inpt = ""
            # While there's no exit call...
            while inpt.lower() != "q":
                # the variable will collect clicked keyboard keys names.
                inpt = term.inkey()
                # If we used the 'q' key to exit this loop, besides the key intended to press
                # it would add 'q' from the exit command. To avoid this, we create a loop
                # that runs while no one presses 'e', creating a exit command to the loop
                # alone but, as there is no more code ahed except a 'return' statement, it
                # in effect closes the program.
                if inpt != "e":
                    # We collect keypresses in a list...
                    choicelst.append(str(inpt))
                    # if there's more than one, we add append it to the previous one. This
                    # way we're able to collect two digit numbers.
                    chcstr = "".join(choicelst)
                    # To compare input result with the idx from the enumerated list.
                    # chc = int(chcstr)
                    if chcstr:
                        choice = [i for f, i in enumerate(content_list) if f == int(chcstr)]
                    with open("choice.bin", "wb") as f:
                        pickle.dump(choice, f)
                else:
                    break
```
  
   <h3>Music Player.</h3>  
   Here I purposefully went for the simpler available option. Even risking too
   simple.  
   [Playsound](https://pypi.org/project/playsound/) has only one command, which
   is to play a file. This command has one boolean argument, to use it on
   blocking mode or not. Has using non-blocking mode doesn't work, that's even
   one less thing to worry about. The other audio libraries are oriented for a
   type of in-depth use that's not my use case. Add to that an irritating habit
   of spewing unneeded output whilst playing a file, and I was looking for
   something much more clean and direct.  
   The only thing I miss that I could have with other players, is the ability to
   fast-forward and rewind. But not enough to get used to a constant barrage of
   information diarrhea.  
   Marvel at the spartan beauty of the player's function:
  
```python
    @snoop
    def player():
        """
        'Playsound' is the simplest player I
        know. It has only one argument, 'block'
        which is boolean that determines if the
        Playsound's execution is blocking or not.
        When I tried it as not blocking it
        wouldn't work.
        """
        with open("song.bin", "rb") as f:
            song = pickle.load(f)
        playsound(song)
```
  
  
   <h3>Ticker.</h3>  
   What I wanted, really, was a progress bar. Something that would tell me how
   long I still have to wait for a music to stop, be a harmless source of visual
   interest and nothing more.  
   I used [Tqdm](https://github.com/tqdm/tqdm), that I had used before, after
   trying a lot of other alternatives, and will use again as it seems the better
   solution for cli progress bars.  
   The way I used progress bars before, and wanted to still do, was to make them
   loop through the range of the music's duration. But now the player didn't had
   that information to divulge. What to do?  
   I started thinking about metadata on how to extract it and, finally, I
   discovered that a library I had installed, [ffmpeg-python](https://github.com/kkroening/ffmpeg-python), had exactly what I wanted.  
   *ffmpeg-probe* gets all metadata in a video file. As I download everything
   from Youtube, although I download only the audio, they're still mp4 files.
   The information is in one dictionary inside a list called *streams*, and you
   fetch it as in any other dictionary inside a list. Below see, first, the
   function that fetches the metadata and, after, the code that launches the
   player and the progress bar. It's multi-threaded so the ticker runs at the
   same time as the player:
  
```python
    def duration():
        """
        We use 'ffmpeg' to get metadata about the
        duration of musics. If there's nothing in
        'duration', we'll assume the song is about
        three minutes long. This information is
        used by Tqdm.
        """
        with open("song.bin", "rb") as g:
            length = pickle.load(g)

        # The metadata is kept in a list called 'streams', that
        # houses a dictionary with the information. To search it
        # know that there is only the dictionary below the list,
        # so it's just a case of ['stream'][0][<metada_you_want>]
        duration = ffmpeg.probe(length)["streams"][0]["duration"]
        if duration:
            return duration
        else:
            duration = 224
            return duration
```

```python
    def ticker():
        """
        The program should present the content of the 'music' folder,
        create a prompt for the user to choose from, and reproduce the files
        with a timer.

        'F6' - Lowers the volume,
        'F7' - Raises it,
        'F8' - Mutes it.
        'Ctrl-Alt-p' - Stops the player.
        """
        dur = duration()
        drt = float(dur)
        drtn = int(drt)

        console = Console()
        console.print(
            """[bold #E9B384]
      ############################
      ##    MUSIC PLAYER        ##
      ############################
      ##     Louder - 'F7'      ##
      ##     Lower  - 'F6'      ##
      ##     Mute   - 'F8'      ##
      ##  Stop   - 'Ctrl-Alt-p' ##
      ############################
      [/]
                """
        )
        for i in tqdm(
            range(drtn),
            position=0,
            ncols=70,
            colour="yellow",
            bar_format="{percentage:3.0f}%|{bar}| {remaining}]",
        ):
            sleep(1)


    if __name__ == "__main__":
        t1 = threading.Thread(target=ticker)
        t2 = threading.Thread(target=player)
        t1.start()
        t2.start()
```
  
---
<h3>UPDATE</h3>  
Just a few hours have passed but a lot as changed since I last wrote here. I,
finally tried [FZF](https://github.com/junegunn/fzf), and I was blown away with
the possibilities of using it in my projects. In this case, it facilitates
immensely the sorting and finding of posts, since neither *id's* nor timestamps
seem to appear in order, when gotten from the database. I've tweaked 'fzf' so it
opens a file when pressing *F1*, so it's a optimal substitution for the modules
I had for viewing HTML and Markdown files. It's very simple to use too. See
below the code for the new *search* module:
  
```python
"""
    Searches Markdown and HTML collections, with the help of 'fzf'.
    """
    import os
    import subprocess

    import questionary
    import snoop
    from questionary import Separator, Style
    from snoop import pp


    def type_watch(source, value):
        return f"type({source})", type(value)


    snoop.install(watch_extras=[type_watch])


    @snoop
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
```
