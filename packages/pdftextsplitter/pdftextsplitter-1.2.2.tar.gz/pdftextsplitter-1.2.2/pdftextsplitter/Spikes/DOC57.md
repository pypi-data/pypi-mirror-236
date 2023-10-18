# Spike DOCANALYSE-57 (TOC-extraction)

This spike is about whether we can read out the Table of Contents (TOC) from a document.
The main question is: what advantage (value) does this bring us?

## TOC Reading

Some PDF documents have a native TOC attached to it, that you can access in the left
sidebar for easy navigation. The issue here is whether we can read out this TOC.

### pdfminer

The answer is, that we can indeed read this information using the pdfminer library.
The code to do this, is stored in ../TextPart/read_native_toc.py.

### word documents

Usually, word documents conatin a lot of structure, including TOC information.
We can easily read out this TOC information by first converting the word document
to PDF and then reading the TOC from that PDF using the above procedure.
We have tested this on the document cellar_dbb134db-e575-11eb-a1a5-01aa75ed71a1.0005.01_DOC_1.doc 
provided by DGMI.

## Advantage

For documents that have a native TOC attached, we can use that TOC to verify whether 
our selection rules (the rule-functions of textpart-derivates like title, footer, etc.)
indeed break the document down in the correct way. Secondly, by mathing the textlines
from the document to native-TOC elements, we could use the native-TOC to upgrade
the quality from our selection rules (by recognising that a certain textline is a headline).
<br />
<br />
This does not mean that our selection rules suddenly become useless. Reading out the TOC 
using pdfminer does NOT mean that we know which arts of the body-text belong to which
TOC-element (that still has to come from our selection rules) and, also, there are a lot of
documents from the DGMI that do not come with a native TOC. We also need to be able to handle
those.

# Answer
We can read the native TOC from both word and pdf documents using pdfminer. This allows
us to either verify the quality of our selection rules, or to upgrade the quality of the 
output (but not both at the same time).
