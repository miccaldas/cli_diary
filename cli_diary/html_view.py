"""
Selects and displays an HTML file.
"""
import subprocess
import webbrowser

# import snoop
# from snoop import pp


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def view():
    """
    Opens *fzf* in the *html_posts* folder, collect the
    user's choice through subprocess and open the file
    with webbrowser.
    """
    htmlfolder = "/home/mic/python/cli_diary/cli_diary/html_posts"
    cmd = "fzf"
    htmlfile = subprocess.run(cmd, cwd=f"{htmlfolder}", stdout=subprocess.PIPE)
    # Subprocess' 'htmlfile.stdout' value is a bytes string. We need 'decode'
    # to turn it to a regular string.
    strfile = htmlfile.stdout.decode("latin-1")
    pth = f"{htmlfolder}/{strfile}"
    # Opens local file in browser.
    webbrowser.open(f"file://{pth}")


if __name__ == "__main__":
    view()
