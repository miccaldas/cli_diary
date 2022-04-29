---
title: web-apps-structural-reasoning
mainfont: Iosevka
---

While doing the web apps projects, I realized that I, fortuitously, had come upon a template for web setups.  
In the very beginning of these projects, I was still trying to understand what would be the substitute of Python in the web world; as the tools I knew, cursorily, HTML and CSS, didn't do what I needed.  
I then discovered PHP, that uncool, unhip, language that I grew to love.  
I was also positively impressed by how easy I could port my knowledge of Python and its syntax to this new language. So it was very much love at first site, in a inversely proportional relationship with JavaScript. Which I maintain is not a language, but the world's most elaborated practical joke.  
As my use of PHP continued, some patterns started to emerge.  
1. Database Calls. Their structure is almost always the same. They may differ if the call has something to show or not; but the need to create:
    - a form to interact with the database,
    - a action page to host the PHP code, proper,
    - a page where this items would be injected through "request" tags,
    - and finally, one CSS file to rule them all.  

So, at the moment, the template structure is this:
<br>
<br>


| Project Folder|

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      +--------------| CSS | 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > index.css
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                    
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|     +-------------------| ACTIONS |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|     |                
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > search_action.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > add_action.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > delete_action.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > see-all.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      +------------------| PAGES |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      | 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > search_page.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > add_page.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > delete_page.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > see-all.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                    
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|     +-------------------| FORMS |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|     | 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > search_form
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > add_form
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > delete_form
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                        +-- > see-all_form
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|       
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                    
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      +------------------| PAGES |                      
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|      | 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                         +-- > search.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                         |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                         +-- > add.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                         |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                         +-- > delete.php
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                         |
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|                         +---> see-all.php
