Some time ago I was testing [Sourcery's](https://docs.sourcery.ai) code quality application, to get an outside opinion, as impersonal as it may be,
about my code. This hobby can be a lonely business. The results were,
more or less, lackluster but I didn't feel to bad.  
I think it's to be expected that, being an amateur and all, that really doesn't 
code that much, the results could never be stellar.  
All in all it was what I expected to be.  
Until I looked into Service Monitoring. 'Sourcery' was as indignant as an unfeeling,
unthinking tool can be. It was so bad it didn't suggest much in the way of alterations, only some earnest calls to revise
and refactor that unholy mess.  
Had I remembered that, apparently, I wrote long and often about the build of
that app, I might've gleaned some knowledge from that the dense, dark, wall
of code that, if it was meant to be used as obfuscation, wouldn't be any more
successful.  
I couldn't understand the 'main' function.  
The 'main' function!  
At my level of sophistication, everything it does is call all other modules in
order. The fact that I wrote a 'main' function that read as Swahili to my some
months older self, would have seemed fantastic to me. Still, here we were.  
With my pride a little piqued, although I hated the tool. It's heavy and
intrusive, I set about to make some betterments to the code. The equivalent of
a coat of paint and a Spring cleaning as it were. More cosmetic than structural
I thought.  
Of course what I didn't know, but do now, is that one of the things that makes
computer engineering challenging, as opposed to tinkering idly on projects that
tickle your fancy, at your leisure, is that most code is propping things up in
companies and can't be rewritten on a whim. If you have a scion of hell living
in your codebase, you'll have to find a way to live with it, because simply,
nobly, morally-minded, option of starting again, is totally out of
the question. I don't envy those poor bastards. Me, on the other hand, don't
have any of those constraints. So I quickly concluded that that it,
for whatever it was, had to go.  
The first, and more challenging task of this refactoring was
to understand what subtleties and special cases were being looked into, that
justified the gongorism of the code. This was my earnest desire, that through
inexperience and enthusiasm, I had been led astray into a wilderness of
complexity that, in the end, if abstruse, showed attention to detail and border
conditions. Unfortunately that was not what I found.  
The app did the things that most simple apps do, didn't had no special affinity
for the quirky or the subtle, it thought and provided solutions for only the more
obvious scenarios. It was just badly designed by someone that has a tendency of
listening to all that's meandering and rambling, than to soundly planned
arguments.  
Truth be told, the signs were there. It's use was unbearably brittle. What would
work today, wouldn't work tomorrow or for all cases. The debugging was opaque,
the documentation, because I had forgotten six, six!, entries that I made here,
was nonexistent. As I said, had I know that this trove of information was here,
I probably would had have been much more conservative on my 'redecoration'. As
I didn't, I basically rewrote it. Some ideas are present in both projects, but
that's just because I'm not very creative and I tend to repeat the same things
to the same people all the time, even when I'm not drunk.  
It was for the best I think. I can now look at it and understand what it does.  
Anyone can. And that's a good thing. Even a mechanical quality assessment tool
was offended by it.  
Here are some examples:
### 1 - Deleting Services
Now, to be frank, on this part I'm doing some conjecturing, I'm, brazenly,
making assumptions on what I wanted to do with that code; when it doesn't
warrant any kind of interpretation. It's "The Great Cloud of Unknowing", it's
impervious to your vain human reason. Your conclusions are, wholly, your own.
But a modicum of exegesis is in order ... I, after all, did wrote it. Much to my
chagrin.  
What I think I was trying to do was, dealing with service deletion and the
ungodly mess that was updating a json file that was being used as a keeper of
truth for the app. Why a json file you ask? When a database, however small,
would've been a better solution? The truth is that I was trying to do something
different from my CRUD apps. Was trying something new; and I had hear good
things of this json fellow. Maybe he could help.  
In short, it was a solution thought out in a whim, for all the wrong (more
non-existent) reasons and with no thought put into.  
It worked as good as you would expect.  
This is what I had:
```python
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
Nothing of this, except the Systemd commands, through no fault of my own, worked
as expected. It kept glitching and I, for some, reason, never quite got around
to understanding dictionaries and json, until very recently. So I was outside
looking in. And when I finally, got a glimpse of comprehension on those
subjects, was only to conclude that they shouldn't be used here. At least no for
me.  
Today I broke the function into small, simpler bits. Separated database
operations from service interactions, did away with the godforsaken json file
and put the data in the smallest, cutest, MySQL database ever.  
Sqlite3 is acting out in my computer, don't judge me!  
Got a function just for the systemd commands and commented profusely the code, knowing
now that, in the future Imwon't remember to check this diary for information.  
```python
# @snoop
def dbdelunit(selunit):
    """
    Deletes a unit in a service in the database.
    """
    for sel in selunit:
        delcmd = f"DELETE FROM services WHERE id = {sel}"
        dbcommit(delcmd)

    console.print(f"  <X> - The {selunit} unit(s) were deleted.", style="bold #E2C275")


# @snoop
def systemctldel(delservices):
    """
    Deletes services or timers
    from systemctl.
    """
    for sel in delservices:
        a = (f"sudo systemctl stop {sel}",)
        b = (f"sudo systemctl disable {sel}",)
        c = ("sudo systemctl daemon-reload",)
        d = (f"sudo trash /usr/lib/systemd/system/{sel}",)
        e = "sudo systemctl reset-failed"

        for cmd in [a, b, c, d, e]:
            subprocess.run(cmd, shell=True)

    console.print(
        f"  <X> - The {delservices} services were deleted from Systemctl.",
        style="bold #E2C275",
    )


# @snoop
def dbfetch(query):
    """
    Gets info from the database.
    """

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="services")
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data


# @snoop
def dbcommit(query):
    """
    Sends info to the database.
    """

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="services")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    console.print(f"  The query {query} was run.", style="bold #E2C275")


# @snoop
def delete():
    """
    Called by 'main'. From information from id's and unit_names,
    we'll delete by unit_name, first in Systemctl by the name
    of the service's, then by id's in the database.
    """

    # First we get information to identify the rows to delete.
    query = "SELECT id, name, unit_name FROM services"
    # Make a db call.
    data = dbfetch(query)
    # We print the output, so the user can choose ehat to delete.
    for i in data:
        console.print(f"  {i[0]} - {i[1]} - {i[2]}", style="bold #939B62", justify="left")
        # print("\n")
    delchoice = console.input("[bold #E2C275]  { X } - Choose the id's you want: [/]")
    # In case we were given more than one id, we seprate them by space.
    selunit = delchoice.split(" ")
    # This converts the id's into strings, which won't do. We turn them
    # back to ints.
    delints = [int(i) for i in selunit]
    # Build a list of unit_names, names, to use when deleting in Systemctl.
    delservices = [i[2] for i in data if i in delints]
    # Call the function to delete Systemctl's services.
    systemctldel(delservices)
    # Call function to delete database entries.
    dbdelunit(delints)
    # We redraw the app's presentation, with the updated number of entries.
    make_dropdown()


if __name__ == "__main__":
    delete()
```
I did something similar to the 'add service' function, that makes this look like
a minimalist triumph, and rewrote the 'main' function, that, from all things
that I don't understand, it's the one I don't understand the most.  
But, conversations to have another time.
