---
title: Cli Apps Database App. Required Loop
date: 08-08-2023 09:14
mainfont: Iosevka
fontsize: 13pt
---

I felt a bit guilty because of my last posts' laziness. I said that I would do
just one post on loops, since they are similar.  
Well, that is bullshit.  
First, the object of this exercise is not to explain my projects to anyone, but
for me to have some kind of memory, not only of code, there's *Github* for that,
but also of what I wanted to do, and the challenges I faced and how I overcame
them. If in fact, I did.  
So, I need to be thorough because, when I look at this project, five months from
now, I won't remember what possessed me to do it, how I came at the code solutions
that I used and what was my thought process. I should, at the very least, explain
the code, if the comments have not done that already, so I am able to reuse it
with a degree of understanding.  
And here I am. Ready to fulfill my historical duty to myself.  
  
<strong><em>WITNESS ME!</em></strong>  
  
I'm going to start by stealing the beginning of the *Cli Apps Database App.
Location Loop*, which started life as *Cli Apps Database App. Function Loops*
when I was feeling too cool to write.  
It explains the *main* and *use_paths* modules, which is required reading for
understanding how the loop fits in the app's logic.  
I'm doing this for you, future reader, as there's no guarantee that you'll read
the *location loop* post first. You're as much deserving of knowledge as the
people who got the order right.  
  
I will show the function loops that query the `allinfo` data collection.  
They are started if the user responds positively to any of the *req_decision* or
*loc_decision* questions. The first fires the `required_loop`, (dedicated to
retrieving information on dependencies), and the second, the `location_loop`,
(aimed at finding and showing folder and files content). I'm going to post the
entirety of the *main* module, so you can understand when and where this things
come into play:
  
  
<h4><u>main</u></h4>  
  
```python
@click.command()
@click.argument("keywords", nargs=-1)
@click.option("-q", "--queries", multiple=True, is_flag=False, flag_value="query", default=[])
@click.option("-i", "--ids", multiple=True, is_flag=False, flag_value="id", default=[], type=int)
@click.option("-n", "--names", multiple=True, is_flag=False, flag_value="query", default=[])
# @snoop
def get_query(keywords, queries, ids, names):
    """
    Because we want to deal with complex queries, we'll get, in the same query, an
    indefinite number of keywords, queries for natural language search, several
    id's and names. This module will receive the information and send output to
    different functions.
    """
    da = os.getenv("DA")
    # This the management code block. Each option/argument, has a allocated management
    # function, that's tasked of cleaning the input and making the db calls for each
    # query. Some will ask you if you want to see a given type of data, regardless if
    # you chose it in the command line or not. Others are more reserved.
    keys = kwd_mngmnt(keywords)
    if queries != ():
        queries_mngmnt(queries)
    if ids != ():
        ids_mngmnt(ids)
    names_mngmnt(names)

    # This is the initiation block. When you get a new query, that's what has to happen.
    filelst = os.listdir(da)
    # The names of pickled files that are created by the management modules.
    if "qlst.bin" or "klst.bin" or "ilst.bin" or "nlst.bin" in filelst:
        # Checks to see what files, from the above list, are present in the directory.
        checkinfo()
        # Joins the information in one document called 'allinfo'.
        aggregate_info()
        # Uses 'fzf' to let the user check the results and choose what he wants to see from
        # the output.
        srch_allinfo()
        # Shows a prettified version of the chosen information.
        show_info(f"{da}data_files", "PACKAGES IN DATA_FILES")
        # # Two questions: do you want to see file dependencies or their location?
        re = req_decision()
        lc = loc_decision()

        # # Depending on the answer, you'll be sent in a loop of functions that'll expose you
        # # to the information you wanted.
        if re == "y":
            required_loop()
        if lc == "y":
            location_loop(f"{da}data_files")

    # # This thing produces binary files like a motherfucker. Cleaning is in order.
    delete_all_files()


if __name__ == "__main__":
    get_query()
```
  
  
The loop structure is defined in a module called <strong><em>use_paths</em></strong>, because that's
what they really are: the directions that define of what's used in *database_app*.  
This is a heavily commented file, and I'll just let it speak for itself.  
  
  
<h4><u>use_paths</u></h4>  
  
