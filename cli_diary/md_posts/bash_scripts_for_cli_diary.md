---
title:
mainfont: Iosevka
---

When I started the cli diary project I didn't have very clear ideas about what I
was going to do. Because of this, there were a lot of things I did that ended up
in the bin.  
But, although they don't make part of the finished product, I still learned some
interesting things doing them.  
Case in point, because I wanted to access the Python blog posts through the
diary, I needed to bulk collect and rename the files. I thought best to work from
the html files directly, but the way they were stored by Hexo is by giving the
title of the post to the folder housing the html file and name them all 'index.html'.  
So I needed to name the files proper.  
To do this I built the following script:  

```bash
collection=/home/mic/python/cli_diary/cli_diary/blog_posts/collection/*
```
This is where I stored all the html files. For ease of use I turned it to a
variable. Note the use of '*' at the end of the link. That tells the shell that
we are referencing the files within the folder and not the folder itself.

```bash
for file in ${collection}; do
    name=$(sed -n -r "s/^.*<p class=\"post-title\">(.*)<\x2fp><\x2fh2>.*$/\1/p1" ${file})
```
Here we iterate through the html files and create a variable from a Sed command.  
To create a variable from a command in bash, you envelop the command with
`$(...)`.  
The post title was defined inside the file as a tag with the class 'post-title',
I needed to retrieve its value.  
This is what the command does:
1. `^.*<p class=\*post-title\*>` indicates everything from the beginning of a
   line to the p tag. The '"' needed to be escaped.  
2. `(.*)` defines a group of characters beginning after the content of point 1
   up to ...
3. this expression, `<\x2fp><\x2fh2>.*$/`, where `\x2f` is a hex code for "/",
   and it also needed to be escaped.  
4. `\1` defines the selection as the group from the previous expression.  
5. `p1` tells Sed to print the first occurrence of the selection.  
6. `${file}` defines that the text to be analyzed is the current iterated file.  

```bash
echo "$name"
```
Here we print the result of the 'name' variable.

```bash
dash=$(echo "$name" | sed -re "s/ /_/g" | tr [:upper:] [:lower:])
```
The 'dash' variable will define the new titles by piping the printed 'name'
variable to Sed that will replace all spaces in 'name' by '_'. Finally the
result of the Sed command will be piped to tr, that will convert uppercase
characters to lowercase.  

```bash
echo "$dash"
```
Here we print the result of the 'dash' variable.

```bash
cp -r ${file} new_titles/"$dash".html
```
Finally we copy the content of the file to a new folder called 'new_titles',
with the variable 'dash' concatenated with '.html' as title.  

As the post files were all in their individual folders, encased in other folders
that divided by month, it was needed to concentrate them in one folder, for ease
of use.  
For that I used the following script:

```bash
find /home/mic/python/cli_diary/cli_diary/blog_posts/2021 -type f -exec cp --backup=numbered -t /home/mic/python/cli_diary/cli_diary/blog_posts/collection {} +
```
First we define where to start the search. `find` will search inside all
subfolders.  
`-type f` defines that the objective is files only.  
`exec cp` executes the copy command.  
`--backup=numbered` defines how it'll name the new files.  
`-t` defines the destination folder.  
`{} +`, I have no idea what it does.
