---
title: "Yake Keyword Extractor"
date: 29/04/2022
mainfont: Iosevka
---

As I have had several projects that implied bulk uploads to databases, the
problem of generating, as automatically as possible, keywords has been on my
mind.  
I tried some NLP tools to see if they could help; NLTK for word frequency, spaCy
for keyword extraction and some others. The best for beginners is, without a
doubt, [Yake](https://github.com/LIAAD/yake). It had the best results of all the
tools that I tried.  
Here I'll explain how I implemented it on the 'notes' app.  

'Notes' is structured like a class that has as first method, two prompts asking
for the title and the text of the note. Immediately after having the note text
inputted, we initiate the tag suggestion method.
It starts with instancing the yake extractor:

```python
   kw_extractor = yake.KeywordExtractor()
```

We reference the note body as a 'text' variable. Just because some code was
already written with that name and I didn't felt like reviewing it.  

```python
   text = self.note
```

The language used is English.  

```python
   language = 'en'
```

'Max Ngram Size' refers to the number of words that can be accounted as keywords.
Setting it to 1 means that the keywords will be one word only.  

```python
          max_ngram_size = 1
```

A 'deduplication threshold' of 0.9, means that it's permitted to repeat similar
words in the keyword list. Although logically setting it to 0.1 and not permit
duplications seems more reasonable, my short experience showed me that a lot of
good content is lost with that option.  

```python
          deduplication_threshold = 0.9
```

This defines how many keyword suggestions will be outputted.  

```python
          numOfKeywords = 10
```

We define the extractor with the characteristics previously seen:  

```python
      custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
```

And house the keywords in a variable list called 'keywords'.  

```python
          keywords = custom_kw_extractor.extract_keywords(text)
```

Each keyword is presented as a tuple made of a string, the name of the keyword,
and a number, the fitness of the keyword. As we are only interested in the
strings, we isolate them in a new list.  

```python
          for kw in keywords:
              kwds.append(kw[0])
```

In order to have a simple way to choose the keywords, we assign a number to each
one, through the method 'Enumerate', and ask the user if he wants to choose up
to three options.  

```python
       for idx, kwd in enumerate(kwds):
          print(idx, kwd)
      kwdcho = input(highlight("If you want to keep any of three keywords, type their number. ", lexer, formatter))
```

If the user chose some keywords, we begin by splitting the output by the with
spaces, as it returns a string with this format: '2 3'. As we split it, we end
up with a list of two strings, as per the example: ['2', '3'].  

```python
          if kwdcho != "":
              kwdchoi = kwdcho.split(" ")
  
```

We now have a list of strings but we need a list of integers. We convert it
here.  

```python
              kwd_choice = []
              for num in kwdchoi:
                  kwd_choice.append(int(num))
```

We recuperate the tuples of the choices:  

```python
              for i in kwd_choice:
                  choice = [(idx, val) for (idx, val) in enumerate(kwds) if idx == i]
                  choices.append(choice)
  
```

Here we flatten 'choices', as it consists of list of tuples within a list.  

```python
              flatter_choices = [i for sublist in choices for i in sublist]
```

We isolate the keywords strings of the choices:  

```python
              kwd_names = []
              for f in flatter_choices:
                  kwd_names.append(f[1])
```

Depending on the length of the list of keywords, we ask to define
as many keywords as needed to get to the number three.  

```python
              if len(kwd_names) == 1:
                  self.k1 = kwd_names[0]
                  self.k2 = input(highlight(" Choose a keyword » ", lexer, formatter))
                  self.k3 = input(highlight(" Choose another... » ", lexer, formatter))
              if len(kwd_names) == 2:
                  self.k1 = kwd_names[0]
                  self.k2 = kwd_names[1]
                  self.k3 = input(highlight(" Choose a keyword » ", lexer, formatter))
              if len(kwd_names) == 3:
                  self.k1 = kwd_names[0]
                  self.k2 = kwd_names[1]
                  self.k3 = kwd_names[2]
```

And, finally, if the user didn't chose any of the suggestions, we prompt him to
input three keywords.  

```python
          else:
              self.k1 = input(highlight(" Choose a keyword » ", lexer, formatter))
              self.k2 = input(highlight(" Choose another... » ", lexer, formatter))
              self.k3 = input(highlight(" And another... » ", lexer, formatter))
```


For context, here it is the full code of the class:

```python
  """Collects user input, checks keywords for similarity, if they're new and their frequency.
  Sends information to the database and creates the md and html pages."""
  import time
  from time import sleep
  
  import click
  import snoop
  import yake
  from mysql.connector import Error, connect
  from pygments import highlight
  from pygments.formatters import TerminalTrueColorFormatter
  from pygments.lexers import get_lexer_by_name, guess_lexer  # noqa: F401
  from snoop import pp
  from thefuzz import fuzz  # noqa: F401
  from thefuzz import process
  
  lexer = get_lexer_by_name("brainfuck", stripall=True)
  formatter = TerminalTrueColorFormatter(linenos=False, style="zenburn")
  
  
  class Add:
      """The class starts with user input and a list with all tags in a string list.
      Having them separated will simplify processes. With this information collected,
      first we'll ask the keywords questions and run its processes, one by one.
      After this is done we'll send the information to the database and create the
      md and html files."""
  
      # @snoop
      def input_data(self):
          """All the user inputs needed to create a new entry are located here."""
          self.title = input(highlight(" Title? » ", lexer, formatter))
          print(highlight(" Write a note.", lexer, formatter))
          sleep(1)
          self.note = click.edit().rstrip()
  
      # @snoop
      def suggest_tags(self):
          """
          We'll use Yake to suggest keywords to the user. He may choose all, some
          or opt for writing them himself.
          """
          kw_extractor = yake.KeywordExtractor()
          text = self.note
          language = "en"
          max_ngram_size = 1
          deduplication_threshold = 0.9
          numOfKeywords = 10
          custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
          keywords = custom_kw_extractor.extract_keywords(text)
          kwds = []
          for kw in keywords:
              kwds.append(kw[0])
          for idx, kwd in enumerate(kwds):
              print(idx, kwd)
          kwdcho = input(highlight("If you want to keep any of three keywords, type their number. ", lexer, formatter))
          if kwdcho != "":
              kwdchoi = kwdcho.split(" ")
              kwd_choice = []
              for num in kwdchoi:
                  kwd_choice.append(int(num))
              choices = []
              for i in kwd_choice:
                  choice = [(idx, val) for (idx, val) in enumerate(kwds) if idx == i]
                  choices.append(choice)
              flatter_choices = [i for sublist in choices for i in sublist]
              kwd_names = []
              for f in flatter_choices:
                  kwd_names.append(f[1])
              if len(kwd_names) == 1:
                  self.k1 = kwd_names[0]
                  self.k2 = input(highlight(" Choose a keyword » ", lexer, formatter))
                  self.k3 = input(highlight(" Choose another... » ", lexer, formatter))
              if len(kwd_names) == 2:
                  self.k1 = kwd_names[0]
                  self.k2 = kwd_names[1]
                  self.k3 = input(highlight(" Choose a keyword » ", lexer, formatter))
              if len(kwd_names) == 3:
                  self.k1 = kwd_names[0]
                  self.k2 = kwd_names[1]
                  self.k3 = kwd_names[2]
          else:
              self.k1 = input(highlight(" Choose a keyword » ", lexer, formatter))
              self.k2 = input(highlight(" Choose another... » ", lexer, formatter))
              self.k3 = input(highlight(" And another... » ", lexer, formatter))
  
      # @snoop
      def taglst(self):
          """Union allows to combine two or more sets of results into one, but,
          the number and order of columns that appear in the SELECT statement
          must be the same, and the data types must be equal or compatible.
          Union removes duplicates.
          """
          try:
              conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
              cur = conn.cursor()
              query = "SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
              cur.execute(query)
              records = cur.fetchall()  # Results come as one-element tuples. It's needed to turn it to list.
              self.records = [i for t in records for i in t]
              conn.close()
          except Error as e:
              print("Error while connecting to db", e)
  
      # @snoop
      def tag_links(self):
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
                  cur.execute(
                      query,
                  )
              self.links = cur.fetchall()
              # Records is a list and row is a tuple with the tag name and number of connections.
              self.links.sort(key=lambda x: x[1])  # This sorts the list by the value of the second element. https://tinyurl.com/yfn9alt7
              conn.close()
          except Error as e:
              print("Error while connecting to db", e)
  
      # @snoop
      def issimilar(self):
          """Uses Thefuzz library to compare keyword strings. If similarity is above 80%,
          it prints a mesage asking if the user wants to change it."""
          conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
          cur = conn.cursor()
          query = "SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
          cur.execute(query)
          records = cur.fetchall()  # Results come as one-element tuples. It's needed to turn it to list.
          self.records = [i for t in records for i in t]
  
          self.keywords = [self.k1, self.k2, self.k3]
          for k in self.keywords:
              value = process.extractOne(k, self.records)
              if 80 < value[1] < 100:  # If we don't define it as less that 100, it will show message when inputing a old keyword.
                  chg_tag_decision = input(
                      highlight(f" You inputed the word {k}, that is similar to the word {value[0]}, that already is a keyword. Won't you use it instead? [y/n] ", lexer, formatter)
                  )
                  if chg_tag_decision == "y":
                      if k == self.k1:
                          self.k1 = value[0]
                      if k == self.k2:
                          self.k2 = value[0]
                      if k == self.k3:
                          self.k3 = value[0]
              else:
                  pass
  
      # @snoop
      def new_tag(self):
          """Will check the keyword names against the db records. If it doesn't find a
          match, it will produce a message saying the tag is new."""
          self.keywords = [self.k1, self.k2, self.k3]
          for k in self.keywords:
              res = any(k in i for i in self.records)
              if not res:
                  print(highlight(f" [*] - The keyword {k} is new in the database.", lexer, formatter))
              else:
                  pass
  
      # @snoop
      def count_links(self):
          """Will check the new keywords, see how many links they'll have, and return that
          information."""
          queries = [
              "SELECT k1, count(*) as links FROM notes GROUP BY k1",
              "SELECT k2, count(*) as links FROM notes GROUP BY k2",
              "SELECT k3, count(*) as links FROM notes GROUP BY k3",
          ]
          for q in queries:
              conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
              cur = conn.cursor()
              query = q
              cur.execute(
                  query,
              )
          self.links = cur.fetchall()
  
          for i in self.links:
              if i[0] == self.k1:
                  new_i = list(i)
                  new_val = [new_i[0], (new_i[1] + 1)]
                  print(highlight(f"[*] - The updated value of the keyword links is {new_val}", lexer, formatter))
              if i[0] == self.k2:
                  new_i = list(i)
                  new_val = [new_i[0], (new_i[1] + 1)]
                  print(highlight(f"[*] - The updated value of the keyword links is {new_val}", lexer, formatter))
              if i[0] == self.k3:
                  new_i = list(i)
                  new_val = [new_i[0], (new_i[1] + 1)]
                  print(highlight(f"[*] - The updated value of the keyword links is {new_val}", lexer, formatter))
  
      # @snoop
      def add_to_db(self):
          """Sends the data to the database"""
          answers = [self.title, self.k1, self.k2, self.k3, self.note]
          try:
              conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
              cur = conn.cursor()
              query = "INSERT INTO notes (title, k1, k2, k3, note) VALUES (%s, %s, %s, %s, %s)"
              cur.execute(query, answers)
              conn.commit()
          except Error as e:
              print("Error while connecting to db", e)
          finally:
              if conn:
                  conn.close()
          print(highlight(f" [*] - The entry named: {self.title}, was added to the database.", lexer, formatter))
  
  
```