```python
"""
Module that define the functions that'll be served
depending on user's choices. If the user chooses
'locations' or 'dependencies', it'll have different
information presented to him. We define what
information it is and in what way is shown.
At the moment I put a limit of 10 in the capacity to
ask again the same type of question. But when I feel
more sure about the workings of this solution I would
like it to be limitless.
"""
import os

import snoop
from dotenv import load_dotenv
from snoop import pp

from location import dislocation, package_location, show_dirpath
from methods import loc_decision, pip_info, req_decision, yay_info
from required_by import choice_processing, collect_deps_info, get_lst, show


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])
load_dotenv()


# @snoop
def required_loop():
    """
    This is the structure of the loop to run
    if user only wants to see dependencies.
    The basic concept is for the user to be
    able to repeat its dependencies searches
    as much as he wants, going as deep as he
    likes. You can leave the loop if you don't
    answer the questions or, by the program's
    will, if there's a problem with the code.
    """
    da = os.getenv("DA")

    # The first call to dependencies is done when
    # there's only package files in 'data_files'.
    # After that is always in 'required_files'. We
    # needed to have a first look at the files still
    # in 'data_files'. That's the reason why there's
    # a get_lst() call before the loop.
    out = get_lst(f"{da}data_files")
    if out == "y":
        for i in range(10):
            show()
            choice_processing("choice_deps.bin")
            srch = collect_deps_info()
            yay_info(srch)
            pip_info(srch)
            # So as not to break the loop, we took out the SystemExit
            # we had for when there was an error, and replaced it with
            # 'return' statements. If there's an error get_lst()
            # returns 'n', if everything went correctly, it outputs 'y'.
            # This way the flow is controlled when designing the loop,
            # making it easier to change when needed.
            gl = get_lst(f"{da}required_files")
            if gl != "y":
                break

    # After the loop has ran, we ask the user if he wants to see
    # the packages locations. In the 'location' loop it's the
    # other way around.
    loc = loc_decision()
    # If it starts after the 'required_loop' having ran, we know that
    # the last information is in 'required_files'. So we set the
    # 'location_loop' location to it.
    if loc == "y":
        location_loop(f"{da}required_files")


if __name__ == "__main__":
    required_loop()


@snoop
def location_loop(folder):
    """
    Loop for the 'location' module. Here,
    because we don't have to create data
    from one location to another, we can
    leave it for the callers of the loop
    the decision on what folder to use.
    """
    for i in range(10):
        inner = package_location(folder)
        if inner != "y":
            break
        dislocation()
        show_dirpath()

    req = req_decision()
    if req == "y":
        required_loop()


if __name__ == "__main__":
    location_loop()
```
  
  
<h3><u>REQUIRED LOOP</u></h3>  
  
  
Most of the functions that the `required loop` uses are in the *required_by* module.  
As you can tell, I spend far too little time thinking on what to name things,
and that, sometimes, comes back and bites me in the ass.  
From the list of packages initially chosen, we'll discover what are their dependencies.  
We start with:  
  
  
<h4><u>get_lst</u></h4>  
  
Iterates through the files in *data_files* or *required_files*, and looks for information on dependencies,
if it finds any it adds the package name and the dependency name in a tuple and stores it in a list.  
If you're keen observer, you'll notice that *get_lst* returns <strong><em>n</em></strong>, in case of error and <strong><em>y</em></strong>, if everything goes according to plan. These return codes are then read by *use_paths*, that will stop the loop if anything's wrong.  
  
