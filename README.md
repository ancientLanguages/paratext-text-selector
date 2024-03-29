# Paratext Text Selector

This script aims to fill a gap in the Paratext toolchain by providing a way for users to select chapters and books to be included in an app or other publication without having to manually edit the `.SFM` files produced by Paratext. Instead, the user creates a specification file that tells this tool what books and chapters to include.

It also includes a variety of other tools that have been useful for preparing books for publication in app form.

## Example use case

For example, publish a selection of Psalms would require someone to manually delete the empty chapter and verse markers for the Psalms that have not yet been translated or approved for publication. This tool removes that problem by allowing users to specify which chapters to include and then automatically copying only those chapters.


# Installation

1. Download and run `python3 setup.py install`
2. `pip install paratext-text-selector`

# Usage

`set-texts <specification file>`

# Specification file

See `textconfig.txt` for an example specification file. The details of how they work are below.

## Minimal definition file

Each definition file is composed of sections which are marked by a name surrounded with `[` and `]`. Each definition file *must* have a `[config]` section that must contain `ptpath`, `outputpath`, and `projectname` as shown in the example below. Note lines starting `#` are comments.

    [config]
    # Path to SFM files created by Paratext
    ptpath = C:\\My Paratext 9 Projects\\MP1
    # Path to folder to output files to
    outputpath = C:\\MyAppTexts
    # Name of the project.
    # Should be the same as the project abbreviation in Paratext.
    projectname = MP1

This config file is correct, but it doesn't do anything yet. For each file you want to process, create a section with the file name or book abbreviation (like used in the Paratext menu). Note that the script assumes it is processing a biblical book abbreviation; to add other books like front or back matter, use the filename prefixed with a `*`.

## Working with biblical books

To get Psalms 1,2 and 30-40 we would add the following section.

    [Psa]
    Chapters = 1,4,30-40

What if we want to exclude the following introductory markers in the file that come before the `\c 1` marker?

    \id PSA - MP1: project example
    \toc3 Psa.
    \toc1 Psalms
    \toc2 Psalms
    \mt1 Psalms

To do this we simply add `NoIntro = true`. The config file doesn't care about capitalization so `nointro = True` would also work. `NoIntro` only works when `Chapters` is being used.

    [Psa]
    Chapters = 1,4,30-40
    NoIntro = true

Imagine that we have already finished Genesis and want to include it in the app too. Simply add the following:

```
[Psa]
Chapters = 1,4,30-40
NoIntro = true

[Gen]
```

To include a whole book without modification all we need to is add a section with the book abbreviation or file name.

## Working with front and back matter books

What if we want a backmatter or front matter book? For these we need to use the file name and because we're using a file name we need to tell the script by prefixing it with a `*`.

```
[*A0FRTMP1.SFM]
nointro = true
```

This will copy all chapters of `A0FRTMP1.SFM` to the output directory.

Imagine that in our front matter book we an introduction, Bible reading plan, and suggested Bible study method. We'd like these to be output to separate files so that they will be separate books in our scripture app. We simple create three sections for the same book and use the `Chapters` command to specify which chapters to include in each. Then we add `Output` to specify the output file name.

Due to a limitation in the code, each section must have a unique name so we simply add a `$` and a number to the end of the file name so that the final name is unique (the `$` and number will be deleted from the final file name). Notice that we have `*A0FRTMP1.SFM`, `*A0FRTMP1.SFM$1`, and `*A0FRTMP1.SFM$2` in the following example.

```
[*A0FRTMP1.SFM]
chapters = 1
nointro = true

[*A0FRTMP1.SFM$1]
nointro = true
chapters = 2
output = ReadingPlan.SFM

[*A0FRTMP1.SFM$2]
nointro = true
chapters = 3
output = StudyMethod.SFM
```



This will copy chapter one to `A0FRTMP1.SFM`, chapter two to `StudyMethod.SFM`, and chapter three to `StudyMethod.SFM`. Note that unless we say `nointro = true`, the intro will automatically be appended to the beginning of the file.

## Including files from outside the default project folder

What if you need to include a file that is not in the project folder (i.e. the one specified in the `[config]` section)? For example, perhaps the introduction is written in the national language and is in the project folder for the back translation. Simply add the `Path` command to the section for that book to tell the script to look somewhere else for that file.

```
[*A0FRTMP1bt.SFM]
chapters = 1
Path = C:\\My Paratext 9 Projects\\MP1bt
```


### Finding front/back matter book file names

If you're unsure what the filename is look in the project direction found under `My Paratext 9 Projects`. Front and backmatter books usually start with `A` the book abbreviation from the Paratext navigation menu should be part of the file's name. The Front matter book might look like `A0FRTMP1.SFM`.

# Other commands

## `ConvertTags`

WARNING! this is one of the most difficult features to use correctly because the syntax of the list has to be exactly has follows. The list needs to be wrapped in `[ ]` and each substitution does as well. Each pair to be substituted needs to be wrapped in *double* quotes.  It doesn't matter if you prefix the backslash or not. If you do it *must* be `\\\\` (yes, four backslashes).

It is recommended to add a trailing space after the tag to be replaced, *unless that tag is the only thing on a line*.

If the list is spread over multiple lines, subsequent lines *must* be indented.

```
ConvertTags = [
  ["to replace ", "replacement "],
  ["to replace 2 ", "replacement 2 "]
  ]
```

This would also be a valid format:

```
ConvertTags = [["to replace ", "replacement "], ["to replace 2 ", "replacement 2 "]]

```

Here is an example. The last two lines have the backslash, the first three don't. The tool doesn't care and both will work. `ib` is the only thing on the line in which it occurs so there is no trailing space after it. If there was, then it would not be replaced.

```
ConvertTags = [
  ["ili ", "li "],
  ["ili2 ", "li2 "],
  ["ib", "b"],
  ["\\\\ip ", "\\\\p "],
  ["\\\\ipr ", "\\\\pr "]
  ]
```
Long story short, if you choose to use this, make sure the syntax is correct and double check the output before you build an app with it.

If you need to change the same set of tags in multiple books you can add a `[DEFAULT]` section with and assign the list to a variable name which can be referenced in the ConvertTags Command as `%(varialbe-name)s`. See the snippet below:

```
[DEFAULT]
tags = [
  ["ili ", "li "],
  ["ili2 ", "li2 "],
  ["ib", "b"],
  ["\\\\ip ", "\\\\p "],
  ["\\\\ipr ", "\\\\pr "]
  ]

...

[GLO]
ConvertTags = %(tags)s
```

## `RemoveDraftGloEntries = <marker>`

This removes any glossary entry that contains the string found in `<marker>`. For example if you had `RemoveDraftGloEntries = zzz` in your specification file, then `\k John - zzz: \k*: Stuff about John` would not appear in the GLO file output if the command is used. It allows you to use keep drafts in Paratext without having to manually remove them from the SFM files before publishing.


## `RemoveChapterLines = true`

This removes `\c ` tags and their number from the output file. Sometimes useful when copying front/back matter to separate files that don't need chapters.
