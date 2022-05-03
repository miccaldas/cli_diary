---
title: "Converting Markdown Files to HTML"
mainfont: Iosevka
---

Some days ago, when looking for static sites platforms, I encountered this [guy](https://jamstack.org/generators/vite/), who as a very simple but nifty solution for creating static sites. But if I liked that, that was nothing compared to what I liked his [site](https://git.icyphox.sh/vite/about/). I know, I know, what's there to like?, there is nothing to catch your eye, the solutions are lazy, the design slapdash, and many more things could be said about it. Mostly all bad. But when I look at it, I just see a tremendously cool site, just in the right spot between being consciously stylish, (which, despite what you might've heard), is not a bad thing in itself, or becoming a hostage of his own coolness.  
I've been looking around this type of solutions because of this blog. Trying to make my mind of what the solution is the best.  
This last week I tried [Jekyll](https://jekyllrb.com/), [Hugo](https://gohugo.io/), [Hexo](https://hexo.io/), [Pelican](https://blog.getpelican.com/) and [Middleman](https://middlemanapp.com/), although this last one shouldn't count, as I looked into it at the end of a very heavy set of days and, if I seem to remember I liked it just fine, but it didn't leave much of an impression in me.  
The one I liked the most was Hexo, followed closely by Hugo. They're simple tools, that keep to themselves and let you do your work. Although, truth be told, that wasn't what I liked the most. It might the best, but is not my favourite. That was, by a wide margin, Pelican. It's so fun to use that I saw myself looking for excuses to do more work on the blog. But the themes are horrible, the development server doesn't work correctly and ... did I already told you about the themes? Yep; not the worst I've seen, but all very utilitarian, and I want something that 'sparks joy', as they say. It's just something that you end up spending a lot of time with, and if the workspace is dull, lukewarm, bland, Microsoft Windows feel to it, I won't be doing this for much longer.   
The one I liked less, again by a wide margin, was Jekyll. In all the platforms I tried, it was relatively easy to migrate my posts from one to another. You would have to adjust for what fields each platform considered relevant to have in the front-matter, but these are details minor.  
But then there's Jekyll.  
Each post will have to have two dates, one in the file title and another in the front-matter. At least for the default theme. If you import posts that don't have this structure, the exact date format, or if he doesn't have in memory the creation of html versions for the md's you bring, he just won't render the post.  
I had to copy dates and some other info, faithfully from the example post presented, just to make it accept my posts. On top of that, the process of changing a theme, one of life's greatest joys, especially in the Jekyll platform, as they have the biggest and best choice of themes I've seen; is to say the least, byzantine. It entails deleting files in different places in the computer, find them, alter the Gemfile, updating it and even after all this I had issues changing the themes. Someone was suggesting in a forum that the best way to change a theme in Jekyll, was to push a new git branch and experiment there with the new theme.  
If you don't understand what is wrong with this mindset, we won't be seeing eye to eye many times.  
To this I would like to add, and this my considered, calculated, and much reflected position, that Ruby is a stupid language, used exclusively by poo-poo sissy-pants, that sleep with Sailor Moon pillows and who like pop more than rock.  
Please take this position very seriously. I put much thought on this and it is clear that this is a hill where I'll happily die on.  
But, as always, I digress. What i really wanted to tell was that, as I tried all these options, there was always something that rubbed me the wrong way, it could theme quality, type of information available on  the front-matter, what type of plugins there are, etc, etc.  
It soon became clear to me that, as is always and since the dawn of time, if you want something that you really like, you'll have to build it yourself.  
That is not to say that I feel that I can replace the people behind this products, in terms of polish, quality or just average hygiene. It's not that. It's just that a solution that you built, no matter how bare bones, will have always much more emotional value than any other option. At least for me.  
Some years ago, I knew quite a lot more about CSS and html than I know now. I never felt the need to refresh my know-how, basically because it's not a subject I find very interesting.  
Because of this, I was googling how to add fonts to a site, when it hit me. I already had a great template! Vite's site was great! In fact I like it so much that my first, and second instinct was to put online his site sources, and just replace his content with my own.  
But then I noticed that his site, at least the version in Github, had all content in markdown form, not html. Well, I don't know if it's possible to publish markdown directly in a site, but because I am an extremely lazy person, I just concluded that it was indeed impossible; and with that, nipped a learning opportunity right in the bud. Crisis avoided.  
So I had all this content that was in, apparently, the wrong format. What do? I do the following:
1. I imported os to manipulate files and markdown to change the format,
```python
  import os
  from os import walk
  from os import listdir
  import markdown
```
2. For some reason I couldn't get this to work with the code divided in functions, as the normal people do. I don't know what went wrong but, in the beginning, when I was trying to build this with [Sultan](https://sultan.readthedocs.io/en/latest/), a very cool alternative to subprocess, for some reason, Python would read the imports, where he would freeze in some part of the import of Sultan, and completely ignore all code inside the functions. When I took off the functions and just let the code run free, it started reading it without a problem.  
Again, someone with a more disciplined mind would've gone to the bottom of this, if for nothing else, to avoid this type of situations on later dates. But I just cogitated that, now, for magical reasons, probably something to do with the moon, it was working. And that was all good to me.  
If you read any more that one post on this blog, you already might've come across the deep disgust with which I see me doing things.  This was another of those times.  
3. got the present directory in a variable,
```python
  directory = os.getcwd()
```
4. created a list with all markdown files inside this folder,
```python
  files_md = [open(i, "rb") for i in os.listdir(directory) if i.endswith('.md')]
```
5. made another list where I kept the same information,, but now in string format,
```python
  str_files = [i for i in os.listdir(directory) if i.endswith('.md')]
```
6. created a variable that keeps the folder where I'll keep the new created html files,
```python
  path = directory + '/' + 'html_files'
```
7. created a list with markdown files in full link, because during a time, I was convinced that might be the reason why whatever it was not working then failed. It later become clear that it was not the case. But I couldn't be bothered to change it. Because that's the kind of men I am.  
```python
  full_link = []
  for i in str_files:
      a = str(directory) + '/' + i
      full_link.append(a)
```
8. And finally I took this from a digital ocean article (where would I be without them?), on how to convert markdown to html. Off course this came only after a unfruitful war with subprocess and Sultan, but it's done now and let us not speak of it ever again.  
