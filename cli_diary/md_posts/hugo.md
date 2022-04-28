---
title: "Uploading to a Hugo Blog"
date: 2021-01-28T20:23:01Z
tags: hugo, blog, scripts
---

This blog has put me in front of some new challenges.  
Well, not really challenges, minor nuisances, in the great big scheme of things ... Trifles ... puerile pursuits really.  
So, [Hugo](<https://gohugo.io>) the web platform that powers this blog, is web-server agnostic. Much due to the fact that it's serving static files. So this entails that content production has, more or less, the following workflow: you write what you have to write, put the photos or images that you want in your post and all is right, proper and ready to go.  
When done, you write `hugo`, just like that, and it will update all the files, creating a folder named  'public', where all the new HTML is, ready to be used. What you do with it, it's totally up to you.  
Want to send it through Apache, Nginx? be my guest. Want to send it to Heroku? It just so happens we have an integration for it!  
Since I only worked with personal blogs or sites, and because no one told me what the best-practices were, and if they did, I didn't get it, I always worked in the server. I would download all the tools I needed for the site, and did all work from there. I'm a big of command line so, this helped a bit. Whenever
something must be done with a GUI tool, editing an image for example, I would work locally and upload it with [sftp](https://en.wikipedia.org/wiki/Secure_file_transfer_program). Which is a wonderful tool, by the way.  
So I never had a mental image of the web framework as a separate entity from the
web-server. Also, and this must the real reason,, through sheer incompetence, generally I would have an horrible time trying to setup these frameworks.  
I could never put the web-server working correctly. It could be that the ssl wouldn't recognize all pages as part of the site, or the homepage was the only one to
be served, or a myriad other things, I felt, I had no knowledge or control.  
So I thought, (brilliantly, I know), that if I downloaded the programs to the server folder, it would be already in a place where it should be, I pondered, and would make the whole process a lot simpler. I concluded.  
For some fortuitous reason, probably better explained by the alignment of the stars, or the protection of a beneficent deity, I got one of these frameworks working.So mired in retrospective determinism was I that I assumed that my guess was right, that you should download, build and manage the framework from the web-site folder. Needless to say that all my folders were exposed on the internet, and open to attack, because, why shouldn't they? If you're going half-ass a project, aim for
the stars I say.  
There's no more eloquent statement of how perfunctory is the interest of other people in what I have to say, than the fact that I had this sad state of affairs
exposed for a year or more on the web, and no one seemed interested in taking advantage of this marvelous opportunity for mischief. So I never questioned this empirical truth for years,  
until the fact that I wasn't succeeding in installing [hexo](https://hexo.io/), (through no fault of hexo's, I 
understood after), made me try to set up the development part in my computer. Just so I could follow the setup instructions to the letter.  
This led me to awesome conclusion that web content and web serving are two different things, never again to be confused.  
So, you have a 'public folder' with all your new shiny HTML, what do you need to do?  
You need to, in the root folder of your blog project, write the following:  
<pre><code> 
   sftp username@hostname
   cd /path/to/server/web-server/folder
   put -r public
   chown -R www-data:www-data public
   bye
</code></pre>
   
The `chown` command is there because every time that there's an upload, the files come with my user, and I need the files to be in the server's user (www-data), so it can access the data.  
There's also the fact that ownership changing in sftp, requires userid and grpid, it won't accept a name.  
And if that's the kind of information you can conjure up on your mind at command; you're a better man that I.  
This process was ripe for automation, I thought, so I started working.  
For the sake of debugging and what interpreter to use, I partitioned the commands in two parts, one to upload the files, the other to change the file's ownership. Finally I created a third to call the other two in sequence.  
The first I called it `send_hugo.sh`:  
 
<pre><code>  
 #!/usr/bin/env zsh

 rsync  -av  --delete -e  'ssh -i /home/mic/.ssh/id_rsa' /home/mic/dazed/public \
 root@45.76.37.62:/var/www/constantconstipation.club/html/ \
 > /home/mic/cronlogs/hugo.log 2>&
</code></pre>
 
In truth I'm not replacing the files, what I am doing is syncing the development version with the production version. This way only what is changed is sent to the server.  
Note that I sent all output to a 'hugo.log' file, so I can know what fresh hell have I dragged myself this time.  
The second is called `permissions_hugo.sh`:

```python
 #!/usr/bin/env python
 from fabric import Connection

 c = Connection(
    host = 'constantconstipation.club',
    user = 'root',
    connect_kwargs={
        'key_filename': '/home/mic/.ssh/id_rsa'
    }
 )

 c .run('cd /var/www/constantconstipation.club/html/ && chown -R \
 www-data:www-data public')
```

This script uses a Python tool called [fabric](https://docs.fabfile.org/en/2.6/index.html), that allows to send commands to the server from your local computer. It can also send files to the server, but it can't pass folders recursively. That is another reason why I split the script in two parts. One is best run as the shell and the other as python. Off course I could have made it all in Python, by using [subprocess](https://docs.python.org/3/library/subprocess.html) in the first part.  
But laziness prevailed, and I stuck with what was easier.  
Finally, I created an alias in .zshrc for the script that calls the other two in sequence, and now I can do the uploading and ownership setting just by writing `upld` in the shell.  
You're probably a worldlier person than I, and may not be very impressed by this setup, but me, having done so little with my life, and understood even less, think it's pretty nifty.  
