# Tracking of DOCANALYSE-89 (Plan_Velo)

This is to write down the problems we encoutered with attempting to make
the plan work for the Plan_velo document:

* Sometimes the program finds too many line regions (unstable calculation). In that situation, it may be the case
that the regular line region is very small. then, some lines in the document that are supposed to be body
text, actually end up being headlines, because the program thinks there is a whiteline between them. The solution
is to check if the regions close by the regular one are indeed quite different, or not. In that case, we absorb
the nearest region into the regular one.
--> That is a refinement issue that is likely to occur for more docs in the future.
--> Modest amount of work.

* In the document like Plan_Velo, there is quite a lot of bold text. As this is a criterion to identify headlines,
things do not work out OK. If the author uses bold text, like 30% of the time (which is the case), it carries little
meaning and we should omit using it as a selection criteria. We calculate the ratio bold characters to total characters
in the document and put a threshold on whether we use bold text as a selection criterion or not (threshold=3%).
--> That one is probably a 1-time issue, although we may have to refine the cut-value a bit (now we have 0.02, 0.03 where bold is OK and 0.30 where bold is not OK).
--> Not a lot of work.

* Enumerations in Plan Velo work with bullets, which is a sign our code did not yet recogise. We added it to the signmark-enumerations.
--> That is a refinement issue that is likely to occur for more docs in the future.
--> Not a lot of work.

* We never tackled 2-column documents before. So we had to make an algorithm (only supported for pdfminer so far)
that distinguished between these two at the moment of text extraction, so the text is extracted in the right order for processing.
This was a very time-consuming & complicated task. Especially because we wanted to do it page-by-page, not for the entire doc at once.
--> that is probably a 1-time issue.
--> that was a LOT of work, especially to do is per page.

* We forgot to do styling on headlines deeper then subsections. This caused the html to look very strange, but it was easily fixed.
--> That was a 1-time issue (bug-finding).

* When chapter titles are clearly marked on their type, guessing the precise cascade is really easy (regex). However,
if this is not done, one has to guess it from the font size (or other layout), which is a lot harder. This document requires
us to do just that. We fixed it by stating that no more then 3 font regions above the regular one should exist. As such, 
we prevent too many variations in cascade levels.
--> That is a refinement issue that is likely to occur for more docs in the future.
--> Modest amount of work.

* We did not take highlights into account before. This document uses highlights to mark headers, not bold fonts or so.
--> It was extremely difficult to implement this in pdfminer, as that one does not recognise this as a font-style naturally. We have implemented a solution using text colors and the attributes that pdfminer offers. this solutions works incredibly well for the French document.
--> A Lot of work, but this was no finetuning, but adding more functionality needed to tackle the document.

* The document puts the letters from the ministers under the WRONG minister. This is because our code searches the document from top to bottom. As such, the Minister-names are recognised as chapter titles and the NEXT letter is put under the name. However, the minister signed the letter, meaning that the PREVIOUS letter belongs to the name. Our standard rules cannot fix this.
--> We fixed this by shifting the content of the alineas up when appropriate. This took a long time do design something that will not shift for chapter titles ABOUT ministers, but only for signings. We test whether the last chapter-title containing the word minister is empty or not. If the document contains signings, this should be the case.
--> Quite some work.

* Note that we still do not recognise every layout element perfectly for the French Plan_Velo document. There are 2 problems:
2) The document contains errors the underlying data. For example: The headline-text: <Soutenir les villes et collectivités engagées dans le développement><de la marche et du vélo> is registered with 2 different font sizes. As such, our code interprets it as 2 different titles on different cascade levels. This is impossible to fix, as we depend on what the PDF gives us.
3) The document contains heavy layout with some numbers on font-72 like 1. 2. 3. etc. As such, it is very difficult to hierarchially order them with the other text. But again,we depend on what the PDF gives us.

* We needed 2 full working days to make the modifications for Plan_Velo, while we needed 3-4 working days to make Copernicus & cellar work.
Both times do NOT include the re-alignment of the test-library, which is always necessary due to small fluctuations in the calculations (that do not really affect the outcome, but we do test againts them. In other situations, the fluctuations may not be so small and we want to know...

* Main reasons:
- 1 column versus 2 columns; no encountered before and a lot of work with laparams (to make page-specific).
- No regex-hooks to appoint cascade levels. Also not encountered before, so we needed some fintuning there.
- Chapter title by highlights; which is not a native feature on pdfminer (we found a solution; but it took time).
- html contained a bug (no styling below subsections; made it look really weird & see to find the problem...)
- 30% Bold text in the document: then it cannot be used to identify structure.
- Letter signings that are about the content BEFORE, not after. And they are political quotes!!!
Were all issues we have never seen before, so then it takes more time.

* Next step is now to go to the user with a gpt-3.5-turbo proper summary and see, if it is useful.

Cellar heeft 380 structure elements, waarvan 2 fout.
Copernicus heeft 58 elementen, allemaal goed.
Plan Velo heeft 67 structure elements, waarvan:
4x foute titel
2x fout in cascade level
5x element dat mist (4/6 big numbers en 1 tussenkopje); ze missen niet, maar zijn leeg.
