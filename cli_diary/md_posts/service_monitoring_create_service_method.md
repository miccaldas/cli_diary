---
title: 'The "Create Service" Method in Service Monitoring'
date: 01/05/2022
mainfont: Iosevka
---

The service_monitoring app has proven to be a handful. Whether because I've been
more distracted than usual or because I'm more ambitious, the net result
is I've been repairing it since I created it. Constantly and deeply. Some of its
methods have become a bit intricate, specifically the delete and creation of
services methods. It's my intention, in this post and in a next one, to document
the code, so as to help in future debugging efforts. That I believe won't be
very far off.  
Here I'll talk about service creator module. I'll be calling a set of Systemd or
Celery services that are associated (for example, a service and a timer in
Systemd or a service and beat in Celery) a 'service' and each of its constituent
services, a 'unit'. Totally arbitrary I know.  
The idea was to automate all the steps in the creation of a service, asking the
user, as minimal a quantity of information as possible.  
And because of this, some desirable flexibility was lost in the altar of
automation. This might be something I'll revisit at a later stage.  

The command is supposed to be initiated on the main directory of the project you
want to create services for.
It determines the current working directory:

```python
          cwds = os.getcwd()
```

collects all files in the folder and subfolders in a list:

```python
          services = []
          for root, dirs, files in os.walk(cwds):
              for file in files:
                  services.append(file)
```

creates another list with files ended in '.service' or '.timer':

```python
     services_present = [i for i in services if i.endswith(".service") or i.endswith(".timer")]
```

and if the list is not empty, we ask the user if he wants to use these services.  
This is here because I, lots of times, tend to write the services files in
advance, and its a way of not repeating efforts.  
If the user responds affirmatively, the service name goes to a new list, if
negatively, to another.

```python
          if services_present != []:
              for service in services_present:
                  use_choice = input(click.style(f" ++ Do you want to use {service}? [y/n] ", fg="bright_white", bold=True))
                  if use_choice == "y":
                      chosen_units.append(service)
                  if use_choice == "n":
                      user_negs.append("n")
```

If we verify that the list of wanted services is empty or the list of negative
ones is not, we assume that he may want to create a service from scratch.  
So we ask him what type of service he wants:

```python
          if services_present == [] or user_negs != []:
              unit_making = questionary.select(
                  "What units do you want to create?",
                  qmark="[x]",
                  pointer="++",
                  use_indicator=True,
                  style=custom_style_monitor,
                  choices=["Service", "Timer", "Both", "None", "Exit"],
              ).ask()
```

As we want to automate the process as much as possible, we don't ask the user
the name he wants for the service; we assume the name of the project folder as
the name of service, and append these new names to yet another list.  

```python
              tail = os.path.basename(os.path.normpath(cwds))
              cmd20 = f"sudo /usr/bin/vim {tail}.service"
              cmd21 = f"sudo /usr/bin/vim {tail}.timer"
              if unit_making == "None":
                  pass
              if unit_making == "Exit":
                  sys.exit()
              if unit_making == "Service":
                  subprocess.run(cmd20, cwd=cwds, shell=True)
                  chosen_units.append(f"{tail}.service")
              if unit_making == "Timer":
                  subprocess.run(cmd21, cwd=cwds, shell=True)
                  chosen_units.append(f"{tail}.timer")
              if unit_making == "Both":
                  subprocess.run(cmd20, cwd=cwds, shell=True)
                  subprocess.run(cmd21, cwd=cwds, shell=True)
                  chosen_units.append(f"{tail}.service")
                  chosen_units.append(f"{tail}.timer")
```

For each unit name in the list, we copy it to the correct directory, reload the
Systemd daemon, start the unit and copy its status to a file.  

```python
          for h in chosen_units:
              cmd22 = f"/usr/bin/sudo /usr/bin/cp {h} '/usr/lib/systemd/system/'"
              subprocess.run(cmd22, cwd=cwds, shell=True)
              cmd23 = "/usr/bin/sudo /usr/bin/systemctl daemon-reload"
              subprocess.run(cmd23, shell=True)
              cmd24 = f"/usr/bin/sudo /usr/bin/systemctl start {h}"
              subprocess.run(cmd24, shell=True)
              cmd25 = f"/usr/bin/sudo /usr/bin/systemctl status {h} > {h}.txt"
              subprocess.run(cmd25, shell=True)
```

We verify if the file was indeed created, open it and read it line by line.
Using Python's regular expression's library, we check if the unit is active -
running, active - waiting or any other state.  In the case of the two first
states, we optionally propose to the user the opening of the unit status view,
in the case of any other state the status view is opened automatically.  