```python
def get_lst(folder):
    """
    Iterates through the files in 'folder'
    and looks for information on dependencies,
    if it finds that package has dependecies,
    it adds the package name and the dependecy
    name in a tuple and stores it in a list.
    """
    cwd = "/home/mic/python/cli_apps/cli_apps/database_app"
    console = Console()

    # I'm putting this here in case if get_lst() doesn't
    # find dependecies, there'll be no 'spltlst.bin' for
    # show(). It searches for the file at the  beginning,
    # looking for a undeleted 'spltlst.bin' from a past
    # run, if it finds it,  it delestes it.
    # In case this run fails and show() uses the old file.
    if "spltlst.bin" in os.listdir(cwd):
        os.remove(f"{cwd}/spltlst.bin")

    fils = os.listdir(folder)

    lst = []
    for file in fils:
        with open(f"{folder}/{file}", "r") as f:
            fil = f.readlines()
            for f in fil:
                # Format found in files created by 'yay -Qi'
                if f.startswith("Required By     : "):
                    if f != f.startswith("Required By     : None\n"):
                        # The title and spaces occupy 18 px, the 20 px
                        # its that value and a small margin of confort.
                        if len(f) > 20:
                            # Deletes the title from the line. We now have
                            # only the dependecies names.
                            deps = f[18:]
                            lst.append((file, deps))
                # Format found in files created by 'pip show'
                if f.startswith("Required-by: "):
                    if len(f) > 15:
                        deps = f[13:]
                        lst.append((file, deps))

    # The info comes with linebreaks, we strip them and eliminate
    # entries with only "None".
    cleanlst = [(a, i.strip()) for a, i in lst if i != "None\n"]

    # If nothing's there, it'll be mostly, for not having found dependecies.
    # We delete the files of 'data_files' and return 'y'. This value wiçç be
    # picked up in the 'use_cases' module, and they'll break the loop.
    if cleanlst == []:
        console.print("T[bold #E48586]         required_by.get_lst(): The chosen packages are required by none.")
        return "n"
    else:
        # If we find dependencies, we look for empty spaces in the strings we
        # collected. If there's empty spaces it's because its a list of dependecies.
        # We split the string so as to create a list.
        spltlst = []
        for tup in cleanlst:
            if ", " in tup[1]:
                nw = (tup[0], tup[1].split(", "))
                for n in nw[1]:
                    if n == "":
                        nw[1].remove(n)
                spltlst.append(nw)
            else:
                nw = (tup[0], tup[1].split(" "))
                for n in nw[1]:
                    if n == "":
                        nw[1].remove(n)
                spltlst.append(nw)

        with open(f"{cwd}/spltlst.bin", "wb") as f:
            pickle.dump(spltlst, f)

        return "y"
```
  
  
<h4><u>show</u></h4>  
  
Visualizes the results.  
  
