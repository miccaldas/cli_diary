"""Experiment to recreate the 'see db' functionality with Textual and Rich."""
from rich.syntax import Syntax
from rich.traceback import Traceback
from snoop import pp

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import var
from textual.widgets import DirectoryTree, Footer, Header, Static


class See(App):
    """Textual blog post reader app."""

    CSS_PATH = "see.css"
    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ("q", "quit", "Quit"),
    ]

    show_tree = var(True)

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        """Builds the UI"""
        path = "/home/mic/python/cli_diary/cli_diary/md_posts"
        yield Header()
        yield Container(
            Vertical(DirectoryTree(path), id="tree-view"),
            Vertical(Static(id="posts", expand=True), id="posts-view"),
        )
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        self.query_one(DirectoryTree).focus()

    def on_directory_tree_file_click(self, event: DirectoryTree.FileClick) -> None:
        """Called when user clicks on posts on the tree view"""
        post_view = self.query_one("#posts", Static)
        try:
            syntax = Syntax.from_path(event.path, word_wrap=True, theme="nord")
        except Exception:
            post_view.update(Traceback(theme="nord", width=None))
            self.sub_title = "ERROR"
        else:
            post_view.update(syntax)
            self.query_one("#posts-view").scroll_home(animate=False)
            self.sub_title = event.path

    def action_toggle_files(self) -> None:
        """Called in response to bindings"""
        self.show_tree = not self.show_tree


if __name__ == "__main__":
    See().run()
