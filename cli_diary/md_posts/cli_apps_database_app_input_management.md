---
title: Cli Apps Database App - Input Management
date: 29-07-2023 02:10
mainfont: Iosevka
fontsize: 13pt
---


For a long time the *cli_apps* project never had a database app. And by that I
mean the usual CRUD I do for all my projects. It was a project where all
interest for me was in automations, not to be used as a means of personal
perusal. Then I started thinking that that might be because the old means of searching
were not creating interesting output in this database. If
I could make it with more questions than only the initial one and cross-examine other
information, even from the same database, that would create a more engaging
proposition.  
With that in mind, I started building a program that could:  
  
1. Simultaneously collect information as:  
   1.1 Keywords. To define as many tags as I wanted.  
   1.2 Names. To search by how many program names I wanted.  
   1.3 Id's. Search by how many id's I wanted.  
   1.4 Queries. Make as many natural searches as required.  
  
2. Aggregate all information collected.  
   I don't want to have one output for *keywords* and another for *queries*. I want
   one view for all the information.  
  
3. Add other sources of information beyond the database.  
   Even if I don't want to keep this information, I should have access to
   it.  
  
4. Presented this information with a modicum of style.  
   It should be pretty to look at.  
  
Not surprisingly, it's point 4, the one that is most lacking at this moment. But,
I'll try once more to make it less visually horrible.  
In order for me not to get lost in a over-long post, I intend to split it in
two: one for input management and another for the analysis and enrichment of the information. After we
have all the input cleaned and organized.  
  
  
<h3>DATA COLLECTION</h3>  
  
I felt that a command line solution for this idea would be a perfect fit. With
all the alternatives, a TUI would have been a slow slog through menus and
clicks. This way you get all the asks in one fell swoop.  
I'm using [Click](https://click.palletsprojects.com/en/8.1.x/), as usual, and I
structured the data collection the following way:  
  
```python
@click.command()
@click.argument("keywords", nargs=-1)
@click.option("-q", "--queries", multiple=True, is_flag=False, flag_value="query", default=[])
@click.option("-i", "--ids", multiple=True, is_flag=False, flag_value="id", default=[], type=int)
@click.option("-n", "--names", multiple=True, is_flag=False, flag_value="query", default=[])
@click.option("--req / --no-req", default=False)
```
  
You'll notice that *keywords* are an argument, not an option; that's because
only arguments are allowed an indeterminate number of entries. And I feel that
you can get to interesting places by being associative with words, seeing where
they get you.  
All the options are optional, it wouldn't make sense any other way, and accept
multiple values.  
I prepared to receive multiple input in these forms; separated by spaces,
separated by commas and a space, separated by commas. I'm sure that there's more
ways to input them, but I expect that I'm going to be a good user and honour
these premises.  
The last option: *--req, --no-req*, serves to flag the user's interest in seeing
the dependencies of his chosen programs. This implies a different workflow, and
it helps to be aware of it from the start.  
I haven't gotten around to arrange a pithy command-line command, so a maximalist
query would look something like this:
  
```shell
python main.py cli python -q click -q mysql -i 3274 -i 23 -n flake8 -n jinja2
```
  
This means that the user is looking for the *cli* and *python* keywords, notice
that as they are an argument they don't have a flag before them. After, we have
two natural search queries; *click* and *mysql*, two id's numbered *3274* and
*23* respectively and, finally, two app names to search: * flake8* and *jinja2*.  
You have to put the option command before every choice. `-i 23 2374` won't work,
only `-i 2374 -i 23`.  
The first thing that `main.py` does when it gets the queries is to distribute it
to the correct management modules:
  
