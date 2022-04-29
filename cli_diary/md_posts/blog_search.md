---
title: Blog Search
mainfont: Iosevka
---

Lately I've been mostly playing with this blog.  
I've tried several designs, always a compromise between what I want to do and what I can do, to see if I can find a look that invites me to write.
In the absence of a clear and quantifiable goal for this blog, my measure of success has got to be something a little more diaphanous, in my case, a layout that makes me want to write in it.  
That always been the difference between long-lived or ephemeral sites that I have had. If it is a design I like, I'll write much more.  
If you're reading this, it'll be obvious to you that I went with a minimalist theme. It was not my first or second choice, but it was clearly the one I felt happier with, given my precarious capacities as a web developer.  
It is, and probably will be for a long time to come, a work in progress.  
For instance, I still can't design a CSS grid for the theme. I tried it, twice, and ended with monstrous atrocities that I had to kill at birth.  
I haven't given up yet. Just regrouping.  
For now, the blog looks, approximately as I would like it to look, but the html and CSS behind it are a mess. And that is coming from me, who's got no great knowledge of the subject and is easily satisfied.  
My goal for this particular endeavour would be to have a solid scaffolding for the blog, based in one recognized CSS method. Could be grid, could be Flexbox. Something standard.  
But clearly, this is something for a later date.  
In what I had, surprisingly, much more success with, was with the backend features of the blog.  
I created a MySQL database to house the metadata for the posts published here, and I was trying to find a way to use it as a search tool.  
I had no idea of how I could do this, until I found the [W3](https://www.w3schools.com/php/php_mysql_select.asp) PHP tutorial, especially the part about mysql.
What got me right away was how intelligible PHP was. It just felt like something that would not be hard to pick up. So much so that, when looking at how it connects to a MySQL database, I was impressed by how similar to python code it was.  
I was able, with the help of the tutorial, to create a page in the blog where you write your search query, and get a table with results from the db.  
Although, in the interest of full disclosure, the table presentation was not my idea. It was in the tutorial, and I didn't felt (feel), comfortable enough to make any changes.
Here's what I ended up using:
  
1. I used a post template of the blog to house the php code. Although I think that wouldn't, in the end, matter very much.  
That is why you'll see here a header and 'col.center' div's, as well as links to stylesheets that were never used.
```html
<!DOCTYPE html>
<html>
<div class="header" style="height:500px;"></div>
<div class=col.center>
<div class="highlight" style="font-family:'Roboto Condensed, sans-serif';">
<link rel="preconnect" href="https://fonts.gstatic.com">                                                                                                                <link href="https://fonts.googleapis.com/css2?family=Inconsolata&family=JetBrains+Mono:ital,wght@1,500&display=swap" rel="stylesheet">
```
  
2. Then, as always, I took a detour trying to style php code with CSS. For that mission I found this [article](https://css-tricks.com/css-variables-with-php/), that purported to explain how to do just that. But I was just too dense to understand it. Anyway, here lies the link to CSS stylesheet, and the latter link; in case that anyone smarter than me can make heads or tails of it.
```html
<link rel="stylesheet" type='text/css' href='style.php' />
```
  
3. I created a page with a search query, where I get the question and send it to another php page for processing. Now with the benefit of hindsight, it's clear to me that I didn't had to do it like this. So much so, that, in the end, I end up sending the output back to this page. But at the time I was just trying to make it work by following carefully the examples. But because it worked at first try I just couldn't be bothered to refine it, and left it as is. At least for now.
```html
<form action="/pages/action_page.php">
  <label for="quest">SEARCH: </label>
  <input type="text" id="quest" name="quest"><br><br>
  <input type="submit" value="Submit">
```
  
4. In the other page, I open a php tag, get the result of the search query and keep it in a variable.
```html
  <?php
  $question =  $_GET['quest'];
```
  
5. Below goes the styling for the table of results, as well as the format for its header. I fought tooth and nail to get these stylings to a CSS file, but I'm
totally out of my depth here, and couldn't make it work. So I stuck with the tutorial example and added one or two personal touches.
```html
echo "<table style='border: solid 5px black; border-collapse: collapse; border-radius: 35px; font-family:Roboto Condensed, sans-serif;'>";
  echo "<tr><th>title</th><th>author</th><th>description</th><th>tags</th><th>categories</th></tr>";
```
  
6. A class is opened where we'll define an iterator, more table stylings and it's structure. I wish I could be more in depth in this commentary, but the guide was scant in details and I haven't done my due diligence yet.
```php
 class TableRows extends RecursiveIteratorIterator {
      function __construct($it) {
          parent::__construct($it, self::LEAVES_ONLY);
    }

    function current() {
        return "<td style='width:500px;border:5px solid black; text-align: center; padding: 15px; border-radius: 35px;'>" .
  parent::current(). "</td>";
    }

    function beginChildren() {
        echo "<tr>";
    }

    function endChildren() {
        echo "</tr>" . "\n";
    }
  }
```
  
7. We then add the login information for the database,
```
  $where = "localhost";
  $user = "root";
  $password = "xxxx";
```
  
8. and connect to it. Again, this code is very similar to the one in Python.
```php
  try {
  	$conn = new PDO("mysql:host=$where;dbname=dazed", $user, $password);
  	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $stmt = $conn->prepare("SELECT title, author, description, tags, categories FROM dazed WHERE MATCH(title, author, description, tags, categories)
                           AGAINST ('$question' IN NATURAL LANGUAGE MODE)");
    $stmt->execute();
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach(new TableRows(new RecursiveArrayIterator($stmt->fetchAll())) as $k=>$v) {
        echo $v;
    }
  }
  	catch(PDOException $e) {
  	echo "Connection failed: " . $e->getMessage();
  }
  $conn = null;
  echo  "</table>";
  ?>
```

