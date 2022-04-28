   This is a cursory presentation of a app, more a collection of scripts really,  
   that I made, so I have a source of information about all the system tools and  
   command-line apps, that so easily are forgotten.  
   It could be divided in three main components:  
   1 - Pip Querying. Where we use pip resources to check what are the installed  
       packages and their presentation.  
   2 - Yay Querying. The same, but now with Yay.  
   3 - Database Management. Python functions dedicated to interact with the database.  
   In the case of 1 and 2, both processes, start with shell scripts that automate the  
   the pip and yay shell commands. After that, there are some sed commands to clean  
   the output.  
   We house the information garnered from these sources in a folder with files for each  
   package. Then, another set of sed scripts will extract the needed information to a  
   new file, that'll have only the info needed to update the database.  
   Lastly it is only a question of reading serially these files and feeding them to the  
   database.  
   To ensure that the information gathered here won't go to waste, I set a script to open,  
   every two hours, a web page of one the entries, so I can study them a little better.  

