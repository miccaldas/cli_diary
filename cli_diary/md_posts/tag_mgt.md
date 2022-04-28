---
title: Notes Tag Management Project Notes
time: 03/09/2021
---


  date: 03/09/2021  
  title: The Basics  
  
  My objective now is to create a rough sketch of the macro tasks that the  
  will entail. So as I not loose track, as I so often do.  
  The idea is for the insertion of new tags and the deletion of old ones, be  
  totally automatic, having no human participation.  
  For this to happen we  need:  

  1. Know what the current tags are,  
  2. verify all newly inputed tags to see if they are not in our record,  
  3. add them to our record if they're new.  
  4. We need to know if someone updates a tag. He could have erased a tag  
     or created a new one.  
  5. We need to update the file with new content,  
  6. also we need to erase it when necessary.  
  7. Tags that have 0 connections WILL BE ELIMINATED. 
  
  #####################     
  
  Looking at this, and from the top of my head; two ideas came to me:  
  DISCARD THE FILE. It's not needed, it's the remnant of an old idea, we  
  would be much better served with a database.  
  USER GUIDANCE, when choosing the tags:  
  - Create a system to tell them if there's already tags with the same name.  
  
  #####################  
  
  Database Roadmap:  
   
    - Test if everything is OK, when we discard of what, seems, to be  
      spurious code, since we abandoned the word cloud idea.  
    - Every time that the HP would be called, it would do a database query,  
      through php, asking for all the tags. That would be what it shows.
    - Maybe is not necessary to build anything vis a vis the database.  
      Probably the 'notes' db is more than the enough. We just need:  
        tag names,  
        number of links. To know if they're dead or not.  
  
  And I think that's it for now. I'm going to start on the database, and see  
  where we go from there.  


### UPDATE:
I've been thinking a little more about it, and there's nothing we can add,  
at this moment, with these objectives, to the db, that would make any  
difference. What we have to do is create more awareness about the processes  
of the functionalities modules, that'll give us most of the information  
we need. See entry below, for more on this issue.  
  
#############################################################################  


  date: 03/09/2021   
  title: Tag Evaluation Structure  

  I'm thinking of something along these lines for the verification of the  
  tags, at the moment of adding a or updating it.  
  I think it can happen one of of three things:  

    1. The tag is new. Do nothing. The tag is already in the database,  
    our functions run from information from it. Nothing has to be updated.  
    It should output a 'The tag is new' information string.  
    
    2. The tag is known. Do nothing. All the work is done.  
    Even the number of connections is automatically taken care of by  
    the database. Output, 'The tag X ha now y connections.'  
    
    3. The tag is similar to other tags. This is more challenging.  
    I still have no idea how to do this.  
    I will take care first of linking the function modules to this new thing  
    we're doing.  

#############################################################################


  date: 04/09/2021  
  title: Connect Tag Evaluation to Functionalities Modules  

  The tag evaluation class is almost finished, I still have to add a method  
  to erase the tag if the connection number gets to 0.  
  But, at the moment it can:  

    1. Assess if the tag is new.  
    2. Send a message telling the user this.  
    3. Assess if it was already in the database.  
    3. If 3 is positive, send a message to the user, with the updated  
    connections number of tag.  
    4. Verify if the tag inserted is very much like an old tag, using a  
    library called "Fuzzywuzzy", link in the 'bkmks' app. If not, do nothing,  
    if yes, send a message to the user, suggesting him that he might want to 
    replace it.  
  
  I intend to add today, a link in the functionalities modules to the class that has all the tag evaluation methods.  
  I'm thinking that creating a simple variable with a list of the three keywords, that can then be imported to class, will be enough.  
  It'll be also necessary to insert in 'add.py', a mechanism that allows the user to see the tag suggestion done by the similarites evaluation  method.  
  Now that I think about it, this poses a problem, the class can't be, at the same time, importing from 'add.py' and exporting to it.  
  I think that the solution is to transform the evaluation function into a separate module.  

###############################################################################


  date: 07/09/2021
  title: Passed fuzzy function to 'add.py'

  Because of import issues, I did what I didn't want to do, added the fuzzy function to add.py.  
  This didn't solve anything as I am still unable to make it work, even inside the same file.  
  It needs to be debugged.  
  Another probable solution would be to turn add,py into a class. But that would certainly bring its own unknown quantity of problems.  

################################################################################


 date: 19/09/21
 title: Fuzzy function working in 'add.py'

 I, finally, made the 'Thefuzz' library, not 'fuzzywuzzy' anymore, working in 'add.py'. I should've bee using the 'process' method o f the
 library, not the default 'fuzz.ratio'. Or, at least, that is how I made it run.  
 I've still to add all the other info calls, but, truth be told, I'm kind of scared of touching it after how long it took to make it work just  for similar keywords.  

##################################################################################
