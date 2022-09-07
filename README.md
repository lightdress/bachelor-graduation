# Thesis Checking System Based on B/S Architecture

If you are a student who wants to consult my codes for your thesis, pay attention:

**It is not a good essay topic. Try to abandon it as early as possible!**

**It is not a good essay topic. Try to abandon it as early as possible!**

**It is not a good essay topic. Try to abandon it as early as possible!**

![run](https://web.archive.org/web/20220907101131/https://n.sinaimg.cn/sinakd2020723s/347/w654h493/20200723/7fda-iwtqvyk5123134.jpg)

## Target

There are two kinds of paper document formats,
which are editable document formats and fixed document formats.

Fixed document formats such as DjVu and PDF are close to what people see.
However, reading and analysing their contents are not easy for computer programs.

This project aims to read and analyse editable document formats such as RTF, ODT and DOCX.
As a cost, it cannot obtain some information about the layout of papers.

LaTeX is also an editable document format.
Nevertheless, LaTeX documents always contain macros.
As a result, reading and analysing a LaTeX document is not easier than reading and analysing its output DjVu or PDF document.

## Design

I believed that I must separate this system into two parts.
These two parts respectively work on reading and analysing the paper document.

The former can contain several different engines,
each of which works on reading documents with specific formats by a unique method.
Because of a lack of time, I only implemented [a buggy DOCX engine](src/core/pp/engines/docx.py) based on [the Python-DOCX library](https://python-docx.readthedocs.io/).

I further divided the latter into several hierarchies.
[The "scanner" hierarchy](src/core/scanner/) tries to scan the document and obtain several segments such as title, abstract title and abstract.
[The "parser" hierarchy](src/core/parser/) tries to parse these segments and get a catalogue of all chapters and sections.
It may not be the best design.
