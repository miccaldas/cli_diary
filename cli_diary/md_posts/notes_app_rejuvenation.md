I just completed some deep and interesting changes to the Notes app, that I
would like to talk to you about. Notes, on account of being the most used, the
most taken care off, the most on demand, has suffered from an overabundance of
attention. This made it the most likely space for experimentation and code
decoration, of all the apps I developed. It had a lot of code that would have
very little practical use, over-engineered solutions, and all this made me more
wary of any type of streamlining intervention. For fear of not knowing what was
responsible for what.  
But lately I've been using more cli applications, and if until very recently I
had always preferred a TUI interface, anything not to memorize commands, I've
come to know, and love, the [Click](https://click.palletsprojects.com)
framework, taught me to trust '--help' for commands.  
I like more and more the simplicity of stating your arguments in one fell swoop,
and the increased speed of not only time spent in task, but also in loading and
unloading. It's just a snappier alternative. And this was something that Notes
was badly needing. I had put a plethora of tag and entries analytical tools that
revealed themselves of no added value, but to create more bloat and add to
loading time. Also the code style was the most ancient in my portfolio. I saw
code patterns of when I was still very new to this.  
Wanting to make it much better than it was, I set about to:  
1. Get back to basics. No more analytics to satisfy idle curiosities, no more of
   momentary nice-to-have's! If it didn't have a clear purpose, it's dead wood.  
2. If it can be inputted in command line mode, it's going to be implemented as
   command line! No more of my beloved option menus and input prompts. Now you
   memorized commands!  
3. Change the UI! Although that was one of the strongest points of the old
   version, as it was a battle tested solution, simple but very robust; I was
   very open for some change.  
4. As less interactions as possible per task. Up until now I was happy to noodle
   around with the interface, if that made the usage less taxing. I was creating
   all new pages showing available information, once, twice, thrice, as many
   times as I needed it. So I would never have to remember or learn nothing new.
   I now decided that the app should be, not difficult, but not easier than it
   needs to be.  

As I already said, I trusted Click with all data collection duties, and used
[Blessed](https://blessed.readthedocs.io/) and [Rich](https://rich.readthedocs.io)
to present the results. I had some bad experiences with both some time ago; but
that was more result of my inexperience and wanting them to do something they
aren't made to do.  
Before this project, I've been creating projects with [Tput](https://linux.die.net/man/1/tput),
which is a fairly low-end tool. But that simplicity made it simple to grasp and,
after you grok it, surprisingly capable. Not in the sense that I would recommend
it as a framework, but as a learning opportunity.  
Now, all things seemed simpler and easier to achieve; although that's also
because I was asking for simple things. Which helps.  
I also deleted a lot files and flattened a lot of folders, reaching a much clear
and maintainable project structure.  
