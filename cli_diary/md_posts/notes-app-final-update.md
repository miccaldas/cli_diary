---
title: notes_app_final_update
date: 2021-09-30 04:18:23
tags: notes, python, web
---

And still the incessant tinkering in the notes app!  
I, not knowing when to leave good enough alone, and wanting very much to put
everything in the app, forgot an earlier, short and rare moment of good
sense that concluded that all this was just very silly.  
And although it is, really, overkill, there was a sensible reason behind it. To
augment my awareness of the tagging system, its evolution and growth, and
through this, make me do better choices in this regard. And this, I think, is
important. Messy tags are not unhelpful as they are an active hindrance.  
Maybe its all for the better and this will make me a more thoughtfull user.
Maybe. But for now it justs feel like I've been gilding the lily.  
So these are the things that I added:

### tag_links
I added a method that downloads all tags in thew db, with their connections
values in a tuple.  
```python
queries = [
        "SELECT k1, count(*) as links FROM notes GROUP BY k1",
        "SELECT k2, count(*) as links FROM notes GROUP BY k2",
        "SELECT k3, count(*) as links FROM notes GROUP BY k3",
        ]
```

### new_tag
This method checks keywords names against the db record, and if it doesn't find
a match, it outputs a message saying the keyword x is new.  
To find a substring inside a list of strings, as is the case in looking for
keywords values in the tag archive, I used this formulation, after not getting
to work something similar but as a list comprehension. I think this is somewhat
deprecated, which is too bad, as is a very clear and simple piece of code.
```python
res = any(k in i for i in self.records)
```

### count_links
This methods checks how many connections a keyword has, and returns that
information.  
```python
        for i in self.links:
            if i[0] == self.k1:
                new_i = list(i)
                new_val = [new_i[0], (new_i[1] + 1)]
                print(color(f"[*] - The updated value of the keyword links is {new_val}", fore="#c6f188"))
```
And that was it. Here is the full code of the methods.

1. count_links:
```python
    @logger.catch
    def count_links(self):
        """Will check the new keywords, see how many links they'll have, and return that
        information."""
        for i in self.links:
            if i[0] == self.k1:
                new_i = list(i)
                new_val = [new_i[0], (new_i[1] + 1)]
                print(color(f"[*] - The updated value of the keyword links is {new_val}", fore="#c6f188"))
            if i[0] == self.k2:
                new_i = list(i)
                new_val = [new_i[0], (new_i[1] + 1)]
                print(color(f"[*] - The updated value of the keyword links is {new_val}", fore="#c6f188"))
            if i[0] == self.k3:
                new_i = list(i)
                new_val = [new_i[0], (new_i[1] + 1)]
                print(color(f"[*] - The updated value of the keyword links is {new_val}", fore="#c6f188"))

    if __name__ == "__main__":
        count_links()
```

2. new_tag
```python
    def new_tag(self):
        """Will check the keyword names against the db records. If it doesn't find a
        match, it will produce a message saying the tag is new."""
        self.keywords = [self.k1, self.k2, self.k3]
        for k in self.keywords:
            res = any(k in i for i in self.records)
            if not res:
                print(color(f"[*] - The keyword {k} is new in the database.", fore="#f18892"))
            else:
                pass

    if __name__ == "__main__":
        new_tag()
```

3. tag_links
```python
@logger.catch
    def tag_links(self):
        """I'll join the three lists and order them by number of connections."""
        queries = [
            "SELECT k1, count(*) as links FROM notes GROUP BY k1",
            "SELECT k2, count(*) as links FROM notes GROUP BY k2",
            "SELECT k3, count(*) as links FROM notes GROUP BY k3",
        ]
        try:
            for q in queries:
                conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
                cur = conn.cursor()
                query = q
                cur.execute(
                    query,
                )
            self.links = cur.fetchall()
            # Records is a list and row is a tuple with the tag name and number of connections.
            self.links.sort(
                key=lambda x: x[1]
            )  # This sorts the list by the value of the second element. https://tinyurl.com/yfn9alt7
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

    if __name__ == "__main__":
        tag_links()

```
