# Imports:
from thefuzz import fuzz
import re
import matplotlib.pyplot as plt
from .regex_expressions import contains_headlines_regex

# Auxillary function:
def count_distinct_integers(array: list[int]) -> int:
    """
    This function counts the number of distinct integers in an array of integers.

    # Parameters: array: list[int]: the array for which we want to perform the counting:
    # Return: int: the number of distinct elements in array.
    """

    # Initialize variables we need:
    length = len(array)
    Counter = 0
    HasBeenFound = False

    # Next, loop over the entire array:
    if (length>0):
        for k in range(0,length):

            # Reset the indicator:
            HasBeenFound = False

            # Next, loop over all elements that we already have had:
            if (k>0):
                for m in range(0,k):

                    # Note that we do NOT include k itself, otherwise
                    # we would always find a positive match to entry k:

                    # Check if there is a match:
                    if (array[m]==array[k]):
                        HasBeenFound = True

            # Now, if we found at least a match somewhere, the element
            # k is not new and we should not count it. Otherwise, we
            # do count it:
            if not HasBeenFound:
                Counter = Counter + 1

    # Then we can now return the answer:
    return Counter


# Function definition:
def calculate_footerboundaries_textpart(self, verbose_option: int):
    """
    This function calculates the header & footer boundary
    directly from the information read-out from the PDF and
    stores them in the textpart-class as members
    (headerboundary and footerboundary), so they can be used
    in the further processing of the text, such as calculating
    whitelines. So this function must be called immediatly after
    textgeneration.

    The choice for thefuzz has been tested and the CPU-speed
    is more then acceptable, compared to textgeneration, breakdown and
    the time it takes to connect to ChatGPT.

    # Parameters: verbose_option: int: This will decide how much terminal output
                  is given during the calculation. 0 means nothing (the higher, the more)
                  and -1 means also no histogram files are saved.
    # Return: None (stored in the class)
    """

    # ----------------------------------------------------------------------------

    # begin by calculating the minimal and maximal vertical
    # positions of the entire page:
    self.min_vert = min(self.positioncontent)
    self.max_vert = max(self.positioncontent)

    # Generate default-values for the boundaries:
    start_footerboundary = self.min_vert + 1.0*(self.max_vert - self.min_vert)/3.0
    start_headerboundary = self.min_vert + 2.0*(self.max_vert - self.min_vert)/3.0
    start_pagenumberthreshold = self.min_vert + 1.0*(self.max_vert - self.min_vert)/5.0

    # NOTE: This method always works, as pdfminer has a syste where top-of-page=high value
    # & botto-of-page=low value. For pymupdf, this is the other way around, but we reverse
    # that in textgeneration, so this method is universally usable.

    # ----------------------------------------------------------------------------

    # Next, refine the calculation. begin with matching all strings to each other
    # and identify how often a certain line repeats itself.
    Fuzzy_threshold = 70.0 # Crucial to pass LineTest1 (<=85) & SplitDoc (<=70) headers.
    Repetition_array = []
    ThisCounter = 0
    Looping_Index = -1
    Page_nr_repitions = []
    This_vert_pos = 0.0

    # Loop over all strings. We let textcontent steer the loop, but we have to deal with other arrays too,
    # so we use Looping_Index as a control index.
    for textline in self.textcontent:

        # Start by increasing the index. We start at -1 and after the first raise, we are at 0.
        Looping_Index = Looping_Index + 1

        # Begin by counting:
        ThisCounter = 0

        # Also extract the vertical position:
        if (Looping_Index<len(self.positioncontent)): This_vert_pos = self.positioncontent[Looping_Index]

        # Also, store the page numbers of the repititions:
        Page_nr_repitions.clear()
        Matching_Index = -1

        # Next, double-loop again over the strings:
        for matchingline in self.textcontent:

            # Same approach for Looping_Index:
            Matching_Index = Matching_Index + 1

            # Also extract the vertical position:
            if (Matching_Index<len(self.positioncontent)): matching_vert_pos = self.positioncontent[Matching_Index]

            # Calculate fuzzy-match ratio. Do it WITHOUT articles; they should not be counted:
            if (textline.startswith("Artikel")): textline = textline.replace("Artikel","")
            if (textline.startswith("artikel")): textline = textline.replace("artikel","")
            if (textline.startswith("Article")): textline = textline.replace("Article","")
            if (textline.startswith("article")): textline = textline.replace("article","")

            if (matchingline.startswith("Artikel")): matchingline = matchingline.replace("Artikel","")
            if (matchingline.startswith("artikel")): matchingline = matchingline.replace("artikel","")
            if (matchingline.startswith("Article")): matchingline = matchingline.replace("Article","")
            if (matchingline.startswith("article")): matchingline = matchingline.replace("article","")

            # Then, after skipping this part, we can calculate the fuzzy match:
            fuzzymatch = fuzz.ratio(textline,matchingline)

            # Fix for a TestTex-situation; H1 & H2 matchen fuzzy while they are NOT the same!
            if (textline.startswith("Eerste"))and(matchingline.startswith("Tweede")): fuzzymatch = 0.0
            if (textline.startswith("Tweede"))and(matchingline.startswith("Eerste")): fuzzymatch = 0.0

            # Test if it passes the threshold:
            if (fuzzymatch>Fuzzy_threshold):

                # Then, count it as a repetition of the textline, but ONLY if both options
                # are either <footer_start or both are >header_start; otherwise we get mixtures
                # that we do not want:
                if ((This_vert_pos<start_footerboundary)and(matching_vert_pos<start_footerboundary))or((This_vert_pos>start_headerboundary)and(matching_vert_pos>start_headerboundary)):

                    # Then, we can count the overlap:
                    ThisCounter = ThisCounter + 1

                    # Store at which page numbers the repition occurred:
                    if (Matching_Index<len(self.pagenumbers)):
                        Page_nr_repitions.append(self.pagenumbers[Matching_Index])

        # Next, we do not want to count repetitions if they occur on
        # the same page more then once (such as happens in Plan_Velo_FR
        # with picture on page 9). headers/Footers repeat themselves once per page.
        # So we adjust this. Also, notice that each textline has at least
        # one repetition, as it repeats to itself.
        if (ThisCounter>1):
            ThisCounter = count_distinct_integers(Page_nr_repitions)

        # The next problem is, that some headers or footers repeat chapter titles.
        # If this is the case, then we should only keep the highest (for headers) or lowest
        # (for footers):
        if (contains_headlines_regex(textline)):

            # Then, check if this is the highest/lowest of them all, by
            # looping again over the other strings:
            matching_vert_pos = 0.0
            Matching_Index = -1
            Thisline_Ismaximum = True

            # Make the loop:
            for matchingline in self.textcontent:

                # Same approach for Looping_Index:
                Matching_Index = Matching_Index + 1

                # Also extract the vertical position:
                if (Matching_Index<len(self.positioncontent)): matching_vert_pos = self.positioncontent[Matching_Index]

                # Next, check if this is the maximum (for headers):
                if (matching_vert_pos>This_vert_pos)and(This_vert_pos>start_headerboundary):

                    # Then, this is not the maximum vert_pos of the repetitions:
                    Thisline_Ismaximum = False

                # Next, check if this is the minimum (for footers):
                if (matching_vert_pos<This_vert_pos)and(This_vert_pos<start_footerboundary):

                    # Then, this is not the minimum vert_pos of the repetitions:
                    Thisline_Ismaximum = False

            # So, if it is a headline AND not the max/min, ignore the repetitions,
            # so table of contents, chapter titles, etc. are not included in the footer/header,
            # as they should not be:
            if (Thisline_Ismaximum==False):
                ThisCounter = 0

        # Obviously, we should also skip empty lines (especially important for pymupdf & LineTest2).
        if (textline==""):
            ThisCounter = 0

        # Next, correct for the self-match:
        if (ThisCounter>0):
            ThisCounter = ThisCounter - 1

        # Then, append it to the array:
        Repetition_array.append(ThisCounter)

        # Give some output:
        if (self.verbosetextline in textline)and(verbose_option>0):
            print("<" + textline + "> REPETITION SCORE ==> index=" + str(Looping_Index) + " & repetition=" + str(ThisCounter))

        # Note that, by construction Repetition_array has the same size as textcontent.

    # ----------------------------------------------------------------------------

    # Next, we have to see if a line starts with a page number. So we loop over all
    # textlines and we use regex to detect the number and then split to extract it.
    # For lines that do NOT start with a number, we add -1 to the array:
    Starting_Numbers = []
    Thenumber = -1

    # Loop over the lines in the PDF:
    for textline in self.textcontent:

        # Reset the number:
        Thenumber = -1

        # Fire regex:
        if (re.compile(r'^(\d+)', re.MULTILINE).search(textline)):

            # Then split & convert:
            split_array = textline.split()
            first_part = split_array[0]
            if first_part.isdigit():
                Thenumber = int(first_part)

        # Next, do the same for lines ENDING with a number:
        if (re.compile(r'(\d+)$', re.MULTILINE).search(textline)):

            # Then split & convert:
            split_array = textline.split()
            last_part = split_array[len(split_array)-1]
            if last_part.isdigit():
                Thenumber = int(last_part)

        # Exclude years:
        if (Thenumber>1800): Thenumber = -1

        # Next, append it to the array:
        Starting_Numbers.append(Thenumber)

    # Next, we have to correlate this to the actual pagenumbers:
    Line_Used_In_Histogram = []
    Pagenumber_Diffs = []
    Looping_Index = -1
    This_extracted_nr = -1
    ThisDifference = 0
    This_vert_pos = 0.0

    # Loop over the actual pagenumbers:
    for thisnr in self.pagenumbers:

        # Start by increasing the index. We start at -1 and after the first raise, we are at 0.
        Looping_Index = Looping_Index + 1

        # Fill the array whether the textline was used in the histogram:
        Line_Used_In_Histogram.append(False)

        # Extract the calculated starting-number:
        if (Looping_Index<len(Starting_Numbers)): This_extracted_nr = Starting_Numbers[Looping_Index]

        # Also extract the vertical position:
        if (Looping_Index<len(self.positioncontent)): This_vert_pos = self.positioncontent[Looping_Index]

        # Calculate the difference (only for valid ones and the ones that are not too high on the page):
        if (This_extracted_nr>=0)and(This_vert_pos<start_pagenumberthreshold):

            # Now, this test SHOULD be sufficient, but it can happen that (Copernicus for example),
            # there is a footnote with the right number on the right page. Then, we get multiple
            # hits on the same page, which is clearly NOT a pagenumber. We do not want this.

            # So we want to know if This_vert_pos is the smallest one of all vert_pos that
            # have the same pagenumber as thisnr. We need a second-loop to verify this.
            Extraction_isvalid = True
            Matching_Index = -1
            some_vert_pos = 1e5

            # make the loop:
            for page_nr in self.pagenumbers:

                # Same approach for Looping_Index:
                Matching_Index = Matching_Index + 1

                # extract vertical position again:
                if (Matching_Index<len(self.positioncontent)): some_vert_pos = self.positioncontent[Matching_Index]

                # Check that This_vert_pos is smallest of them all:
                if (some_vert_pos<This_vert_pos)and(page_nr==thisnr):

                    # Then, we are not valid anymore:
                    Extraction_isvalid = False

            # Now, only add to the histogram for valid ones:
            if Extraction_isvalid:
                ThisDifference = thisnr - This_extracted_nr
                Pagenumber_Diffs.append(ThisDifference)
                Line_Used_In_Histogram[Looping_Index] = True

                # return some output:
                if (verbose_option>2):
                    print(" ----------------> Pagenumbers for Histogram: pdf-nr=" + str(thisnr) + " & doc-nr=" + str(This_extracted_nr) + " & diff=" + str(ThisDifference) + " & vert-pos=" + str(This_vert_pos))

    # Next, we must make a histogram and extract the peak (that is the recurring difference
    # that indicates that a footer starts with a pagenumber):
    if (len(Pagenumber_Diffs)>=2):

        # Then we can make a calculation:
        max_diff = max(Pagenumber_Diffs)
        min_diff = min(Pagenumber_Diffs)
        hist_range = abs(max_diff-min_diff)
        hist_bins = 10*round(hist_range)+10

        # Give some output:
        if (verbose_option>3):
            print(" ----------------> --> Histogram bins: max_diff=" + str(max_diff) + " & min_diff=" + str(min_diff) + " range=" + str(hist_range) + " hist_bins=" + str(hist_bins))
            print(Pagenumber_Diffs)

    else:

        # then we need to supply a default-value:
        hist_bins = 10

        # Give some output:
        if (verbose_option>3):
            print(" ----------------> --> Histogram bins: hist_bins=" + str(hist_bins) + " ==> Nothing else known, as the array length is <=1")
            print(Pagenumber_Diffs)

    # Create the histogram:
    DiffHist = plt.hist(Pagenumber_Diffs, bins=hist_bins)

    # Save it, if that is what we want:
    if (verbose_option>=0):
        plt.savefig(self.outputpath + self.documentname + "_PagenUmberDiffs.png")

    # Close the histogram:
    plt.close()

    # Next, find the position of the largest bin:
    maxbin = 0.0
    maxindex = -1
    maxposition = 0.0

    # Verify that we have a usable histogram:
    if (len(DiffHist)>=2):

        # Search for largest bin:
        bincontents = DiffHist[0]
        for k in range(0,len(bincontents)):
            if (bincontents[k]>maxbin):
                maxbin = bincontents[k]
                maxindex = k

        # Translate index into position:
        if (maxindex>=0):
            maxposition = 0.5*(DiffHist[1][maxindex]+DiffHist[1][maxindex+1])

    # Then, now establish the difference to test:
    Diff_To_Test_For = round(abs(maxposition))
    if (round(maxposition)==-1): Diff_To_Test_For = -1 # To pass Plan_Velo_FR.

    # print it:
    if (verbose_option>0):
        print(" ############ PAGE NUMBER DIFFERENCE = " + str(Diff_To_Test_For))

    # ----------------------------------------------------------------------------

    # Next, now that we know the repitition, we have to decide which
    # lines are part of headers & footers. We will use a dynamical boundary for
    # calculating how much repitition is required, as it may also be the case that
    # multiple chapters need to address the same themes and have, therefore, the
    # same titles. This degree of repetition is usually a lot less then every page,
    # so we make it depend on the number of pages in the document:
    Repetition_threshold = 1.0 + max(self.pagenumbers)/5.1
    # Crucial that we accept 2 as allowed for LineTest1, but not 8 for Plan_Velo_FR.

    # Initialize variables we need:
    Part_of_Footer = []
    Part_of_Header = []
    Looping_Index = -1
    This_vert_pos = 0.0
    This_Repitition = 0
    This_extracted_nr = -1
    This_pdf_number = -1
    valid_for_hist = False

    # We let textcontent again steer the loop, and use Looping_Index as a control index.
    for textline in self.textcontent:

        # Start by increasing the index. We start at -1 and after the first raise, we are at 0.
        Looping_Index = Looping_Index + 1

        # Extract vertical position:
        if (Looping_Index<len(self.positioncontent)): This_vert_pos = self.positioncontent[Looping_Index]

        # Extract repitition:
        if (Looping_Index<len(Repetition_array)): This_Repitition = Repetition_array[Looping_Index]

        # Extract the calculated starting-number per line:
        if (Looping_Index<len(Starting_Numbers)): This_extracted_nr = Starting_Numbers[Looping_Index]

        # Extract page numbers (according to PDF):
        if (Looping_Index<len(self.pagenumbers)): This_pdf_number = self.pagenumbers[Looping_Index]

        # Extract validness for histogram:
        if (Looping_Index<len(Line_Used_In_Histogram)): valid_for_hist = Line_Used_In_Histogram[Looping_Index]

        # Now, if we pass the repetition threshold and are below the start_footerboundary, we are part
        # of the footer:
        if (This_Repitition>Repetition_threshold)and(This_vert_pos<start_footerboundary):
            Part_of_Footer.append(True)

            # Give some output:
            if (verbose_option>1):
                print(" ==> IN FOOTER (repetition)    <" + textline + "> pdf-nr=" + str(This_pdf_number) + " vert_pos="+str(This_vert_pos) + " loopindex=" + str(Looping_Index) + " repetition=" + str(This_Repitition))

        # Then, also test whether the given line is a page number: then, it must be valid for usage in the histogram
        # and its difference must be equal to the main difference:
        elif (This_extracted_nr==(This_pdf_number-Diff_To_Test_For))and(valid_for_hist==True):
            Part_of_Footer.append(True)
            # Notice that PDF index page numbers are always larger then the numbers on the page, never smaller, so extracted = pdf - diff is the correct equation.

            # Give some output:
            if (verbose_option>1):
                print(" ==> IN FOOTER (page-numbers)    <" + textline + "> pdf-nr=" + str(This_pdf_number) + " vert_pos="+str(This_vert_pos) + " loopindex=" + str(Looping_Index) + " repetition=" + str(This_Repitition))

        # In any other case, we are NOT part of the footer:
        else:
            Part_of_Footer.append(False)

        # Next, play the same game with the header:
        if (This_Repitition>Repetition_threshold)and(This_vert_pos>start_headerboundary):
            Part_of_Header.append(True)

            # Give some output:
            if (verbose_option>1):
                print(" ==> IN HEADER (repetition)    <" + textline + "> pdf-nr=" + str(This_pdf_number) + " vert_pos="+str(This_vert_pos) + " loopindex=" + str(Looping_Index) + " repetition=" + str(This_Repitition))

        # In any other case, we are NOT part of the header:
        else:
            Part_of_Header.append(False)

    # ----------------------------------------------------------------------------

    # Now that we have proper candidates, generate a footer & header boundary:
    Footer_pos_array = []
    Header_pos_array = []
    Looping_Index = -1

    # Loop over all position contents:
    for thispos in self.positioncontent:

        # Start by increasing the index. We start at -1 and after the first raise, we are at 0.
        Looping_Index = Looping_Index + 1

        # Filter out the ones that are part of the footer:
        if (Looping_Index<len(Part_of_Footer)):
            if Part_of_Footer[Looping_Index]:
                Footer_pos_array.append(thispos)

        # Same for the header:
        if (Looping_Index<len(Part_of_Header)):
            if Part_of_Header[Looping_Index]:
                Header_pos_array.append(thispos)

        # Note that the arrays Header_pos_array & Footer_pos_array are much
        # shorter then the other ones; so far we were dealing with arrays of the same
        # size as textcontent (at least, they should be!) but these are much shorter.

    # ----------------------------------------------------------------------------

    # Then, calculate the actual boundaries from these arrays. For the footer,
    # this means a little above the max. of all lines that should be part of
    # the footer. If there are none, the boundary should be below the
    # full minimum, as this means nothing should be cut off.
    if (len(Footer_pos_array)>0):
        self.footerboundary = max(Footer_pos_array)+1.0
    else:
        self.footerboundary = self.min_vert - 1.0

    # Play the same game for the header (but vice versa with signs):
    if (len(Header_pos_array)>0):
        self.headerboundary = min(Header_pos_array)-1.0
    else:
        self.headerboundary = self.max_vert + 1.0

    # Done. Give some final results:
    if (verbose_option>0):
        print("")
        print(" ==> Position Range = [" + str(self.min_vert) + "," + str(self.max_vert) + "]")
        print(" ==> Calculated Footer boundary = " + str(self.footerboundary))
        print(" ==> Calculated Header boundary = " + str(self.headerboundary))
        print("")

    # ATTENTION: Establishing these boundaries does NOT mean that the entire content
    # of the footer-class is already known from the beginning. Only the cutting boundaries
    # for header & footer are known, but during breakdown, the selection rule of the footer
    # class may deviate from this decision, for example by including textparts with a small
    # fontsize in the footer as well, even though they do not fall on the 'correct' side
    # of the boudaries. As such, footer.rule() during breakdown gets the final say, not the
    # numbers we calculate here.
