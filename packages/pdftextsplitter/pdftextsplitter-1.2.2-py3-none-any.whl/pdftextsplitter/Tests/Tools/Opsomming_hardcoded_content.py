import sys
sys.path.insert(1, "../../")

from TextPart.textalinea import textalinea
from TextPart.masterrule import texttype
from TextPart.enum_type import enum_type

def hardcodedalineas_Opsomming() -> list[textalinea]:
    """
    This code holds the content of the textalineas-array in the textsplitter-class
    for the document Opsomming
    It is generated with the printcode()-functions of textsplitter & textalinea
    and it is supposed to be used only after a complete document analysis
    the outcome of this analysis (this script) can then be efficiently used
    for running regression-tests in the future.

    # Parameters: None (everything is hardcoded)
    # Return: list[textalinea] the hardcoded textalineas-array.
    """

    alineas = []

    thisalinea = textalinea()
    thisalinea.textlevel = 0
    thisalinea.texttitle = "Opsomming"
    thisalinea.nativeID = 0
    thisalinea.parentID = -1
    thisalinea.alineatype = texttype.TITLE
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "Hier even een stukje text om te zorgen dat een normale regelafstand het vaakste voorkomt. Why, my dear, you must know, Mrs. Long says that Netherﬁeld is taken by a young man of large fortune from the north of England; that he came down on Monday in a chaise and four to see the place, and was so much delighted with it, that he agreed with Mr. Morris immediately; that he is to take possession before Michaelmas, and some of his servants are to be in the house by the end of next week. Not all that Mrs. Bennet, however, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Dit is echt een hoofdstuk met een lange titel."
    thisalinea.nativeID = 1
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "Hier even een stukje text om te zorgen dat een normale regelafstand het vaakste voorkomt. Why, my dear, you must know, Mrs. Long says that Netherﬁeld is taken by a young man of large fortune from the north of England; that he came down on Monday in a chaise and four to see the place, and was so much delighted with it, that he agreed with Mr. Morris immediately; that he is to take possession before Michaelmas, and some of his servants are to be in the house by the end of next week. Not all that Mrs. Bennet, however, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Hier even een stukje text om te zorgen dat een normale regelafstand het")
    thisalinea.textcontent.append("vaakste voorkomt.")
    thisalinea.textcontent.append("Why, my dear, you must know, Mrs. Long says that Netherﬁeld is taken by a young")
    thisalinea.textcontent.append("man of large fortune from the north of England; that he came down on Monday in a")
    thisalinea.textcontent.append("chaise and four to see the place, and was so much delighted with it, that he agreed")
    thisalinea.textcontent.append("with Mr. Morris immediately; that he is to take possession before Michaelmas, and")
    thisalinea.textcontent.append("some of his servants are to be in the house by the end of next week. Not all that Mrs.")
    thisalinea.textcontent.append("Bennet, however, with the assistance of her ﬁve daughters, could ask on the subject,")
    thisalinea.textcontent.append("was suﬃcient to draw from her husband any satisfactory description of Mr. Bingley.")
    thisalinea.textcontent.append("They attacked him in various ways–with barefaced questions, ingenious suppositions,")
    thisalinea.textcontent.append("and distant surmises; but he eluded the skill of them all, and they were at last obliged")
    thisalinea.textcontent.append("to accept the second-hand intelligence of their neighbour, Lady Lucas. Her report was")
    thisalinea.textcontent.append("highly favourable. Sir William had been delighted with him. He was quite young,")
    thisalinea.textcontent.append("wonderfully handsome, extremely agreeable, and, to crown the whole, he meant to")
    thisalinea.textcontent.append("be at the next assembly with a large party. Nothing could be more delightful! To be")
    thisalinea.textcontent.append("fond of dancing was a certain step towards falling in love; and very lively hopes of")
    thisalinea.textcontent.append("Mr. Bingley’s heart were entertained.")
    thisalinea.textcontent.append("Nu testen we nog even of een zin die eindigt met een bepaald woord en dan op de")
    thisalinea.textcontent.append("volgende regel een getal, ook gezien wordt als opsomming: dit is Figure")
    thisalinea.textcontent.append("2. en dan gaat de tekst hopelijk normaal verder.")
    thisalinea.textcontent.append("En dan teste we dat ook nog even voor condition")
    thisalinea.textcontent.append("2. en dan gaat de tekst hopelijk ook verder.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "1. Dit kan zowel een hoofdstuk ..."
    thisalinea.nativeID = 2
    thisalinea.parentID = 1
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Dit kan zowel een hoofdstuk als opsomming zijn. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Dit kan zowel een hoofdstuk als opsomming zijn.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "2. Dit is dan de vervelende ..."
    thisalinea.nativeID = 3
    thisalinea.parentID = 1
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Dit is dan de vervelende opsomming die vertelt dat het vorige punt een opsom- ming is en geen headlines. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Dit is dan de vervelende opsomming die vertelt dat het vorige punt een opsom-")
    thisalinea.textcontent.append("ming is en geen headlines.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 1"
    thisalinea.nativeID = 4
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "1. Dit kan dan weer zowel een hoofdstuk als opsomming zijn. (a) En nog wat (b) en nog meer 2. Dit is de tweede opsomming. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Dit kan dan weer zowel ..."
    thisalinea.nativeID = 5
    thisalinea.parentID = 4
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Dit kan dan weer zowel een hoofdstuk als opsomming zijn. (a) En nog wat (b) en nog meer "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Dit kan dan weer zowel een hoofdstuk als opsomming zijn.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) En nog wat "
    thisalinea.nativeID = 6
    thisalinea.parentID = 5
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) En nog wat "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) En nog wat")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) en nog meer "
    thisalinea.nativeID = 7
    thisalinea.parentID = 5
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) en nog meer "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) en nog meer")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Dit is de tweede opsomming. "
    thisalinea.nativeID = 8
    thisalinea.parentID = 4
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Dit is de tweede opsomming. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Dit is de tweede opsomming.")
    alineas.append(thisalinea)

    return alineas
