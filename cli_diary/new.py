"""
Creates a markdown file for the user to write a post,
converts it to html and registers it in the database.
"""
import os
import subprocess
import yake
import click
import isort
import snoop
from mysql.connector import Error, connect
from snoop import pp

def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])

# @snoop
def new():
    """
    Open a vim file through subprocess,
    converts it to html with pandoc and
    puts it on the 'html_posts' folder.
    Updates database with new entry.
    """

    title = input(click.style(" [X] - What is the title of your post? ", fg="bright_green", bold=True))
    md_file = f"{title}.md"

    cmd = f"vim {md_file}"
    subprocess.run(cmd, cwd="md_posts", shell=True)

    cmd1 = f"pandoc --highlight-style=breezedark -s -o html_posts/{title}.html md_posts/{md_file}"
    subprocess.run(cmd1, shell=True)

    with open(f"md_posts/{md_file}", "r") as f:
        data = f.readlines()

    data_str = " "
    text = data_str.join(data)

    kw_extractor = yake.KeywordExtractor()  # noqa: F841
    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.9
    numOfKeywords = 10
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    kwds = []
    for kw in keywords:
        kwds.append(kw[0])
    for idx, kwd in enumerate(kwds):
        print(click.style(f" {idx, kwd}", fg="red", bold=True))
    kwdcho = input(click.style("If you want to keep any of three keywords, type their number. ", fg="bright_green", bold=True))
    if kwdcho != "":
        kwdchoi = kwdcho.split(" ")
        kwd_choice = [int(i) for i in kwdchoi]
        choices = []
        for i in kwd_choice:
            choice = [(idx, val) for (idx, val) in enumerate(kwds) if idx == i]
            choices.append(choice)
        flatter_choices = [i for sublist in choices for i in sublist]
        kwd_names = [f[1] for f in flatter_choices]
        if len(kwd_names) == 1:
            k1 = kwd_names[0]
            k2 = input(click.style(" Choose a keyword » ", fg="bright_green", bold=True))
        if len(kwd_names) == 2:
            k1 = kwd_names[0]
            k2 = kwd_names[1]
    else:
        k1 = input(click.style(" Choose a keyword » ", fg="bright_green", bold=True))
        k2 = input(click.style(" Choose another... » ", fg="bright_green", bold=True))

    answers = [title, k1, k2]

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = "INSERT INTO cli_diary (title, k1, k2) VALUES (%s, %s, %s)"
        cur.execute(query, answers)
        conn.commit()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, e
    finally:
        if conn:
            conn.close()
        return query

if __name__ == "__main__":
    new()
