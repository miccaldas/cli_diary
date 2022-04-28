---
title: "Sqlite Triggers"
date: 2021-01-28T19:50:33Z
slug: ""
description: "How to create triggers fro sqlite3"
keywords: [sqlite, trigger, triggers]
draft: false
tags: [sqlite, triggers]
math: false
toc: false
---

When creating FTS5 tables in SQLite, one of the thing I tended
to forget was what triggers should I create and what's the
syntax to do that.  
In short, I learned nothing from all the other times I created
triggers, nothing stuck in my memory, I remembered nothing.  
Now I understand the look teachers would give me in school.  
It's how I presently look at myself. A mix of exasperation and
dismay.  
Since the function of the trigger is to react to some alteration
in the table, I think that triggers for:   
1. after a insertion on the table,  
2. after a deletion on the the table,    
3. after an update on the table,  

are enough to cover all the bases.  
Here are the examples with their syntax:  

```CREATE TRIGGER aft_insert AFTER INSERT ON pwd  
BEGIN  
INSERT INTO pwd_fts(pwdid, site, username, passwd, comment, time)  
VALUES(new.pwdid, new.site, new.username, new.passwd, new.comment,
       new.time);  
END;  

CREATE TRIGGER aft_del AFTER DELETE ON pwd  
BEGIN  
INSERT INTO pwd_fts(pwdid, site, username, passwd, comment, time)  
VALUES ('delete', old.pwdid, old.site, old.username, old.passwd,
        old.comment, old.time);  
END;  

 CREATE TRIGGER aft_updt AFTER UPDATE ON pwd  
 BEGIN  
 INSERT INTO pwd_fts(pwdid, site, username, passwd, comment, time)  
 VALUES ('delete', old.pwdid, old.site, old.username, old.passwd,
         old.comment, old.time);  
 INSERT INTO pwd_fts(pwdid, site, username, passwd, comment, time)  
 VALUES(new.pwdid, new.site, new.username, new.passwd, new.comment,  
        new.time);  
 END;```


