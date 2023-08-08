---
title: Notes App Rejuvenation
mainfont: Iosevka
fontsize: 13pt
---


I just completed some deep and interesting changes to the Notes app, that I
would like to talk to you about.  
Notes, on account of being the most used, the most taken care off, the most on
demand app I have, has suffered from an overabundance of attention.  
This made it the most likely space for experimentation and code decoration, for
spurious reasons.  
It had a lot of code that would have very little practical use, the code seemed 
to be trying new things, every three lines, and it was obvious that many things
were tried, and some of them failed.  
Lately I've been using more cli applications, and if until very recently I had
always preferred a TUI interface, anything not to memorize commands, I've
come to know, and love [Click](https://click.palletsprojects.com) framework, that taught me to trust `--help`.  
I like more and more the simplicity of stating your arguments in one fell swoop,
and the increased speed of not only time spent in task, but also in loading and
unloading. It's just a snappier alternative. And this was something that Notes
was badly needing. I created several analytical tools to study tags and posts,
that revealed themselves of no use added value; only able to create more bloat and add to
loading time. Also the code style was the most ancient in my portfolio.   

Wanting to make it much better than it was, I set about to:  

1. <h4><u>Get back to basics</u></h4>. No more analytics to satisfy idle curiosities, no more of
   momentary nice-to-have's! If it doesn't have a clear purpose, it's dead wood.  
2. <h4><u>If it can be inputted in command line mode, it's going to be implemented as
   command line</u></h4>. No more of my beloved option menus and input prompts. Now you
   memorized commands!  
3. <h4><u>Change the UI</u></h4>. Although that was one of the strongest points of the old
   version, as it was a battle tested solution, simple but very robust; I was
   very open for some change.  
4. <h4><u>Less interactions as possible per task</u></h4>. Up until now I was happy to noodle
   around with the interface, if that made the usage less taxing. I was creating
   all new pages showing available information, once, twice, thrice, as many
   times as I needed it. So I would never have to remember or learn nothing new.
   I now decided that the app should be, not difficult, but not easier than it
   needs to be.  

As I already said, I trusted Click with all data collection duties, and used
[Blessed](https://blessed.readthedocs.io/) and [Rich](https://rich.readthedocs.io) 
to present the results.  
I had some bad experiences with both some time ago; but that was more result of my inexperience, and wanting them to do something they
aren't made to do.  
Before this I'd been creating projects with [Tput](https://linux.die.net/man/1/tput),
which is a fairly low-end tool. But that simplicity made it simple to grasp and,
after you grok it, surprisingly capable. Not in the sense that I would recommend
it as a framework, but as a learning opportunity.  
Now, all things seemed simpler and easier to achieve; although that's also
because I was asking for simple things. Which helps.  
I also deleted a lot files and flattened a lot of folders, reaching a much clear
and maintainable project structure.  
