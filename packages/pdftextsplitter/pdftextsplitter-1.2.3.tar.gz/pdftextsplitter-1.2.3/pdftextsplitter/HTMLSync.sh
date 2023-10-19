#!/bin/bash

# This script will synchronize the html's in True-outputs
# with the ones in Calc-outputs after changes to the html-parser
# have been made.

# ATTENTION:
# First run your tests and inspect the results. Once you know that
# the new html's look OK (by visual inspection) and no other errors
# are found in the tests, it is OK to run this script. Otherwise NOT!!!
# therefore, you need to type that you checked:

# Execute regression tests:
cd ./Tests/Scripts/
python RegressionTests.py dummy
cp ../Calc_Outputs/Copernicus_html_visualization.html ../True_Outputs/Copernicus_html_visualization.html
cp ../Calc_Outputs/cellar_html_visualization.html ../True_Outputs/cellar_html_visualization.html
cp ../Calc_Outputs/Plan_Velo_FR_html_visualization.html ../True_Outputs/Plan_Velo_FR_html_visualization.html
cp ../Calc_Outputs/Christiaan PhD Thesis_html_visualization.html ../True_Outputs/

# Execute SplitDoc Testst:
python TestSplitDoc.py pdfminer
cp ../Calc_Outputs/SplitDoc_html_visualization.html ../True_Outputs/SplitDoc_pdfminer_html_visualization.html
cp ../Calc_Outputs/TestTex_html_visualization.html ../True_Outputs/TestTex_pdfminer_html_visualization.html
python TestSplitDoc.py pymupdf
cp ../Calc_Outputs/SplitDoc_html_visualization.html ../True_Outputs/SplitDoc_pymupdf_html_visualization.html
cp ../Calc_Outputs/TestTex_html_visualization.html ../True_Outputs/TestTex_pymupdf_html_visualization.html

# Execute Whitelines Test:
python TestWhiteLines.py pdfminer
cp ../Calc_Outputs/LineTest1_html_visualization.html ../True_Outputs/LineTest1_pdfminer_html_visualization.html
cp ../Calc_Outputs/LineTest2_html_visualization.html ../True_Outputs/LineTest2_pdfminer_html_visualization.html
python TestWhiteLines.py pymupdf
cp ../Calc_Outputs/LineTest1_html_visualization.html ../True_Outputs/LineTest1_pymupdf_html_visualization.html
cp ../Calc_Outputs/LineTest2_html_visualization.html ../True_Outputs/LineTest2_pymupdf_html_visualization.html

# Execute Column-test:
python TestTwoColumns.py dummy
cp ../Calc_Outputs/Plan_Velo_FR_page5_html_visualization.html ../True_Outputs/Plan_Velo_FR_page5_html_visualization.html

# Execute Enumeration-test:
python TestEnumerations.py dummy
cp ../Calc_Outputs/Opsomming_html_visualization.html ../True_Outputs/Opsomming_html_visualization.html

# Execute html parser unit test:
python TestHTMLPrint.py
cp ../Calc_Outputs/TestHTMLconversion_html_visualization.html ../True_Outputs/TestHTMLconversion_html_visualization.html
