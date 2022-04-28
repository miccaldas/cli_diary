---
title: URL shortener
date: 2021-06-23 08:24:00
tags: url shortener, python, url
---


If I think of the things I use on a daily basis, I believe that I created a python, homemade version of almost everything.  
Things like notes, password manager, music player and assorted small things.  
The one thing I lacked was a URL shortener that, if not a necessity, is something I find myself using frequently.  
I was using [twzer](https://github.com/ngevan/twzer), a cli URL shortener that works so well that I didn't have any interest in creating alternatives. And now that I have created it, twzer still shines as the best option.  
But this one is mine, I made it. So it's this that I am going to use.  
In the imports you'll see a mention from __future__, that I imagine is a python2 library. That means that I probably don't need it in this code, but I'm feeling too lazy to test if this is correct. Let the fossil code stay.  
[Contextlib](https://docs.python.org/3/library/contextlib.html) is a library that provides utilities for the with statement.  
[Urllib.parse](https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse) is necessary to escape the URL, [Urllib.request](https://docs.python.org/3/library/urllib.request.html), is a library to open URLs.  
Colr, is the usual pretiffier.  
  
```python
from __future__ import with_statement
import contextlib
from urllib.parse import urlencode
from urllib.request import urlopen
from colr import color
```
  
We define the function to shorten the URL:
```python
def make_shorten(url):
```
  
we append the escaped URL to the end of tinyurl’s api URL. Then we open the request_url using urlopen.
```python
request_url = ('http://tinyurl.com/api-create.php?' +
                   urlencode({'url': url}))
    with contextlib.closing(urlopen(request_url)) as response:
```
  
The urlopen function returns a stream of bytes rather than a string, so in order to print it and alter it, we have to convert it into utf-8.
```python
return response.read().decode('utf-8')
```
  
Finally all that remains to be done is presentation:
```python
url = input(color('What is your url? ', fore='#f37735'))
url_short = make_shorten(url)
print(color('+------------------------------+', fore='#f7d0cb'))
print(color('| ', fore='#f7d0cb') + color(url_short, fore='#f37735') + color(' |', fore='#f7d0cb'))
print(color('+------------------------------+', fore='#f7d0cb'))
```
  
And that's it.
