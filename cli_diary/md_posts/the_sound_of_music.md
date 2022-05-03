---
title: "The Sound of Music"
mainfont: Iosevka
---

Sometimes, a lot of times, I discover something new and cool about Python and promptly forget it.  
I try to create notes to remind me of what I've done, I keep bookmarks on the pages that I find, but this isn't enough. If I don't use it regularly, I'll forget
that I have notes or bookmarks and start projects from scratch, as if for the first time.   
Just today I was checking the files on a music player that I wrote, badly, and found that I had used the [psutil](https://psutil.readthedocs.io) library to create some of the commands.  
Truth be told, this was so completely erased from my mind, that I had to check what psutil was about, as well as see what the hell the [subprocess](https://docs.python.org/3/library/subprocess.html) commands did exactly.  
Here is my 'resume play' command, as way of an example:  
1. The library I'm using on the player is [pydub](https://github.com/jiaaro/pydub/), a very simple audio repository that, to my eyes, had the distinct advantage of having code I could, more or less, understand. It seems to me, and I've seen it written many times, that using code that you can grok, even if less feature full, is always preferable to inserting code in your projects that, for all practical purposes, is a black box.  
2. I also had to install something to run the MP3 files I have, because, as they say in their GitHub page,  
> You can open and save WAV files with pure python. For opening and saving non-wav files – like mp3 – you'll need ffmpeg or libav.
I chose to go with ffmpeg, as I already looked, briefly, to its documentation, when choosing what player to use.  
This left me with the realization that if I wanted to create commands to alter the play function, I would have to create ways to manipulate running processes. That's where subprocess comes in.  
I had found [here](https://askubuntu.com/questions/180336/how-to-find-the-process-id-pid-of-a-running-terminal-program) a way to identify processes numbers from the application name, but it was a bash command; so I thought of subprocess.  
It only now occurs to me, now, that, if I was using psutil, I had no need for subprocess, as the former had the capacity to return a pid from a app name. But, at  the time, subprocess was a more known quantity than psutil and, to be completely frank, the thought of using it to find the pid didn't even crossed my mind.  
I think I'll later, rewrite these modules to use only psutil. If for nothing else, just to use fewer libraries.  
This is what I've ended up doing, finding the pid with with subprocess and terminating it with psutil.  
3. I imported the libraries,  
```python
  import psutil
  import subprocess
```
4. created a function,  
```python
  def resume():
      """Use subprocess to, first find out the pid, and then stop it with psutil"""
```
5. created a variable 'processes' that houses the subprocess command.  
The bash script uses the [ps](https://man7.org/linux/man-pages/man1/ps.1.html) command, adding the `ax` options, that outputs the results in BSD syntax. This was done because I copied code and didn't thought about it. Which is a very dumb thing to do. I will change it ro read `ps -e`, when I refactor this module.
The result is piped to grep, so as to find the ffplay, ffmpeg player, occurrences.  
```python
  processes = subprocess.Popen(["ps ax | grep 'ffplay'"],
```
6. declared the command as a shell command,
```python
  shell=True,
```
7. piped the results to standard output and kept it.
```python
  stdout=subprocess.PIPE,
```
8. and sent any errors to be shown in the screen.
```python
  stderr=subprocess.STDOUT)
```
9. Now I make sure that is possible to see the outputs of the command,
```python
  stderr=subprocess.STDOUT
```
10. I collect the pid from the output that has this format `967 tty1 S 0:02 sh /home/mic/.xinitrc`, being the first number, the pid number,
```python
  pid = stdout.split()[0]
```
11. as Popen is a byte object, I translate it to a string,
```python
  pid_str = pid.decode('utf-8')
```
12. create a variable to house a psutil command that turns the string to an integer,
```python
  p = psutil.Process(int(pid_str))
```
13. And, as this is the resume command, it resumes a process that was previously stopped.
```python
  p.resume()
```
After making this reconstruction exercise, it's clear to me now that there's a lot of things that can be bettered here. And that's what I'm going to do.
I leave you with the complete code, with all my comments.  
```python
  """ Module to stop the ffplay, ffmpeg's player, by stopping its process """
  import psutil
  import subprocess
  
  
  def resume():
      """Use subprocess to, first find out the pid, and then stop it with psutil"""
      # 3)
      processes = subprocess.Popen(["ps ax | grep 'ffplay'"],
                                   shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
      # 'ps ax | grep 'python3 playsound_player.py' looks for the pid of the command.
      # https://askubuntu.com/questions/180336/how-to-find-the-process-id-pid-of-a-running-terminal-program
      # 'stdout=subprocess.PIPE' pipes the standard output and keeps it.
      # 'stderr=subprocess.STDOUT', sends the errors to the screen
      # 1)
  
      stdout, stderr = processes.communicate()   # This allows us to see the outputs of the command
      pid = stdout.split()[0]                    # It collects just the pid.
      pid_str = pid.decode('utf-8')              # Decodes the Popen byte object into a string.
  
      p = psutil.Process(int(pid_str))           # psutil is a library the deals with process management
      p.resume()                                 # 2)
  
  
  resume()
  
  
  """
  NOTES
  1) - https://cmdlinetips.com/2014/03/how-to-run-a-shell-command-from-python-and-get-the-output/
  2) - https://github.com/giampaolo/psutil
  3) - http://queirozf.com/entries/python-3-subprocess-examples
  https://docs.python.org/3/library/subprocess.html
  """
```
