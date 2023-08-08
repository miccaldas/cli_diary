---
title: Cli Apps Database App. Methods
date: 08-08-2023 13:33
mainfont: Iosevka
fontsize: 13pt
---

I realized now that I left something unsaid. I didn't speak on the lowly helper
methods, that help to shape the loops and the initial process.  
Some you already know, as the ones that compose the initial processing of
information, but there are two or three I didn't mentioned. This is their time.  
  
  
<h4><u>input_decision</u></h4>  
  
This small function, and the next that's even smaller, proved themselves so
useful and versatile that, if I'm not transplanting them as they are, they
deeply inspired me to create their more generalist cousins, to use in other
projects.  
Although I'm using mostly *Rich* to format the output, their `input` solution is
shit. First the prompt appears a line below the prompt text and second, it's
completely squashed against the left margin of the terminal wall. I don't know
if it's like this on purpose or if I'm missing something. But as it is, I'm not using it.  
Instead I used `click.style`. A known quantity, that never disappoints.  
As you can see, you can change the prompt text and color of the string.  
What more do you need?  
  
  
```python
def input_decision(prompt, color=(160, 196, 157)):
    """
    Template for inputs, asking the user
    for a decision. 'Rich' doesn't work
    correctly with input. Has to be 'click'.
    """
    dec = input(
        style(
            f"          {prompt} ",
            # fg=color,
            bold=True,
        )
    )

    return dec
```
  
  
<h4><u>print_template</u></h4>  
  
Now comes a very similar concept, but for printing strings. Here, because it's
simpler, we can use *Rich* again.  
  
```python
def print_template(text, style="bold #AAC8A7"):
    """
    Template to format string presentation.
    """
    console = Console()
    console.print(Padding(f"[{style}][+] - {text}[/]", (0, 3, 0, 10)))
```
  
  
<h4><u>subcall</u></h4>  
  
This is meatier terrain. Although gradually and in baby steps.  
The two functions after this one, `yay_info()` and `pip_info()`, have a lot of 
subprocess operations, all very much alike. This function, creates a template
that simplifies the creation of the command.  
It basically uses the commands `yay -Qi` and `pip show`, both information
queries of their respective databases, to get data on the packages chosen by the
user. So it's just a matter of asking a question and sending it to a text file.  
The components are:
  
1. **`shellcmd`** - This can be a *yay* or *pip* command.  
2. **`flnm`** - The name of the file.  
3. **`fldr`** - Folder name. Could be *data_files* or *required_files*.  
4. **`flnmid`** - A prefix indicating if it comes from *yay* or *pip*.  
5. **`stderr`** - Both apps produce error outputs that can be, both, informative
   and excessive. Sometimes stderr will go to a file, others to `/dev/null`.  
  
```python
def subcall(shellcmd, flnm, fldr, flnmid, stderr):
    """
    Makes 'subprocess' calls for 'yay_info'
    and 'pip_info'. To simplify the code.
    """
    da = os.getenv("DA")

    cmd = f"{shellcmd} {flnm} > {fldr}/{flnm}{flnmid} {stderr}"
    subprocess.run(cmd, cwd=da, shell=True)
```
  
  
<h4><u>yay_info</u></h4>  
  
Extracts information from the `yay -Qi` command.  
Although this may seem trivial at first, it has a set of small details, that
make it much more complex than I initially anticipated. On the bright side, it
has shown to be trustworthy and reliable. For which I'm grateful.  
As usual, there's a lot of comments to guide through it, but maybe just a word
or two on the fact that; because there needs to be two data folders and that
some loops start in one and end in another; it's important always to refer what
folder we are using. As you do different things in different places. Because of
this, all information that comes through this data gathering functions, comes
tagged with a reference to the destination folder. This information may be
important to understand some of the comments.  
  
