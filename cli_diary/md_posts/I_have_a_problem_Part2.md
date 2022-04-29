---
title: "I Have a Problem Part2"
mainfont: Iosevka
---

New news on the database and table automation front. None of them good. After a strong beginning, as told in the update to the first part of this series,
I reached another deadlock, two actually:  

1. How to unpack dictionary items to free standing variables,  
2. How to automate the string manipulations necessary for transforming the received input into a SQL query that SQLite accepts.  

In regards to the collecting the information from the user, I have the following set-up:  

```python  
def collect_data():  
    db_name = input(color('What name do you want for the database? ', fore='#585a47'))
    table_name = input(color('What name do you want for the table? ', fore='#585a47'))
    print('\n')
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
As you can see, in order to steer clear of the long, repetitive lists from my first attempt, I managed to encapsulate all needed questions and answers in the
very compact set of lines. And that pleases me to no end. But what I didn't considered this time, is that by using loops, I can't isolate in variables, each iteration of the loop. I can access them as data points inside a dictionary; but that doesn't give me the freedom that I need to manipulate the answers strings to serve
 SQL query.  
 At the same time, I ask myself if I'm wrong about this. That the dictionaries methods are enough for me to pass all necessary information to the query. But if it is, I haven't been smart enough to figure it it out.  
 The thing is this: The output I currently get, explaining what columns to use and what attributes they'll have, has the following aspect.  
 This is for a test table which would have the following structure:  

 1. Column Name: 'ID'       Column Attributes: INT, NOT NULL, PRIMARY KEY,  
 2. Column Name: 'Title'    Column Attributes: TEXT,  
 3. Column Name: 'Link'     Column Attributes: TEXT  

 For it to become an acceptable query, it will have to have this format:  

 ```sql
 CREATE TABLE <table_name>( id INT NOT NULL PRIMARY KEY, title TEXT, link TEXT)
 ```
And this is how I'm getting the information from the questions processing function:  

```python
OrderedDict([('id', ['int', 'not null', 'primary key']), ('title', ['text']), ('link', ['text'])])
```

A few things about this; the 'OrderedDict' is a string that comes from creating this dictionary as an [ordered dictionary](https://docs.python.org/3/library/collections.html#collections.OrderedDict), a type of dictionary that has some item manipulations methods that seemed interesting to me. For one the order in what the items were inputted is remembered, and it doesn't change from one invocation to another, as it happens in the other dictionaries.  
So, for the sake of argument, let's imagine that I'm right, (oh, in what shaky foundations we build this reasoning!), and that there is the need to free the information from its dictionary prison. In that case we have to embark in a series of alterations to this output, for it to be accepted by SQLite.  
My first problem is all the punctuation that has to go. At this moment, If I ask how many elements are in that string, the answer is 3:  

```python
1. [('id', ['int', 'not null', 'primary key']),
2. ('title', ['text']),
3. ('link', ['text'])
```

So I need to eliminate all the python syntax symbols.  
To do that, I did the following operations:  

1. Transform the output into a list. In order to be able to access elements individually, is necessary to turn the items from the dictionary into a list. So we create a list called 'items', with all it's content. 'Item' refers to a key:value pair.  
```python
items = list(a.items())  
```
2. Create a empty list to house the transformed values we will create.  
```python
results = []
```
3. Create a loop where we'll iterate through the items and subject them to several manipulations:  
```python
for i in items:
```
4. Create a new variable to house the transformation from a list into a string. The new variable is needed for reasons of clarity and it will be necessary when doing the string manipulations, as strings are immutable, each alteration creates a new string. The reason to turn it to a string is because all the methods that I know of changing characters, are string methods. If I'm wrong, please tell me, as this is not the most comfortable of environments.  
```python
ita = str(i)
```
5. Now we clean the output of the "()[]'" characters.  
```python
itb = ita.translate({ord(i): None for i in "()[]'"})
```
6. We separate the items in different units, using the commas as measurements where to cut.  
```python
itc = itb.split(',')
```
7. We cleave the first element of this separated string and keep it in a list. It is the first columns name. Now that I'm looking back at this, I think that this
step is superfluous, but I'll leave it, to document what I've done. Warts and all.  
```python
itd = itc[0]
results.append(itd)
```
8. Now we separate the rest of the column specifications (its attributes), in another variable.  
```python
ite = itc[1:]
```
9. And we turn it into a string.  
```python
itf = str(ite)
```
10. Now we clean this output of the characters, "[],'".  
```python
itg = itf.translate({ord(i): None for i in "[],'"})
```
11. And turn their characters into uppercase. It's not really needed but, it's a SQL convention that I honor because it makes the output more legible. Then we append it
to the list.  
```python
ith = itg.upper()
results.append(ith)
```
12. Now for the creation of the query. We start with the beginning of the query in a string. The rest will be added when we insert the values.  
```python
query1 = 'CREATE TABLE ' + table_name + '('
```
13. Now we iterate through the list were we saved our variables, and add them some punctuation needed to build the query. And we're done.  
```python
for result in results:
    query1 += result + ' '
query2 = query1 + ')'
```
The resulting output is this:  
```sql
CREATE TABLE cards(id  INT  NOT NULL  PRIMARY KEY title  TEXT link  TEXT )
```

And I observe that, after all this, we still have configuration problems.  
The command lacks two commas that are fundamental. I know this because I tried to sent it as is (trusting that the Gods of SQL were with me), and it didn't work.
What is needed is a comma after 'PRIMARY KEY', and another after the first 'TEXT'. Like this.  
```sql
CREATE TABLE cards(id  INT  NOT NULL  PRIMARY KEY, title  TEXT, link  TEXT )
```
And this is where I get into trouble.  
Remember that we're dealing with a string, so any attempt at indexing has to take into account that, the there is an index for each character and space in the query.
There are, now, no concepts like three elements, each indexed with its own tag.  
Now, if we want to manipulate the string we'll have to think character by character.  
But that would be a wasted effort. The places were we want to put our commas will be in the different indexes every time a new table is built. There's no way to guarantee that every time, at that location, will be the end of 'PRIMARY KEY', for example.  
So I looked for methods that would delete characters by their recurrence or by type.  
I tried this function I found in Stack Overflow:  
```python
 def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop until we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s


 s = str(results)
 s1 = nth_repl(s, ',', '', 1) # Replaces 1st occurrence of a comma
 s2 = nth_repl(s1, ',', '', 2)
 s3 = nth_repl(s2, ',', '', 3)
```
It didn't work. Don't know why. It should have worked. But the fucking commas were still there, after each attempt I did.  
I tried to get there by skipping every other comma in the query. Like so:  
```python
for i in range(0, len(a), 2):
    s = 'CREATE TABLE cards(id  INT  NOT NULL  PRIMARY KEY title  TEXT link  TEXT )'
    s1 = s.replace('a', ''))
    print(s1)
