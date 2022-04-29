---
title: "Service Monitoring Schema"
mainfont: Iosevka
---

  I built a cli app to help me monitor my services on Celery as well as Systemd.  
  I tried for it to work as automatically as possible, because of that there are a lot of  
  files that change the structure of other files and/or request information from them.  
  Here is a rough schema of the main information flows in the app:  
  
                                   +------+  
                                   | Main |  
                                   +------+  
                                      |  
                                      |  
                                 +----------+  
                    -----------> | Dropdown |  
                    |            +----------+  
                    |                 |  
                    |                 |  
                    |          +---------------+  
             ----------------> | Dropdown Info | <----------------  
            |       |          +---------------+          |      |  
            |       |                 |                   |      |  
            |       |                 |                   |      |  
            |       |          +----------------+         |      |  
            |       |    ----- | Answer Methods | ---------      |  
            |       |    |     +----------------+                |  
            |       |    |            |                          |  
            |       |    |            |                          |  
            |       ---------- +---------------+                 |  
            |       ---------> | Make Dropdown | <---------      |  
            |       |    |     +---------------+          |      |  
            |       |    |            |                   |      |  
            |       |    |            |                   |      |  
            |       |    |     +----------------+         |      |  
            |       |    |---->| Append to Json |-----------------  
            |       |          +----------------+  
            |       |                 |  
            |       |                 |  
            |       |           +-------------+  
            ------------------  | Delete Json |  
                                +-------------+  

   In short, the information is presented in a dropdown with a list of services/functions  
   that the user can choose, to see information or perform some action on said services.  
   The services list is fed from the json file, that every module changes, every time that  
   the number or type of service is altered.  