```python
def show():
    """
    Visualizes the results.
    We use mostly *Rich* to views results, except
    in the *input* method. Although 'rich' has
    their own implementation of 'input', it shows
    the prompt, one line below the text and pressed
    to the border of the screen.
    """
    da = os.getenv("DA")

    if "spltlst.bin" in os.listdir(da):
        with open(f"{da}spltlst.bin", "rb") as t:
            deps = pickle.load(t)

        if deps != []:
            # 'numbered_deps' will collect the id'd version of 'deps' this module will create.
            numbered_deps = []
            console = Console()
            console.print(
                Padding("[bold #E9FFC2]DEPENDENCIES[/]", (3, 10, 0, 10)),
                justify="center",
            )
            for i in range(len(deps)):
                if deps[i][0]:
                    console.print(
                        Padding(f"[bold #AAC8A7]\n{deps[i][0][:-4]}[/]", (0, 10, 0, 10))
                    )
                if type(deps[i][1]) == list:
                    for idx, t in enumerate(deps[i][1]):
                        # collects a dependency id made of the index of the chosen package,
                        # plus the index of the dependecy. This permits us to know what is
                        # the package and dependecy name.
                        numdp = [f"{i}{idx}", f"{t}", f"{deps[i][0][:-4]}"]
                        numbered_deps.append(numdp)
                        console.print(
                            Padding(
                                f"[bold #FFD6A5]\[{i}{idx}] - [/][bold #E9FFC2]{t}[/]",
                                (0, 10, 0, 14),
                            )
                        )
                else:
                    console.print(
                        Padding(
                            f"[bold #E9FFC2]\[{i}0] - {deps[i][1]}[/]", (0, 10, 0, 14)
                        )
                    )
                    numdp = [f"{i}0", f"{deps[i][1]}", f"{deps[i][0][:-4]}"]
                    numbered_deps.append(numdp)
            print("\n")
            choice_deps = input(
                style(
                    "          Choose the dependecies you want to see. Press Enter to quit. ",
                    bold=True,
                    fg=(160, 196, 157),
                )
            )
            console.print("\n")

            if choice_deps != "":
                with open(f"{da}choice_deps.bin", "wb") as g:
                    pickle.dump(choice_deps, g)
                with open(f"{da}numdeps.bin", "wb") as f:
                    pickle.dump(numbered_deps, f)
        else:
            console.print(
                "[bold #FFD6A5]         rrequired_by.show():[/bold #FFD6A5] [bold #E48586]'spltlst.bin' is an empty list."
            )
```
  
  
This is what you'll see:  
  
  
![Required](/home/mic/python/cli_diary/cli_diary/imgs/deps.png)
  
  
<h4><u>choice_processing</u></h4>  
  
This is, by far, the most useful function of the bunch. So much so ,that I'm
going to put it somewhere central, where all the other projects can get to it.  
What it does is simple, but has some steps, and if you can outsource it, you
will.  
It turns a string with several elements, in a list of strings.  
They can be separated by spaces, commas and spaces, or commas only, it *listifies* them all.  
At the moment, it reads from a binary and outputs another. But I think I'm
going to change that to returning the list. There's no time delay or memory
usage that justifies returning a binary.
  
```python
def choice_processing(binary):
    """
    As "choice_deps" comes in as a string, that may contain one
    or more choices, and because the user can write its input
    in several ways, will try to predict some of them, and handle
    the input so to have a list of dependecies in the end.
    """
    da = os.getenv("DA")

    if f"{binary}" in os.listdir(da):
        with open(f"{da}{binary}", "rb") as f:
            choices = pickle.load(f)

        if " " in choices:
            choice = choices.split(" ")
        if ", " in choices:
            choice = choices.split(", ")
        if " " not in choices:
            choice = choices
        if "," in choices:
            choice = choices.split(",")

        with open(f"{da}choice.bin", "wb") as g:
            pickle.dump(choice, g)
    else:
        console = Console()
        console.print(
            f"[bold #FFD6A5]         required_by.choice_processing():[/bold #FFD6A5] [bold #E48586]Couldn't find the {binary} file."
        )
        raise SystemExit
```
  
  
<h4><u>collect_deps_info</u></h4>  
  
Collects information on the chosen dependencies.  
  
```python
# @snoop
def collect_deps_info():
    """
    Collects information on the chosen dependencies.
    """
    da = os.getenv("DA")

    with open(f"{da}numdeps.bin", "rb") as f:
        numdeps = pickle.load(f)
    with open(f"{da}choice.bin", "rb") as g:
        choice = pickle.load(g)

    srch = [
        (numdeps[i][1], numdeps[i][2])
        for i in range(len(numdeps))
        if numdeps[i][0] in choice
    ]
    # This will add a code to the 'srch' list that'll allow 'yay_info'
    # and 'pip_info' to know what is the internal structure of 'srch',
    # that is very different from that that is created by 'srch_allinfo'
    # when called by 'main'.
    srch.append("req")
    return srch
```
  
  
And here stops the iteration of the loop. There's still some things I need to
change.  
Now, after choosing to follow a package dependencies, if its choice is required by nothing, the loop stops.  
I would like to get it back to the beginning, for the user to choose another package, if he wants it.  
It's in my *TODO's* list.
