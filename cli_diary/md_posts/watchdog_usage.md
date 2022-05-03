---
title: "Watchdog Usage"
date: 03/05/2022
mainfont: Iosevka
---

Whenever I move a project to 'old_alternative_files', there are a lot of files
and folders that are, or specific to being a package, or unnecessary for the
purposes of checking old code; such as logs for example.  
I wanted something that would detect when a new folder was created in
'old_alternative_projects', and would erase said files and folders.  
For that I found [Watchdog](https://python-watchdog.readthedocs.io/en/stable/).
It monitors events on the filesystem and implements whatever code you want to
run on the said events.  
  
<h3>WatchOldAlternative</h3>
This class sets a directory to watch and runs the methods we wrote, in case of a
event:

We define a directory to monitor:

```python
      watchDirectory = "/home/mic/python/old_alternative_projects"
```

instantiate the `Observer` class, that'll will do the monitoring of the
directory:

```python
      def __init__(self):
          self.observer = Observer()
```

define a method that'll run the script with the Handler class. Note the
`recursive=True` flag, it's there in case you want to monitor the folder and
sub-folders.  

```python
      def run(self):
          """
          Runs the handler class.
          """
          event_handler = Handler()
          self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
          self.observer.start()
          try:
              while True:
                  sleep(5)
          except:
              self.observer.stop()
              print("Observer Stopped")
  
          self.observer.join()
```
  

<h3>Handler</h3>
The class `Handler` defines the events to be monitored and what to do when it
happens.  

Here we determine that if the event, that is defined as `on_created` (which monitors creation of folders or files) pertains to a directory, we'll keep its `event.src_path`, (the directory's full path), in a variable called `pth`.  
We then get the folder name by isolating the tail of path.

```python
      if event.is_directory:
          pth = event.src_path
          pp(pth)
          tail = os.path.basename(os.path.normpath(pth))
```

Here we have a list with the names of the folders we want to delete, if the
folder has the same name as any of the entries in this list, it'll be sent to
trash.  
If it ends with 'egg-info', send it to the trash also.  

```python
      del_dir = [".git", "logs", "build", "__pycache__"]
      if tail in del_dir:
          cmd = f"/home/mic/.local/bin/trash-put -d {pth}"
          subprocess.run(cmd, shell=True)
      cmd = f"/home/mic/.local/bin/trash-put {pth}"
      if tail.endswith("egg-info"):
          subprocess.run(cmd, shell=True)
```

If the event is new file, it's the same procedure, only with a different list of
deletable names.  

```python
      else:
          pth = event.src_path
          tail = os.path.basename(os.path.normpath(pth))
          del_file = [".gitignore", ".gitconfig", "LICENSE", "MANIFEST.in", "pyproject.toml", "setup.py", "setup.cfg", "__init__.py"]
          cmd = f"/home/mic/.local/bin/trash-put {pth}"
          if tail in del_file:
              subprocess.run(cmd, shell=True)
```


The full code:

```python
  """
   The 'old_alternative_projects' is a directory for code that can be reused.
   When sending a package to this directory, all package related files are
   not needed anymore and should be deleted.'
   """
   import os
   import subprocess
   from time import sleep
  
   import isort
   import snoop
   from snoop import pp
   from watchdog.events import FileSystemEventHandler
   from watchdog.observers import Observer
  
  
   def type_watch(source, value):
      return "type({})".format(source), type(value)
  
  
   snoop.install(watch_extras=[type_watch])
  
  
   class WatchOldAlternative:
      """
      Set 'old_alternative_projects' as the directory
      to watch.
      """
  
      watchDirectory = "/home/mic/python/old_alternative_projects"
  
      def __init__(self):
          self.observer = Observer()
  
      def run(self):
          """
          Runs the handler class.
          """
          event_handler = Handler()
          self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
          self.observer.start()
          try:
              while True:
                  sleep(5)
          except:
              self.observer.stop()
              print("Observer Stopped")
  
          self.observer.join()
  
  
   class Handler(FileSystemEventHandler):
      """
      Defines event to be monitored and
      what to do when it happens.
      """
  
      @staticmethod
      # @snoop
      def on_created(event):
          if event.is_directory:
              pth = event.src_path
              pp(pth)
              tail = os.path.basename(os.path.normpath(pth))
              del_dir = [".git", "logs", "build", "__pycache__"]
              if tail in del_dir:
                  cmd = f"/home/mic/.local/bin/trash-put -d {pth}"
                  subprocess.run(cmd, shell=True)
              cmd = f"/home/mic/.local/bin/trash-put {pth}"
              if tail.endswith("egg-info"):
                  subprocess.run(cmd, shell=True)
          else:
              pth = event.src_path
              tail = os.path.basename(os.path.normpath(pth))
              del_file = [".gitignore", ".gitconfig", "LICENSE", "MANIFEST.in", "pyproject.toml", "setup.py", "setup.cfg", "__init__.py"]
              cmd = f"/home/mic/.local/bin/trash-put {pth}"
              if tail in del_file:
                  subprocess.run(cmd, shell=True)
  
  
   if __name__ == "__main__":
      watch = WatchOldAlternative()
      watch.run()
```
