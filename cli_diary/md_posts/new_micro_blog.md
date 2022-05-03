---
title: new-micro-blog
mainfont: Iosevka
---

I just remade the micro_blog app. Although I liked the way it looked and how it worked, I was extremely aware that the app was running on Urwid, that grand Dame of coding, all wit, charm and Alzheimer, and if I liked it, that had more to do to a rare and happy moment of serendipity, and not anything that we could ever hope to repeat and redo.  
The inspiration came in a roundabout way. I was trying to wrap my head around [SQLAlchemy](https://www.sqlalchemy.org), and why it was so bloody hard to understand, and why, Oh my God, why?!, the documentation was so breathlessly obscurantist. Honestly, in my opinion, it's much, much simpler to try to understand SQL commands, than it is to venture to the esoteric realms of the ORMs.
I, personally always liked to learn SQL, it's a fun language and it is used in a very cool area, databases. Can't fathom why someone would sacrifice so much to avoid it.  
As it was expected, I couldn't make heads or tails of SQLAlchemy, so I started looking at other, simpler, ORMs, where I could have an introduction that wasn't as violent. I finally ended up in [Peewee](http://docs.peewee-orm.com), who has sane sounding documentation, and an apparent willingness to complicate things only if strictly necessary. Even so, I had some difficulty entering in the logic of these software. My breakthrough occurred when I gave up on their documentation and started building the project examples they have on their site. They're all cool ideas, and I felt inspired to do them all.  
The first one I did ended up substituting the old micro_blog app by a new one. So it's engaging stuff.  
The project proposed entailed creating a diary cli app that would have a encrypted database backend. Which I thought was pretty cool. This immediately reminded me of the micro_blog project, as I intended it to be a strongly confessional experience. It ended up being me absent mindedly writing some of the most inane and milquetoast observations ever heard outside a political parliament.  
Not that I have given up on it. No. I still think the idea has value. It is just that I haven't been on the right mindset for fearless self-examination for quite some time.  
The project proved out to be as entertaining as its concept. The solutions presented are interesting and they were all in a comfortable level of difficulty. Not very overly hard, but with enough intelligence and creativity to be interesting.  
And here's what I did:  
1. The module starts with the declaring of a SQLite variable as our database. It's been a while since I used SQLite databases. That was fun too. Then, as is customary on this type of software, It will be instantiated a class, that in its constituent parts, will end up representing all the concepts of a traditional SQL database.  
```python
  class Entry(Model):
      """Defines table and its structure
  
      :param content: column/attribute, defines a text column in the table
      :param timestamp: column/attribute defines timestamp
  
      """
  
      content = TextField()
      timestamp = DateTimeField(default=datetime.datetime.now)
  
      class Meta:
          """ """
  
          database = db
```
2. After that we define the database connection and its first table.
```python
  @logger.catch  # Decorator for loguru. All errors will go log. Has to be on all functions
  def initialize():
      """Defines db connection and a
      db table.
  
      :param db: init: application, defines connection
          Entry.create_table, command, creates a db table
      :param passphrase: str, password
  
      """
      pwd = str(os.environ["MICRO_PWD"])
      db.init("micro_blog.db", passphrase=pwd)
      Entry.create_table()
```
3. In this function we define the app's work loop as well as present to the user, the functionalities that the app has to offer.  
```python
  @logger.catch
  def menu_loop():
      """Sets the loop where the all application will run.
  
      :param choice: Last choice of functionality to use,
                     from the apps alternatives.
      Returns:
              prints functionality menu
  
      """
      choice = None
      while choice != "q":
          for key, value in menu.items():
              print(color("%s) %s" % (key, value.__doc__), fore="#c3bcb1"))
          choice = input(color("Actions: ", fore="#c3bcb1")).lower().strip()
          if choice in menu:
              menu[choice]()
```
4. Here we define how to add a entry to the app.
```python
  @logger.catch
  def add_entry():
      """Add Entry
  
      :param 'Enter your entry...': str, Asks for new content entry.
      :param 'Save entry...': str, If yes creates content data and
                                and prints 'Saved sucessfully'
      :returns: str
      :rtype: 'Saved sucessfully.'
  
      """
      print(color("Enter your entry. Press ctrl+d when finished.", fore="#c3bcb1"))
      data = sys.stdin.read().strip()
      if data and input(color("Save entry? [Yn] ", fore="#c3bcb1")) != "n":
          Entry.create(content=data)
          print(color("Saved successfully.", fore="#a4bdba"))
```
5. View all entries in the app:
```python
  @logger.catch
  def view_entries(search_query=None):
      """View previous entries
  
      :param query: variable, Selects all content entries by descending order of
           timestamp.
      :param search_query: variable, If it originates in the search function,
           redirect it to here. (Default value = None)
      :returns: Timestamp, entries content and options to manage said content.
  
      """
      query = Entry.select().order_by(Entry.timestamp.desc())
      if search_query:
          query = query.where(Entry.content.contains(search_query))
  
      for entry in query:
          timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M%p")
          print("\n")
          print(color(timestamp, fore="#a4bdba"))
          print(color("=" * len(timestamp), fore="#a4bdba"))
          print(color(entry.content, fore="#c3bcb1"))
          print(color("n) next entry", fore="#a4bdba"))
          print(color("d) delete entry", fore="#a4bdba"))
          print(color("q) return to main menu", fore="#a4bdba"))
          if input(color("Choice? (Nq) ", fore="#a4bdba")) == "q":
              break
```
6. Search for entries. That in this case, piggybacks on the view entries function.  
```python
  @logger.catch
  def search_entries():
      """Search entries
  
  
      :returns: Question regarding what is the keyword to use in
               their search?
  
      """
      view_entries(input(color("Search query: ", fore="#c3bcb1")))
```
7. This function defines the deletion of content entries.  
```python
  @logger.catch
  def delete_entry():
      """Deletes entry in database
  
      :param del_id: variable, ID value of the entry to delete
      :param del_row: variable, The row to be deleted
      :param del_row.execute: command, Order to erase entry.
  
      """
      del_id = input(color("What is the ID of the entry you want to delete? "))
      del_row = Entry.delete().where(Entry.id == del_id)
      del_row.execute()
```
8. And this one, the updating of the entries.  
```python
  @logger.catch
  def update_query():
      """Updates a value in a row
  
      :param updt_content: str, New content
      :param updt_val: command, Update command
  
      """
      updt_id = input(color("What is the id of your update? ", fore="#a4bdba"))
      Entry.updt_column = input(color("What column do you want to update? ", fore="#a4bdba"))
      updt_content = input(color("What is it you want to change? ", fore="#a4bdba"))
      updt_val = Entry.update({Entry.updt_column: updt_content}).where(Entry.id == updt_id)
      updt_val.execute()
```
9. This is the menu that app loop keeps serving.  
```python
  menu = OrderedDict(
      [
          ("a", add_entry),
          ("v", view_entries),
          ("s", search_entries),
          ("d", delete_entry),
          ("u", update_query),
      ]
  )
```
10. Finally it's defined what to do when a user tries to login to the db.  
In it's first incarnation, the database was a impregnable fortress, ready to withstand any attack. An example of prudent common sense and sound security precautions. Unfortunately it also made entering in the app a drag. To cut a long story short, I sabotaged all the security measures, just so that I wouldn't have to sign in every time I went to app.  
I am not a wise man.  
```python
  if __name__ == "__main__":
      # Collect the passphrase using a secure method.
      pwd = str(os.environ["MICRO_PWD"])
      if pwd is None:
          passphrase = getpass(color("Enter password: ", fore="#c3bcb1"))
          if passphrase != pwd:
              sys.stderr.write("Passphrase required to access diary.\n")
              sys.stderr.flush()
              sys.exit(1)
  
      # Initialize the database.
      initialize()
      menu_loop()
```

The full code:
```python
  #!/usr/bin/env python3
  """Encrypted version of the Micro Blog. Now done with Peewee ORM"""
  import sys
  import os
  from collections import OrderedDict
  import datetime
  from loguru import logger
  from getpass import getpass
  from peewee import *
  from playhouse.sqlcipher_ext import SqlCipherDatabase
  from colr import color
  
  fmt = "{time} - {name} - {level} - {message}"
  logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
  logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)
  
  # Defer initialization of the database until the script is executed from the
  # command-line.
  db = SqlCipherDatabase(None)
  
  
  class Entry(Model):
      """Defines table and its structure
  
      :param content: column/attribute, defines a text column in the table
      :param timestamp: column/attribute defines timestamp
  
      """
  
      content = TextField()
      timestamp = DateTimeField(default=datetime.datetime.now)
  
      class Meta:
          """ """
  
          database = db
  
  
  @logger.catch  # Decorator for loguru. All errors will go log. Has to be on all functions
  def initialize():
      """Defines db connection and a
      db table.
  
      :param db: init: application, defines connection
          Entry.create_table, command, creates a db table
      :param passphrase: str, password
  
      """
      pwd = str(os.environ["MICRO_PWD"])
      db.init("micro_blog.db", passphrase=pwd)
      Entry.create_table()
  
  
  @logger.catch
  def menu_loop():
      """Sets the loop where the all application will run.
  
      :param choice: Last choice of functionality to use,
                     from the apps alternatives.
      Returns:
              prints functionality menu
  
      """
      choice = None
      while choice != "q":
          for key, value in menu.items():
              print(color("%s) %s" % (key, value.__doc__), fore="#c3bcb1"))
          choice = input(color("Actions: ", fore="#c3bcb1")).lower().strip()
          if choice in menu:
              menu[choice]()
  
  
  @logger.catch
  def add_entry():
      """Add Entry
  
      :param 'Enter your entry...': str, Asks for new content entry.
      :param 'Save entry...': str, If yes creates content data and
                                and prints 'Saved sucessfully'
      :returns: str
      :rtype: 'Saved sucessfully.'
  
      """
      print(color("Enter your entry. Press ctrl+d when finished.", fore="#c3bcb1"))
      data = sys.stdin.read().strip()
      if data and input(color("Save entry? [Yn] ", fore="#c3bcb1")) != "n":
          Entry.create(content=data)
          print(color("Saved successfully.", fore="#a4bdba"))
  
  
  @logger.catch
  def view_entries(search_query=None):
      """View previous entries
  
      :param query: variable, Selects all content entries by descending order of
           timestamp.
      :param search_query: variable, If it originates in the search function,
           redirect it to here. (Default value = None)
      :returns: Timestamp, entries content and options to manage said content.
  
      """
      query = Entry.select().order_by(Entry.timestamp.desc())
      if search_query:
          query = query.where(Entry.content.contains(search_query))
  
      for entry in query:
          timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M%p")
          print("\n")
          print(color(timestamp, fore="#a4bdba"))
          print(color("=" * len(timestamp), fore="#a4bdba"))
          print(color(entry.content, fore="#c3bcb1"))
          print(color("n) next entry", fore="#a4bdba"))
          print(color("d) delete entry", fore="#a4bdba"))
          print(color("q) return to main menu", fore="#a4bdba"))
          if input(color("Choice? (Nq) ", fore="#a4bdba")) == "q":
              break
  
  
  @logger.catch
  def search_entries():
      """Search entries
  
  
      :returns: Question regarding what is the keyword to use in
               their search?
  
      """
      view_entries(input(color("Search query: ", fore="#c3bcb1")))
  
  
  @logger.catch
  def delete_entry():
      """Deletes entry in database
  
      :param del_id: variable, ID value of the entry to delete
      :param del_row: variable, The row to be deleted
      :param del_row.execute: command, Order to erase entry.
  
      """
      del_id = input(color("What is the ID of the entry you want to delete? "))
      del_row = Entry.delete().where(Entry.id == del_id)
      del_row.execute()
  
  
  @logger.catch
  def update_query():
      """Updates a value in a row
  
      :param updt_content: str, New content
      :param updt_val: command, Update command
  
      """
      updt_id = input(color("What is the id of your update? ", fore="#a4bdba"))
      Entry.updt_column = input(color("What column do you want to update? ", fore="#a4bdba"))
      updt_content = input(color("What is it you want to change? ", fore="#a4bdba"))
      updt_val = Entry.update({Entry.updt_column: updt_content}).where(Entry.id == updt_id)
      updt_val.execute()
  
  
  menu = OrderedDict(
      [
          ("a", add_entry),
          ("v", view_entries),
          ("s", search_entries),
          ("d", delete_entry),
          ("u", update_query),
      ]
  )
  
  
  if __name__ == "__main__":
      # Collect the passphrase using a secure method.
      pwd = str(os.environ["MICRO_PWD"])
      if pwd is None:
          passphrase = getpass(color("Enter password: ", fore="#c3bcb1"))
          if passphrase != pwd:
              sys.stderr.write("Passphrase required to access diary.\n")
              sys.stderr.flush()
              sys.exit(1)
  
      # Initialize the database.
      initialize()
      menu_loop()
```
