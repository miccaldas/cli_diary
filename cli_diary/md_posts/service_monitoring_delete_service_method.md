---
title: "Service Monitoring, Delete Service Method Presentation"
date: 01/05/2022
mainfont: Iosevka
---

This is kind of a 'part 2' of the `service_monitoring_create_service_method` post.  
In it I presented the service_monitoring app, and what it tries to do and the
reasons why it needs to be documented. So if these topics interest you, start
there.  
This method deletes Systemd or Celery services safely. It also changes the json
file, that serves as source of truth for the app, and the dropdown file, that
presents the available services.  
  
We start by reading the json file into a string:
  
```python
        with open("/home/mic/python/service_monitoring/service_monitoring/dropdown_info.json", "r") as f:
            servs = f.read()  # It has to be read(), not readlines(), because the latter is a list.
        info = json.loads(servs)
```
  
Create an empty list that will user later on:
  
```python
    decision_lst = []
```
  
There are two types of inputs for the app's methods:  
1. The information pertains to a specific service.  
   In that case, the information received by the class will have an existing service name and the method we want to use.  
2. The information does not pertain to a specific service.  
   Here, the class will receive a list with a `dummy_service` string as the service name, and the method, that is the only thing of relevance in this case.  
  
To filter only the queries to specific services, we verify if the string
`dummy_service` is contained in the variable `self.units`, that reads from the
second member of the list given by the `dropdown` module.  
If it's not, we question the user if he wants to disable x unit. We'll do it for
all units contained in `self.units`.  
For all units that the user answers affirmatively, there'll be an entrance on
the `decision_lst` list, that'll keep the user's choices for all the queries.  
  
```python
    if "dummy_service" not in self_units:
        for unit in self.units:
            decision = input(click.style(f" ++ Do you want to disable unit {unit}? [y/n] ", fg="bright_white", bold=True))
            if decision == "y":
                decision_lst.append(f"{unit}")
```
  
If, on the other hand, the information available does contain the string
`dummy_service` and relates to a general query, we ask what units he wants to
delete. If the answer is nothing, we exit the program. If it's something, we
must be aware that the answer can be multiple services. For this we split the
resulting string from the input function into a list of strings, obtained by
using `split` on spaces.  
Off course this means that no commas should be added when inputting the list of units to delete.  
We add the list's items to the `decision_lst` list.  
  
```python
    else:
        deci = input(click.style(" ++ What unit(s) do you want to delete? ", fg="bright_white", bold=True))
        if deci == "":
            sys.exit()
        else:
            decision = deci.split(" ")
        for i in decision:
            decision_lst.append(i)
```
  
For each unit chosen, we'll run consecutively, the following commands:  
1. Stop unit.  
2. Disable unit.  
3. Delete unit file in Systemd directory.  
4. Reload Systemd daemon.  
5. Reset failed services.  
  
```python
    for service in decision_lst:
        cmd15 = f"sudo systemctl stop {service}"
        subprocess.run(cmd15, shell=True)
        cmd16 = f"sudo systemctl disable {service}"
        subprocess.run(cmd16, shell=True)
        cmd18 = f"sudo rm /usr/lib/systemd/system/{service}"
        subprocess.run(cmd18, shell=True)
        cmd17 = "sudo systemctl daemon-reload"
        subprocess.run(cmd17, shell=True)
        cmd19 = "sudo systemctl reset-failed"
        subprocess.run(cmd19, shell=True)
```
  
Now we'll update the json file. Contrary to what is done in `create_service`
method, where this part is done by another module, here we concentrate all
operations in the same function. I think this is the best option, and might still
change the `create_service` workflow.  
  
We open the file:
  
```python
    monitor = "/home/mic/python/service_monitoring/service_monitoring"
    data = json.load(open(f"{monitor}/dropdown_info.json"))
```
  
The python structure of the json file is a dictionary, that has, as value, a
list of dictionaries, that themselves have lists as values.  
As I'm not too accustomed to dictionaries, this can be quickly become
overwhelming.  
In this case, two scenarios may present themselves: the user intends to erase all
units of a service or he just wants to delete some of them.  
  
In the first case we do:  
For all entries in the `dropinfo` list of values, with the dictionary item `units`; if the contents of the units to erase is equal to the units present for that
list member:  
1. delete member,  
2. open new json file and write updated dictionary to it,  
3. delete old json file,  
4. rename new file with the name of old,  
5. run `make_dropdown`, that'll update the services list in the UI.  
  
