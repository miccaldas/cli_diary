---
title: Cli Apps Database App - Data Reception
date: 07-08-2023 02:43
mainfont: Iosevka
fontsize: 13pt
---


My aim with this post is to make, to use what I think is architectural jargon, a
<strong><em>descriptive memory</em></strong>, of a phase that comes after
data management, but before proper data analysis.  
You'll notice a profuse use of pickled files. Even if a bit notorious and, in my
view, unjustly maligned, they have two qualities that trump, for my use case,
all objections:  
  
1. <strong>They provide availability.</strong>  
   Suddenly you don't have to run *n* functions to get a bit of information you
   just saw but forgot. The data is there, easy to access.  
2. <strong>They lower memory use.</strong>  
   Not by themselves, mind you, but if I have the output of my last three or
   four functions, I don't need to run them all to be able to power the fifth.  
   I'll just feed it the results of the fourth, in a handy python object format,
   (no more wrestling with files in string format and try to turn them to an
   iterable you can use!), and my senescent computer won't even notice.  
  
Back to *database_app* initial path. We've received data, it's true, but at this moment we don't have an holistic
view of the processed information.  
We need to check the current directory to see if it contains files
produced by the management modules. If it finds at least one, the process continues.  

```python
    filelst = os.listdir(os.getcwd())
    if "qlst.bin" or "klst.bin" or "ilst.bin" or "nlst.bin" in filelst:
```
  
These are the subsequent modules:  
  
<h4>checkinfo</h4>  
  
 It'll check what files, from the list above, are there, and make a list of their names.  
  
```python
def checkinfo():
    """
    We'll check what 'bin' files there are,
    and make a list of their names.
    """
    filelst = os.listdir(os.getcwd())
    srch_results = ["qlst.bin", "klst.bin", "ilst.bin", "nlst.bin"]
    results = [i for i in srch_results if i in filelst]

    return results
```
  
<h4>aggregate_info</h4>  
  
From the list produced by *checkinfo*, *aggregate_info* will read the files and
join their content in one file.  
You'll notice the use of variables instead of indexes in the list comprehension,
I used to think that this was cool as fuck, still do, but it's a finicky
solution, it creates a lot of errors because of wrong number of items. So, now
I'm back to using indexed values, like the regular folk.  
  
```python
def aggregate_info():
    """
    Collects and merges file contents produced by 'search'.
    """
    fls = checkinfo()
    allinf = []

    for f in fls:
        with open(f, "rb") as fl:
            partial = pickle.load(fl)
            if partial != [] and partial != "":
                for i in partial:
                    # This code allows to merge to an existing list,
                    # elements of another.
                    allinf += [i]
    allinfo = [(a, b, c, d.strftime("%d/%m/%Y"), e, f, g, h, i, j) for a, b, c, d, e, f, g, h, i, j in allinf]

    with open("allinfo.bin", "wb") as f:
        pickle.dump(allinfo, f)


if __name__ == "__main__":
    aggregate_info()
```
  
<h4>srch_allinfo</h4>  
  
After years of not getting *fzf*, I'm now, officially hooked. I'm implementing
it whenever it makes sense, in my projects. This is just another case of just
that.  
By now we have all the answers for the user's queries, and some things that the
MySQL's natural search sees fit to include. This usually is an extensive array
of information, probably more than the user wanted. This module uses *fzf* to choose from what we gathered, what he really wants to see.  
You'll see mentions of two functions, *yay_info* and *pip_info*. These are
modules that query the *Pacman/AUR* and *Pip* package databases, respectively,
and get information on the packages chosen by the user.  
  
```python
def srch_allinfo():
    """
    Searches 'allinfo' with fzf and, if needed,
    collects user selections.
    """
    fzf = FzfPrompt()

    with open("allinfo.bin", "rb") as f:
        allinfo = pickle.load(f)

    sr = fzf.prompt(allinfo)
    srch = (sr, "ai")

    yay_info(srch)
    pip_info(srch)


if __name__ == "__main__":
    srch_allinfo()
```
  
