---
title: Service Monitoring Epilogue
mainfont: Iosevka
fontsize: 13pt
---


Some time ago I was testing [Sourcery's](https://docs.sourcery.ai) code quality application, to get an outside opinion, as impersonal as it may be,
about my code. This hobby can be a lonely business.  
The results were, more or less, lackluster but I didn't feel to bad.  
I think it was to be expected. Being an amateur who doesn't  code that much, the results could never have been stellar.  
All in all it was what I expected to be.  
  
Until I looked inside the `service_monitoring` project.  
*Sourcery* was as indignant as an unfeeling, unthinking tool can be.  
It was so bad it didn't suggest much in the way of changes, only some earnest calls to revise
and refactor that unholy mess.  
Had I remembered that, apparently, I wrote long and often about the build of
that app, I might've shed some light on that the dense, dark, wall of code,  that,
if meant to be used as obfuscation,  
it wouldn't have been more successful.  
  
I couldn't understand the `main` function.  
The `main` function!  
At my level of coding sophistication, everything it does is call all other modules in
order.  
The fact that I wrote a `main` function that was totally opaque to my, five or six
months older self, would have seemed fantastic to me.  
Still, here we were.  
  
With my pride a little piqued, I set about to make some betterments to the code.  
The equivalent of a coat of paint and a Spring cleaning as it were.  
More cosmetic than structural, I thought.  
Of course what I didn't know, but do now, is that one of the things that makes
computer engineering challenging, as opposed to tinkering idly on projects that
tickle your fancy, is the fact that, most serious code is propping things up in
companies and can't be rewritten on a whim.  
You may have the scion of Hell living in your codebase, but you'll just have to find ways of passing time together.  
  
Because the simple, noble, morally righteous, option of starting afresh, is totally out of
the question.  
  
I don't envy those poor bastards.  
We, the tinkerers, on the other hand, don't have any such qualms.  
So I quickly concluded that that `service_monitoring` project had to go.  
  
The first, and more challenging task of refactoring, was to understand what border cases were there, that
justified the gongorism of the code.  
  
This thought represented my earnest desire, that, through inexperience and enthusiasm, I had been led astray into a wilderness of
complexity that, in the end, if abstruse, showed attention to detail and limit
conditions.  
Unfortunately that was not what I found.  
  
The app did the things that most simple apps do. Didn't had no special affinity
for the quirky or the subtle, it thought and provided solutions for only the more
obvious scenarios. If you muscled through the spaghetti code, you'd understand
that the only thing worthy of note on this app, was how unfathomable it was.  
Like a stupid person who acts mysteriously.  
  
Truth be told, the signs were there. It's use was unbearably brittle. What would
work today, wouldn't work tomorrow or for all cases.  
The debugging was dim and grey, the documentation, was nonexistent.  
Even though I did find the time to write six, six, posts on the matter here, and
then  promptly forget about it.  
Had I know  that this trove of information was here, I probably would had have been
much more conservative on my *remodeling*.  
As I didn't, I basically rewrote it.  
Some ideas are present in both projects, but that's just because I'm not very creative and I tend to repeat things
to the same people all the time. Even when not drunk.  
  
It was for the best I think. I can now look at it and understand what it does.  
Anyone can. And that's a good thing.  
Here are some examples:
  
  
<h3><u>1 - Deleting Services</u></h3>  
  
  
Now, to be frank, I'm doing some conjecturing, I'm, brazenly making assumptions on what I wanted, some months ago,
to do with that code; when it, probably, doesn't warrant any kind of interpretation.  
MY conclusions are, wholly, my own. They don't oblige my old code to anything.
We're complete strangers, and your guess is as good as mine.  
  
But a modicum of exegesis is in order ... I, after all, did wrote it. Much to my
chagrin.  
  
What I think I was trying to do was: to deal with services deletion and the ungodly mess that updating a json file
became.  
I was using it, the json file, as the single source of truth for the app.  
Why a json file you ask? The truth is that I was looking to do something
different from my CRUD apps.  
Something new; exciting... and I had heard good things of this *json* business. Maybe it could help.  
In short, it was a solution thought in a whim, for all the wrong (more non-existent), 
reasons and with no thought put into it.  
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
  
  
Nothing of this, except the *Systemd* commands, through no fault of my own, worked
as expected. It kept glitching and I, for some, reason, never quite got around
to understanding dictionaries and *json*, until very recently.  
So I was outside looking in.  
  
Today I broke the function into small, simpler bits. Separated database
operations from service interactions, did away with the godforsaken *json* file
and put the data in the smallest, cutest, *MySQL* database ever.  
Got a function just for the *systemd* commands and commented profusely the code, knowing
now that, in the future I won't remember to check this diary for information.  
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
I also rewrote the`'main` function, that,  
from all things that I don't understand,  
it's the one I don't understand the most.  