```python
def yay_info(srch):
    """
    Module to extract information on
    packages from 'yay'. There are
    several types of input that come
    to this function, if it comes
    from fzf, its a string that needs
    to be evaluated to a list, if it
    comes from 'required_by', it could
    a string or a list of strings.
    """
    da = os.getenv("DA")

    shellcmd = "yay -Qi"
    # This sends stderr output to a file. The initial reason for this was
    # Pip's penchant for outputting an enormous quantity of warning messages
    # when you call 'pip show'. To hide it, the first thought was to send it
    # to /dev/null. Then I thought that, in the midst of the spurious messages,
    # could be something that's important. Besides, I don't want to loose yay's
    # output. So a text file it is.
    stderr = " 2>> error_files/yay_stderr.txt"
    # If 'srch' comes from 'srch_allinfo', will need to evaluate the
    # output, as 'fzf' presents a list as a string. To id it,
    # 'srch_allinfo' adds, at the end of 'srch', the string 'ai'.
    # This means the format of 'srch' in this case is two element tuple
    # with a list of tuples in string format as its first element, and
    # the code 'ai' as its second.
    if srch[-1] == "ai":
        fldr = "data_files"
        datapth = f"{da}{fldr}"
        flnmid = "_yay"
        # This deletes the contents of 'data_files'. It's done to ensure
        # there's no contamination between requests, whilst giving time
        # enough to play with the data. Until a new request comes in.
        cmd = f"/usr/bin/trash-put {datapth}/* 2> /dev/null"
        subprocess.run(cmd, shell=True)
        # In this case, 'srch' will be a two member tuple; the first, a
        # string with information, the second, a code to identify its
        # provenance. We only need the first. 'srch' comes from 'pyfzf',
        # which means
        for i in srch[0]:
            # 'i' is a tuple, but 'pyfzf' passes it as string. We have to
            # convert it to tuple. That's what eval() is for.
            selection = eval(i)
            # To ensure we looked thouroughly through 'Yay's database,
            # we'll try to look for packages in two of the ways they're
            # usually written. In this case, if the 'srch' request has a
            # package that start's with 'python-':
            if selection[1].startswith("python-"):
                # We try with this name first.
                flnm = f"{selection[1]}"
                subcall(shellcmd, flnm, fldr, flnmid, stderr)
                # Then we'll check if the file created with its name has a
                # file size of 0. This means, most probably, that it didn't
                # find the package.
                if os.stat(f"{datapth}/{flnm}{flnmid}").st_size == 0:
                    # If it didn't find the package, we try to search for it
                    # without the "python-" prefix.
                    flnm = f"{selection[1]}[7:]"
                    subcall(shellcmd, flnm, fldr, flnmid, stderr)
            else:
                # Here, regarding filename, it's the opposite of above. We
                # start with packages that don't have a 'python-' prefix,
                # and try to add it if they fail to be found.
                flnm = f"{selection[1]}"
                subcall(shellcmd, flnm, fldr, flnmid, stderr)
                if os.stat(f"{datapth}/{flnm}{flnmid}").st_size == 0:
                    flnm = f"python-{selection[1]}"
                    subcall(shellcmd, flnm, fldr, flnmid, stderr)

    # 'srch' originating in 'required_by', will have a last entry called 'req'.
    if srch[-1] == "req":
        fldr = "required_files"
        datapth = f"{da}{fldr}"
        # This deletes the contents of 'required_files'. This is to ensure
        # there's no contamination between requests, whilst giving time
        # enough time to play with the data. Until a new request comes in.
        cmd = f"/usr/bin/trash-put {datapth}/* 2> /dev/null"
        subprocess.run(cmd, shell=True)
        # This makes it so we won't loop through the 'req' entry.
        for s in srch[:-1]:
            # For notess on how 'flnm' is defined, see above comments
            # from lines 142 to 161.
            if s[0].startswith("python-"):
                flnm = f"{s[0]}"
                flnmid = f"_{s[1]}"
                subcall(shellcmd, flnm, fldr, flnmid, stderr)
                if os.stat(f"{datapth}/{flnm}{flnmid}").st_size == 0:
                    flnm = f"{s[0]}[7:]"
                    subcall(shellcmd, flnm, fldr, flnmid, stderr)
            else:
                flnm = f"{s[0]}"
                flnmid = f"_{s[1]}"
                subcall(shellcmd, flnm, fldr, flnmid, stderr)
                if os.stat(f"{datapth}/{flnm}{flnmid}").st_size == 0:
                    flnm = f"python-{s[0]}"
                    subcall(shellcmd, flnm, fldr, flnmid, stderr)
```
  
  
<h4><u>pip_info</u></h4>  
  
The same thing but for *pip*. And much simpler, thank God for that.  
Just the fact that we don't need to try two different title options,
makes everything much easier.  
  
```python
def pip_info(srch):
    """
    Module to extract information on
    packages from 'pip'.
    """
    shellcmd = "pip show"
    stderr = " 2>> error_files/pip_stderr.txt"
    # If 'srch' comes from 'srch_allinfo', will need to evaluate the
    # output, as 'fzf' presents tuples as strings. To id it,
    # 'srch_allinfo' adds, at the end of 'srch', the string 'ai'.
    # This way we'll know we can't process it without evaluating it.
    if srch[-1] == "ai":
        fldr = "data_files"
        # In this case, 'srch' will be two member tuple; the first, a
        # string with information, the second, a code to identify its
        # provenance. We only need the first.
        for i in srch[0]:
            selection = eval(i)
            flnm = f"{selection[1]}"
            flnmid = "_pip"
            subcall(shellcmd, flnm, fldr, flnmid, stderr)
    # The 'req' code tell 's us that it's a request from 'required_by'.
    # This means that is a list of tuples with a chosen package as
    # second member, and one of its dependencies as the first.
    if srch[-1] == "req":
        fldr = "required_files"
        # The last element of 'srch' is the provenance code 'req'.
        # We don't need it for this.
        for s in srch[:-1]:
            flnm = f"{s[0]}"
            flnmid = f"_{s[1]}"
            subcall(shellcmd, flnm, fldr, flnmid, stderr)
```
  
  
<h4><u>delete_all_files</u></h4>  
  
Last but by no means the least is `delete_all_files`, which does more or less
what it says in the title.  
The binary files that I created with abandon, as with much other cases of
profligacy, end up being a pollution problem.  
Not only they occupy real-estate, they interfere with any attempt to read the
updated versions.  
Cleanliness is necessary and virtuous.  
But we can't delete too soon, even after showing the information to the user.
He might have more questions, so it must be kept until a new query comes.  
This module is controlled by `main` and used in the end of all processes.  
  
```python
def delete_all_files():
    """
    Deletes all binary files in present directory and 'mngmnt'.
    """
    da = os.getenv("DA")
    mn = os.getenv("MN")

    cwd_fls = os.listdir(da)
    mngmnt_fls = os.listdir(mn)
    cwd_bins = [i for i in cwd_fls if i.endswith(".bin")]
    mngmnt_bins = [i for i in mngmnt_fls if i.endswith(".bin")]
    if cwd_bins != []:
        for b in cwd_bins:
            os.remove(f"{da}{b}")
    if mngmnt_bins != []:
        for b in mngmnt_bins:
            os.remove(f"{mn}{b}")
```
