---
title: "Changing Storage"
date: 2021-01-27T23:17:41Z
slug: ""
description: "Where the narrator tells the story of how he was wrong, then right, then wrong again."
keywords: [mysql, sqlite, python]
draft: false
tags: [mysql, sqlite, python]
math: false
toc: true
---
There was an attempt to create a version of the notes and bookmarks apps I created,  
with great suffering I might add, in MySQL.  
I was having problems with SQLite, which I couldn't understand, now, after much
thought, feel exactly the same way.  
More on this later.  
Unfortunately I found out that the other SQL's I tried, MySQL and PostgreSQL,
have the habit of reading the code that passes through them and try to run it.  
Not caring at all that these notes are to be static repositories of my
ever-expanding knowledge, not commands to execute.  
I still don't understand if this behaviour is to be expected, or if my SQL
version has a problem in it, (or if I fucked it up somehow). At this moment,  
[2021-01-24 01:00:32],  
I have had, for all of one day, a Stack Overflow question about this issue
exactly. Up until now, no one's biting.  
Stranger still, I only saw this behaviour in the UPDATE command, not in the
INSERT command.  
For, instance, if you insert of piece of SQL code through INSERT he will
process it without a whimper. If it is a UPDATE command, it will try to
run it eagerly.  
As I said, no idea.  
But the app is there, it's built and it works. Just don't feed it SQL code.  
Well, all this forced me yo look again to the SQLite app that I was
trying to run away from,  to see if we could reach an understanding.  
When doing anything that involved actions on data already in the db, it would
complain that it had received 7 pieces of information, say, and that it had
only 6 columns, as an example,  to put it in.  
I agreed with the first part, but had strong misgivings about the second.  
I had very recently changed the db's structure (and if you're familiar with
SQLite we will know what a palaver it can be.), so I knew that the structure of
both tables were correct.  
I say tables because, in SQLite, if you're going to use full-text search,
you'll need two tables, (actually more), the one where you keep your stuff
and a virtual table that maps the content of the main one and it's used to do
the full-text searches.  
So I knew that these two tables had the same structure in terms of column number
and type. But still I checked.  
I entered SQLite and punched '.schema notes', 'notes' is the name of the main
table, and '.schema notes_fts', 'schema_fts' is the virtual table's.   
As I expected they showed the same structure; so this couldn't be the problem.
If the problem wasn't what the code message said it was, what could it be?  
I started to think that this would require an amount of SQL knowledge that I had
not, and, in all honesty, wasn't totally prepared to go get it.  
Add to this that SQLite communicates in much the same way the Sibyls did in
ancient Greece, short, ciphered and mysterious.  
So I gave up on the SQLite version and started the MySQL creation. But that you:
already know. When I got back at looking at SQLite version, I had a break-through,
if it wasn't going to tell me what I wanted to know, I could at least, look at
how its data was structured, and get my answers there.  
So I dumped the database to a csv file and had a look.  
If not the first, the second thing I thought looking at it, was that SQLite
was right. It didn't have seven columns.
For some reason, the command was given to create a table with the seven fields,
(and that is what was registered in '.schema'; the command, not the reality),  
and didn't do it.  
I probably should be worried that the db has a facultative approach to my commands,
but, in truth, I'm just happy that is a problem I can solve.
I recreated the tables and all is working now.


### UPDATE
Well, it's now,  
 [2021-01-28 01:051:43],  
 and now I know that if some of this can be
blamed on the database, the great provider of error messages, really came from the
Python connector.  
There is a great number of operations that are done quietly in
SQLite's shell, that fail miserably when piped through the connector. I tried to
understand a little better the error messages, as they sounded as improbable as as
they were irritating, but there doesn't seem to be anything googlable about Python's
SQLite module.  
Which I find odd but, in a strangely comforting way, expected, for if
rationally I know this isn't true, in my heart of hearts, I know this is done
exclusively to get on my nerves.  
Well, "Sheila, take a bow", your wish was granted!  
You would think that if someone take's something up as a hobby, this should bring him
some peace, some respite from the toils of daily living ...    
This as brought me nothing but grief.  
Even when I can finally solve whatever was wrong, I'm, by then, so emotionally depleted
that I don't find it exhilarating. It just means that I can go to bed now. Yay ...

### UPDATE
And in the day of our Lord,  
[2021-02-21 20:37:14]  
Something new has turned badly on the SQLite database.  
Now, for some unknown reason, the search function is not working. First it showed no results for notes done after the beginning of January, then, when I tried it again, it would show no results *and* open the password app. Finally it stabilized in outputting that the database disk was malformed.    
I've officially given up on SQLite, and passed my apps to MySQL, which has been, up until now, a much smoother ride.  
Maybe I'll come back later at this problem, just to understand what in the hell is going wrong. But, for now, I just want my apps working.  
Does it bothers me? Yes it does, mostly because I fear that this might be a symptom of a deeper problem in my computer. But I haven't seen any anomalous behavior in
other programs, so, for now, I'll leave well enough alone.
