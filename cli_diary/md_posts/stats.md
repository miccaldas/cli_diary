---
title: stats
mainfont: Iosevka
---

This conversation will be, again, about the notes app, and some minor
tweaks that I made. There was a lot of things I tried to implement in the
app that, although successful, were a bit too much information for little
value. As I didn't want to loose all that I had did, as some have the
silly charm of things that are not serious, needed, but just superfluous
and mildly cool. Or at least that's what I think.  
I decided to aggregate all this spurious information in a small module 
called 'stats.py'. It is accessed through the main interface as its own
entry, so it won't bother anyone who doesn't want to be bothered.  

### tag_list
The first one returns a list of tags ordered by the number of mentions it
has. I've done it thusly:
To present the tags by number of mentions, I used the MySQL expression:
```python
  queries = [
          "SELECT k1, count(*) as links FROM notes GROUP BY k1",
          "SELECT k2, count(*) as links FROM notes GROUP BY k2",
          "SELECT k3, count(*) as links FROM notes GROUP BY k3",
      ]
```
This returns a tuple with the tag and the number of links.  
To sort the list of tuples by the link number values, I had to find a way to
sort the tuples by its second value.  
I find the following expression that does just that but that, sadly, I don't
understand at all.  
```python
  records.sort(
              key=lambda x: x[1]
          )
```
In order to clean the output of all the tuple and list symbols, I used a list
comprehension to flatten out the list of tuples to just a list.  
```python
  records = [i for t in records for i in t]
```
I now had a clean output but I wanted to give some colour to the presentation.
Specifically I wanted the tag name to be in a colour and the value in another.
The solution I found was to zip the list and iteratively connect it with
herself.  
This was a very cool solution, that I'm not involved at all, except as avid
reader of Stack-Overflow.  
```python
  it = iter(records)
  for x, y in zip(it, it):
      print(color("  " + x, fore="#acac87")), print(color("  " + str(y), fore="#f18892"))
```

### entries
This functions just returns the number of entries in the database, with this
expression:  
```python
  "SELECT COUNT(*) FROM notes"
```
And there is nothing more to say, really.  

### tags
This one was surprisingly difficult.  I needed to make three queries to the
database, one for each keyword column, with this format:  
```python
  "SELECT COUNT(DISTINCT k1) FROM notes"
```
"Count" adds the k1 entries and "distinct" ensures that no repeated value is
taken in consideration. My idea was to bundle all the queries, as done before,
and sum the results between the elements of a list. I thought wrong.  
For some reason, each value taken from k1, k2, k3, were presented as a organic
whole. The list had just one entry and the values had no individual existence.
So, no way to sum them. The not elegant but efficacious solution was to process
each column separately, insuring that its output was separated from the other
values. Something like this:  
```python
  try:
      conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
      cur = conn.cursor()
      query = queryk1
      cur.execute(
          query,
      )
      recordk1 = cur.fetchone()
  
      query = queryk2
      cur.execute(
          query,
      )
      recordk2 = cur.fetchone()
  
      query = queryk3
      cur.execute(
          query,
      )
      recordk3 = cur.fetchone()
```
This is atrocious I know, but I just couldn't grok how to solve that problem.
Now I had three lists, each with a one-element tuple inside it, that I needed
to add up. Once again, I helped myself to some magical coding, and used a
solution that I don't understand at all.  
```python
  soma = tuple(map(sum, zip(recordk1, recordk2, recordk3)))
```

Here's the complete code:
```python
  """Module will aggregate disparate statistics about the app."""
  from loguru import logger
  from colr import color
  from mysql.connector import connect, Error
  
  fmt = "{time} - {name} - {level} - {message}"
  logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
  logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)
  
  
  @logger.catch
  def tag_list():
      """I'll join the three lists and order them by number of connections."""
      queries = [
          "SELECT k1, count(*) as links FROM notes GROUP BY k1",
          "SELECT k2, count(*) as links FROM notes GROUP BY k2",
          "SELECT k3, count(*) as links FROM notes GROUP BY k3",
      ]
      try:
          for q in queries:
              conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
              cur = conn.cursor()
              query = q
              logger.info(query)
              cur.execute(
                  query,
              )
          records = cur.fetchall()
          # Records is a list and row is a tuple with the tag name and number of connections.
  
          records.sort(
              key=lambda x: x[1]
          )  # This sorts the list by the value of the second element. https://tinyurl.com/yfn9alt7
          records = [i for t in records for i in t]
          it = iter(records)  # Solution to intercalate colorization, taken from here https://tinyurl.com/ygpwdrcl
          for x, y in zip(it, it):
              print(color("  " + x, fore="#acac87")), print(color("  " + str(y), fore="#f18892"))
      except Error as e:
          print("Error while connecting to db", e)
      finally:
          if conn:
              conn.close()
  
  
  if __name__ == "__main__":
      tag_list()
  
  
  @logger.catch
  def entries():
      """Returns the number of entries in the database"""
      try:
          conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
          cur = conn.cursor()
          query = "SELECT COUNT(*) FROM notes"
          cur.execute(
              query,
          )
          records = cur.fetchall()
          records = [i for t in records for i in t]
          records = str(records)
          records = records[1:-1]
          tag_num = int(records) * 3
          print("\n")
          print(color(f"  The number of database entries is {records}", fore="#a5a590"))
      except Error as e:
          print("Error while connecting to db", e)
      finally:
          if conn:
              conn.close()
  
  
  if __name__ == "__main__":
      entries()
  
  
  @logger.catch
  def tags():
      """Counts all keywords without duplications"""
      queryk1 = "SELECT COUNT(DISTINCT k1) FROM notes"
      queryk2 = "SELECT COUNT(DISTINCT k2) FROM notes"
      queryk3 = "SELECT COUNT(DISTINCT k3) FROM notes"
      try:
          conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
          cur = conn.cursor()
          query = queryk1
          cur.execute(
              query,
          )
          recordk1 = cur.fetchone()
  
          query = queryk2
          cur.execute(
              query,
          )
          recordk2 = cur.fetchone()
  
          query = queryk3
          cur.execute(
              query,
          )
          recordk3 = cur.fetchone()
  
          soma = tuple(map(sum, zip(recordk1, recordk2, recordk3)))  # Taken from here: https://tinyurl.com/y35we4g7
          soma = str(soma)
          soma = soma[1:-2]
          print(color(f"  The number of tags in the database is {soma}", fore="a5a590"))
  
      except Error as e:
          print("Error while connecting to db", e)
      finally:
          if conn:
              conn.close()
  
  
  if __name__ == "__main__":
      tags()
```