```python
    for i in range(len(data["dropinfo"])):
        if decision_lst == data["dropinfo"][i]["units"]:
            data["dropinfo"].pop(i)
        open(f"{monitor}/dropdown_info1.json", "w").write(json.dumps(data, indent=4, sort_keys=True))
        os.remove(f"{monitor}/dropdown_info.json")
        os.rename(f"{monitor}/dropdown_info1.json", f"{monitor}/dropdown_info.json")
        make_dropdown()
```
  
For the second case:  
1. create list of `units` lists, contained in each of `dropinfo` members,  
2. verify that list of units to erase is different from all `units` lists,  
3. if that is the case, for each unit to be deleted:  
4. we'll iterate through all members of `dropinfo`,  
5. and if we find the name of one of the units to be deleted inside one of the `units` lists,  
6. remove the corresponding entry in said list.  
7. Open new json file and write updated dictionary to it,  
8. delete old json file,  
9. rename new file with the name of old,  
10. run `make_dropdown`.  

```python
    tst = [v.get("units") for v in data["dropinfo"]]
    if decision_lst not in tst:
        for u in decision_lst:
            for t in range(len(data["dropinfo"])):
                if u in data["dropinfo"][t]["units"]:
                    data["dropinfo"][t]["units"].remove(u)
                open(f"{monitor}/dropdown_info1.json", "w").write(json.dumps(data, indent=4, sort_keys=True))
                os.remove(f"{monitor}/dropdown_info.json")
                os.rename(f"{monitor}/dropdown_info1.json", f"{monitor}/dropdown_info.json")
                make_dropdown()
```
  
  
Here is the full code:

```python
    @snoop
    def delete_service(self):
        """
        First stops the unit, then disables it and
        lastly, deletes files. If service is
        completely erased, it'll delete also the
        entry on the json file and run again the
        dropdown creation file.
        The reason I repeated the 'stop_service'
        and 'daemon_reload' methods, instead of
        simply calling them from this method, is
        that if I did that, there would be a lot
        of spurious empty and dotted lines. This
        way the presentation is cleaner.
        """

        with open("/home/mic/python/service_monitoring/service_monitoring/dropdown_info.json", "r") as f:
            servs = f.read()  # It has to be read(), not readlines(), because the latter is a list.
        info = json.loads(servs)

        decision_lst = []

        if "dummy_service" not in self.units:
            for unit in self.units:
                decision = input(click.style(f" ++ Do you want to disable unit {unit}? [y/n] ", fg="bright_white", bold=True))
                if decision == "y":
                    decision_lst.append(f"{unit}")
        else:
            deci = input(click.style(" ++ What unit(s) do you want to delete? ", fg="bright_white", bold=True))
            if deci == "":
                sys.exit()
            else:
                decision = deci.split(" ")
            for i in decision:
                decision_lst.append(i)

        for service in decision_lst:
            cmd15 = f"sudo systemctl stop {service}"
            subprocess.run(cmd15, shell=True)
            cmd16 = f"sudo systemctl disable {service}"
            subprocess.run(cmd16, shell=True)
            cmd18 = f"sudo rm /usr/lib/systemd/system/{service}"
            subprocess.run(cmd18, shell=True)
            cmd17 = "sudo systemctl daemon-reload"
            subprocess.run(cmd17, shell=True)
            cmd19 = "sudo systemctl reset-failed"
            subprocess.run(cmd19, shell=True)

        monitor = "/home/mic/python/service_monitoring/service_monitoring"
        data = json.load(open(f"{monitor}/dropdown_info.json"))

        for i in range(len(data["dropinfo"])):
            if decision_lst == data["dropinfo"][i]["units"]:
                data["dropinfo"].pop(i)
            open(f"{monitor}/dropdown_info1.json", "w").write(json.dumps(data, indent=4, sort_keys=True))
            os.remove(f"{monitor}/dropdown_info.json")
            os.rename(f"{monitor}/dropdown_info1.json", f"{monitor}/dropdown_info.json")
            make_dropdown()

        tst = [v.get("units") for v in data["dropinfo"]]
        if decision_lst not in tst:
            for u in decision_lst:
                for t in range(len(data["dropinfo"])):
                    if u in data["dropinfo"][t]["units"]:
                        data["dropinfo"][t]["units"].remove(u)
                    open(f"{monitor}/dropdown_info1.json", "w").write(json.dumps(data, indent=4, sort_keys=True))
                    os.remove(f"{monitor}/dropdown_info.json")
                    os.rename(f"{monitor}/dropdown_info1.json", f"{monitor}/dropdown_info.json")
                    make_dropdown()

        print("\n\n")
```