<h4>show_info</h4>  
  
This module selects, cleans and shows the information selected in
*srch_allinfo*. The function needs two arguments:
  
1. <strong>Folder</strong>  
   Where *yay_info* and *pip_info* put the text files with data on the packages.
   There's two possible locations:  
   1.1. *data_files* - Used in the beginning of the query process, when no
   analysis has taken place.  
   1.2 *required_files* - Where are stored the package information that had more
   than one utilization, but it's still part of the session.  
2. <strong>Title</strong>  
   What will be the title for the screen with the data presentation. By default,
   in this stage, it usually is *PACKAGES IN DATA FILES*.  
  
Before opening the files, we check for file size to see if they're empty, the
files are always produced, even if the database queries come back empty.  
We use `os.stat()` to check for file size and, if true, delete them. The truth
is that this functionality is a bit of a fossil, I created a way to deal with empty
files upstream. But as I am a belt and suspenders kind of guy, I leave it here.  
We use *Rich* to present the results and what's left to say, it's said in the
comments in the code. So I'll just post that.  
  
```python
def show_info(folder, title):
    """
    We look in the data_file, to see what packages have
    information available on them, we create links of
    their location, so we can show their content. We use
    Rich to get a better look.
    """
    console = Console()

    cwd = os.getcwd()
    data = f"{cwd}/{folder}"
    file_names = os.listdir(data)

    # List to house the links that'll create based on 'file_names'.
    lnks = []
    for name in file_names:
        lnk = f"{data}/{name}"
        lnks.append(lnk)

    for lnk in lnks:
        # Checking for file size, if it's zero, we pop it
        # out of the list.:
        stt = os.stat(lnk)
        if stt.st_size == 0:
            console.print(Padding(f"[bold #E48586]The file {lnk} as 0 size. Deleted.", (3, 10, 0, 10)))
            idx = lnks.index(lnk)
            lnks.pop(idx)

    # List to house the output of all the chosen files.
    fullcont = []
    for t in lnks:
        with open(t, "r") as f:
            cont = f.readlines()
            content = [i.strip() for i in cont]
            # The info of one package appeared immediately after the other.
            # List's 'insert', adds a entry at a given position, without
            # replacing nothing.
            content.insert(0, "\n")
            # The '+=' formulation, between lists, makes it so the first
            # absorbs the elements of the second one.
            fullcont += content

    console.print(
        Padding(f"[bold]{title}[/]", (3, 10, 0, 10)),
        justify="center",
    )
    for line in fullcont:
        if line.startswith("Location: "):
            console.print(Padding(f"[red]{line}[/]", (0, 10, 0, 10)))
        else:
            console.print(Padding(f"{line}", (0, 10, 0, 10)))

    console.print("\n\n")


if __name__ == "__main__":
    show_info()
```
This is how it looks like for a small search for two markdown viewers:  
  
![dbapp_output](/home/mic/python/cli_diary/cli_diary/imgs/mgc.png "Output")
  
Below this output we'll print two input queries that'll direct us to the
analysis part of the app. But that's for another day:
  
```python
def req_decision():
    """
    Asks the user if he wants to see the
    dependecies of any package.
    """
    console = Console()
    required = input_decision("Do you want to explore one of these package dependecies?[y/n] ")

    if required == "y":
        return "y"


if __name__ == "__main__":
    req_decision()


# @snoop
def loc_decision():
    """
    Asks the user if he wants to see the
    folder contents of a package.
    """
    console = Console()
    ailocation = input_decision("Do you want to see more on the location of these files?[y/n] ")
    if ailocation == "y":
        return "y"


if __name__ == "__main__":
    loc_decision()
```
  
  
![dbapp_questions](/home/mic/python/cli_diary/cli_diary/imgs/questions.png "Questions")

