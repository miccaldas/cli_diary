---
title: connect-to-mysql-through-php
date: 2021-06-29 12:04:46
tags: php, pdo, mysql
---

It's been a while since I wrote on this blog.  
As per usual, I got distracted doing absolutely nothing and forgot, for months, about this page.  
In the meantime I remade its UI using the [Hexo](https://hexo.io) platform; I got bored of   
all the frontend work that entails maintaining a site built from scratch. It is a type of work that I don't respond well too. It's  
minute, detail-oriented, patient, and rewards persistence. All things that are alien to me.  
All in all, I'm happy with the result. The layout I chose answers my aesthetic needs better than I ever could. This was one case of leaving it to the pros.  
But this isn't the subject that has brought me here. I wanted to talk about connecting to a database in a web setting.  
I just installed [Nginx](https://nginx.org/en/), and was looking for some cool projects that I could do.  
I remembered that I could replicate my cli apps in a web setting. So I decided to create a page where you insert a search word and the app comes back with  
all the bookmarks that were detected for that word.  
When I started to do research on this, and by "research", I mean, trying different things to see if they work, I was amazed at the number of web tutorials that gave examples that wont compile. I don't know if its because it's old code, my inability to understand it, or for sheer ineptitude of the tutorials authors,, but the fact remains that there's a lot of iffy information out there.  
Because of this, and to speed up a possible come back at this issue on a later date, I want to document the example that, in fact, compiled.  
And here it is.  
As the page that calls the php is just html about forms, I'm going to skip it and talk only about the php script.  
1. First we keep in a variable, the query value that was sent from the question page, Where 'pwd'
is the 'name' value of the HTML tag of the 'submit' function.  
```php
$question = $_GET['pwd'];
```
2. Define your login information in variables. Note the '$pdo' variable, that uses [php-pdo](https://www.php.net/manual/en/book.pdo.php)  
encompasses all values and that is what is going to be used later. I'll just quote PHP's own documentation to explain this: 
> Connections are established by creating instances of the PDO base class. It doesn't matter which  
> driver you want to use; you always use the PDO class name. The constructor accepts parameters  
> for specifying the database source (known as the DSN) and optionally for the username and  
> password (if any).  
```php
$where = "localhost";
$user = "root";
$password = "xxxx";
$dbname = "pwd";
$pdo = new PDO("mysql:host=$where;dbname=$dbname", $user, $password);
```
3. This I don't have no idea what it does or what is doing here. I'll leave it for magical thinking
reasons.  
```php
$a=1;
```
4. We create a variable that'll deal with the preparation of sending the SQL query.
```php
 $stmt = $pdo->prepare("SELECT site, username, comment, passwd FROM pwd WHERE MATCH(site, username, \
 comment) AGAINST ('$question' IN NATURAL LANGUAGE MODE)");
```
5. This executes the prepared statement.  
```php
$stmt->execute();
```
6. This returns an array with all the results.  
```php
$users = $stmt->fetchAll()
```
7. Once again, I cede the stage to PHP's documentation:
> The foreach construct provides an easy way to iterate over arrays. foreach works only on arrays and
> objects, and will issue an error when you try to use it on a variable with a different data type
> or an uninitialized variable.
```php
 foreach($users as $user) 
```
8. This final part is a bit of mash with html, as I had to insert tags to style the output. What is  
relevant to know is that each line echo's a entry of the mysql output.  
```php
<p><div class="title"><?php echo "   SITE - "; echo $user["site"]; ?><br>
<?php echo "  USER -  "; echo $user["username"]; ?><br>
<?php echo "    COMMENT - "; echo $user["comment"]; ?><br>
<?php echo "   PASSWORD - "; echo $user["passwd"]; ?></p></div><br>
```

And now the whole code:
```php
<?php

            $question = $_GET['pwd'];

            $where = "localhost";
            $user = "root";
            $password = "xxxx";
            $dbname = "pwd";
            $pdo = new PDO("mysql:host=$where;dbname=$dbname", $user, $password);    

            $a=1;
            $stmt = $pdo->prepare("SELECT site, username, comment, passwd FROM pwd WHERE MATCH(site, username, comment) AGAINST ('$question' IN NATURAL LANGUAGE MODE)");
            $stmt->execute();
            $users = $stmt->fetchAll();
            foreach($users as $user) 
        {  
?>
<p><div class="title"><?php echo "   SITE - "; echo $user["site"]; ?><br>
<?php echo "  USER -  "; echo $user["username"]; ?><br>
<?php echo "    COMMENT - "; echo $user["comment"]; ?><br>
<?php echo "   PASSWORD - "; echo $user["passwd"]; ?></p></div><br>
<br>
<br>
<?php } ?>
```
