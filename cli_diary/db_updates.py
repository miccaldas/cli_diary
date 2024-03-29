"""
Sometimes this app has content that's added but not through
the 'new post' command. Which means that it doesn't get
put in the db and doesn't show in the 'search' and 'see'
commands. This module will run twice monthly to check what
files are in the 'md_posts' folder, if there's something
new, it'll be added to the db.
"""
import os
import string
import subprocess

# import snoop
import yake
from dotenv import load_dotenv
from mysql.connector import Error, connect

# from snoop import pp

from db import dbdata


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])
load_dotenv()


# @snoop
def yake_processing(text):
    """
    Each note text will pass through here, the
    Yake keyword creator, to create up to 2
    keywords. It'll be called from the 'db_update'
    function.
    """
    kw_extractor = yake.KeywordExtractor()
    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.9
    numOfKeywords = 4
    custom_kw_extractor = yake.KeywordExtractor(
        lan=language,
        n=max_ngram_size,
        dedupLim=deduplication_threshold,
        top=numOfKeywords,
        features=None,
    )
    # Yake's list of keywords.
    keywords = custom_kw_extractor.extract_keywords(text)
    # Erasing any punctuation that might in the keywords.
    punct_kwds = [i[0].translate(str.maketrans("", "", string.punctuation)) for i in keywords]
    # Turning them all to lowercase.
    lower_kwds = [i.lower() for i in punct_kwds]
    # Stripping them of spaces.
    clean_kwds = [i.strip() for i in lower_kwds]

    return clean_kwds


# @snoop
def db_updates():
    """
    Creates a list of files on the markdown posts directory.
    Gets list of titles of posts in the database.
    Checks if the directory has any posts not in the db.
    If yes, it reads their content through yake, that outputs
    two keywords that will be used as values for the k1/2 columns.
    Uploads the new values to the database.
    """
    diary = os.getenv("CLIDIARY")
    mdpth = f"{diary}md_posts"
    mdlist = os.listdir(mdpth)
    query = "SELECT title FROM cli_diary"
    data = dbdata(query, "fetch")

    dblst = [f"{i[0]}.md" for i in data]

    newentries = [i for i in mdlist if i not in dblst]
    newdata = []
    if newentries:
        for post in newentries:
            with open(f"{mdpth}/{post}", "r") as h:
                text = h.read()
                print(text)
                yake = yake_processing(text)
                newdata.append([post[:-3], yake[0], yake[1]])
    for i in newdata:
        print(i)
    for i in newdata:
        query1 = f"INSERT INTO cli_diary (title, k1, k2) VALUES ('{i[0]}', '{i[1]}', '{i[2]}')"
        dbdata(query1, "commit")


if __name__ == "__main__":
    db_updates()
