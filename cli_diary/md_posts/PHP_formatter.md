---
title: PHP-formatter
mainfont: Iosevka
---

 I just finished a project where I learned a lot of new things and I
 need to put everything on paper, so I don't forget.  
 I was fiddling around with a website I'm making in PHP and noticed that,
 in regards to formatting, I had a bit of a problem.  
 There are automatic formatters for almost all languages under the sun, but
 what doesn't exist, and it's not surprising, is a formatter for
 code that is embedded in another language's file.  
 Let me be clearer, I came to PHP because I wanted to make database calls and
 automate some aspects of my toy sites. That meant, and means, that my code is
 not heavy-duty PHP. It's more a lot of HTML interspersed with the occasional
 PHP.  
 The HTML written in a PHP file, although not understood by the latter, it's
 still decoded successfully by the browser, which allows for running its code in
 HTML or PHP files. The same doesn't happen with PHP. If written in a HTML file,
 its code will be treated as comment and won't get run.  
 What this means is that you can program front/back end in PHP, but not in
 HTML, which ends up with people like yours truly, writing everything in files
 with PHP extensions.  
 Another thing that is important to mention is that HTML is ugly. It's painful
 to look at, and I, and I imagine a lot more people, have this deep desire to
 make it look less awful.  
 That's where the formatters come in. Although generally a little bossy and opinionated,
 they're nevertheless, an almost-good solution to the problem.  
 It never gets pretty, but it is much better than the starting point.  
 I found that I had no way to format the HTML I had inside PHP files, and that
 felt bad.  
 But, I thought, if I altered the extension of the file just for a little bit, I
 could use the formatter, change it back again, and the changes would already
 been done! Easy. Except that, after a cursory reflexion, it really
 isn't. It would be really cumbersome going through that process every time I wanted to format.  
 It was then that I decided to automate it.  
 Even if it took considerably longer than doing it manually.  
 As it did.  
 I also took this as an opportunity to try different cli app builders that I had
 on the backburner as something to try one day. Well, the day had come.  
 I wanted to create a class that would encompass all the steps of the process,
 which are:  

 1. Make a list of all PHP files in the current folder,  
 2. Change their extensions from '.php' to '.html',  
 3. Open the folders, write a small message and close it back again,  
 4. Get the HTML files, already formatted, and change them back to PHP.  

 The reasoning behind step 3 is this; I have my formatters running automatically
 in Vim, every time that a file is saved. So, it only takes opening and closing
 them to guarantee that the formatting is done. The message is just as an
 assurance that is really working and that an effort has been made.  
 For the cli app build, I first tried [Typer](https://typer.tiangolo.com), which
 if really cool and complete, I couldn't make it work in a Class environment.  
 The commands wouldn't work if they shared argument space with things like 'self'.
 So I tried [Fire](https://google.github.io/python-fire), and it was love at
 first site. Not only it supported classes, it was immensely more intuitive, easy
 and user-friendly. I got the idea that you can't go do all the things that you
 can with Typer, but I'm a simple man with simple needs. Fire will suffice.  
 I started by creating a folder called 'html', to put the
 files. If it's mid/large project, it can get messy real quick.  

 ~~~python
dir = os.getcwd()
        path = dir + "/" + "html"
        os.mkdir(path)
 ~~~

 Then I made a list of all the PHP extension files in the current folder, I'm
 assuming this will be opened where the content will be.  

 ~~~python
 self.php_file_list = []
        files = os.listdir(os.curdir)
        for file in files:
            if ".php" in file:
                self.php_file_list.append(file)
        return self.php_file_list
 ~~~

 Now, in the file creation step, I had to account for two possible sources of
 data: one, the user through command line commands, two, our pre-made list that
 we just seen. If no file list is supplied by the user, the PHP file list is
 used.  
 I tried to maintain the paths relative, although I loathe working with them, so
 I wouldn't have to change them each time there's another project. If this will work,
 only time will tell.  

 ~~~python
flist = self.available_php_files()
        if files:
            ficheiros = files
        else:
            ficheiros = flist

            for file in ficheiros:
                if ".php" in file:
                    src = "./" + file
                    self.dst = "html/"
                    shutil.copy(src, self.dst)
                    self.new_dir = os.listdir(self.dst)
                    for file in self.new_dir:
                        infilename = os.path.join(self.dst, file)
                        newfile = infilename.replace(".php", ".html")
                        os.rename(infilename, newfile)
 ~~~

 The next step was an interesting one. I had a loop I wanted to run through for
 every file path in the HTML folder. It would open it, write a
 message, and close it again.  
 But when I tried it, it was iterating through all entries, writing a message for each entry in each file,
 when what I needed was one message per file.  
 So to make it go just one round, I set a counter to zero, defined a while loop
 that ran only if the counter was below one. It worked pretty well.  
 I should also mention that os.listdir(some_folder) will give you a list of all
 the files in said folder. This might not be too exciting, but it's the type of
 things that I'll forget.  

 ~~~python
os.chdir(self.dst)
        self.curdir = os.getcwd()
        sourcelst = []
        for file in os.listdir(self.curdir):
            source = self.curdir + "/" + file
            sourcelst.append(source)

        def runs(file):
            with open(file, "a") as f:
                f.write("<!--This file was automatically formatted.-->")

        run_once = 0
        while run_once < 1:
            for file in sourcelst:
                runs(file)
                run_once += 1

        self.signed_files = []
        for source in sourcelst:
            self.signed_files.append(source)
 ~~~

 Now we get the HTML files, copy them to their original folder and there we
 change the extension back to '.php'.  

 ~~~python
 for file in self.signed_files:
            src = file
            new = os.path.dirname(__file__)
            shutil.copy(src, new)

        for file in os.listdir(new):
            if ".html" in file:
                infilename = os.path.join(new, file)
                newfile = infilename.replace(".html", ".php")
                os.rename(infilename, newfile)
 ~~~

 And lastly a main function that sums up all the steps.  

 ~~~python
        self.create_html_folder()
        self.available_php_files()
        self.create_files()
        self.open_write_comment()
        self.new_php()
        self.new_php
 ~~~

 With the awesomeness of Fire, most of my user interaction woes were resolved.  
 All it takes is putting a small snippet of code in the bottom of the class,
 like this:  

 ~~~python
if __name__ == "__main__":
    fire.Fire(PhpFormatter)
 ~~~

 and all the methods, objects and properties are accessible through this kind of
 syntax:  

 ~~~
 <filename> <method_name> --<properties> <arguments>
 ~~~

 All in all, a fun project.