```python
@click.command()
@click.argument("keywords", nargs=-1)
@click.option("-q", "--queries", multiple=True, is_flag=False, flag_value="query", default=[])
@click.option("-i", "--ids", multiple=True, is_flag=False, flag_value="id", default=[], type=int)
@click.option("-n", "--names", multiple=True, is_flag=False, flag_value="query", default=[])
@click.option("--req / --no-req", default=False)
@snoop
def get_query(keywords, queries, ids, names, req):
    """
    Because we want to deal with complex queries, we'll define that we can receive,
    in the same query, an indefinite number of keywords, queries for natural:
    language search, several id's and names. This module will receive the information
    and send output to different functions.
    """
    cwd = os.getcwd()
    data = f"{cwd}/data_files"
    required = f"{cwd}/required_files"

    keys = kwd_mngmnt(keywords)

    if queries != ():
        queries_mngmnt(queries)

    if ids != ():
        ids_mngmnt(ids)

    names_mngmnt(names)
```
  
You can also see code creating variables containing some paths that are used often. I define them at the
beginning of the function and use them as needed.  
  
  
<h3>INPUT MANAGEMENT</h3>  
  
Although the objective is to be holistic with the data presentation, their
treatment still has different silos, and that's how it should be.  
For each of the content options, I created a *management* module, that coordinates
helper functions that enrich and transform the data.  
Here is an example of one of the more complex, the *names* one, so you can
see the structure of the management process, that is rather similar between the
options:  
<h4>Names Management Module:</h4>  
  
```python
def names_mngmnt(names):
    """
    Calls all functions regarding names.
    """
    if names:
        with open("names.bin", "wb") as f:
            pickle.dump(names, f)

        sql_expression("names.bin", "nqy.bin")
        get("nqy.bin", "nlst.bin")
    else:
        question = input_decision("Do you want to see a list of names?[y/n]? ")
        if question == "y":
            column_content("SELECT name FROM cli_apps", "allnm.bin")
            show_column(
                "allnm.bin",
                "Choose Some Names!",
                "names.bin",
            )
            sql_expression("names.bin", "nqy.bin")
            get("nqy.bin", "nlst.bin")

            os.remove("names.bin")
            os.remove("nqy.bin")
            os.remove("allnm.bin")


if __name__ == "__main__":
    names_mngmnt()
```
  
The first thing it does is create a pickled list with all the name queries from the
user. This way several functions can use the information without having to make
function calls that are not needed.  
Then it builds a SQL query from user input, makes the database call and, again,
pickles the results  
Off course some housekeeping is important, as these binary files can not last long,
or the next query will be contaminated by the latter.  
Let's see each of these functions in detail:  
  
<h5>sql_expression</h5>  
  
This, and the next functions, serve all management modules. It creates a single
SQL query that uses all the command-line inputs.  
  
```python
def sql_expression(in_binary, out_binary):
    """
    We'll see what content there are
    in the output of the arguments/options,
    and turn them to a sql expression. that
    we'll pickle.
    """
    with open(f"{in_binary}", "rb") as f:
        asks = pickle.load(f)

    collection = []
    if in_binary == "queries.bin":
        qry = "SELECT * FROM cli_apps WHERE MATCH(name, presentation) AGAINST ('dummy') "
    if in_binary == "keywords.bin":
        qry = 'SELECT * FROM cli_apps WHERE t1 = "dummy" OR t2 = "dummy" OR t3 = "dummy" OR t4 = "dummy"'
    if in_binary == "ids.bin":
        qry = "SELECT * FROM cli_apps WHERE id = dummy"
    if in_binary == "names.bin":
        qry = "SELECT * FROM cli_apps WHERE name = 'dummy'"

    for ask in asks:
        # This is for keywords.
        if "t1" in qry:
            kqry = qry.replace("dummy", ask)
            collection.append(kqry)
        # Same for names.
        if "name = 'dummy'" in qry:
            nqry = qry.replace("dummy", ask)
            collection.append(nqry)
        # Id's
        if "id = dummy" in qry:
            iqry = qry.replace("dummy", str(ask))
            collection.append(iqry)
        # Queries.
        if "('dummy')" in qry:
            qqry = qry.replace("dummy", ask)
            collection.append(qqry)
        # If there's morethan one choice we link them with 'UNION', that eliminates repeats.
        collection.append(" UNION")
    # There'll be one 'UNION' to many. This deletes it.
    collection.pop(-1)
    # 'Order' in a mysql expression comes at the end. We add it now.
    collection.append(" ORDER BY time")
    # We turn this list to string, so it's accepted as sql query.
    collection_str = " ".join(collection)

    with open(f"{out_binary}", "wb") as g:
        pickle.dump(collection_str, g)


if __name__ == "__main__":
    sql_expression()
```
  