```
The idea was to insert a command every two iterations of the loop, to coincide with the end of the attribute definitions, that would write a comma. But in the output, the commas came before the rest of the content.  
I tried to add a comma to the values when they are inserted into to the list, but this only compounded the problems, not solved it.  
But no luck, I never seemed to be on the commas I wanted to eliminate.  
There was other stuff I tried or thought about. For instance, removing all the commas with 'translate' and then put only the ones I needed. Like so:  
```python
s = 'abc12321cba'
print(s.translate({ord('a'): None}))
```
But this would only take from a place where I had too many commas, to another, where I didn't have enough.  
At this point in time, I'm too tired and burnt out to think about this issue anymore. I'll leave it alone for a few days and come back, hopefully, with another attitude.
As it was clear that I was getting nowhere in this direction, I thought to change the paradigm. What if instead of taking the loop values directly to the query, we would put them first in variables, and then from those well defined, clean variables, build a SQL expression.  
This was closer to my original idea, (which, if ugly as hell, it's still the one that works best, from all those that i came up with.), to declare all variables out loud, and go from there. As I am acutely aware of the horrible, horrible code that that approach begets, I tried to find a middle ground.  
My idea was to create variables for each data item after leaving the loop, and create the query from them.  
The problem that I faced, and that seems to me, as complex as the latter, is how to name variables that would be created automatically in a loop?  
All that I read about this was how a terrible idea this is, and that we would be much better served if we created a dictionary.  
Well, I have a dictionary, what I need is to free myself from it!  
And here, again, slouches the old doubt, do I know enough about python dictionaries to say that this can't be done with their methods?  
Although how I don't have an inkling how I would go about doing it, there's always a nagging feeling in the back of my brain, telling me that this enormous problem is fruit of my ignorance, and that this could be solved with less coding and more studying. Which, even if true, would turn this endeavor into a massive chore. I have a lot of difficulties concentrating in a task where I'm not actively involved. To sit and absorb, doesn't come easy to me. And yes, I had a lovely time at school, as you might imagine.
But I tried not be dissuaded by voices that, however well-meaning and informed, were explaining a problem that I didn't fully understand and, most important, didn't address my most urgent concern; how to solve MY problem.  
So I tried to build the variables by globals():  
```python
for key in range(9):
    globals()['key_{}'.format(key)] = 'a'
```
but find it too cumbersome to be of any real value. I tried also to build them through exec and in this particular instance, couldn't get it to work.  
I'm keenly aware as I write these words that, these difficulties, may not be intrinsic to the problem, but fruit of  my own stupidity and ignorance.  
Which makes me second guess myself even more. What, if you knew me, would know that is a lot.  
I'm mainly writing these words in the hope that this is seen by someone that can help, or just say Hi!, but also in an effort to, through writing, get a clearer
understanding of the problem. Most of the time I navigate in a hazy dark soup of half-arsed intuitions and scraps of things I read online, and it feels like this all process needs more clarity and definition.  
Hence this blog. And these words of mine; to you.
