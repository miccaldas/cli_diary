---
title: "Anatomy of a Celery Service"
date: 01/05/2022
mainfont: Iosevka
---

[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html),
is a task queue manager that I started to use as an alternative to Cron.  
Now, I'm starting to wonder that Cron wasn't so bad after all.  
Celery has the, deservedly, reputation of being finicky, but what is more absent
of the conversation is what joy it is to use when everything goes right. It's
full of options, it's fast, silent, and doesn't seem to overtax my aging
computer. As I said, on a good day is all roses.  
What I found more challenging was putting up the services in the beginning. I
think I have the hang of it now, but I need to systematize this information in
writing, so as not to lose it.  
I'm going to use as an example, the service used to run the scripts that
update a database with the names of all packages installed, from AUR and Pacman.  
Unlike some services, this one never gave me troubles, runs when it should, and
should be a good candidate as a template service.  

The first thing I found out is we need to have an added level to the directory
structure, to acommodate Celery. If you try to host Celery's files on the
traditional level:  

Package_folder  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ _______Package_folder  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ _______Files  
  
will quickly discover that Celery complains of not finding the files.
Furthermore, it is decidedly easier if this third level is called 'celery':  
  
Package_folder  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ _______Package_folder  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ _______Celery  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ _______Files
  

These are the necessary modules to build the service:  
  
<h3>app.py</h3>  
Here we create a Celery instance, defining:  
1. App name. In this case, 'celery'.  
2. Backend. This is the database that you'll use. It's suggested that you use
   [Rabbitmq](https://www.rabbitmq.com), but I couldn't get it to work, so I
   used [Redis](https://redis.io), which is ridiculously simple to setup and
   works so well you'll forget that its there.  
   The url used is standard for all Redis instances, changing only the last
   digit, that defines the number of the database in use.  
3. The broker is the same as the backend.  
4. 'include' defines the name of the module that calls the scripts. In this
    case, 'main'.  
5. Here we define the scheduler. This software is in charge of repeating tasks
   and defines when the app is called. We use "beat", that is Celery's
   scheduler, and define an entry with:  
   1. Entry name. Here, 'yay_cron',  
   2. Task Command. Here 'tasks.run'. This is the name of the file that houses
      the tasks, followed by the function name to be used.  
   3. Schedule. I'm using the crontab format that mimics the Cron syntax. The
      schedule defines the task to be run in the third day of the week,
      Wednesday.  

```python
 from celery import Celery
 from celery.schedules import crontab

 app = Celery(
    "celery",
    backend="redis://localhost:6379/0",
    broker="redis://localhost:6379/0",
    include=["main"],
    beat_schedule={
        "yay_cron": {"task": "tasks.run", "schedule": crontab(day_of_week=3)},
    },
 )
```
  
  
<h3>celeryconfig</h3>
As you might've surmised from the file's name, this is where the app
configurations are kept. It's necessary to repeat some of information on the
'app' module:  
1. Result Backend. Redis as we have seen.  
2. Broker URL. Redis' standard url.  
3. Autodiscover Tasks. This automates the process of importing all the files in
   directory 'celery'.  
4. Timezone. Where are you situated.  

```python
from app import app


result_backend = "redis://localhost:6379/0"
broker_url = "redis://localhost:6379/0"
app.autodiscover_tasks(packages=["celery"])
timezone = "Europe/Lisbon"
```


<h3>celerybeat-schedule</h3>
A GNU database with the defined schedules. It has no direct user intervention.  


<h3>tasks</h3>
Where we define the functions that set what will be be actually done.  
Here it works as a kind of 'main' module, as 'main.py' proper, has a slightly
different use in this context.  
Setting a function as a celery task is done through the `@app.task` decorator.  

```python
 import snoop
 from loguru import logger

 from app import app
 from cron import cron
 from db_upload import db_upload
 from delete_transient_files import delete_transient_files
 from query_builder import query_builder

 fmt = "{time} - {name} - {level} - {message}"
 logger.add("../logs/info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)  # noqa: E501
 logger.add("../logs/error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)  # noqa: E501

 subprocess.run(["isort", __file__])


 def type_watch(source, value):
    return "type({})".format(source), type(value)


 snoop.install(watch_extras=[type_watch])


 @app.task
 def run():
    """
    We call all the functions and scripts that
    source, treat, store and clean, the information
    regarding the packages installed by pacman and AUR.
    Aditionally it's created a notification to warn the
    user that the update has ran.
    """
    cmd = "/home/mic/python/cli_apps/cli_apps/yay_querying/celery/yay_lst.sh"
    subprocess.run(cmd, shell=True)

    query_builder()

    cmd1 = "/home/mic/python/cli_apps/cli_apps/yay_querying/celery/extract_file_info.sh"
    subprocess.run(cmd1, shell=True)

    db_upload()

    delete_transient_files()

    cron()
```


<h3>main</h3>
Here we just import the tasks file, that houses the functions that'll be the
service, call the task function, and run it with the `delay()` method, that
initiates a service.  

```python
from app import app
from tasks import run

if __name__ == "__main__":
    run.delay()
```


As Celery's services don't have daemonization capabilities, we need to use
Systemd for running the units on the background.  
I created two Systemd services, one for beat, the other for celery proper.  

<h3>yay_worker.service</h3>
This is the Celery service. Here we define that it should start after the
internet is running in the system, the directory where the initial command
should be run, and what that command is.  
In this case, the command calls Celery on a app ('-A') called 'celery' as per
the name of the folder. This must be exactly this way; the app name must have
the folder name, or else it won't work. The 'worker' name structure is defined
by integrating a hostname `%%h` in its name, that is defined by `-n
worker_name@hostname`. `-E` sends task-related events to the backend, and
`--loglevel`, defines the level of logging.  
Systemd closes all services after an x period of inactivity. As these are weekly
activities, chances are that they would be disabled before having the time to
work. So as not to close the service, we define a 'TimeoutStartSec' that's
longer than the set wait period. 10200 minutes it's slightly longer than a week.  

```ini
[Unit]
Description=Celery Task for Yay Updating.
After=network.target

[Service]
WorkingDirectory=/home/mic/python/cli_apps/cli_apps/yay_querying/celery
ExecStart=/usr/bin/celery -A celery worker -n celery@%%h -E --loglevel=INFO
TimeoutStartSec=10200min
User=mic
Group=mic
Type=simple
Restart=always

[Install]
WantedBy=multi-user.target
```
