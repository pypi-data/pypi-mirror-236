# Test procedure

### Test documents
The idea is to test all code using test documents. These are very small documents of a single
page (unless the test requires multiple pages) and only a few lines of text. The documents
are so simple that the desired output is exactly known in advance.
<br />
For each such a document, there is an input, a true output and a calculated output
(which is the result from the test). For each test document, there is a single python
script (possibly containing multiple tests) that performs the tests with the
document. The script should be added to AllTests.py to be called automatically.
<br />
Note that each test should be designed in a way that if the test succeeds, it
only returns a true boolian and no single terminal-printed line. If the test fails,
it should return a false-boolian and terminal-printed lines are allowed to facilitate
finding the problem. All unit tests should not take any inputs.
<br />
The same filosophy is also applied when the input and/or output is not a document,
but some other file, or hard-coded infromation (reference data). 
This occurs, for example, with testing the generation of wordclouds.
This gives an image as output, not a document.

### Example
../Script/TextExtraction_001.pdf is a document designed to test the text extraction form a pdf.
../True_Outputs/TextExtraction_001.txt containes the desired output against which we test.
../Calc_Outputs/TextExtraction_001.txt is the file where the unit tests write their result to for comparison.
../Script/TextExtraction_001.py contains all unit tests utilizing this document.
../Script/AllTests.py collects all test-scripts so they can be run efficiently.
<br />
Note that it is very well possible for ../Script/TextExtraction_001.py to contain multiple
unit tests (This one contains 4: a, b, c, d; one for each text extraction algorithm). The idea
is that all these test use only ../Script/TextExtraction_001.pdf as input.

### Procedure

The idea is that for all functionality that is added to the repository, tests are added
to this folder. For each piece of functionality, a seperacte testScript.py is added
to this folder (like ../Script/TextExtraction_001.py) that performs the test. This
test should then be added to ../Script/AllTests.py so that it is taken along
automatically in the full sequency of tests. It should also be added to test_collection.py
at the lowest possible level, so that the code coverage can be measured. <br />
<br />
The functionality should be tested
with unit-tests (that only test a seperate piece of code) and integration tests
(that test how the different peices of code interact with other pieces). This way,
one can be sure that when making changes, nothing accidentally breaks. <br />
<br />
We also test the functionality with regression tests (testing the full code at once).
The main difference between our integration and regression tests, is taht integration
tests use small toy docs designed to specifically provoke a certain behaviour, while
our regression tests use real documents provided by the users. <br />
<br />
It is a strategic decision that we do NOT include regression tests in test_collection.py.
This way, we measure code coverage without the regression tests (otherwise it would 
always be >90%). The regression tests are added to AllTests.py (in dummy form to reduce costs).
On the other hand, AllTests.py does not include printing tests, while test_collection.py does.
Without the printing tests, good code coverage cannot always be obtained, while printing
a lot of terminal output is not useful in the test report of AllTests.py. <br />

### Dummy summarization

In case you have problems connecting to ChatGPT, (for example because you ran out of free requests), it
is possible to replace the summarization of ChatGPT by a dummy function while you can still test
all other functionality. This will also allow you to run tests without internet connection.
In order to use this functionality, simply run a script like 'python Alltests.py dummy'
Without the extra parameter, the testing functions will actually connect to ChatGPT and
perform a 'true' test of it summarization capabilities.
