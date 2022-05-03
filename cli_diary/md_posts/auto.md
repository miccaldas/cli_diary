---
title: Auto
mainfont: Iosevka
---

I am very sure that I must not be the first person that stopped writing in a blog, because tinkering with it took all the time he had.  
I understand now the emphasis some people give to a clean environment to write in, free from distractions.  
That is not the environment that I'm in right now. Making the blog as I go along, has pushed me in several directions, all of them 
interesting, all of them adding something to the site and, all orthogonal to each other.  
So, to take a breather, I stopped to write this post.  
After trying the simplicity of the flat files and static sites, I noticed wistfully, that this system did without a database. In fact it was one of its selling points. No added complexity from  managing a database, they say. Well, after trying their solution I was reminded that their simplicity comes at the cost of ease of use, as is so many times the case. Or, more realistically, it's just a reflection of my own ignorance. I was having a difficult time understanding the management and manipulation of the metadata. In the static files solutions, it's all done with files that get information through JavaScript template tricks that I didn't understand at all.  
That was another thing that started tugging at me. Learn a bit of JavaScript.  
A database I understand. At least I understand those that cater to my simple needs.  
So I created a small python class to help collect and keep some metadata on my posts, that I'll keep on a mysql database.  
This is what I did:  

1.  I imported [string](https://www.journaldev.com/23788/python-string-module), to capitalize words without having to worry with errors coming from apostrophes,
[Sultan](https://sultan.readthedocs.io/en/latest/), because it's easier than Subprocess, mysql.connector to link to the db and [Colr](https://github.com/welbornprod/colr) to make it less drab.
```python
  import string
  from sultan.api import Sultan
  from mysql.connector import connect
  from colr import color
```

2. Opened the class and defined the global variable 'tit' for title, because it
soon became clear that it would be needed for a lot of methods.
```python
  class Meta():
  
      def __init__(self, tit):
          self.tit = input(color('  [T] - Title? ', fore='#fa2033'))
```

3. Title method. Collects the title chosen by the user and capitalizes the
first letter of every word.
```python
  def title(self):
      """ Collects the title chosen by the user and capitalizes the
      first letter of every word. """
      self.title = string.capwords(self.tit)  # https://bit.ly/3pMw9ew
      return self.title
```

4. Create a db entry with the URL of the post.
```python
  def link(self):
      """ Creates an entry with a link where the post will be. """
      slug = input(color('  [S] - Slug? ', fore='#fa2033'))
      lnk = '/usr/share/nginx/html/analytics/ascii/public/pages/posts/'\
            + slug + ".html"
      return lnk
```

5. Create a draft page.
```python
  def page(self):
      """ Creates the draft page. """
      s = Sultan()
      draft_path = "/usr/share/nginx/html/analytics/ascii/drafts/" \
          + "'" + self.tit + "'" + ".md"
      with Sultan.load() as s:
          s.touch(draft_path).run()
```
 
6. Asks the user for a description of the post.
```python
  def description(self):
      """ Asks the user for a description of the post. """
      descript = input(color('  [D] - Write a description: ',
                             fore='#fa2033'))
      return descript
```

7. Ask for tags.
```python
  def tags(self):
      """ Asks the user for the tags of the post. """
      tgs = input(color('  [T] - Tags? ', fore='#fa2033'))
      return tgs
```

8. Asks for categories.
```python
  def categories(self):
      """ Asks the user for the categories of the post. """
      cat = input(color('  [C] - Choose the Categories ', fore='#fa2033'))
      return cat
```

9. Turns all function results in strings so it can be sent as a query.
```python
  def answers(self):
      tit = str(self.title())
      desc = str(self.description())
      tags = str(self.tags())
      cat = str(self.categories())
      lnk = str(self.link())
      answrs = [tit, desc, tags, cat, lnk]
      return answrs
```

10. Send it to the database.
```python
  def connection(self):
      self.page()
      conn = connect(
              host="localhost",
              user="root",
              password="xxxx",
              database="dazed")
      cur = conn.cursor()
      query = """ INSERT INTO dazed (title, description, tags, categories, link)
              VALUES (%s, %s, %s, %s, %s) """
      cur.execute(query, self.answers())
      conn.commit()
      conn.close()
```

Here is the whole code:

```python
  
  """ This class will house the functions for the creation of the\
  post's metadata. """
  import string
  from sultan.api import Sultan
  from mysql.connector import connect
  from colr import color
  
  
  class Meta():
  
      def __init__(self, tit):
          self.tit = input(color('  [T] - Title? ', fore='#fa2033'))
  
      def title(self):
          """ Collects the title chosen by the user and capitalizes the
          first letter of every word. """
          self.title = string.capwords(self.tit)  # https://bit.ly/3pMw9ew
          return self.title
  
      def link(self):
          """ Creates an entry with a link where the post will be. """
          slug = input(color('  [S] - Slug? ', fore='#fa2033'))
          lnk = '/usr/share/nginx/html/analytics/ascii/public/pages/posts/'\
                + slug + ".html"
          return lnk
  
      def page(self):
          """ Creates the draft page. """
          s = Sultan()
          draft_path = "/usr/share/nginx/html/analytics/ascii/drafts/" \
              + "'" + self.tit + "'" + ".md"
          with Sultan.load() as s:
              s.touch(draft_path).run()
  
      def description(self):
          """ Asks the user for a description of the post. """
          descript = input(color('  [D] - Write a description: ',
                                 fore='#fa2033'))
          return descript
  
      def tags(self):
          """ Asks the user for the tags of the post. """
          tgs = input(color('  [T] - Tags? ', fore='#fa2033'))
          return tgs
  
      def categories(self):
          """ Asks the user for the categories of the post. """
          cat = input(color('  [C] - Choose the Categories ', fore='#fa2033'))
          return cat
  
      def answers(self):
          tit = str(self.title())
          desc = str(self.description())
          tags = str(self.tags())
          cat = str(self.categories())
          lnk = str(self.link())
          answrs = [tit, desc, tags, cat, lnk]
          return answrs
  
      def connection(self):
          self.page()
          conn = connect(
                  host="localhost",
                  user="root",
                  password="xxxx",
                  database="dazed")
          cur = conn.cursor()
          query = """ INSERT INTO dazed (title, description, tags, categories, link)
                  VALUES (%s, %s, %s, %s, %s) """
          cur.execute(query, self.answers())
          conn.commit()
          conn.close()
  
  
  meta = Meta('0')
  meta.connection()
```
--------------------------------------------------------------------------------------------

## UPDATE
It is now 21-08-2021 and I rediscovered this project that I think is very cool. There is no way to get it back as the 'dazed' database doesn't exist anymore. But it's a pity. I would have liked very much to revisit this project.  