*sql_expression* has as arguments: what is the file with the user input?, where
do you want me to put it? Or, in other words: `in_binary` and `out_binary` respectively.  
Depending from where the information comes, its created a template SQL query,
that'll be looped through each one of the user's queries, so as to insert in the
them the names of said queries.  
Although we have several valid SQL expressions, they might, probably, overlap,
causing repetitions in the output. To remedy this, we'll unite each of these with
`UNION` SQL commands, that join the information from the several expressions without
repetitions.  
It has the added advantage that it aggregates the output.  
This method creates an unnecessary `UNION` clause at the end of the expression
list. We pop it out.  
Finally, we transform everything into a string, and its ready to use!  
  
<h5>get</h5>  
  
Makes the necessary database calls.  
  
```python
def get(in_binary, out_binary):
    """
    The db call, which expression is
    taken from a pickled file, is made
    here. We pickle its results.
    """
    with open(f"{in_binary}", "rb") as f:
        query = pickle.load(f)

    qr = dbdata(query, "fetch")

    with open(f"{out_binary}", "wb") as g:
        pickle.dump(qr, g)


if __name__ == "__main__":
    get()
```
As in the case of the latter function, all it needs to know is where to get the
information and where to put it.  
The database code is another module that serves all the others. I'm always about to
start a post on it but I keep forgetting. Hope to do it soon.  
For now let's just say that *fetch* indicates that the `cur.fetchall()` option
is to be used.  
  
Before doing anything more with the data, the program, if it realizes that the
user didn't chose any keywords or names, will ask you if you want to see a list of
either. If the user says yes, the chosen lists will show *keywords* or *names*, as the
case may be, and it'll be possible to add any selections done now, to your original selection.
The next functions are used only if you answered 'yes' to seeing any of the list.  
  
<h5>column_content</h5>  
  
Makes the database call to get the data to show the user.  
  
```python
def column_content(query, out_binary):
    """
    We'll make a db call for the asked
    column and return it.
    """
    qrysrch = dbdata(query, "fetch")
    qs = [i[0] for i in qrysrch]

    with open(f"{out_binary}", "wb") as f:
        pickle.dump(qs, f)


if __name__ == "__main__":
    column_content()
```
  
<h5>show_column</h5>  
  
Aggregates and shows data of the  four tag columns in the database.  
  
```python
def show_column(in_binary, fzftitle, out_binary):
    """
    With the columns content from 'column_content',
    we format them with 'rich' and present them.
    """
    with open(f"{in_binary}", "rb") as f:
        lst = pickle.load(f)

    fzf = FzfPrompt()
    newcont = fzf.prompt(
        lst,
        f'--border bold --border-label="╢{fzftitle}╟" --border-label-pos bottom',
    )
    if newcont != []:
        with open(f"{out_binary}", "wb") as f:
            pickle.dump(newcont, f)


if __name__ == "__main__":
    show_column()
```
  
It needs to know where the information is, `in_binary`, the [fzf](https://github.com/junegunn/fzf) title to use, `fzftitle` and where to put the results, `out_binary`.  
I'm using [pyfzf](https://github.com/nk412/pyfzf), which is this charming little wrapper around *fzf*, that let's you use *python's* objects as source of information for it. In this case I'm showing the lists results in *fzf*.  
  
  
When this process ends, and if we used all command-line options, as we did in our
example, we end with four binary files:  
**qlst.bin** for queries,  
**klst.bin** for keywords,  
**ilst.bin** for id's,  
**nlst.bin** for names.  
These will be the 'ur' files for all the other methods. But that's for another
post.  

