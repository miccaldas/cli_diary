---
title: urwid_project
mainfont: Iosevka
---

For no reason in particular, I've been playing with a version of the bookmarks app done in [Urwid](http://urwid.org).  
One of the first things that strikes you while using this library is that it is old. The examples have the fit and finish of a 80's Visual Basic cassette and the library has the clunky, organic charm of a project that grew naturally for many years.    
Urwid has tons of charm.  
And, on top of the charm, there's the fact that I still can't grok how [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) actually works.  
So, for now, Urwid is my go-to.  
One thing that doesn't work in urwid is, making several questions in the same function.  
Because of this, to add a bookmark entry in Urwid, I created six files:
* One to insert the title,
* another for the comment,
* another for the link,
* and three more for the tag entries. k1, k2, k3.

The same happened when I adapted the update function to Urwid. I had to create a file for each of the data points, that are needed to make an update. One for the column, another for the id and another for the update.  
Only now, after it's done, comes to me that I could have pooled all the add and update functions in two modules. I just had to create different functions for each one, and I would have now much less files.  
But, at the same time, I like the cleanliness of having them distributed by files. It's easier to isolate and debug.  
Besides Urwid I also imported [Loguru](https://loguru.readthedocs.io/en/stable/index.html), a simple to setup and use logging app; that I intend to install in all my future projects.  
sys is needed for Loguru.  
Here is the example of one such file, 'add_title.py':  

```python
import sys
import urwid
from loguru import logger
```
Here I define the parameters for Loguru. It has nothing to do with our current subject.
```python
fmt = "{time} - {name} - {level} - {message}"
logger.add("spam.log", level="DEBUG", format=fmt)
logger.add(sys.stderr, level="ERROR", format=fmt)
```
First we create a function that defines the exit key as 'Q' or 'q'.
```python
def exit_on_q(key):
    if key in ("q", "Q"):
        raise urwid.ExitMainLoop()
```
Next we call the QuestionBox class and, inside it, create a function that defines that Urwid will record all keyboard key-presses as input; with the exception of of 'enter'.
```python
class QuestionBox(urwid.Filler):
    """We'll create a tui window in urwid to ask the question"""

    def keypress(self, size, key):
        if key != "enter":
            return super(QuestionBox, self).keypress(size, key)
        texto = u"%s.\n\nPRESS Q TO EXIT." % edit.edit_text
        self.original_widget = urwid.Text(texto, align="center")
```
We define a color palette for the window.
```python
palette = [
    ("banner", "white", "#ff6f69"),
    ("streak", "white", "light red"),
    ("bg", "white", "#ff6f69"),
]
```
We ask for the title name from the user.
```python
edit = urwid.Edit(("banner", u"WHAT IS THE TITTLE?\n"), align="center")
```
Create the fill and loop objects:
```python
fill = QuestionBox(edit)
loop = urwid.MainLoop(fill, palette, unhandled_input=exit_on_q)
```
Set the terminal color for 256.
```python
loop.screen.set_terminal_properties(colors=256)
```

An [AttrMap](https://tinyurl.com/ye9kwop6) decoration is created to wrap the text widget with display attribute 'streak'. AttrMap widgets allow you to map any display attribute to any other display attribute, but by default they will set the display attribute of everything that does not already have a display attribute. A second AttrMap widget is created to wrap the Filler widget with attribute 'bg'.  
```python
loop.widget = urwid.AttrMap(fill, "bg")
```
And, finally, we run the loop.
```python
loop.run()
```
Since I can't send the information immediately to the database, as all the data points required are dispersed by three files, I chose to store it in a file, yes, more files, so I could send it later. And by later I mean, after having all the information needed.  
```python
f = open("title.txt", "w")
f.write(edit.get_edit_text())
f.close()
```
The full document:
```python
"""Adding a new note. Title question"""
import sys
import urwid
from loguru import logger


fmt = "{time} - {name} - {level} - {message}"
logger.add("spam.log", level="DEBUG", format=fmt)
logger.add(sys.stderr, level="ERROR", format=fmt)


def exit_on_q(key):
    if key in ("q", "Q"):
        raise urwid.ExitMainLoop()


class QuestionBox(urwid.Filler):
    """We'll create a tui window in urwid to ask the question"""

    def keypress(self, size, key):
        if key != "enter":
            return super(QuestionBox, self).keypress(size, key)
        texto = u"%s.\n\nPRESS Q TO EXIT." % edit.edit_text
        self.original_widget = urwid.Text(texto, align="center")


palette = [
    ("banner", "white", "#ff6f69"),
    ("streak", "white", "light red"),
    ("bg", "white", "#ff6f69"),
]

edit = urwid.Edit(("banner", u"WHAT IS THE TITTLE?\n"), align="center")
fill = QuestionBox(edit)
loop = urwid.MainLoop(fill, palette, unhandled_input=exit_on_q)
loop.screen.set_terminal_properties(colors=256)
loop.widget = urwid.AttrMap(fill, "bg")
loop.run()

f = open("title.txt", "w")
f.write(edit.get_edit_text())
f.close()
```
-----------------------------------------------------------------------------------------

When I finally ended writing the app, and all the work was, apparently, done, I realized something that it could have been brought to my attention earlier. The Urwid documentation syntax, has a lot of content outside functions. This will be a big problem when importing all the files to the main file.  
Add to this that, because I slavishly/mindlessly copied what I had seen in the documentation, I didn't use any ``if __name__ == '__main__':`` code in any file. This was shaping up to be an import nightmare.  
I really didn't wanted to refactor all  my code, so as to put it inside functions. If for nothing else, because Urwid wouldn't probably work that way.  
The solution I came up with was, create a python script where I execute all files, in Subprocess, as if they were running in the shell, 'python <file_name.py>.
Let's see an example. First we define the options on this main.py file. The 'u' in the beginning of the string defines its content as unicode. This is a definition that is not needed [since the birth of python3](https://docs.python.org/3/howto/unicode.html), but this is how it's written in Urwid's documentation; and, because I only knew this after writing the app, it stays in the code until such time as I feel willing to refactor.   
```python
choices = u"Add, See, Search, Delete, Update, Exit".split()
```
We define a vertical menu with this options.
```python
def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, "click", item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))
```
Then we define the choice process.
```python
def item_chosen(button, choice):
    response = urwid.Text([u"You chose ", choice, u"\n"])
    done = urwid.Button(u"OK")
    urwid.connect_signal(done, "click", exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map="reversed")]))
    item_chosen.pick = str(choice[:-1])  # Result comes with trailing comma. This gets rid of it.
```
And the conditions for exiting the program.
```python
def exit_program(button):
    raise urwid.ExitMainLoop()
```
Here we define the visual look of the widget.
```python
main = urwid.Padding(menu(u"Pythons", choices), left=2, right=2)
top = urwid.Overlay(
    main,
    urwid.SolidFill(u"\N{MEDIUM SHADE}"),
    align="center",
    width=("relative", 60),
    valign="middle",
    height=("relative", 60),
    min_width=20,
    min_height=9,
)
urwid.MainLoop(top, palette=[("reversed", "standout", "")]).run()
```
And finally we arrive at the main function, where I use subprocess to start the files in python through the shell; thus circumventing the import problem.
```python
def main():
    if item_chosen.pick == "Add":
        subprocess.run("python add_title.py", shell=True)
        subprocess.run("python add_comment.py", shell=True)
        subprocess.run("python add_link.py", shell=True)
        subprocess.run("python add_k1.py", shell=True)
        subprocess.run("python add_k2.py", shell=True)
        subprocess.run("python add_k3.py", shell=True)
        subprocess.run("python connections.py", shell=True)
    if item_chosen.pick == "See":
        subprocess.run("python see.py", shell=True)
    if item_chosen.pick == "Search":
        subprocess.run("python  search.py", shell=True)
    if item_chosen.pick == "Delete":
        subprocess.run("python delete.py", shell=True)
    if item_chosen.pick == "Update":
        subprocess.run("python update_column.py", shell=True)
        subprocess.run("python update_id.py", shell=True)
        subprocess.run("python update_update.py", shell=True)
        subprocess.run("python updt_connections.py", shell=True)
    if item_chosen.pick == "Exit":
        sys.exit()
```
The full text:
```python


#!/usr/bin/python3.9
"""Main Module of the App. Where all the commands are accessed from"""
import sys
import subprocess
import urwid
from loguru import logger


fmt = "{time} - {name} - {level} - {message}"
logger.add("spam.log", level="DEBUG", format=fmt)
logger.add(sys.stderr, level="ERROR", format=fmt)


choices = u"Add, See, Search, Delete, Update, Exit".split()


def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, "click", item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def item_chosen(button, choice):
    response = urwid.Text([u"You chose ", choice, u"\n"])
    done = urwid.Button(u"Ok")
    urwid.connect_signal(done, "click", exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map="reversed")]))
    item_chosen.pick = str(choice[:-1])  # Result comes with trailing comma. This gets rid of it.


def exit_program(button):
    raise urwid.ExitMainLoop()


main = urwid.Padding(menu(u"Pythons", choices), left=2, right=2)
top = urwid.Overlay(
    main,
    urwid.SolidFill(u"\N{MEDIUM SHADE}"),
    align="center",
    width=("relative", 60),
    valign="middle",
    height=("relative", 60),
    min_width=20,
    min_height=9,
)
urwid.MainLoop(top, palette=[("reversed", "standout", "")]).run()


def main():
    if item_chosen.pick == "Add":
        subprocess.run("python add_title.py", shell=True)
        subprocess.run("python add_comment.py", shell=True)
        subprocess.run("python add_link.py", shell=True)
        subprocess.run("python add_k1.py", shell=True)
        subprocess.run("python add_k2.py", shell=True)
        subprocess.run("python add_k3.py", shell=True)
        subprocess.run("python connections.py", shell=True)
    if item_chosen.pick == "See":
        subprocess.run("python see.py", shell=True)
    if item_chosen.pick == "Search":
        subprocess.run("python  search.py", shell=True)
    if item_chosen.pick == "Delete":
        subprocess.run("python delete.py", shell=True)
    if item_chosen.pick == "Update":
        subprocess.run("python update_column.py", shell=True)
        subprocess.run("python update_id.py", shell=True)
        subprocess.run("python update_update.py", shell=True)
        subprocess.run("python updt_connections.py", shell=True)
    if item_chosen.pick == "Exit":
        sys.exit()


if __name__ == "__main__":
    main()
```
