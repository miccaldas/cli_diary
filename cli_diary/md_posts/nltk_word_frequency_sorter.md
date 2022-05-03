---
title: "Sort Text by Word Frequency With NLTK"
date: 30/04/2022
mainfont: Iosevka
---

I found [NLTK](https://www.nltk.org), 'Natural Language Toolkit', when I was
looking for something to extract keywords from text. Off course at the time I
didn't knew that keyword extraction is called keyword extraction, so I was
looking for tag creation which, I found out, is a totally different story, but
led me to an article that suggested word frequency analysis as a method to
generate keywords. I now know that this is totally inadequate for this purpose
but it can have merit on other uses; and for that I'm documenting it here.  
I'll use as an example, a module I wrote to bulk import the contents of a blog
to a database. I wanted something that would automate the creation of tags for
the content, so I tried NLTK.

For each post file I would read its contents, strip it of line break symbols and
turn it into a string, as that is the accepted format for NLTK.  

```python
          with open(file, "r") as f:
              da = f.readlines()
              dat = [i.strip() for i in da]
              data = str(dat)
```

I defined a list of characters to ignore on the text analysis...

```python
         badchars = ".!?,'\":<>="
```

created a list of words longer than four characters, striped of said characters:

```python
         words = [word.strip(badchars) for word in data.strip().split() if len(word) > 4]
```

create a dictionary with the words and a numerical key:

```python
         word_freq = {}
         for word in words:
             word_freq[word] = word_freq.get(word, 0) + 1
```

create a list of tuples made up of the words and their id:

```python
        tx = [(v, k) for (k, v) in word_freq.items()]
```

sort list in descending order:

```python
        tx.sort(reverse=True) 
```

and present the tuple list with the values first.

```python
        word_freq_sorted = [(k, v) for (v, k) in tx]
```

The end result is a list with a lot, and I mean a lot, of trash in the form of
useless words, punctuations marks and other assorted artefacts that contribute
nothing to the task at hand.  
For this particular case, this is the 'cleaning' commands I had to give, and it
didn't get as clean as I would like.  
To erase all entries in a list containing a specific character, first create a
list with all entries that have the character, then create a new list from the
original list that excludes the entries on the latter.  

```python
          new_freq0 = [i for i in word_freq_sorted if i[0].startswith("class=")]
          new_freq1 = [i for i in word_freq_sorted if i not in new_freq0]
          new_freq2 = [i for i in new_freq1 if i[0].startswith("&")]
          new_freq3 = [i for i in new_freq1 if i not in new_freq2]
          new_freq4 = [i for i in new_freq3 if "><" in i[0]]
          new_freq5 = [i for i in new_freq3 if i not in new_freq4]
          new_freq6 = [i for i in new_freq5 if "<" in i[0]]
          new_freq7 = [i for i in new_freq5 if i not in new_freq6]
          new_freq8 = [i for i in new_freq7 if "=" in i[0]]
          new_freq9 = [i for i in new_freq7 if i not in new_freq8]
          new_freq10 = [i for i in new_freq9 if "." in i[0]]
          new_freq11 = [i for i in new_freq9 if i not in new_freq10]
          new_freq12 = [i for i in new_freq11 if ">" in i[0]]
          new_freq13 = [i for i in new_freq11 if i not in new_freq12]
          new_freq14 = [i for i in new_freq13 if "#" in i[0]]
          new_freq15 = [i for i in new_freq13 if i not in new_freq14]
          new_freq16 = [i for i in new_freq15 if i[0] != "div"]
          new_freq17 = [i for i in new_freq16 if i[0] != "none"]
          new_freq18 = [i for i in new_freq17 if i[0] != "none;"]
          new_freq19 = [i for i in new_freq18 if i[0] != "margin"]
          new_freq20 = [i for i in new_freq19 if i[0] != "color"]
          new_freq21 = [i for i in new_freq20 if i[0] != "code"]
          new_freq22 = [i for i in new_freq21 if "/" in i[0]]
          new_freq23 = [i for i in new_freq21 if i not in new_freq22]
          new_freq24 = [i for i in new_freq23 if i[0] != "span"]
          new_freq25 = [i for i in new_freq24 if i[0] != "font-weight"]
          new_freq26 = [i for i in new_freq25 if i[0] != "bold;"]
          new_freq27 = [i for i in new_freq26 if "\\" in i[0]]
          new_freq28 = [i for i in new_freq26 if i not in new_freq27]
          new_freq29 = [i for i in new_freq28 if i[0] != "padding"]
          new_freq30 = [i for i in new_freq29 if i[0] != "description"]
          new_freq31 = [i for i in new_freq30 if i[0] != "files"]
          new_freq32 = [i for i in new_freq31 if i[0] != "would"]
          new_freq33 = [i for i in new_freq32 if i[0] != "font-size"]
          new_freq34 = [i for i in new_freq33 if i[0] != "that"]
          new_freq35 = [i for i in new_freq34 if i[0] != "lines"]
          new_freq36 = [i for i in new_freq35 if i[0] != "padding-left"]
          new_freq37 = [i for i in new_freq36 if i[0] != "param"]
          new_freq38 = [i for i in new_freq37 if i[0] != "background-color"]
          new_freq39 = [i for i in new_freq38 if i[0] != "solid"]
          new_freq40 = [i for i in new_freq39 if i[0] != "margin-top"]
          new_freq41 = [i for i in new_freq40 if i[0] != "overflow"]
          new_freq42 = [i for i in new_freq41 if i[0] != "other"]
          new_freq43 = [i for i in new_freq42 if i[0] != "position"]
          new_freq44 = [i for i in new_freq43 if i[0] != "display"]
          new_freq45 = [i for i in new_freq44 if i[0] != "except"]
          new_freq46 = [i for i in new_freq45 if i[0] != "height"]
          new_freq48 = [i for i in new_freq46 if i[0] != "Error"]
          new_freq49 = [i for i in new_freq48 if i[0] != "auto;"]
          new_freq50 = [i for i in new_freq49 if i[0] != "body"]
          new_freq51 = [i for i in new_freq50 if i[0] != "through"]
          new_freq52 = [i for i in new_freq51 if i[0] != "while"]
          new_freq53 = [i for i in new_freq52 if i[0] != "@media"]
          new_freq54 = [i for i in new_freq53 if "em;" in i[0]]
          new_freq55 = [i for i in new_freq53 if i not in new_freq54]
          new_freq56 = [i for i in new_freq55 if "px;" in i[0]]
          new_freq57 = [i for i in new_freq55 if i not in new_freq56]
          new_freq58 = [i for i in new_freq57 if "-" in i[0]]
          new_freq59 = [i for i in new_freq57 if i not in new_freq58]
          new_freq60 = [i for i in new_freq59 if i[0] != "width"]
          new_freq = [i for i in new_freq60 if i[0] != "title"]
```

Finally I took the two most frequent words and use them as tag values.  
Below the full code:

```python
  """
  We prepare the html files of the python blog to
  be uploaded to the cli_diary database.
  """
  import os
  
  import isort
  import nltk
  import snoop
  from loguru import logger
  from mysql.connector import Error, connect
  from snoop import pp
  
  fmt = "{time} - {name} - {level} - {message}"
  logger.add("../logs/info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)  # noqa: E501
  logger.add("../logs/error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)  # noqa: E501
  
  
  def type_watch(source, value):
      return "type({})".format(source), type(value)
  
  
  snoop.install(watch_extras=[type_watch])
  
  
  # @logger.catch
  # @snoop
  def upload():
      """
      We start by creating the paths to every post file,
      then we remove the file termination from the name
      and use it for the title. We read the contents of
      the files and define them as entries. For the tags,
      we use nltk to choose the two words most used in
      the post and define them as tags.
      """
  
      f = []
      for filename in os.listdir("html_posts"):
          f.append(os.path.join("html_posts", filename))
  
      for file in f:
          tit = os.path.basename(os.path.normpath(file))
          title = tit[:-5]
  
          with open(file, "r") as f:
              da = f.readlines()
              dat = [i.strip() for i in da]
              data = str(dat)
              badchars = ".!?,'\":<>="
              words = [word.strip(badchars) for word in data.strip().split() if len(word) > 4]
              word_freq = {}
              for word in words:
                  word_freq[word] = word_freq.get(word, 0) + 1
              tx = [(v, k) for (k, v) in word_freq.items()]
              tx.sort(reverse=True)
              word_freq_sorted = [(k, v) for (v, k) in tx]
  
              new_freq0 = [i for i in word_freq_sorted if i[0].startswith("class=")]
              new_freq1 = [i for i in word_freq_sorted if i not in new_freq0]
              new_freq2 = [i for i in new_freq1 if i[0].startswith("&")]
              new_freq3 = [i for i in new_freq1 if i not in new_freq2]
              new_freq4 = [i for i in new_freq3 if "><" in i[0]]
              new_freq5 = [i for i in new_freq3 if i not in new_freq4]
              new_freq6 = [i for i in new_freq5 if "<" in i[0]]
              new_freq7 = [i for i in new_freq5 if i not in new_freq6]
              new_freq8 = [i for i in new_freq7 if "=" in i[0]]
              new_freq9 = [i for i in new_freq7 if i not in new_freq8]
              new_freq10 = [i for i in new_freq9 if "." in i[0]]
              new_freq11 = [i for i in new_freq9 if i not in new_freq10]
              new_freq12 = [i for i in new_freq11 if ">" in i[0]]
              new_freq13 = [i for i in new_freq11 if i not in new_freq12]
              new_freq14 = [i for i in new_freq13 if "#" in i[0]]
              new_freq15 = [i for i in new_freq13 if i not in new_freq14]
              new_freq16 = [i for i in new_freq15 if i[0] != "div"]
              new_freq17 = [i for i in new_freq16 if i[0] != "none"]
              new_freq18 = [i for i in new_freq17 if i[0] != "none;"]
              new_freq19 = [i for i in new_freq18 if i[0] != "margin"]
              new_freq20 = [i for i in new_freq19 if i[0] != "color"]
              new_freq21 = [i for i in new_freq20 if i[0] != "code"]
              new_freq22 = [i for i in new_freq21 if "/" in i[0]]
              new_freq23 = [i for i in new_freq21 if i not in new_freq22]
              new_freq24 = [i for i in new_freq23 if i[0] != "span"]
              new_freq25 = [i for i in new_freq24 if i[0] != "font-weight"]
              new_freq26 = [i for i in new_freq25 if i[0] != "bold;"]
              new_freq27 = [i for i in new_freq26 if "\\" in i[0]]
              new_freq28 = [i for i in new_freq26 if i not in new_freq27]
              new_freq29 = [i for i in new_freq28 if i[0] != "padding"]
              new_freq30 = [i for i in new_freq29 if i[0] != "description"]
              new_freq31 = [i for i in new_freq30 if i[0] != "files"]
              new_freq32 = [i for i in new_freq31 if i[0] != "would"]
              new_freq33 = [i for i in new_freq32 if i[0] != "font-size"]
              new_freq34 = [i for i in new_freq33 if i[0] != "that"]
              new_freq35 = [i for i in new_freq34 if i[0] != "lines"]
              new_freq36 = [i for i in new_freq35 if i[0] != "padding-left"]
              new_freq37 = [i for i in new_freq36 if i[0] != "param"]
              new_freq38 = [i for i in new_freq37 if i[0] != "background-color"]
              new_freq39 = [i for i in new_freq38 if i[0] != "solid"]
              new_freq40 = [i for i in new_freq39 if i[0] != "margin-top"]
              new_freq41 = [i for i in new_freq40 if i[0] != "overflow"]
              new_freq42 = [i for i in new_freq41 if i[0] != "other"]
              new_freq43 = [i for i in new_freq42 if i[0] != "position"]
              new_freq44 = [i for i in new_freq43 if i[0] != "display"]
              new_freq45 = [i for i in new_freq44 if i[0] != "except"]
              new_freq46 = [i for i in new_freq45 if i[0] != "height"]
              new_freq48 = [i for i in new_freq46 if i[0] != "Error"]
              new_freq49 = [i for i in new_freq48 if i[0] != "auto;"]
              new_freq50 = [i for i in new_freq49 if i[0] != "body"]
              new_freq51 = [i for i in new_freq50 if i[0] != "through"]
              new_freq52 = [i for i in new_freq51 if i[0] != "while"]
              new_freq53 = [i for i in new_freq52 if i[0] != "@media"]
              new_freq54 = [i for i in new_freq53 if "em;" in i[0]]
              new_freq55 = [i for i in new_freq53 if i not in new_freq54]
              new_freq56 = [i for i in new_freq55 if "px;" in i[0]]
              new_freq57 = [i for i in new_freq55 if i not in new_freq56]
              new_freq58 = [i for i in new_freq57 if "-" in i[0]]
              new_freq59 = [i for i in new_freq57 if i not in new_freq58]
              new_freq60 = [i for i in new_freq59 if i[0] != "width"]
              new_freq = [i for i in new_freq60 if i[0] != "title"]
  
              answers = []
              answers.append(title)
              answers.append(data)
              answers.append(new_freq[0][0])
              answers.append(new_freq[1][0])
  
          try:
              conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
              cur = conn.cursor()
              query = "INSERT INTO cli_diary (title, entry, k1, k2) VALUES (%s, %s, %s, %s)"
              cur.execute(query, answers)
              conn.commit()
          except Error as e:
              print("Error while connecting to db", e)
          finally:
              if conn:
                  conn.close()
  
  
  if __name__ == "__main__":
      upload()
```
