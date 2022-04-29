---
title: Micro Diary
mainfont: Iosevka
---

I had this idea that it would be nice to have a space where I could keep, as you keep code snippets, idea snippets.  
Small observations, asides to myself, all the small minutiae that ends up having more heft that we anticipate.  
My idea is to create a cli environment that is inviting to write and read, and also to put it online to be, also, accessed mainly by terminal.  
At the moment I have the writing part done, same procedure as always, write to database, access it from there, and have a facsimile of of navigation through the content.  
I call it a facsimile only because I have no shame, it's not even that. At the moment is a no-simile. But the truth is I can scroll through the entries doing ctrl-q, for reasons that'll be clearer in a moment. So, I am happy for now.  
I wanted something very simple, just a short text and a date. Nothing more.  
The problem is the concept of page in a terminal.  
Not that it has not been done. It has, for ages. Just not by me or with tools I can understand.  
One of my greatest, and saddest failures, was my inability to understand the [curses](https://docs.python.org/3/howto/curses.html) library.  
I could never get my head around it, no matter how many tutorials I read.  
But, buttressed in the knowledge that that was then, and this is now, a present where I'm more python worldly, we hope, I tried again.  
Strangely, to some success.  
Not with curses mind you, that is still a dark continent for me; but with [urwid](http://urwid.org), a library as old as time itself that, on this occasion, shared a small part of its secrets with me. Just as with curses, I already knew urwid. I spent many unhappy hours trying to decipher it's arcane code.  
Now that I know a bit more, I still find it very difficult to follow.  
It's very class based, and if that is not your comfort zone, as it isn't mine, you'll have a bad time.  
But thankfully I have recently dabbled a bit in classes, and the subject is fresher in my head than usual. So I understood some of the stuff that was there.  
This is what I did.
  
I went to the tutorial in their site and looked for the simplest example I could steal. I found one that was adequately pedestrian and created this module to write a post.  
First there is a function to create a keybinding to exit the file. It links 'q' or 'Q' to a 'ExitMainLoop' urwid function, that takes you out of the main loop. The main loop is where most of the urwid code is contained. Even if you exit the main loop, the program will execute whatever may be after its completion.
```python
def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
```
  
And now the 'voodoo code' begins. I will tentatively try to explain what is in here; much more as an exercise to clarify my thoughts than any attempt at explaining what is there. I just hope it's enough for future me.  
A class is created to house our app, or widget, in urwid parlance. This one inherits from [Filler](http://urwid.org/reference/widget.html?highlight=filler#urwid.Filler), a class that describes a visual widget that occupies space above and below a given area.  
Here we'll use the urwid method of keypress, to shape it to our needs. I think that is more or less the philosophy of this library; get the code and shape it.  
A function called [keypress](http://urwid.org/reference/widget.html?highlight=keypress#urwid.Filler.keypress) instantiates urwid.Filler.keypress(). We define that, if the key is not 'Enter', it should return the attributes of the parent class, write the text to explain that it's the 'q' character that gets you out of mischief and align it by the center.  
If this explanation feels a bit 'hand-wavy', that's because it is.
```python
class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        texto = u"%s.\n\nPress Q to exit." % edit.edit_text
        self.original_widget = urwid.Text(texto, align='center')
```
  
Next is defined a colour palette for the display attributes that we're using. These have a foreground and background values. I copied this three elements from the example, but it could have any other configuration.  
```python
palette = [
    ('banner', 'white', '#ff6f69'),
    ('streak', 'white', 'light red'),
    ('bg', 'white', '#ff6f69'),
]
```
Now it's defined a text editing field, [urwid.Edit](http://urwid.org/reference/widget.html?highlight=edit#urwid.Edit), which acts as a prompt of sorts. We give it a name, so we can color it as a display attribute, put on a unicode glyph for prettiness sake and tell it to align the text in the center.
```python
edit = urwid.Edit(('banner', u"🡺\n\n"), align='center')
```
  
We then create a variable that we'll embody our Question Box class with text editing field inserted.
```python
fill = QuestionBox(edit)
```
  
We define the main loop with classes, color settings and keybinding,
```python
loop = urwid.MainLoop(fill, palette, unhandled_input=exit_on_q)
```
  
We declare that'll will be using 256 colours.
```python
loop.screen.set_terminal_properties(colors=256)
```
  
The background is defined,
```python
loop.widget = urwid.AttrMap(fill, 'bg')
```
  
and the loop is ran.
```python
loop.run()
```
  
  
After closing the main loop, we write the user-written post to a file. The reason for this convoluted solution is that I couldn't get the value in any other way.  
I discovered, through trial and error, that you can't put two edit commands in the same loop. As an example, in this case I need to input, per post, not only its text, but also its tags. What would be convenient, would be a solution that looked like this:
```
edit = urwid.Edit('POST')
edit1 = urwid.Edit('TAGS')
blah, blah,
loop.definition
loop.run
```
But this is impossible. The only solution I found. And by that I mean, the only solution that avoided that I looked deeply and seriously to the structure of the library, and instead looked for a solution that gave a result in the least amount of time; was to create two modules, one for each edition moment, and connect it later in the 'main' file.  
This has proven harder that expected, as I imported the urwid modules, nothing more was read in the main file.  
Again, and true to form, I avoided trying to solve this problem by structuring the main file not as main.py but as main.sh. Thusly:
```
#!/usr/bin/env zsh

python3 post.py # Where the writing of the post was defined.
python3 tags.py # The same for the tags.
python3 connections.py # This is the next part.
```
  
We have now two text files, one with the text of the post, the other with the tags that accompany it.  
All that there is now to do is to upload it to the db.  
Which is done this way:  
```python
from mysql.connector import connect, Error


def connections():
    f = open('post.txt', 'r')
    f_tags = open('tags.txt', 'r')

    post_content = f.read()
    tags_content = f_tags.read()

    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="micro_diary")
        cur = conn.cursor()
        answers = [post_content, tags_content]
        query = """ INSERT INTO micro_diary (text, tags) VALUES (%s, %s) """
        cur.execute(query, answers)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()

    f.close()
    f_tags.close()


if __name__ == '__main__':
    connections()
```
  
To see the content, I created the following module that, by the fact that I showed a lot of others like it, I won't loose much time explaining it.
```python
from mysql.connector import connect, Error
import urwid


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


def see():

    palette = [
        ('banner', 'white', '#ff6f69'),
        ('streak', 'white', 'light red'),
        ('bg', 'white', '#ff6f69'),
    ]

    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="micro_diary")
        cur = conn.cursor()
        query = "SELECT * FROM micro_diary"
        cur.execute(query,)
        records = cur.fetchall()
        for row in records:
            txt = urwid.Text(('banner', '%s\n\n%s' % (row[1], row[2])), align='center')
            fill = urwid.Filler(txt)
            loop = urwid.MainLoop(fill, palette, unhandled_input=exit_on_q)
            loop.screen.set_terminal_properties(colors=256)
            loop.widget = urwid.AttrMap(fill, 'bg')
            loop.run()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    see()
```
