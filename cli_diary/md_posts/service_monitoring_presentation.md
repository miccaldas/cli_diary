---
title: "Service Monitoring Presentation"
mainfont: Iosevka
---


   <h3>Dropdown</h3>

   I very much wanted to automate as much of this process as possible. That
   implied that I shouldn't have to manually alter the dropdown with the
   services, every time one is created or destroyed. It should read dynamically from an
   always updated information source.  
   The problem with this is that 'Questionary' only accepts static content as
   its alternatives. You can't feed it from a loop, for example. To circumvent
   this, I created the 'making_dropdown_file.py', that builds the dropdown file
   with write instructions. Something like this:

   ```python
      f.write(" def dropdown():")
   ```

   This way I was able to insert a loop that will write dictionary entries into
   the dropdown choices:

   ```python
      d.write("         app = questionary.select(\n")
      d.write('             "What app do you want to use?",\n')
      d.write('             qmark="[x]",\n')
      d.write('             pointer="++",\n')
      d.write("             use_indicator=True,\n")
      d.write("             style=custom_style_monitor,\n")
      d.write("             choices=[\n")
      for i in range(len(res["dropinfo"])):
         d.write(f"               '{res['dropinfo'][i]['name']}',\n")
      d.write('               Separator("----- EXIT -----"),\n')
      d.write("               'Exit'\n")
      d.write("            ]\n")
      d.write("        ).ask()\n")
   ```

   This ends up looking like this:

   ```python
      app = questionary.select(
        "What app do you want to use?",
         qmark="[x]",
         pointer="++",
         use_indicator=True,
         style=custom_style_monitor,
         choices=[
                  "Backups Service",
                  "Yay Service",
                  "Git Automate",
                  "Home Git Automate",
                  "Flower",
                  "Pip",
                  "service_monitoring",
                  "home_git_updt",
                  Separator("----- EXIT -----"),
                  "Exit",
              ],
          ).ask()
   ```

   The dropdown module defines the user interface for the app. Too late did I
   notice that I needed, because of reasons that'll be understood when we talk
   about the 'main' module, to differentiate between queries that were specific
   to a service and those that were general in nature.  
   To understand that we create an initial question that, according to the
   answer, will direct the user to one of two dropdowns:

   ```python
       ambit = questionary.confirm(
          "Is your question about a specific service?",
          qmark="[x]",
          default=False,
          auto_enter=False,
       ).ask()
   ```

   If the answer is 'yes', the user will be lead to a dropdown with methods that
   pertain to information regarding a specific service, if no, it will be
   directed to a dropdown of general methods.  

  <h3>dropdown_info.json</h3>

  This is the one source of knowledge in the app. It was firstly created
  manually, but from now on it's changed through the 'delete_json.py' and
  'append_to_json.py' modules, that can be called manually, but are integrated in
  the other modules, whenever there's a creation or destruction of a service. As
  I said, the objective is to be as automated as possible.  
  As an example of the information kept there:

 ```json
        {
            "app": "main",
            "name": "Backups Service",
            "path": "/home/mic/python/backups/backups/celery",
            "units": [
                "backups_beats.service",
                "backups_celery.service"
            ]
        },
 ```

 <h3>Main</h3>

 In the 'main' function of the 'main' module, we divide the input coming from
 'dropdown' according to length:
 If the length is 2, that means that information returned from the service
 specific dropdown, as it only returns two pieces of data, the service name and
 the method to use.  
 The generalist dropdown returns three pieces of data, two are dummy values to
 satisfy the method class, (a made up app name and unit), and the method the
 user chosen.  
 In the first case:

 ```python
      if len(dropdown) == 2:
          for i in dropdown:
              if i == "Exit":
                  sys.exit()
          data = []
          for i in range(len(info["dropinfo"])):
              if dropdown[0] == info["dropinfo"][i]["name"]:
                  data.append(info["dropinfo"][i]["app"])
                  data.append(info["dropinfo"][i]["path"])
                  data.append(info["dropinfo"][i]["units"])
              drop = data[0]
              path = data[1]
              units = data[2]
              if path != "none":
                  os.chdir(path)
              ress = []
              answer = Answers(drop, units)
              for method in methods:
                  res = f"answer.{method}()"
                  ress.append(res)
              for task in ress:
                  print("\n")
                  print("---------------------------------------------------------------------------")
                  print("\n")
                  exec(task)
              sys.exit()
   ```

  The generalist is pretty similar.



