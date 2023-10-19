import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.read_native_toc import Native_TOC_Element

def hardcoded_DNN_TOC() -> list[Native_TOC_Element]:
    """
    Function to load hard-coded Native_TOC_Element-objects that
    correspond to the DNN-paper.
    
    # Parameters: None.
    # Return: list[Native_TOC_Element]: those Native_TOC_Element elements:
    """
    
    # --------------------------------------------------------
    
    element0 = Native_TOC_Element()
    element0.cascadelevel = 0
    element0.title = "Development of a Deep Neural Network for the data analysis of the NeuLAND neutron detector"
    
    element1 = Native_TOC_Element()
    element1.cascadelevel = 1
    element1.title = "Introduction"
    
    element2 = Native_TOC_Element()
    element2.cascadelevel = 1
    element2.title = "Methodology"
    
    element3 = Native_TOC_Element()
    element3.cascadelevel = 2
    element3.title = "Data generation and preparation"
    
    element4 = Native_TOC_Element()
    element4.cascadelevel = 2
    element4.title = "Multiplicity determination"

    element5 = Native_TOC_Element()
    element5.cascadelevel = 2
    element5.title = "``Hit'' selection"
    
    element6 = Native_TOC_Element()
    element6.cascadelevel = 2
    element6.title = "Reference algorithms"
    
    element7 = Native_TOC_Element()
    element7.cascadelevel = 2
    element7.title = "Sources of uncertainties"
    
    element8 = Native_TOC_Element()
    element8.cascadelevel = 1
    element8.title = "Performance of multiplicity determination"
    
    element9 = Native_TOC_Element()
    element9.cascadelevel = 1
    element9.title = "``Hit'' selection performance"
    
    element10 = Native_TOC_Element()
    element10.cascadelevel = 1
    element10.title = "Extraction of the neutron scattering angle and its impact on observables"
    
    element11 = Native_TOC_Element()
    element11.cascadelevel = 1
    element11.title = "Conclusion"
    
    element12 = Native_TOC_Element()
    element12.cascadelevel = 1
    element12.title = "CRediT authorship contribution statement"
    
    element13 = Native_TOC_Element()
    element13.cascadelevel = 1
    element13.title = "Declaration of competing interest"
    
    element14 = Native_TOC_Element()
    element14.cascadelevel = 1
    element14.title = "Acknowledgments"
    
    element15 = Native_TOC_Element()
    element15.cascadelevel = 1
    element15.title = "Appendix. Network structure optimalization"
    
    element16 = Native_TOC_Element()
    element16.cascadelevel = 1
    element16.title = "References"
    
    # Now compose the array:
    elements = [element0, element1, element2, element3, element4, element5, element6, element7, element8, element9, element10, element11, element12, element13, element14, element15, element16] 
    return elements

def hardcoded_LineTest1_TOC_pdfminer() -> list[Native_TOC_Element]:
    """
    Function to load hard-coded Native_TOC_Element-objects that
    correspond to the LineTest1.pdf document.
    
    # Parameters: None.
    # Return: list[Native_TOC_Element]: those Native_TOC_Element elements:
    """
    
    # --------------------------------------------------------
    
    element0 = Native_TOC_Element()
    element0.cascadelevel = 1
    element0.title = "1. ACHTERGROND VAN HET VOORSTEL"
    
    element1 = Native_TOC_Element()
    element1.cascadelevel = 2
    element1.title = "1.1. Motivering en doel van het voorstel"
    
    element2 = Native_TOC_Element()
    element2.cascadelevel = 2
    element2.title = "1.2. Verenigbaarheid met bestaande bepalingen op het beleidsterrein"
    
    # Now compose the array:
    elements = [element0, element1, element2] 
    return elements

def hardcoded_LineTest1_TOC_pymupdf() -> list[Native_TOC_Element]:
    """
    Function to load hard-coded Native_TOC_Element-objects that
    correspond to the LineTest1.pdf document.
    
    # Parameters: None.
    # Return: list[Native_TOC_Element]: those Native_TOC_Element elements:
    """
    
    # --------------------------------------------------------
    
    element0 = Native_TOC_Element()
    element0.cascadelevel = 2
    element0.title = "1. "
    
    element1 = Native_TOC_Element()
    element1.cascadelevel = 2
    element1.title = "1.1. Motivering en doel van het voorstel"
    
    element2 = Native_TOC_Element()
    element2.cascadelevel = 2
    element2.title = "1.2. Verenigbaarheid met bestaande bepalingen op het beleidsterrein"
    
    # Now compose the array:
    elements = [element0, element1, element2] 
    return elements
    
