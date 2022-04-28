---
title: More tales about search
date: 2021-06-23 08:44:00
tags: search, python, blog
---

There were developments regarding the blog's search.  
I wasn't very happy with my first stab at implementing a search function.  
If you recall, I used a database to collect metadata about the posts and then sourced it with PHP's PDO.  
The problem was that the example that I copied, presented the data in table. Something I didn't like.  
Add to that the fact that there was a considerable part of that code that I didn't understand, and all that made me think I needed another solution.  
I wanted to show the title of the posts, as a link, and a small description. Interestingly I found out that doing exactly what I wanted, is much simpler and had the added benefit of allowing me to grok a lot more about PDO's functionalities.   
I start by collecting the user's search choice:  
```php
$question = $_GET['quest'];
```
defining the login information,
```php
try {
  $where = "localhost";
  $user = "root";
  $password = "xxxx";
  $dbname = "dazed";
```
defining the login object,
```php
$pdo = new PDO("mysql:host=$where;dbname=$dbname", $user, $password);
```
defining the query,
```php
$sql = "SELECT title, link, description FROM dazed WHERE \
MATCH(title, author, description, tags, categories)\
AGAINST ('$question' IN NATURAL LANGUAGE MODE)";
```
connecting,
```php
$q = $pdo->query($sql);
```
this defines how the information is gotten. Fetching associatively downloads the query plus their column name, as keys,
```php
 $q->setFetchMode(PDO::FETCH_ASSOC);
  }
  ```
  defining what to output in case of error,
  ```php
  catch(PDOException $e) {
     echo "Error: " . $e->getMessage();
  }
?>
```
in other tags, we'll define how the information will be outputted. This means that, row for row, we should get the data from the columns link and title
and print it as a link. The latter with '[]' around the information.  
```php
<?php while ($row = $q->fetch()): ?>
<a href="<?php echo ($row['link']); ?>"><?php echo '['; ?><?php echo ($row['title']); ?><?php echo ']'; ?></a>
```
finally get the description column value and close the 'while' loop.
```php
<h6><?php echo ($row['description']); ?></h6>
<?php endwhile; ?>
```
  
  
And this is the complete code:
```php
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>search_list</title>
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
<script src="https://corteousquestions.club/libraries/w3.js"></script>
<link href="search_list.css" rel="stylesheet">
</head>
<body>
<div class="grid-container">
 <div class="content-wrap">
 <div class="col_center">
<?php
$question = $_GET['quest'];

try {
  $where = "localhost";
  $user = "root";
  $password = "xxxx";
  $dbname = "dazed";
  $pdo = new PDO("mysql:host=$where;dbname=$dbname", $user, $password);
  $sql = "SELECT title, link, description FROM dazed WHERE MATCH(title, author, description, tags, categories) AGAINST ('$question' IN NATURAL LANGUAGE MODE)";
  $q = $pdo->query($sql);
  $q->setFetchMode(PDO::FETCH_ASSOC);
  } catch(PDOException $e) {
     echo "Error: " . $e->getMessage();
  }
?>
<?php while ($row = $q->fetch()): ?>
<a href="<?php echo ($row['link']); ?>"><?php echo '['; ?><?php echo ($row['title']); ?><?php echo ']'; ?></a>
<h6><?php echo ($row['description']); ?></h6>
<?php endwhile; ?>
</div>
</div>
</div>
<div w3-include-html="https://corteousquestions.club/partials/footer_pages.html">
<script>w3.includeHTML();</script>
</body>
</html>
```
