# Testing Tools

Sometimes, different test scripts require the same comparison procedure, 
or the same reference information (hard-coded)
over and over again. For example, the need for comparing two .txt-files
often arises. The tools to address these needs (only for the purpose
of testing the code) are collecten in this folder. Then, multiple
tests can call these tools, which avoids duplication of code.

# Importing the testing tools in the package

Some of the tools in this folder are available to import as a package.
these tools are: <br />
* ByteComparison # Allows to compare two arbitrary files by checking if their byte-content is the same (so we can only say if the files are the same or not).
* CodeCoverage   # Allows to interpret the output for a code coverage measurement more easily (the report must be available as a .txt-file).
* CompareImages  # Allows to compare two .png-files by checking which pixels are the same.
* CompareTexts   # Allows to compare two strings/texts with fuzzy matching.
* DjangoCoverage # Same as CodeCoverage, but now for Django tests (this package does not use django).
* FileComparison # Allows to compare .txt-files (or .html-files) by checking line-by-line if the content is the same.
* ImgRMS         # Allows to calculate an RMS (Roo-Mean-Square) between two pictures so you can say how close they are to each other.
* MySystem       # An enumeration-class with possible OS-systems that can be detected.
* detectsystem   # A function that can detect which OS you are using (it needs MySystem).
<br />
<br />
These tools should be imported like: <br />
from textsplitter import ByteComparison <br />
and if that does not work, use: <br />
from textsplitter.Tests.Tools import ByteComparison <br />
