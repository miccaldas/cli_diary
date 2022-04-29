---
title: Footer
mainfont: Iosevka
---

I've been struggling with a web problem that, seen by the amount of google entries with similar situations, is very common.  
To wit, how to anchor a footer to the end of the page?  
You  can't define a fixed height, because the content will grow or shrink, which might leave the footer on the middle of the page or, worst, in the very beginning.
The last one happened to me, and I'm still trying to understand how did I accomplish such feat.  
I thought that there would be a fairly standard answer to this query, since there's a multitude of footers in a immensity of sites, all behaving as they should.
But it is not exactly the case. For one, there is a plurality of answers, each with a different method, and all, with varying degrees of sophistication.
In the beginning I tried the ones that were tied to CSS structures, such as [Flexbox](https://www.w3schools.com/css/css3_flexbox.asp) or [Grid](https://www.w3schools.com/css/css_grid.asp) but, as I wrote in the last post, these, I discovered, are a little harder to master than I anticipated. As we speak, I still haven't been able to get one to work as it should.  
Not just work, mind you, that at least, I was capable to achieve, but to work in the way that they're supposed to.  
I'm very, very new at this, so having to check on W3 for every little detail on how to do everything, and trying to implement a layout that presupposes from its user some degree of experience, has proven, thus far, more than I can handle.  
But, worry not. I know that is only a matter of time and persistence until everything comes together. Just not now.  
For these reasons, I was in the market for a simple solution. Something independent of fancy layouts, and that could be implemented by someone of my enormous level of ignorance.  
I found [this](https://www.freecodecamp.org/news/how-to-keep-your-footer-where-it-belongs-59c6aa05c59c/), and it worked.  
Below goes a explanation of my implementation for this blog.  
--------------------------------------------------------------------------------------

## The HTML
  
As per the instructions, I created a div that would contain all the other items present in page.
```html
<div class="grid-container">
```
It's minimum height is set at 100% of the visible screen, (which is called viewport; I know that now.), And it's position is relative.
The position property, something I'm not sure I understand completely,
> sets how an element is positioned in a document.
Writes the [Mozilla Developer Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/position), unhelpfully.  
So I'm just going to explain it in my own words. Which if it has the clear possibility of being misleading or just flat out wrong; will give me the opportunity to think through this.  
There are the following types of positioning:  
1. Static. The default. It stays where you put it and obeys the normal flow of the document. Put it in another way, it stays exactly where you put it.  
2. Relative. The element is positioned in relation with a former position it had. Simply put, if its position was x=80px and y=40px, and if is new position is, for instance, "top: 20px", the element would moved down 20 px down to a position in x=80px/y=20px.  
3. Absolute. By default it is the top left corner, completely out of the flow. You then define 'top' and 'left' to locate it.  
4. Fixed. Same as the absolute position, but relative, always to the html element. Fixed elements are not affected by scrolling and are always on screen.  
I think that the position has to be relative so other elements can use it as a reference, since static elements can not.  
5. Then I set another div `<div class="content-wrap">` called content wrap, that has a bottom padding value equal to the height of the footer.  
6. The footer is positioned as absolute, with the value '0' in `bottom`, assuring that it stays in the end of the page. It's position will be relative to the grid-container, and go up and down as there is less or more content.
This is my html:
  
```html
<!DOCTYPE html>
<head>
<title>indice</title>
<meta charset="utf-8" />
<style>
</style>
<link rel="stylesheet" href="index.css">
<link rel="preconnect" href="https://fonts.gstatic.com">                                                                                                                <link href="https://fonts.googleapis.com/css2?family=Diplomata+SC&family=Roboto+Condensed:ital@1&display=swap" rel="stylesheet">
</head>
<body>
<div class="grid-container">
<div class="content-wrap">
 <div class="posts">
<a href="https://corteousquestions.club/posts/proj.html">[1]</a></br>
<a href="https://corteousquestions.club/posts/triggers.html">[2]</a></br>
<a href="https://corteousquestions.club/posts/storage.html">[3]</a></br>
<a href="https://corteousquestions.club/posts/have_problem.html">[4]</a></br>
<a href="https://corteousquestions.club/posts/problem2.html">[5]</a></br>
<a href="https://corteousquestions.club/posts/epilogue.html">[6]</a></br>
<a href="https://corteousquestions.club/posts/music.html">[7]</a></br>
<a href="https://corteousquestions.club/posts/music2.html">[8]</a></br>
<a href="https://corteousquestions.club/posts/rss.html">[9]</a></br>
<a href="https://corteousquestions.club/posts/hugo.html">[10]</a></br>
<a href="https://corteousquestions.club/posts/md.html">[11]</a></br>
<a href="https://corteousquestions.club/posts/rss2.html">[12]<a></br>
<a href="https://corteousquestions.club/posts/auto.html">[13]<a></br>
<a href="https://corteousquestions.club/posts/14_blog_search.html">[14]<a></br>
</div>
</div>
<div class="footer"><a href='http://minegit.club/root'>gitea</a><span>   </span><a href="mailto:mclds@protonmail.com">mail</a><span>   </span><a href="pages/about_us.html">about</a><span>   </span><a href="pages/gpg.txt">gpg</a><span>   </span><a href='https://corteousquestions.club/pages/comments.html'>comments</a><span>   </span><a href="pages/search.html">search</a></div>
</div>
</body>
</html>
```
-----------------------------------------------------------------------------------------

## The CSS
For my CSS file, I have the following values:
1. For the grid-container, I gave it `margin: 0` and `padding: 0`, to guarantee that it occupies all of the viewbox. If this is not there, a lot of times we use a background that does not occupy the totality of the screen visible area.  
The position is relative, because of the reasons previously exposed, and `min-height: 100vh` guarantees that it fills the height of the document. 'Vh' is a measurement that is 1% of the height of the viewport.  
```
.grid-container {
	margin: 0;
	padding: 0;
	position: relative;
	min-height: 100vh;
}
```
  
2. 'Posts' is the div where all the content will be housed. I aligned the text to the center so it is in the middle of the screen, and gave it a 300px top padding, so as to be vertically centered. More or less.  
```
.posts {
	padding-top: 300px;
	font-size: 45px;
	text-align: center;
}
```
  
3. The content-wrap was defined as 2.5rem. Rem being a measurement relative to the font size of the root element. In most browsers is a value around 16px.
```
.content-wrap {
	padding-bottom: 2.5rem;
}
```
  
4. The footer has a absolute position and bottom 0, as discussed. Added the centered text alignment to have it in the middle of the page.
```
.footer {
	position: absolute;
	bottom: 0;
	width: 100%;
	height: 2.5rem;
	text-align: center;
}
```
  
5. And here are my link definitions for the site; that makes them half invisible, but that's how I liked them.
```
/* unvisited link */
a:link { color: #dbe2f1; }

/* visited link */
a:visited { color: #dbe2f1; }

/* mouse over link */
a:hover { color: #bbbbbb; }

/* selected link */
a:active { color: #cccccc; }
```
  
6. And, finally, just something I have in all my CSS'. A trick to create space in html.
```
 span + span {                                                                                                                                                          	margin-left: 10px;
 }
 ```

