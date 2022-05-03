---
title: "Cli Apps Pip Presentation"
date: 02/05/2022
mainfont: Iosevka
---

This is a cursory presentation of a app, more a collection of scripts really, that I made, so I have a source of information about all the system tools and
command-line apps, that so easily are forgotten.  
It could be divided in two main components:  
1 - Pip Querying. Where we use pip resources to check what are the installed packages and their presentation.  
2 - Yay Querying. The same, but now with Yay.  
We'll be using the pip version as example, as they're both pretty similar.  
This is the app's structure:  
  
![](/home/mic/python/cli_apps/cli_apps/workflow.png)
  
The process begins by appending to the last created list of app names a prefix
of 'old_', this will allow us to create a new list that'll use to compare their
contents, and just use as input, apps that are not in the database.  

<h3>initiation_scripts.sh</h3>
In 'initiation_scripts.sh' we input a pip command that outputs all
installed pip apps in the system, and send it to a file.  
As the output comes with information about the version that we don't need, we
use Sed to isolate just the names and send them to another file.  

```bash
 pip list --format freeze > /home/mic/python/cli_apps/cli_apps/lists/first_pip.txt
 sed -nre 's/(^.*)==(.*$)/\1/p' /home/mic/python/cli_apps/cli_apps/lists/first_pip.txt > /home/mic/python/cli_apps/cli_apps/lists/names_linux.txt
```

<h3>query_builder.py</h3>
We create two variables with the paths to the files with the old and new lists
of installed apps:

```python
      cwd = os.getcwd()
      name_path = f"{cwd}/lists/names_linux.txt"
      old_name_path = f"{cwd}/lists/old_names_linux.txt"
```

open the files and read them:

```python
      with open(name_path, "r") as f:
          names = f.readlines()
  
      with open(old_name_path, "r") as f:
          old_names = f.readlines()
```

remove the line break symbols:

```python
      clean = [i.strip() for i in names]
      old_clean = [v.strip() for v in old_names]
```

and if an entry in the new list is not in the old, we extract the information
about the package through a pip command, and keep the result in separated files.  

```python
      for name in clean:
          if pp(name not in old_clean):
              cmd = f"pip show {name} > package_files/{name}.txt"
              subprocess.run(cmd, shell=True)
```

<h3>extract_file_info.sh</h3>
Here we use Sed to extract from the files created in the last step, just the lines pertaining to 'name',
'summary' and 'location'; to new files.  
The origin directory of the files is called 'package_files', the directory that
houses the new, clean information is called 'results'.  

```bash
 results=/home/mic/python/cli_apps/cli_apps/results/
 texts=/home/mic/python/cli_apps/cli_apps/package_files/*

 for file in ${texts}; do
    echo "$file"
    trunc_file=${file:49:-4}
    echo "$trunc_file" 
    ftrans0="${results}${trunc_file}"
    echo "$ftrans0"
    
    # 1 - Write to file name, description and url..
    sed -nre "s/^Name: (.*$)/\1/p1" "$file" >> "$ftrans0"
    sed -nre "s/^Summary: (.*$)/\1/p1" "$file" >> "$ftrans0"
    sed -nre "s/^Location: (.*$)/\1/p1" "$file" >> "$ftrans0"

 done
```

<h3>db_upload.py</h3>
Now that we have the information we want to upload extracted and clean, we'll
send it to the database.  
For every file in 'results', we open to read them, clean the output of line
break symbols, store the data points in a list, and feed them to a MySQL query
that uploads it to the database.  

```python
      folders = "/home/mic/python/cli_apps/cli_apps/results/"
      paths = [os.path.join(folders, file) for file in os.listdir(folders)]
  
      for file in paths:
          with open(file, "r") as f:
              fdata = f.readlines()
              name = fdata[0].strip()
              presentation = fdata[1].strip()
              url = fdata[2].strip()
              answers = [name, presentation, url]
              try:
                  conn = connect(host="localhost", user="mic", password="xxxx", database="cli_apps")
                  cur = conn.cursor()
                  query = "INSERT INTO cli_apps (name, presentation, url) VALUES (%s, %s, %s)"
                  cur.execute(query, answers)
                  conn.commit()
              except Error as e:
                  print("Error while connecting to db", e)
              finally:
                  if conn:
                      conn.close()
```

<h3>delete.py</h3>
Here we delete all transitional files, that were needed for the upload but,
since that's done, now serve no purpose.  

```python
      cwd = os.getcwd()
      results = f"{cwd}/results"
      packs = f"{cwd}/package_files"
  
      fldrs = [results, packs]
      for fld in fldrs:
          paths = [os.path.join(fld, file) for file in os.listdir(fld)]
          for path in paths:
              os.remove(path)
```

<h3>cron</h3>
Finally we create a cron job that'll generate a dunst notification, warning that
the scripts were ran and that the database was updated.  

```python
      cron = CronTab("mic")
      dunst = "/usr/bin/dunstify"
      job = cron.new(command=f'{dunst} "cli_apps pip has updated."')
      job.minute.every(59)
      cron.write()
```

I also created a Systemd service and a timer to automate the running of the
scripts.  