def hardcoded_LineTest2_pdfminer_TOC() -> list[Native_TOC_Element]:
    """
    Function to load hard-coded Native_TOC_Element-objects that
    correspond to the LineTest1.pdf document.
    
    # Parameters: None.
    # Return: list[Native_TOC_Element]: those Native_TOC_Element elements:
    """
    
    # --------------------------------------------------------
    
    element0 = Native_TOC_Element()
    element0.cascadelevel = 1
    element0.title = "I. CONTEXT AND CONTENT OF THE PROPOSAL"
    
    element1 = Native_TOC_Element()
    element1.cascadelevel = 1
    element1.title = "II. STATE OF PLAY"
    
    element2 = Native_TOC_Element()
    element2.cascadelevel = 1
    element2.title = "III. THE PROPOSED MANDATE"
    
    # Now compose the array:
    elements = [element0, element1, element2] 
    return elements

def hardcoded_LineTest2_pymupdf_TOC() -> list[Native_TOC_Element]:
    """
    Function to load hard-coded Native_TOC_Element-objects that
    correspond to the LineTest1.pdf document.
    
    # Parameters: None.
    # Return: list[Native_TOC_Element]: those Native_TOC_Element elements:
    """
    
    # --------------------------------------------------------
    
    element0 = Native_TOC_Element()
    element0.cascadelevel = 1
    element0.title = "I."
    
    element1 = Native_TOC_Element()
    element1.cascadelevel = 1
    element1.title = "II. STATE OF PLAY"
    
    element2 = Native_TOC_Element()
    element2.cascadelevel = 1
    element2.title = "III."
    
    # Now compose the array:
    elements = [element0, element1, element2] 
    return elements

def hardcoded_cellar_TOC() -> list[Native_TOC_Element]:
    """
    Function to load hard-coded Native_TOC_Element-objects that
    correspond to the cellar_DGMI document using pymupdf.
    
    # Parameters: None.
    # Return: list[Native_TOC_Element]: those Native_TOC_Element elements:
    """
    
    # --------------------------------------------------------

    true_elements = []
    
    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 0
    thiselement.title = "1. ACHTERGROND VAN HET VOORSTEL"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 747.3
    thiselement.Zpos = 0
    thiselement.page = 2
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "1.1. Motivering en doel van het voorstel"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 668.6
    thiselement.Zpos = 0
    thiselement.page = 2
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "1.2. Verenigbaarheid met bestaande bepalingen op het beleidsterrein"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 518.6
    thiselement.Zpos = 0
    thiselement.page = 4
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "1.3. Verenigbaarheid met andere beleidsterreinen van de Unie"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 662.6
    thiselement.Zpos = 0
    thiselement.page = 6
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 0
    thiselement.title = "2. RECHTSGRONDSLAG, SUBSIDIARITEIT EN EVENREDIGHEID"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 356.5
    thiselement.Zpos = 0
    thiselement.page = 7
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "2.1. Rechtsgrondslag"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 336.7
    thiselement.Zpos = 0
    thiselement.page = 7
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "2.2. Subsidiariteit (bij niet-exclusieve bevoegdheid)"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 635.1
    thiselement.Zpos = 0
    thiselement.page = 8
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "2.3. Evenredigheid"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 299.6
    thiselement.Zpos = 0
    thiselement.page = 8
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "2.4. Keuze van het instrument"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 521.9
    thiselement.Zpos = 0
    thiselement.page = 9
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 0
    thiselement.title = "3. EX-POSTEVALUATIE, RAADPLEGING VAN BELANGHEBBENDEN EN EFFECTBEOORDELING"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 753.3
    thiselement.Zpos = 0
    thiselement.page = 10
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "3.1. Evaluatie van de bestaande wetgeving en controle van de resultaatgerichtheid ervan"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 719.7
    thiselement.Zpos = 0
    thiselement.page = 10
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "3.2. Raadpleging van belanghebbenden"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 394.2
    thiselement.Zpos = 0
    thiselement.page = 10
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "3.3. Bijeenbrengen en gebruik van expertise"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 649
    thiselement.Zpos = 0
    thiselement.page = 11
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "3.4. Effectbeoordeling"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 447.7
    thiselement.Zpos = 0
    thiselement.page = 11
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "3.5. Resultaatgerichtheid en vereenvoudiging"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 313.4
    thiselement.Zpos = 0
    thiselement.page = 12
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "3.6. Grondrechten"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 414.3
    thiselement.Zpos = 0
    thiselement.page = 13
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 0
    thiselement.title = "4. GEVOLGEN VOOR DE BEGROTING"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 342.9
    thiselement.Zpos = 0
    thiselement.page = 13
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 0
    thiselement.title = "5. OVERIGE ELEMENTEN"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 271.5
    thiselement.Zpos = 0
    thiselement.page = 13
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "5.1. Uitvoeringsplanning en regelingen betreffende controle, evaluatie en rapportage"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 251.7
    thiselement.Zpos = 0
    thiselement.page = 13
    true_elements.append(thiselement)

    thiselement = Native_TOC_Element()
    thiselement.cascadelevel = 1
    thiselement.title = "5.2. Artikelsgewijze toelichting"
    thiselement.Xpos = 70.9
    thiselement.Ypos = 562.3
    thiselement.Zpos = 0
    thiselement.page = 14
    true_elements.append(thiselement)
    
    return true_elements
