import sys
sys.path.insert(1, '../../')

from TextPart.textalinea import textalinea
from TextPart.masterrule import texttype
from TextPart.enum_type import enum_type

def hardcodedalineas_SplitDoc(option: str) -> list[textalinea]:
    """
    Function to load hard-coded textalinea-elements
    that you want to find in the SplitDoc-result.
    
    # Parameters:
    option: str: tells you which library for reading PDF's you ask the content for: pdfminer or pymupdf.
    # Return: list[textalinea]: those textalinea elements:
    """
    
    # --------------------------------------------------------
    
    alinea0 = textalinea()
    alinea0.textlevel = 0
    alinea0.texttitle = "pdfminer or pymupdf"
    alinea0.textcontent.clear()
    alinea0.textcontent.append("We add this alinea to trigger an error when you enter the wrong option.")
    alinea0.summary = "We add this alinea to trigger an error when you enter the wrong option."
    alinea0.parentID = -10
    alinea0.horizontal_ordering = -10
    alinea0.nativeID = -1
    alinea0.sum_CanbeEmpty = False
    alinea0.alineatype = texttype.HEADLINES
    alinea0.enumtype = enum_type.UNKNOWN
    
    alineaT = textalinea()
    alineaT.textlevel = 0
    alineaT.texttitle = "SplitDoc"
    alineaT.nativeID = 0
    alineaT.parentID = -1
    alineaT.alineatype = texttype.TITLE
    alineaT.enumtype = enum_type.UNKNOWN
    alineaT.horizontal_ordering = 0
    alineaT.summary = "1 Let’s kick-of test-driven development 2 1.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1.2 Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1.3 Methods again . . . . . . . . . . . . . . . "
    alineaT.sum_CanbeEmpty = False
    alineaT.textcontent.clear()
    
    alineaTa = textalinea()
    alineaTa.textlevel = 1
    alineaTa.texttitle = "First basic test Document"
    alineaTa.nativeID = 1
    alineaTa.parentID = 0
    alineaTa.alineatype = texttype.HEADLINES
    alineaTa.enumtype = enum_type.UNKNOWN
    alineaTa.horizontal_ordering = 0
    alineaTa.summary = ""
    alineaTa.sum_CanbeEmpty = True
    alineaTa.textcontent.clear()
    
    alinea1 = textalinea()
    alinea1.textlevel = 1
    alinea1.texttitle = "1 Let’s kick-of test-driven development"
    alinea1.textcontent.clear()
    alinea1.textcontent.append("We start with some general text about the chapter.")
    alinea1.textcontent.append("with a line-break embedded in it.")
    alinea1.summary = "We start with some general text about the chapter. with a line-break embedded in it. This is a small test for text extraction. And here is some more text. With a line break and other stuf. Lets add some whitespaces: And some text. With some text..."
    alinea1.parentID = 0
    alinea1.horizontal_ordering = 2
    alinea1.nativeID = 3
    alinea1.sum_CanbeEmpty = False
    alinea1.alineatype = texttype.HEADLINES
    alinea1.enumtype = enum_type.UNKNOWN
    
    alinea2 = textalinea()
    alinea2.textlevel = 2
    alinea2.texttitle = "1.1 Introduction"
    alinea2.textcontent.clear()
    alinea2.textcontent.append("This is a small test for text extraction.")
    alinea2.summary = "This is a small test for text extraction."
    alinea2.parentID = 3
    alinea2.horizontal_ordering = 0
    alinea2.nativeID = 4
    alinea2.sum_CanbeEmpty = False
    alinea2.alineatype = texttype.HEADLINES
    alinea2.enumtype = enum_type.UNKNOWN
    
    alinea3 = textalinea()
    alinea3.textlevel = 2
    alinea3.texttitle = "1.2 Methods"
    alinea3.textcontent.clear()
    alinea3.textcontent.append("And here is some more text.")
    alinea3.textcontent.append("With a line break and other stuf.")
    alinea3.summary = "And here is some more text. With a line break and other stuf."
    alinea3.parentID = 3
    alinea3.horizontal_ordering = 1
    alinea3.nativeID = 5
    alinea3.sum_CanbeEmpty = False
    alinea3.alineatype = texttype.HEADLINES
    alinea3.enumtype = enum_type.UNKNOWN
    
    alinea4 = textalinea()
    alinea4.textlevel = 2
    alinea4.texttitle = "1.3 Methods again"
    alinea4.textcontent.clear()
    alinea4.textcontent.append("Lets add some whitespaces:")
    alinea4.textcontent.append("And some text.")
    alinea4.summary = "Lets add some whitespaces: And some text."
    alinea4.parentID = 3
    alinea4.horizontal_ordering = 2
    alinea4.nativeID = 6
    alinea4.sum_CanbeEmpty = False
    alinea4.alineatype = texttype.HEADLINES
    alinea4.enumtype = enum_type.UNKNOWN
    
    alinea5 = textalinea()
    alinea5.textlevel = 2
    alinea5.texttitle = "1.4 One more section"
    alinea5.textcontent.clear()
    alinea5.textcontent.append("With some text...")
    alinea5.summary = "With some text..."
    alinea5.parentID = 3
    alinea5.horizontal_ordering = 3
    alinea5.nativeID = 7
    alinea5.sum_CanbeEmpty = False
    alinea5.alineatype = texttype.HEADLINES
    alinea5.enumtype = enum_type.UNKNOWN
    
    alinea6 = textalinea()
    alinea6.textlevel = 1
    alinea6.texttitle = "2 A new chapter starts now"
    alinea6.textcontent.clear()
    alinea6.textcontent.append("Now comes some extra text.")
    alinea6.textcontent.append("With a line break.")
    alinea6.summary = "Now comes some extra text. With a line break. Lets give a splendid additional story. with a beautiful subsection embedded in it."
    alinea6.parentID = 0
    alinea6.horizontal_ordering = 3
    alinea6.nativeID = 8
    alinea6.sum_CanbeEmpty = False
    alinea6.alineatype = texttype.HEADLINES
    alinea6.enumtype = enum_type.UNKNOWN
    
    alinea7 = textalinea()
    alinea7.textlevel = 2
    alinea7.texttitle = "2.1 A new section"
    alinea7.textcontent.clear()
    alinea7.textcontent.append("Lets give a splendid additional story.")
    alinea7.summary = "Lets give a splendid additional story. with a beautiful subsection embedded in it."
    alinea7.parentID = 8
    alinea7.horizontal_ordering = 0
    alinea7.nativeID = 9
    alinea7.sum_CanbeEmpty = False
    alinea7.alineatype = texttype.HEADLINES
    alinea7.enumtype = enum_type.UNKNOWN
    
    alinea8 = textalinea()
    alinea8.textlevel = 3
    alinea8.texttitle = "2.1.1 Nice subsection"
    alinea8.textcontent.clear()
    alinea8.textcontent.append("with a beautiful subsection embedded in it.")
    alinea8.summary = "with a beautiful subsection embedded in it."
    alinea8.parentID = 9
    alinea8.horizontal_ordering = 0
    alinea8.nativeID = 10
    alinea8.sum_CanbeEmpty = False
    alinea8.alineatype = texttype.HEADLINES
    alinea8.enumtype = enum_type.UNKNOWN

    alinea9 = textalinea()
    alinea9.textlevel = 1
    alinea9.texttitle = "Contents"
    alinea9.textcontent.clear()
    alinea9.textcontent.append("1 Let’s kick-of test-driven development")
    alinea9.textcontent.append("2")
    alinea9.textcontent.append("1.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2")
    alinea9.textcontent.append("1.2 Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2")
    alinea9.textcontent.append("1.3 Methods again . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2")
    alinea9.textcontent.append("1.4 One more section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3")
    alinea9.textcontent.append("2 A new chapter starts now")
    alinea9.textcontent.append("4")
    alinea9.textcontent.append("2.1 A new section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4")
    alinea9.textcontent.append("2.1.1 Nice subsection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4")
    alinea9.parentID = 0
    alinea9.horizontal_ordering = 1
    alinea9.nativeID = 2
    alinea9.sum_CanbeEmpty = False
    alinea9.summary = ""
    alinea9.alineatype = texttype.HEADLINES
    alinea9.enumtype = enum_type.UNKNOWN
    for textline in alinea9.textcontent:
        alinea9.summary = alinea9.summary + textline + " "
    
    alinea10 = textalinea()
    alinea10.textlevel = 1
    alinea10.texttitle = "Contents"
    alinea10.textcontent.clear()
    alinea10.textcontent.append("1 Let’s kick-of test-driven development")
    alinea10.textcontent.append("2")
    alinea10.textcontent.append("1.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
    alinea10.textcontent.append("2")
    alinea10.textcontent.append("1.2 Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
    alinea10.textcontent.append("2")
    alinea10.textcontent.append("1.3 Methods again")
    alinea10.textcontent.append(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
    alinea10.textcontent.append("2")
    alinea10.textcontent.append("1.4 One more section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
    alinea10.textcontent.append("3")
    alinea10.textcontent.append("2 A new chapter starts now")
    alinea10.textcontent.append("4")
    alinea10.textcontent.append("2.1 A new section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
    alinea10.textcontent.append("4")
    alinea10.textcontent.append("2.1.1 Nice subsection . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
    alinea10.textcontent.append("4")
    alinea10.parentID = 0
    alinea10.horizontal_ordering = 1 
    alinea10.nativeID = 2
    alinea10.sum_CanbeEmpty = False
    alinea10.summary = ""
    alinea10.alineatype = texttype.HEADLINES
    alinea10.enumtype = enum_type.UNKNOWN
    for textline in alinea10.textcontent:
        alinea10.summary = alinea10.summary + textline + " "

    # Add the correct contents:
    textalineas = [alineaT, alineaTa, alinea1, alinea2, alinea3, alinea4, alinea5, alinea6, alinea7, alinea8]
    if (option=="pdfminer"): textalineas.insert(2,alinea9)
    elif (option=="pymupdf"): 
        textalineas.insert(2,alinea10)
        
        # To correct for that pymupdf accidentally finds another level==1 in the titlepage that pdfminer does not:
        for alinea in textalineas:
            if (alinea.textlevel==1):
                alinea.horizontal_ordering = alinea.horizontal_ordering + 1
        textalineas[1].horizontal_ordering = 0
        
    else: textalineas.insert(0,alinea0)
    
    return textalineas

def hardcodedalineas_TestTex(option: str) -> list[textalinea]:
    """
    Function to load hard-coded textalinea-elements
    that you want to find in the TestTex-result.
    
    # Parameters:
    option: str: tells you which library for reading PDF's you ask the content for: pdfminer or pymupdf.
    # Return: list[textalinea]: those textalinea elements:
    """
    
    # --------------------------------------------------------
    
    alinea0 = textalinea()
    alinea0.textlevel = 0
    alinea0.texttitle = "pdfminer or pymupdf"
    alinea0.textcontent.clear()
    alinea0.textcontent.append("We add this alinea to trigger an error when you enter the wrong option.")
    alinea0.summary = "We add this alinea to trigger an error when you enter the wrong option."
    alinea0.parentID = -10
    alinea0.horizontal_ordering = -10
    alinea0.nativeID = -1
    alinea0.sum_CanbeEmpty = False
    alinea0.alineatype = texttype.HEADLINES
    alinea0.enumtype = enum_type.UNKNOWN
    
    alineaT = textalinea()
    alineaT.textlevel = 0
    alineaT.texttitle = "TestTex"
    alineaT.textcontent.clear()
    alineaT.summary = "1 Eerste hoofdstuk 2 1.1 Eerste sectie in het eerste hoofdstuk. . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1.2 En nog een sectie . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1.2.1 Zelfs met een subsectie erin!!! . . . . . . . . . . . "
    alineaT.parentID = -1
    alineaT.horizontal_ordering = 0
    alineaT.nativeID = 0
    alineaT.sum_CanbeEmpty = False
    alineaT.alineatype = texttype.TITLE
    alineaT.enumtype = enum_type.UNKNOWN
    
    alineaTa = textalinea()
    alineaTa.textlevel = 1
    alineaTa.texttitle = "Test title"
    alineaTa.textcontent.clear()
    alineaTa.summary = ""
    alineaTa.parentID = 0
    alineaTa.horizontal_ordering = 0
    alineaTa.nativeID = 1
    alineaTa.sum_CanbeEmpty = True
    alineaTa.alineatype = texttype.HEADLINES
    alineaTa.enumtype = enum_type.UNKNOWN
    
    alineaTb = textalinea()
    alineaTb.textlevel = 3
    alineaTb.texttitle = "Remco van Groesen Ministerie van Infrastructuur en Waterstaat March 23, 2023"
    alineaTb.textcontent.clear()
    alineaTb.summary = ""
    alineaTb.parentID = 1
    alineaTb.horizontal_ordering = 0
    alineaTb.nativeID = 2
    alineaTb.sum_CanbeEmpty = True
    alineaTb.alineatype = texttype.HEADLINES
    alineaTb.enumtype = enum_type.UNKNOWN
    
    alinea1p = textalinea()
    alinea1p.textlevel = 1
    alinea1p.texttitle = "Chapter 1"
    alinea1p.textcontent.clear()
    alinea1p.summary = ""
    alinea1p.parentID = 0
    alinea1p.horizontal_ordering = 2
    alinea1p.nativeID = 4
    alinea1p.sum_CanbeEmpty = True
    alinea1p.alineatype = texttype.HEADLINES
    alinea1p.enumtype = enum_type.UNKNOWN
    
    alinea1 = textalinea()
    alinea1.textlevel = 1
    alinea1.texttitle = "Eerste hoofdstuk"
    alinea1.textcontent.clear()
    alinea1.textcontent.append("Hier staat een inleidende tekst.")
    alinea1.summary = "Hier staat een inleidende tekst. Hier staat over het algemeen een hele hoop tekst Wow, nog een sectie???? Dit had ik niet verwacht."
    alinea1.parentID = 0
    alinea1.horizontal_ordering = 3
    alinea1.nativeID = 5
    alinea1.sum_CanbeEmpty = False
    alinea1.alineatype = texttype.HEADLINES
    alinea1.enumtype = enum_type.UNKNOWN
    
    alinea2 = textalinea()
    alinea2.textlevel = 2
    alinea2.texttitle = "1.1 Eerste sectie in het eerste hoofdstuk."
    alinea2.textcontent.clear()
    alinea2.textcontent.append("Hier staat over het algemeen een hele hoop tekst")
    alinea2.summary = "Hier staat over het algemeen een hele hoop tekst"
    alinea2.parentID = 5
    alinea2.horizontal_ordering = 0
    alinea2.nativeID = 6
    alinea2.sum_CanbeEmpty = False
    alinea2.alineatype = texttype.HEADLINES
    alinea2.enumtype = enum_type.UNKNOWN
    
    alinea3 = textalinea()
    alinea3.textlevel = 2
    alinea3.texttitle = "1.2 En nog een sectie"
    alinea3.textcontent.clear()
    alinea3.textcontent.append("Wow, nog een sectie????")
    alinea3.summary = "Wow, nog een sectie???? Dit had ik niet verwacht."
    alinea3.parentID = 5
    alinea3.horizontal_ordering = 1
    alinea3.nativeID = 7
    alinea3.sum_CanbeEmpty = False
    alinea3.alineatype = texttype.HEADLINES
    alinea3.enumtype = enum_type.UNKNOWN
    
    alinea4 = textalinea()
    alinea4.textlevel = 3
    alinea4.texttitle = "1.2.1 Zelfs met een subsectie erin!!!"
    alinea4.textcontent.clear()
    alinea4.textcontent.append("Dit had ik niet verwacht.")
    alinea4.summary = "Dit had ik niet verwacht."
    alinea4.parentID = 7
    alinea4.horizontal_ordering = 0
    alinea4.nativeID = 8
    alinea4.sum_CanbeEmpty = False
    alinea4.alineatype = texttype.HEADLINES
    alinea4.enumtype = enum_type.UNKNOWN
    
    alinea5p = textalinea()
    alinea5p.textlevel = 1
    alinea5p.texttitle = "Chapter 2"
    alinea5p.textcontent.clear()
    alinea5p.summary = ""
    alinea5p.parentID = 0
    alinea5p.horizontal_ordering = 4
    alinea5p.nativeID = 9
    alinea5p.sum_CanbeEmpty = True
    alinea5p.alineatype = texttype.HEADLINES
    alinea5p.enumtype = enum_type.UNKNOWN
    
    alinea5 = textalinea()
    alinea5.textlevel = 1
    alinea5.texttitle = "Tweede hoofdstuk"
    alinea5.textcontent.clear()
    alinea5.textcontent.append("Het tweede hoofdstuk gaat een stuk korter zijn dan de eerste")
    alinea5.summary = "Het tweede hoofdstuk gaat een stuk korter zijn dan de eerste Dit is alles wat in het tweede hoofdstuk staat."
    alinea5.parentID = 0
    alinea5.horizontal_ordering = 5
    alinea5.nativeID = 10
    alinea5.sum_CanbeEmpty = False
    alinea5.alineatype = texttype.HEADLINES
    alinea5.enumtype = enum_type.UNKNOWN

    alinea6 = textalinea()
    alinea6.textlevel = 2
    alinea6.texttitle = "2.1 Dit is alles wat in het tweede hoofdstuk staat"
    alinea6.textcontent.clear()
    alinea6.textcontent.append("Dit is alles wat in het tweede hoofdstuk staat.")
    alinea6.summary = "Dit is alles wat in het tweede hoofdstuk staat."
    alinea6.parentID = 10
    alinea6.horizontal_ordering = 0
    alinea6.nativeID = 11
    alinea6.sum_CanbeEmpty = False
    alinea6.alineatype = texttype.HEADLINES
    alinea6.enumtype = enum_type.UNKNOWN
    
    alinea7 = textalinea()
    alinea7.textlevel = 1
    alinea7.texttitle = "Contents"
    alinea7.textcontent.clear()
    alinea7.textcontent.append("1 Eerste hoofdstuk")
    alinea7.textcontent.append("2")
    alinea7.textcontent.append("1.1 Eerste sectie in het eerste hoofdstuk. . . . . . . . . . . . . . . . . . . . . . . . . . . . 2")
    alinea7.textcontent.append("1.2 En nog een sectie . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2")
    alinea7.textcontent.append("1.2.1 Zelfs met een subsectie erin!!! . . . . . . . . . . . . . . . . . . . . . . . . . . . 2")
    alinea7.textcontent.append("2 Tweede hoofdstuk")
    alinea7.textcontent.append("3")
    alinea7.textcontent.append("2.1 Dit is alles wat in het tweede hoofdstuk staat . . . . . . . . . . . . . . . . . . . . . . 3")
    alinea7.parentID = 0
    alinea7.horizontal_ordering = 1
    alinea7.nativeID = 3
    alinea7.sum_CanbeEmpty = False
    alinea7.summary = ""
    alinea7.alineatype = texttype.HEADLINES
    alinea7.enumtype = enum_type.UNKNOWN
    for textline in alinea7.textcontent:
        alinea7.summary = alinea7.summary + textline + " "
    
    alinea8 = textalinea()
    alinea8.textlevel = 1
    alinea8.texttitle = "Contents"
    alinea8.textcontent.clear()
    alinea8.textcontent.append("1")
    alinea8.textcontent.append("Eerste hoofdstuk")
    alinea8.textcontent.append("2")
    alinea8.textcontent.append("1.1")
    alinea8.textcontent.append("Eerste sectie in het eerste hoofdstuk. . . . . . . . . . . . . . . . . . . . . . . . . . . .")
    alinea8.textcontent.append("2")
    alinea8.textcontent.append("1.2")
    alinea8.textcontent.append("En nog een sectie . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
    alinea8.textcontent.append("2")
    alinea8.textcontent.append("1.2.1")
    alinea8.textcontent.append("Zelfs met een subsectie erin!!! . . . . . . . . . . . . . . . . . . . . . . . . . . .")
    alinea8.textcontent.append("2")
    alinea8.textcontent.append("2")
    alinea8.textcontent.append("Tweede hoofdstuk")
    alinea8.textcontent.append("3")
    alinea8.textcontent.append("2.1")
    alinea8.textcontent.append("Dit is alles wat in het tweede hoofdstuk staat . . . . . . . . . . . . . . . . . . . . . .")
    alinea8.textcontent.append("3")
    alinea8.parentID = 0
    alinea8.horizontal_ordering = 1
    alinea8.nativeID = 3
    alinea8.sum_CanbeEmpty = False
    alinea8.summary = ""
    alinea8.alineatype = texttype.HEADLINES
    alinea8.enumtype = enum_type.UNKNOWN
    for textline in alinea8.textcontent:
        alinea8.summary = alinea8.summary + textline + " "

    # Add the correct contents:
    textalineas = [alineaT, alineaTa, alineaTb, alinea1p, alinea1, alinea2, alinea3, alinea4, alinea5p, alinea5, alinea6]
    if (option=="pdfminer"): textalineas.insert(3,alinea7)
    elif (option=="pymupdf"): 
        textalineas.insert(3,alinea8)
    else: textalineas.insert(0,alinea0)
    
    return textalineas    
