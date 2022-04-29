---
title: creator
mainfont: Iosevka
---

I've been playing around with PHP lately. As always I'm remaking old projects in
new languages and tools.  
The problem with PHP is that lulls you into a false sense of security,
everything seems familiar, easy, intuitive, and most of the time it is, but it
has its quirks, and an excessive reliance on the familiar and the known, stops
you from making progress. As I think I've done.  
I created a very simple site that creates passwords. It asks what is the length that you want on you
password, and uses a randomness library to choose the characters.  
I used numbers, letters and punctuation marks as the basis of my passwords. I
used 93 elements to combine. To manipulate it I turned it into an array, where
numbers - sequentially from 0 to 93 - are the keys of the tuple, although I
don't think that there's tuples in PHP, and the characters are the values. This
is particularly useful because the randomness modules for PHP that I found, only
deal with numbers. So the user chooses a number that is the length of his
password, the PHP module will iterate through the sequence and choose random
numbers between 0 and 93. We see what characters those number represent and
'voilá', you have a password!  
As I'm sure I already wrote about this here, I'll try not to repeat myself more
than necessary. Nevertheless, working with PHP and HTML created in me some
routines that I like to respect. I don't know how correct it is what I'm going
to say but, it is the way that seems to me more adequate to work with projects
that have a lot of back and front end work.  
As I seem to gravitate to projects that are centered on the use of databases,
that was how I first discovered PHP. And from there I created the following
habits:
1. Separate presentation from the build of the app. I use PHP files instead of
   HTML files because I can inject code to an HTML structure that only serves to
   house them. My files are very small, as all development is done in modules
   that are added via PHP inclusions. This creates simple and easy to understand
   documents, and allows me to use a HTML template that I use as scaffolding for
   most of my projects.
2. Separate the forms from the HTML and the PHP. Create their own files and
   include them as insertions, exactly like I do with the PHP code.  

I called the file that builds the passwords, "generator.php", as you'll see it
does much more than that, and if I'm very aware that that is a very bad coding
habit, the truth is that I had a lot of difficulties getting though this, so I
cut some corners.  
First I import the array of symbols that looks a bit like this:
```
    83 => '@',
    84 => '[',
    85 => ']',
    86 => '^',
    87 => '_',
    88 => '`',
    89 => '{',
    90 => '|',
    91 => '}',
    92 => '~',
```
My form was very simple, it was just a place where to input a number. I then
verify with the function [isset](https://www.php.net/manual/en/function.isset.php) if the GET variables are working. Isset verifies if a variable is declared and if it is different than null. This does not save you from problems because, as I discovered myself, if a variable is a string with 0 characters isset acknowledges that is a string, has a set size and accepts it as good. Further down a long road I discovered the function [array_key_exists](https://www.php.net/manual/en/function.array-key-exists.php), which returns true if a key is in an array. As all GET and POST methods are arrays, this helps understand if the variables are there or no.

```php
<?php require 'corrected_list.php';

