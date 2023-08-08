---
title: Cli Apps Database App. A Bird's Eye View
date: 07-08-2023 07:21
mainfont: Iosevka
fontsize: 13pt
---


This is a short post but, I think, an important one.  
At least important to understand the *database_app's* logic.  
As the other posts on this theme tend to delve deep into each of the parts of the app, here I aims to show how they interact and, hopefully,
explain why the app has this structure and not another.  
  
As I said in another post, the overarching aim for the app was to find a new
search paradigm, that did more than consume data in database approved formats, to one that leverages the syncretic nature of human thinking.  
If a database encourages, and quite rightly so, an analytical and compartmentalized view of information, we, as humans, think
in free, and not so free, associations, with explanations binding disparate pieces information, using processes that are experimental, failure-prone, iterative,
but that seem to find knowledge in the midst of turbulence.  
In short, the process is messy but fruitful.  
  
I wanted to create a method that aided the creation of the associative
processes that fuel imagination.  
  
With this in mind, I reached some organizational principles:
  
1. <strong><em>Everything must connect to everything.</em></strong>  
   Instead of silos, let's create a linked system, that you can traverse in its
   entirety just by querying the available data points. This leads me
   right to the second point, that is:  
2. <strong><em>Information should be combined.</em></strong>  
   As the ancients from the East have said, time and again, identity is an
   illusion.  
   The database model reificates this error of perception, by leading
   us in mistaking the starkly separated, non-fungible, classes needed to
   catalog and store information, as having ontological reality. Not letting us
   see them as the simple artefacts of *count* and *store* processes that they
   really are.  
  
   Paraphrasing a poem of [Philip Larkin](https://en.wikipedia.org/wiki/Philip_Larkin): *they don't mean to; but they do*.  
  
   Truth is,  
   at least for me,  
   and I'm the only one here;  
   is that information has a deeply transient and context-dependent nature. To take it from
   this rich and dynamic environment, cristallyzes it to death.  
   This is not the database's fault.  
   They were never meant as templates for the architecture of thought.  
   They are, and rightly so, intent on preserving and protecting information.  
   All laudable objectives, but not very amenable to fostering use or growth.  
  
   The problems come from living with these tools, for so long, so absent
   mindedly, and so *innate* is their presence, that we seem them as natural
   occurrences and first principles.  
   But they're not. And we must be vigilant to not let ourselves be subsumed in the
   logic of the tool.  
3. <strong><em>There is no such thing as too much depth.</em></strong>  
    Rabbit holes are there to be followed. If I want to drill down on a package
    dependencies and follow who depends on whom, for as long as the thread may
    run, I should.  
  
To get to the heights of these lofty ideals, I created a structure around a
globally available data source, that I called, with a lot of hubris,
`allinfo`. Passing through it, are function loops that, aided by a group of
collectively available helper methods, extract information in a dynamic, associative way.  
The structure is composed of the following elements:  
  
1. <strong><em>Query reception.</em></strong>  
   Where we make available, and incentivize its use, several data points,
   heterogeneous in nature.  
  
2. <strong><em>Data management.</em></strong>  
   What I call *data management* is the still, compartmentalized, treatment of
   each option of the query; with the objectives of:  
   2.1. converting it into a *SQL* expression,  
   2.2. clean the output,  
   2.3. return a file with its findings.  
   For each option there is a specific management module. Although they share all important functions.  
  
3. <strong><em>Initial funnel.</em></strong>  
   A sequence of functions that:  
   3.1. *Check for availability of management information.*
        They see if the files that have their output are present. If they find at least one, a list is made
        of the files.  
   3.2. *Aggregate the found information*.
        It's the birth of `allinfo`. All the information needed during a session is here.  
   3.3. *User's choice.*
        Of this retrieved pack of data, the user will choose what he wants to see. Usually is always a subset.  
   3.4. *Visualizing the data.*
        The user is presented with the content of its choices. Based on this knowledge he'll be:  
   3.5. *Asked what he wants to do with it.*
        At the moment I have built two data loops that consume these results. The user can choose one or the two,
        but they'll always be present in the others loop, making cross referencing the two data sources, almost inevitable.  
  
   They are:  
4. <strong><em>Dependencies.</em></strong>  
   This loop will scan through package dependencies, for one or more
   packages, drilling into its required files, as deep as the user wants. As I
   said, at any moment this information can be crossed with the other loop.  
  
5. <strong><em>Locations.</em></strong>  
    If you want to see a package location on the computer. If you say yes, it'll
    open the directory and ask you if you want to open any file. This process
    can be repeated as many times as you want, or interrupted to search for more
    dependencies.  
  
The only thing I haven't mentioned, are the methods that power these loops.  
There's an interesting collection of little, some not so little, functions to
aid them on their endeavours. Some have proven so useful, that I'm thinking in
putting them in the *reusable_files* directory, so I can access them whenever I
want.  

I leave you with a diagram of what I see when I talk about the
architecture of this solution:  
  
  
![Diagram](/home/mic/python/cli_diary/cli_diary/imgs/dbapp_diagram.png "db_app diagram")