```python
          for line in data:
              x = re.search("^\s+Active: active \(running\).+\n$", line)
              w = re.search("^\s+Active: active \(waiting\).+\n$", line)
              if x or w:
                  success = input(click.style(f"++ {h} is active. Do you want to see its status? [y/n]: ", fg="bright_white", bold=True))
                  if success == "y":
                      subprocess.run(cmd26, shell=True)
                  break
              else:
                  print(click.style(f" ++ {h} is not active. We'll open the status view for debugging.", fg="bright_white", bold=True))
                  sleep(0.30)
                  subprocess.run(cmd26, shell=True)
                  break
```

Finally we call the entry() function, housed in another module, that inputs the
new service information into the json file. After that we call another external
module to update the app's services dropdown.  

Here's the complete code:

```python
      # @snoop
      def create_service(self):
          """
          It will first search for files with the prefix 'service' or 'timer' on the
          current working directory. If it finds them, it asks if these are the files
          to be used, if yes, it processes them with the program, if no, it will copy a
          default service file to cwd and open it as file called, '<current_dir>.service'.
          Then it will ask if you want to create a timer, if yes, it's same procedure
          as it was for service, but now we use a default timer file.
          These files, pre-built or made now, will be copied to '/usr/lib/systemd/system',
          send the daemon-reload' command, their status checked, to see it they are loaded,
          started with systemctl and checked again, to see if they are working correctly.
          This new service will be manually added to the json file and the dropdown file updated.
          """
          custom_style_monitor = Style(
              [
                  ("qmark", "fg:#ff5c8d bold"),
                  ("question", "fg:#E0DDAA bold"),
                  ("pointer", "fg:#BB6464 bold"),
                  ("highlighted", "fg:#E5E3C9 bold"),
                  ("selected", "fg:#94B49F bold"),
                  ("text", "fg:#F1E0AC bold"),
              ]
          )
  
          cwds = os.getcwd()
          services = []
          for root, dirs, files in os.walk(cwds):
              for file in files:
                  services.append(file)
          services_present = [i for i in services if i.endswith(".service") or i.endswith(".timer")]
  
          chosen_units = []
          user_negs = []
          if services_present != []:
              for service in services_present:
                  use_choice = input(click.style(f" ++ Do you want to use {service}? [y/n] ", fg="bright_white", bold=True))
                  if use_choice == "y":
                      chosen_units.append(service)
                  if use_choice == "n":
                      user_negs.append("n")
          if services_present == [] or user_negs != []:
              unit_making = questionary.select(
                  "What units do you want to create?",
                  qmark="[x]",
                  pointer="++",
                  use_indicator=True,
                  style=custom_style_monitor,
                  choices=["Service", "Timer", "Both", "None", "Exit"],
              ).ask()
              tail = os.path.basename(os.path.normpath(cwds))
              cmd20 = f"sudo /usr/bin/vim {tail}.service"
              cmd21 = f"sudo /usr/bin/vim {tail}.timer"
              if unit_making == "None":
                  pass
              if unit_making == "Exit":
                  sys.exit()
              if unit_making == "Service":
                  subprocess.run(cmd20, cwd=cwds, shell=True)
                  chosen_units.append(f"{tail}.service")
              if unit_making == "Timer":
                  subprocess.run(cmd21, cwd=cwds, shell=True)
                  chosen_units.append(f"{tail}.timer")
              if unit_making == "Both":
                  subprocess.run(cmd20, cwd=cwds, shell=True)
                  subprocess.run(cmd21, cwd=cwds, shell=True)
                  chosen_units.append(f"{tail}.service")
                  chosen_units.append(f"{tail}.timer")
  
          for h in chosen_units:
              cmd22 = f"/usr/bin/sudo /usr/bin/cp {h} '/usr/lib/systemd/system/'"
              subprocess.run(cmd22, cwd=cwds, shell=True)
              cmd23 = "/usr/bin/sudo /usr/bin/systemctl daemon-reload"
              subprocess.run(cmd23, shell=True)
              cmd24 = f"/usr/bin/sudo /usr/bin/systemctl start {h}"
              subprocess.run(cmd24, shell=True)
              cmd25 = f"/usr/bin/sudo /usr/bin/systemctl status {h} > {h}.txt"
              subprocess.run(cmd25, shell=True)
  
          cmd26 = f"/usr/bin/sudo /usr/bin/systemctl status {h}"
          sleep(0.30)
          if f"{h}.txt":
              with open(f"{h}.txt", "r") as f:
                  data = f.readlines()
              print("\n")
              for line in data:
                  x = re.search("^\s+Active: active \(running\).+\n$", line)
                  w = re.search("^\s+Active: active \(waiting\).+\n$", line)
                  if x or w:
                      success = input(click.style(f"++ {h} is active. Do you want to see its status? [y/n]: ", fg="bright_white", bold=True))
                      if success == "y":
                          subprocess.run(cmd26, shell=True)
                      break
                  else:
                      print(click.style(f" ++ {h} is not active. We'll open the status view for debugging.", fg="bright_white", bold=True))
                      sleep(0.30)
                      subprocess.run(cmd26, shell=True)
                      break
          entry()
          make_dropdown()
```
