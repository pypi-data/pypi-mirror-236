# Overview of the code

The code consist of three parts: conversion, preparation and analysis.

## Conversion

This is the phase where the document from its native file format is
converted to a plain .txt file. It is possible to take part of the layout
properties along in this conversion, but images (and other objects
that cannot be converted to tekst) are lost. There are different
tools that can be used for this step:

### pdftotext

This tool can be used in GenerateTextFile.py by either calling a shell command,
or as a python library. The shell command structure allows
the user to control the layout-parameter and the python library does not.
We prefer to use the -default option (non_raw_non_physical_layout), 
because that will perserve quite a lot from
the layout, while the multi-column structure is removed. This is desirable,
as keeping a multi-column structure in the .txt file (which is what -layout does)
results in adding sentences to the same line that have nothing to do with each other.
The last of the 3 options (-raw) is undesirable as well, as it removes too much
layout components.

### pypdf2

This is another python library that extracts text from PDF files. A PDF basically
contains 'draw text commands', which are interpreted by the reader. What pypdf2
does, is to locate those commands and extract the text. We added this option
to the GenerateTextFile.py script to eperiment with different tools.

### pymupdf

A text extractor python library for PDF files. According to the benchmarks[https://github.com/py-pdf/benchmarks]
of different tools, it is extremely fast and reliable. We added this option
to the GenerateTextFile.py script to eperiment with different tools.

## Preparation

This step cuts the .txt-file obtained during conversion into multiple
.txt files that can then be analysed separately. Here are also multiple
solutions available

### Own development

For this step we use code specifically developed for this project.
This code is available in PrepareTextFile.py. It relies on ContainsCountry.py
(which checks whether a string contains a country name) and GetTitleLines.py
(which contains the hard-coded lines of the title-location).

### Other tools

This still needs to be investigated.

## Analysis

This step summarizes the content of the different outputs of the preparation
phase into a single summary .txt-file. This can be done by a combination
of multiple techniques. GenerateKeywords.py combines the title and headlines
(obtained in the preparation phase) with a keyword extraction on the text body
(also obtained in the preparation phase)

### Use of the title headlines

The preparation phase can be used to identify the title and the table of contents and/or
the headlines (chapters, sections, etc.) By setting these apart, they can be easily 
imported in the final summary file.

### Keyword extraction

Python has several efficient tools for extracting keywords. We have implemented
two: rake_nltk and yake. According to documentation, rake_nltk is very powerful
and easy to use. However, on our documents it does not peform very well as those
documents require very specific domain knowledge to read and rake_nltk is not very
well equipped for that.\
\
yake is also not domain specific, but it does allow the user to manipulate several
parameters of the keyword extraction relatively easy. By searching text body
(obtained in the preparation phase) several times with different settings, we can obtain
quite a good overview of the text content. In our case, we use a phase length of 3 and 4
and search the document twice for the top-10 keywords each (overlap threshold = 0.9 in both cases).

