---
title: "Anatomy of a Celery Service"
date: 01/05/2022
mainfont: Iosevka
---

[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html),
is a task queue manager that I started to use as an alternative to Cron.  
After trying several modes of implementation of its servers that all lead to non
functioning services, I came upon this one, the simplest one, that does the job
correctly.  
I'll use as example, a service that backups the computer.  

<h3>tasks.py</h3>
This is where you'll write your functions that'll become Celery tasks, as well
as its configurations.  

1. Define configurations. The broker and backend url's are standard for Redis,
   the only that changes its the database number at the end.  

```python
  BROKER_URL = "redis://localhost:6379/0"
  BACKEND_URL = "redis://localhost:6379/1"
```

2. Define app. This will be a Celery instance, and its composed of the name of
   the files where the tasks are and the broker and backend url's.  

```python
  app = Celery(
      "tasks",
      broker=BROKER_URL,
      backend=BACKEND_URL,
  )
```

3. Finally, we setup a decorator on the tasks functions, to identify them as
   such.  

```python
  @app.task(name="usr_backup")
```

4. If we need to set up the task as periodical, we add another function that
   defines its attributes.  
   In this case we define the period to be every Monday, at 7h30, and we can
   forego of 'main.py' file. The information in 'tasks.py' will suffice.  
   **Please note that, if using a periodical task, the command to start the app
   will be `celery -A tasks beat`. There's no need to call the worker.**  
   The example I'll put here its from another app, so it
   wont be visible in the full code:

```python
  @app.on_after_configure.connect
  def setup_periodic_tasks(sender, **kwargs):
      sender.add_periodic_task(
          crontab(hour=7, minute=30, day_of_week=1),
          check_urls(),
    )
```

Full code:

```python
  import isort
  import snoop
  from snoop import pp
  from celery import Celery
  import subprocess


  def type_watch(source, value):
      return "type({})".format(source), type(value)


  snoop.install(watch_extras=[type_watch])

  BROKER_URL = "redis://localhost:6379/0"
  BACKEND_URL = "redis://localhost:6379/1"
  app = Celery(
      "tasks",
      broker=BROKER_URL,
      backend=BACKEND_URL,
  )


  @app.task(name="usr_backup")
  @snoop
  def backup():
    """"""
    cmd = "rsync -azP --delete /boot /home/mic/secondary-hard-drive/directories_bkup"
    subprocess.run(cmd, shell=True)
    cmd1 = "rsync -azP --delete /etc /home/mic/secondary-hard-drive/directories_bkup"
    subprocess.run(cmd1, shell=True)
    cmd2 = "rsync -azP --exclude /home/mic/secondary-hard-drive --delete /home /home/mic/secondary-hard-drive/directories_bkup"
    subprocess.run(cmd2, shell=True)
    cmd3 = "rsync -azP --delete /opt /home/mic/secondary-hard-drive/directories_bkup"
    subprocess.run(cmd3, shell=True)
    cmd4 = "rsync -azP --delete /usr /home/mic/secondary-hard-drive/directories_bkup"
    subprocess.run(cmd4, shell=True)
    cmd5 = "rsync -azP --delete /var /home/mic/secondary-hard-drive/directories_bkup"
    subprocess.run(cmd5, shell=True)
    cmd6 = "rsync -azP --delete /srv /home/mic/secondary-hard-drive/directories_bkup"
    subprocess.run(cmd6, shell=True)
```


<h3>main.py</h3>
Here we take the task and put it in the queue to be used. This does not start
the service, just prepares it. The `delay()` function is responsible for doing so.  
`result.id` is just to check if the process was successful.  

```python
  from tasks import backup

  result = backup.delay()
  print(result.id)
```


In the end, through command line or Systemd service, you give the command to
start the service:

```bash
  celery -A tasks worker --loglevel=INFO
```