if (isset($_GET['length'])) {

    $length = $_GET['length'];
```
As I alluded earlier, here we create a counter with the $i variable and set it
at 0, and while the counter count is lower than the password length, we get
key:value from the array, isolate the value and add it, loop by loop, to a new
string that'll be the password.  
```php
    while ($i++ < $length)
    {
        $pass = rand(0, 92);
        $pwd_keys[$i] = $pass;
    }

    foreach($pwd_keys as $key => $key_value)
    {
        $item = $keys[$key_value];
        while ($i++ < $length)
            $results[$i] = $item;
        $mail .= $item;
    }
```
After having isolated the new password in variable, I print it to the site.  
I also thought that it would be instructive to learn ho to work with emails in
PHP. So I decided to allow the user to get his new password in the mail. He just
has to insert a valid email and the new password is sent automatically.  
This was harder that I expected. I couldn't figure out how to make the value of
the password persist, so you can create a password and then decide if you want
to send it through mail or not. What happened was that the variable was already
gone when the later step of inserting the email came around. I then tried to
write the new password to a text file, so I could retrieve it later. But for
some reason, obviously by an error from my part, whenever I tried to read it, it
would be erased. It was obvious that I was doing something wrong, but I also
felt that my error was done earlier and it was decoupling the password creation
step from the email insertion step. If I could do it all in one go, the problems
would disappear and I wouldn't need text files to keep the password value.  
So in the form for inserting the email, I created an hidden field, identified by
a name and that would use the password variable as a value for the GET method.  
As it was integrated in the email form, when I would send it, the two pieces of
information went in tandem.  
```php
    echo "<h1 class='message'>Your New Password is:</h1>";
    echo "<h1 class='password'>$mail</h1>";
    echo "<form action='' method='get'>";
    echo "<input type='hidden' id='pwd' name='pwd' value=$mail></input>";
    echo "<input type='email' id='email' name='email' placeholder='Password in Email'></input>";
    echo "<input type='submit' value='Send'></input>";
    echo "</form>";
```
The form data was treated in the same page as I wasn't able to read
it successfully from another page. This was for the best, as this was
my objective all along. Not having to change pages through the all process.  
I created a function that first verifies if there is a GET method available, if
yes, it allocates the values of the variables to new variables, defines a sender
email, that I created earlier, when installing the mail server. Which was,
oddly, a stress-free experience and went very well. So thank God for small
mercies.  
I used PHP's mail function, using Sendmail supported by a Postfix server.  
```php
     function mailCreator() {
        if ($_GET) {
            $to = $_GET["email"];
            $from = "root@constantconstipation.club";
            $message = $_GET['pwd'];
            $subject = "New Password";
            $headers = "From: " . $from;
            mail($to,$subject,$message,$headers);
            }
            else { echo "There's nothing here."; };
        }
    mailCreator();
    }
```
I should also mention that I had an horrible time with CSS, with everything that
could go wrong, going wrong. Code that wouldn't appear in the browser or it
wouldn't accept the new changes, an hassle.  
Everyday grows my respect and admiration for the people who work with CSS on a
daily basis. It's a capricious, fickle bitch.  
Anyway, here's the homepage of the site, where most things happen:
```php
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>HP</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="Mclds">
    <meta name="description" content="Homepage">
    <link rel="stylesheet" type="text/css" href="index.css" media="screen">
</head>
<body>
    <div class="header">
        <?php include "header.php"; ?>
    </div>

    <div class="flex-container">
        <div class="column_left">
        </div>

        <div class="column_center">
            <div class="content">
                <div class="pwdform_container">
                    <?php require "pwd_form.php"; ?>
                </div>

                <div class="pwdaction">
                    <?php require "generator.php"; ?>
                </div>
            </div>
        </div>

        <div class="column-right">
        </div>
        <?php include 'footer.php'; ?>
    </div>
    <!-- https://tinyurl.com/tonwks2 -->
    <script>
    if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
    }
    </script> <!-- https://tinyurl.com/yyeckra6 -->

    <script>

    if(typeof window.history.pushState == 'function') {
        window.history.pushState({}, "Hide", "https://constantconstipation.club");
    }
    </script>
</body>
</html>
```
And here's the file with all the PHP:
```php
<?php require 'corrected_list.php';

if (isset($_GET['length'])) {

    $length = $_GET['length'];

    $i = 0;
    $pwd_keys = array();
    $results = array();
    $mail = " ";

    while ($i++ < $length)
    {
        $pass = rand(0, 92);
        $pwd_keys[$i] = $pass;
    }

    foreach($pwd_keys as $key => $key_value)
    {
        $item = $keys[$key_value];
        while ($i++ < $length)
            $results[$i] = $item;
        $mail .= $item;
    }

    echo "<h1 class='message'>Your New Password is:</h1>";
    echo "<h1 class='password'>$mail</h1>";
    echo "<form action='' method='get'>";
    echo "<input type='hidden' id='pwd' name='pwd' value=$mail></input>";
    echo "<input type='email' id='email' name='email' placeholder='Password in Email'></input>";
    echo "<input type='submit' value='Send'></input>";
    echo "</form>";

     function mailCreator() {
        if ($_GET) {
            $to = $_GET["email"];
            $from = "root@constantconstipation.club";
            $message = $_GET['pwd'];
            $subject = "New Password";
            $headers = "From: " . $from;
            mail($to,$subject,$message,$headers);
            }
            else { echo "There's nothing here."; };
        }
    mailCreator();
    }
?>
```
I almost forgot, and this is important. In the index.php file there are two
small JavaScript scripts that are very useful. One stops the PHP file from being
called every time that the page  is refreshed and the other deletes the GET
information from the pages URL, as it calls it every time there's a refresh.
