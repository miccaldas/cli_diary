---
title: "I Have a Problem"
mainfont: Iosevka
---

I'm having a lot of difficulties with a project of mine.  I have a bookmarks and notes python apps, that were created under the premise that a SQLite database
was there to do most of the lifting.  
Since this is mainly for personal use, I never bothered to achieve a great degree of polish.  
But I have, very recently, procured two accounts for git services, to wit,  [Notabug](https://notabug.org/), and [Github](https://github.com/).  
I still didn't got the hang of it. I still feel that this isn't necessary for me, as an hobbyist, but I can be wrong. And I have been so many times.  
The one I'm using more seriously, is Notabug. Why? Because they're so cool! Seriously, there's no other reason but the fact that I think the Notabug's project
kicks GitHub's corporate ass.  
It might be considered as shallow and superficial, and, in a way, it is, but let me clarify for you the reasons I dedicate some much time to this hobby.
You see, I'm an aesthete at heart. If I don't find it beautiful, I have no interest on whatever it might be.  
And I think that the command line, is one of the most gorgeous spaces in tech land.  
It was the desire to understand it, to master it, that started my journey. I was one of those people who had nothing but contempt towards anything computer related.
It seemed to me as the kind of thing a engineer might like, safe, abstract, small and something that normal people wouldn't waste time with.  
I remembered my irritation with any program that had any type of learning curve, I thought that it showed sloppiness in the presentation.   
That person is no more. I've become all that I once despised. And I'm still, a bit ashamed, if I'm going to be candid.  

> Cool is just conservatism dressed in black  

But onward to what brought me here:  
Now that I'm making my app public, I would welcome some input, I felt the need to clean it up a bit. One of the things I thought could be fun was to
automate it. I already did something like this, but wasn't happy with results. Results that, by the way, were much better than my current attempt.  
Taj Mahal to bus stop kind of difference.  
So what I intend to do is present a questionnaire to the putative users, where they could choose:  
 1. Database name,
 2. Table name,
 3. The table's columns and their attributes.
 At first I thought in creating a conditioned questions questionnaire; where you could advance according to what you want. Something like this:
 
```
want create column?
     yes
         what name column?
     no
         exit
 want attribute for column?
     yes
         what attribute?
     no
         exit
 want second attribute for column?
     yes
         what attribute?
     no
         exit
     I want other column
         what name column?
             want attribute for column?
                 yes
                     what attribute?
                         do you want another attribute?
                             yes
                             no
                             I want another column
                 no
                     exit'
```

I think you can see just by this _gribouille_ what was the problem I found. Nesting till the cows come home.  
I thought that this can't be the best way to solve this problem, at least not the way I'm doing it.  
So after an afternoon of looking at this thing, I felt myself inching closer and closer to the solution that sparked the need to find a better way.  
At the moment this is what I have:  

```python
  from icecream import ic
  
  
  class Basededados:
      """ This class will handle the definition of the database configuration, and text prepping to turn it into a SQLite query. """
  
      def __init__(self):
          self.key0 = 'id'
          self.spec1 = 'INTEGER'
          self.spec2 = 'NOT NULL'
          self.spec3 = 'PRIMARY KEY'
          self.key1 = 'title'
          self.spec4 = 'TEXT'
          # self.spec5 =
          # self.spec6 =
          self.key2 = 'comment'
          self.spec7 = 'TEXT'
          # self.spec8 =
          # self.spec9 =
          self.key3 = 'link'
          self.spec10 = 'TEXT'
          # self.spec11 =
          # self.spec12 =
          self.key4 = 'k1'
          self.spec13 = 'TEXT'
          # self.spec14 =
          # self.spec15 =
          self.key5 = 'k2'
          self.spec16 = 'TEXT'
          # self.spec17 =
          # self.spec18 =
          self.key6 = 'k3'
          self.spec19 = 'TEXT'
          # self.spec20 =
          # self.spec21 =
          self.key7 = 'time'
          self.spec22 = 'DATETIME'
          self.spec23 = 'DEFAULT'
          self.spec24 = 'CURRENT_TIMESTAMP'
          # self.key8 =
          # self.spec25 =
          # self.spec26 =
          # self.spec27 =
          self.table_name = 'teste1'
  
      def column_specs(self):
          """ Defines the columns names and specifications for the sqlite database. """
          a = {}
          # Column 0
          key = self.key0
          a.setdefault(key, [])
          a[key].append(self.spec1)
          a[key].append(self.spec2)
          a[key].append(self.spec3)
  
          # Column 1
          key = self.key1
          a.setdefault(key, [])
          a[key].append(self.spec4)
          # a[key].append(self.spec5)
          # a[key].append(self.spec6)
  
          # Column 2
          key = self.key2
          a.setdefault(key, [])
          a[key].append(self.spec7)
          # a[key].append(self.spec8)
          # a[key].append(self.spec9)
  
          # Column 3
          key = self.key3
          a.setdefault(key, [])
          a[key].append(self.spec10)
          # a[key].append(self.spec11)
          # a[key].append(self.spec12)
  
          # Column 4
          key = self.key4
          a.setdefault(key, [])
          a[key].append(self.spec13)
          # a[key].append(self.spec14)
          # a[key].append(self.spec15)
  
          # Column 5
          key = self.key5
          a.setdefault(key, [])
          a[key].append(self.spec16)
          # a[key].append(self.spec17)
          # a[key].append(self.spec18)
  
          # Column 6
          key = self.key6
          a.setdefault(key, [])
          a[key].append(self.spec19)
          # a[key].append(self.spec20)
          # a[key].append(self.spec21)
  
          # Column 7
          key = self.key7
          a.setdefault(key, [])
          a[key].append(self.spec22)
          a[key].append(self.spec23)
          a[key].append(self.spec24)
  
          # Column 8
          # key = self.key8
          # a.setdefault(key, [])
          # a[key].append(self.spec25)
          # a[key].append(self.spec26)
          # a[key].append(self.spec27)
  
          # print(a)
  
      def creating_the_db(self):
          import sqlite3
  
          try:
              conn = sqlite3.connect(self.table_name)
              cur = conn.cursor()
              ic("Database created and Successfully Connected to SQLite")
              sqlite_select_Query = "select sqlite_version();"
              cur.execute(sqlite_select_Query)
              record = cur.fetchall()
              ic("SQLite Database Version is: ", record)
              conn.commit()
          except sqlite3.Error as e:
              ic("Error while connecting to db", e)
          finally:
              if(conn):
                  conn.close()
  
      def envio_de_query(self):
          import sqlite3
  
          questao = 'CREATE TABLE ' + self.table_name + ' (' + self.key0 + ' ' + self.spec1 + ' ' + self.spec2 + ' ' + self.spec3 + ', ' \
              + self.key1 + ' ' + self.spec4 + ', ' + self.key2 + ' ' + self.spec7 + ', ' + self.key3 + ' ' + self.spec10 + ', ' \
              + self.key4 + ' ' + self.spec13 + ', ' + self.key5 + ' ' + self.spec16 + ', ' + self.key6 + ' ' + self.spec19 + ', ' \
              + self.key7 + ' ' + self.spec22 + ' ' + self.spec23 + ' ' + self.spec24 + ')'
          # print(questao)
          try:
              conn = sqlite3.connect(self.table_name)
              cur = conn.cursor()
              query = questao
              cur.execute(query,)
              conn.commit()
          except sqlite3.Error as e:
              print("Error while connecting to db", e)
          finally:
              if(conn):
                  conn.close()
  
  
  a = Basededados()
  # dictionary_data = a.column_specs()
  create_db = a.creating_the_db()
  # emission = a.envio_de_query()
  # a.creating_the_db()
  
  
  if __name__ == '__main__':
      Basededados()
```  

As we can, all, agree, this is not very pretty.    
But I'm not beat, just tired. I'll look again at this in a week or so, with fresh eyes, and something will come up.  
We hope.  

-------------------------------------------------------------------------------------

## UPDATE
I solved it! At least part of it. The part it seemed most difficult when I last talked to you. Now, because of this new directions, new challenges are
appearing. I hope I can solve them too. My greatest worry was to avoid those interminable lists of exactly the same structured variables, and I managed that. Behold:

```python
   a = collections.OrderedDict()
   col_num = int(input(color('How many columns will you need? ', fore='#ff6f69')))
   for y in range(col_num):
      col_name = input(color('What is the name of your column? ', fore='#ff6f69'))
      key = col_name
      a.setdefault(key, [])
      att_num = int(input(color('How many attributes will you need? ', fore='#ff6f69')))
      for x in range(att_num):
          att_name = input(color('What is the name of your attribute? ', fore='#ff6f69'))
          a[key].append(att_name)
```



And that was it. It seems so simple now, but I had to return to this problem many times to get it right.  
More on this, when I finally finish it.  
