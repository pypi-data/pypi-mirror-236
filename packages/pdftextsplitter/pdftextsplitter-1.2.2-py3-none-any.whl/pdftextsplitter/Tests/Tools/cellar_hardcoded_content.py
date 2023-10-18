import sys
sys.path.insert(1, '../../')

from TextPart.textalinea import textalinea
from TextPart.masterrule import texttype
from TextPart.enum_type import enum_type

def hardcodedalineas_cellar() -> list[textalinea]:
    """
    This code holds the content of the textalineas-array in the textsplitter-class
    for the document cellar
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
    thisalinea.texttitle = "cellar"
    thisalinea.nativeID = 0
    thisalinea.parentID = -1
    thisalinea.alineatype = texttype.TITLE
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "Brussel, 14.7.2021 COM(2021) 559 final 2021/0223 (COD) Voorstel voor een (Voor de EER relevante tekst) {SEC(2021) 560 final} - {SWD(2021) 631 final} - {SWD(2021) 632 final} - {SWD(2021) 637 final} - {SWD(2021) 638 final} Dit voorstel betreft de vaststelling van een nieuwe verordening voor de uitrol van infrastructuur voor alternatieve brandstoffen. De nieuwe verordening impliceert dat Richtlijn 2014/94/EU1 van het Europees Parlement en de Raad betreffende de uitrol van infrastructuur voor alternatieve brandstoffen zal worden ingetrokken. Mobiliteit en vervoer zijn essentieel voor iedere Europese burger en voor onze hele economie. Vrij verkeer van personen en goederen over de binnengrenzen van "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Brussel, 14.7.2021")
    thisalinea.textcontent.append("COM(2021) 559 final")
    thisalinea.textcontent.append("2021/0223 (COD)")
    thisalinea.textcontent.append("Voorstel voor een")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "VERORDENING VAN HET EUROPEES PARLEMENT EN DE RAAD betreffende de uitrol van infrastructuur voor alternatieve brandstoffen en tot intrekking van Richtlijn 2014/94/EU van het Europees Parlement en de Raad"
    thisalinea.nativeID = 1
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(Voor de EER relevante tekst) {SEC(2021) 560 final} - {SWD(2021) 631 final} - {SWD(2021) 632 final} - {SWD(2021) 637 final} - {SWD(2021) 638 final} "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(Voor de EER relevante tekst)")
    thisalinea.textcontent.append("{SEC(2021) 560 final} - {SWD(2021) 631 final} - {SWD(2021) 632 final} -")
    thisalinea.textcontent.append("{SWD(2021) 637 final} - {SWD(2021) 638 final}")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "TOELICHTING"
    thisalinea.nativeID = 2
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = ""
    thisalinea.sum_CanbeEmpty = True
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "1. ACHTERGROND VAN HET VOORSTEL"
    thisalinea.nativeID = 3
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "Dit voorstel betreft de vaststelling van een nieuwe verordening voor de uitrol van infrastructuur voor alternatieve brandstoffen. De nieuwe verordening impliceert dat Richtlijn 2014/94/EU1 van het Europees Parlement en de Raad betreffende de uitrol van infrastructuur voor alternatieve brandstoffen zal worden ingetrokken. Mobiliteit en vervoer zijn essentieel voor iedere Europese burger en voor onze hele economie. Vrij verkeer van personen en goederen over de binnengrenzen van de Europese Unie is een van de fundamentele vrijheden van de EU en haar interne markt. Mobiliteit biedt Europese burgers en bedrijven talrijke sociaaleconomische voordelen maar heeft ook een steeds grotere impact op het "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Dit voorstel betreft de vaststelling van een nieuwe verordening voor de uitrol van")
    thisalinea.textcontent.append("infrastructuur voor alternatieve brandstoffen. De nieuwe verordening impliceert dat")
    thisalinea.textcontent.append("Richtlijn 2014/94/EU1 van het Europees Parlement en de Raad betreffende de uitrol van")
    thisalinea.textcontent.append("infrastructuur voor alternatieve brandstoffen zal worden ingetrokken.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1.1. Motivering en doel van het voorstel"
    thisalinea.nativeID = 4
    thisalinea.parentID = 3
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "Mobiliteit en vervoer zijn essentieel voor iedere Europese burger en voor onze hele economie. Vrij verkeer van personen en goederen over de binnengrenzen van de Europese Unie is een van de fundamentele vrijheden van de EU en haar interne markt. Mobiliteit biedt Europese burgers en bedrijven talrijke sociaaleconomische voordelen maar heeft ook een steeds grotere impact op het milieu, onder meer in de vorm van een toename van de uitstoot van broeikasgassen en plaatselijke luchtverontreiniging, die de gezondheid en het welzijn van de mens aantasten. In december 2019 heeft de Commissie de mededeling2 over de Europese Green Deal aangenomen. In "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Mobiliteit en vervoer zijn essentieel voor iedere Europese burger en voor onze hele")
    thisalinea.textcontent.append("economie. Vrij verkeer van personen en goederen over de binnengrenzen van de Europese")
    thisalinea.textcontent.append("Unie is een van de fundamentele vrijheden van de EU en haar interne markt. Mobiliteit")
    thisalinea.textcontent.append("biedt Europese burgers en bedrijven talrijke sociaaleconomische voordelen maar heeft ook")
    thisalinea.textcontent.append("een steeds grotere impact op het milieu, onder meer in de vorm van een toename van de")
    thisalinea.textcontent.append("uitstoot van broeikasgassen en plaatselijke luchtverontreiniging, die de gezondheid en het")
    thisalinea.textcontent.append("welzijn van de mens aantasten.")
    thisalinea.textcontent.append("In december 2019 heeft de Commissie de mededeling2 over de Europese Green Deal")
    thisalinea.textcontent.append("aangenomen. In de Europese Green Deal wordt opgeroepen de uitstoot van")
    thisalinea.textcontent.append("broeikasgasemissies door vervoer met 90 % te verminderen. Het is de bedoeling de")
    thisalinea.textcontent.append("economie van de EU tegen 2050 klimaatneutraal te maken en de verontreiniging tegelijk tot")
    thisalinea.textcontent.append("nul te herleiden. In september 2020 heeft de Commissie haar voorstel voor een Europese")
    thisalinea.textcontent.append("klimaatwet aangenomen. Daarin is bepaald dat de netto-uitstoot van broeikasgassen tegen")
    thisalinea.textcontent.append("2030 ten minste 55 % lager moet liggen dan in 1990 en dat Europa een verantwoorde koers")
    thisalinea.textcontent.append("moet varen om tegen 20503 klimaatneutraal te worden. In de mededeling4 een ambitieuzere")
    thisalinea.textcontent.append("klimaatdoelstelling voor Europa voor 2030 wordt gewezen op het belang van een")
    thisalinea.textcontent.append("holistische benadering van grootschalige en lokale infrastructuurplanning en op de behoefte")
    thisalinea.textcontent.append("aan een passende uitrol van infrastructuur voor alternatieve brandstoffen om de transitie")
    thisalinea.textcontent.append("naar een nagenoeg emissievrij wagenpark tegen 2050 te ondersteunen. Op 21 april 2021")
    thisalinea.textcontent.append("bereikten de Raad en het Parlement een voorlopig politiek akkoord over de Europese")
    thisalinea.textcontent.append("klimaatwet.")
    thisalinea.textcontent.append("In december 2020 heeft de Commissie de mededeling5 “Strategie voor duurzame en slimme")
    thisalinea.textcontent.append("mobiliteit” aangenomen. Die legt de basis voor de manier waarop die transformatie van het")
    thisalinea.textcontent.append("EU-vervoerssysteem kan worden bewerkstelligd en bevat concrete mijlpalen om het")
    thisalinea.textcontent.append("vervoerssysteem op koers te houden naar een slimme en duurzame toekomst. De")
    thisalinea.textcontent.append("vervoerssector is nog steeds sterk afhankelijk van fossiele brandstoffen. Voor alle")
    thisalinea.textcontent.append("vervoerswijzen is het bevorderen van het gebruik van emissievrije en emissiearme")
    thisalinea.textcontent.append("voertuigen, vaartuigen en luchtvaartuigen en van hernieuwbare en koolstofarme")
    thisalinea.textcontent.append("brandstoffen een prioritaire doelstelling om de hele vervoerssector duurzamer te maken.")
    thisalinea.textcontent.append("Het toenemende aanbod en gebruik van hernieuwbare en koolstofarme brandstoffen moet")
    thisalinea.textcontent.append("hand in hand gaan met de uitrol van een billijk geografisch gespreid omvattend netwerk van")
    thisalinea.textcontent.append("laad- en tankinfrastructuur om grootschalig gebruik van emissiearme en emissievrije")
    thisalinea.textcontent.append("voertuigen in alle vervoerswijzen mogelijk te maken. Met name op de markten voor")
    thisalinea.textcontent.append("personenauto’s zullen consumenten pas op grote schaal voor emissievrije voertuigen kiezen")
    thisalinea.textcontent.append("als zij er zeker van zijn dat zij hun voertuig overal in de EU en kunnen bijladen of tanken")
    thisalinea.textcontent.append("en als dat even gemakkelijk wordt als voor voertuigen op conventionele brandstoffen. Het")
    thisalinea.textcontent.append("is belangrijk dat geen enkele regio of gebied van de Unie achterblijft en dat regionale")
    thisalinea.textcontent.append("verschillen in de uitrol van infrastructuur voor alternatieve brandstoffen adequaat worden")
    thisalinea.textcontent.append("aangepakt bij de opstelling en uitvoering van nationale beleidskaders.")
    thisalinea.textcontent.append("Richtlijn 2014/94/EU betreffende de uitrol van infrastructuur voor alternatieve brandstoffen")
    thisalinea.textcontent.append("(“de richtlijn”) voorziet in een kader met gemeenschappelijke maatregelen voor de uitrol")
    thisalinea.textcontent.append("van dergelijke infrastructuur in de EU. De lidstaten moeten nationale beleidskaders")
    thisalinea.textcontent.append("ontwikkelen om markten voor alternatieve brandstoffen te creëren en ervoor zorgen dat er")
    thisalinea.textcontent.append("voldoende openbaar toegankelijke laad- en tankpunten komen, met name om het vrije")
    thisalinea.textcontent.append("grensoverschrijdende verkeer van dergelijke voertuigen en vaartuigen op het TEN-T-")
    thisalinea.textcontent.append("netwerk mogelijk te maken. In haar recente verslag over de toepassing van Richtlijn")
    thisalinea.textcontent.append("2014/94/EU betreffende de uitrol van infrastructuur voor alternatieve brandstoffen")
    thisalinea.textcontent.append("constateert de Commissie dat enige vooruitgang is geboekt bij de uitvoering6 van de")
    thisalinea.textcontent.append("richtlijn. De tekortkomingen van het huidige beleidskader zijn echter ook duidelijk")
    thisalinea.textcontent.append("zichtbaar: aangezien er voor de lidstaten geen gedetailleerde en bindende methode bestaat")
    thisalinea.textcontent.append("om streefcijfers te berekenen en maatregelen vast te stellen, loopt het ambitieniveau bij de")
    thisalinea.textcontent.append("vaststelling van streefcijfers en de ondersteuning van het bestaande beleid sterk uiteen. In")
    thisalinea.textcontent.append("het verslag wordt echter geconcludeerd dat er nog geen sprake is van een uitgebreid en")
    thisalinea.textcontent.append("volledig infrastructuurnetwerk voor alternatieve brandstoffen in de Unie als geheel. Evenzo")
    thisalinea.textcontent.append("heeft de Europese Rekenkamer in haar speciaal verslag over laadinfrastructuur opgemerkt")
    thisalinea.textcontent.append("dat er grote belemmeringen blijven bestaan voor het reizen in de EU met elektrische")
    thisalinea.textcontent.append("voertuigen en dat de uitrol van oplaadinfrastructuur in de Unie moet worden versneld7.")
    thisalinea.textcontent.append("De Commissie heeft een ex-postevaluatie van deze richtlijn8 uitgevoerd. Daaruit is")
    thisalinea.textcontent.append("gebleken dat de richtlijn niet het adequate instrument is om de verhoogde klimaatambitie")
    thisalinea.textcontent.append("voor 2030 te verwezenlijken. Een van de belangrijkste problemen is dat de")
    thisalinea.textcontent.append("infrastructuurplanning van de lidstaten doorgaans onvoldoende ambitieus, consistent en")
    thisalinea.textcontent.append("coherent is, waardoor de infrastructuur ontoereikend blijft of ongelijk is gespreid. Er zijn")
    thisalinea.textcontent.append("nog steeds problemen met de interoperabiliteit van de fysieke aansluitingen, terwijl er")
    thisalinea.textcontent.append("nieuwe problemen op het gebied van communicatienormen zijn ontstaan, onder meer")
    thisalinea.textcontent.append("inzake de uitwisseling van gegevens tussen de verschillende actoren in het ecosysteem voor")
    thisalinea.textcontent.append("elektromobiliteit. Ten slotte ontbreekt het aan transparante consumenteninformatie en")
    thisalinea.textcontent.append("gemeenschappelijke betalingssystemen, wat de acceptatie door gebruikers beperkt. Zonder")
    thisalinea.textcontent.append("verdere EU-maatregelen zal dit gebrek aan interoperabele, gemakkelijk te gebruiken")
    thisalinea.textcontent.append("oplaad- en tankinfrastructuur wellicht een belemmering worden voor de noodzakelijke")
    thisalinea.textcontent.append("marktgroei van emissiearme en emissievrije voertuigen, vaartuigen en — in de toekomst —")
    thisalinea.textcontent.append("luchtvaartuigen.")
    thisalinea.textcontent.append("Dit voorstel maakt deel uit van het algemeen pakket gerelateerde beleidsinitiatieven in het")
    thisalinea.textcontent.append("kader van het “Fit for 55”-pakket. Deze beleidsinitiatieven stemmen overeen met de")
    thisalinea.textcontent.append("maatregelen die in alle sectoren van de economie nodig zijn in aanvulling op de nationale")
    thisalinea.textcontent.append("inspanningen om de verhoogde klimaatambitie voor 2030 te verwezenlijken, zoals")
    thisalinea.textcontent.append("beschreven in het werkprogramma 20219 van de Commissie.")
    thisalinea.textcontent.append("Met dit initiatief wil de Commissie de beschikbaarheid en bruikbaarheid van een fijnmazig")
    thisalinea.textcontent.append("en omvattend netwerk van infrastructuur voor alternatieve brandstoffen in de hele EU")
    thisalinea.textcontent.append("waarborgen. Alle gebruikers van voertuigen op alternatieve brandstof (met inbegrip van")
    thisalinea.textcontent.append("schepen en luchtvaartuigen) moeten zich in de hele Unie gemakkelijk kunnen verplaatsen")
    thisalinea.textcontent.append("dankzij essentiële infrastructuur zoals snelwegen, havens en luchthavens. De specifieke")
    thisalinea.textcontent.append("doelstellingen zijn: i) in alle lidstaten de beschikbaarheid van minimuminfrastructuur")
    thisalinea.textcontent.append("waarborgen om het beoogde gebruik van voertuigen op alternatieve brandstof voor alle")
    thisalinea.textcontent.append("vervoerswijzen te ondersteunen om de klimaatdoelstellingen van de EU te halen; ii) de")
    thisalinea.textcontent.append("volledige interoperabiliteit van de infrastructuur waarborgen; en iii) zorgen voor volledige")
    thisalinea.textcontent.append("gebruikersinformatie en adequate betalingsopties.")
    thisalinea.textcontent.append("Om de doelstelling van de Europese Green Deal inzake de reductie van de")
    thisalinea.textcontent.append("broeikasgasemissies door vervoer te halen en in de EU een gemeenschappelijke")
    thisalinea.textcontent.append("vervoersmarkt te ontwikkelen, moet het Europese vervoersnetwerk emissiearme en")
    thisalinea.textcontent.append("emissievrije voertuigen, vaartuigen en luchtvaartuigen volledige connectiviteit en een")
    thisalinea.textcontent.append("naadloze gebruikerservaring bieden. Dat vereist op zijn beurt voldoende kwantiteit en")
    thisalinea.textcontent.append("volledige interoperabiliteit van de infrastructuur over de grenzen heen. Die doelstellingen")
    thisalinea.textcontent.append("kunnen alleen worden bereikt met een gemeenschappelijk Europees regelgevingskader. Dit")
    thisalinea.textcontent.append("initiatief zal bijdragen tot een coherente en consistente ontwikkeling en uitrol van")
    thisalinea.textcontent.append("wagenparken, laad- en tankinfrastructuur en gebruikersinformatie en -diensten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1.2. Verenigbaarheid met bestaande bepalingen op het beleidsterrein"
    thisalinea.nativeID = 5
    thisalinea.parentID = 3
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "Dit initiatief spoort met de andere beleidsinitiatieven van het “Fit for 55”-pakket. Het vormt met name een aanvulling op: i) de verordeningen tot vaststelling van CO2-emissienormen voor nieuwe personenauto’s10, nieuwe lichte bedrijfsvoertuigen11 en zware bedrijfsvoertuigen; en ii) het wetgevingsvoorstel voor de vaststelling van nieuwe CO2- emissienormen voor nieuwe auto’s en nieuwe lichte bedrijfsvoertuigen na 2020, die eveneens deel uitmaken van het “Fit for 55”-pakket12. De CO2-emissienormen vormen een sterke stimulans voor de uitrol van emissiearme en emissievrije voertuigen, waardoor er ook vraag naar infrastructuur voor alternatieve brandstoffen wordt gecreëerd. Dit initiatief zal die transitie mogelijk maken door te waarborgen dat "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Dit initiatief spoort met de andere beleidsinitiatieven van het “Fit for 55”-pakket. Het vormt")
    thisalinea.textcontent.append("met name een aanvulling op: i) de verordeningen tot vaststelling van CO2-emissienormen")
    thisalinea.textcontent.append("voor nieuwe personenauto’s10, nieuwe lichte bedrijfsvoertuigen11 en zware")
    thisalinea.textcontent.append("bedrijfsvoertuigen; en ii) het wetgevingsvoorstel voor de vaststelling van nieuwe CO2-")
    thisalinea.textcontent.append("emissienormen voor nieuwe auto’s en nieuwe lichte bedrijfsvoertuigen na 2020, die")
    thisalinea.textcontent.append("eveneens deel uitmaken van het “Fit for 55”-pakket12. De CO2-emissienormen vormen een")
    thisalinea.textcontent.append("sterke stimulans voor de uitrol van emissiearme en emissievrije voertuigen, waardoor er")
    thisalinea.textcontent.append("ook vraag naar infrastructuur voor alternatieve brandstoffen wordt gecreëerd. Dit initiatief")
    thisalinea.textcontent.append("zal die transitie mogelijk maken door te waarborgen dat er voldoende openbare laad- en")
    thisalinea.textcontent.append("tankinfrastructuur voor lichte en zware wegvoertuigen beschikbaar is.")
    thisalinea.textcontent.append("Er bestaat ook een sterke synergie tussen dit initiatief en de herziening van de richtlijn")
    thisalinea.textcontent.append("hernieuwbare energie13, het voorstel voor een verordening van het Europees Parlement en")
    thisalinea.textcontent.append("de Raad inzake het waarborgen van een gelijk speelveld voor duurzaam luchtvervoer")
    thisalinea.textcontent.append("(RefuelEU Luchtvaart)14 en het voorstel voor een verordening van het Europees Parlement")
    thisalinea.textcontent.append("en de Raad betreffende het gebruik van hernieuwbare en koolstofarme brandstoffen in de")
    thisalinea.textcontent.append("zeevaart (FuelEU Zeevaart)15, waarin verplichtingen worden vastgesteld met betrekking tot")
    thisalinea.textcontent.append("het aanbod van en de vraag naar hernieuwbare en koolstofarme vervoersbrandstoffen. Elk")
    thisalinea.textcontent.append("van die instrumenten bevordert een toename van het aanbod van of de vraag naar duurzame")
    thisalinea.textcontent.append("alternatieve brandstoffen in één of meer vervoerswijzen.")
    thisalinea.textcontent.append("Voor vervoer over water beantwoordt dit initiatief aan de duidelijke eis van de Europese")
    thisalinea.textcontent.append("Green Deal om aangemeerde schepen te verplichten walstroom te gebruiken. Het is volledig")
    thisalinea.textcontent.append("complementair met het initiatief FuelEU-Zeevaart en zal ervoor zorgen dat er in havens")
    thisalinea.textcontent.append("voldoende walstroomvoorzieningen worden geïnstalleerd om elektriciteit te leveren voor")
    thisalinea.textcontent.append("aangemeerde passagiersschepen (o.a. ro-ro-passagiersschepen,")
    thisalinea.textcontent.append("hogesnelheidspassagiersvaartuigen en cruiseschepen) en containerschepen, en dat wordt")
    thisalinea.textcontent.append("ingespeeld op de vraag naar koolstofvrije gassen (d.w.z. bio-LNG en synthetische")
    thisalinea.textcontent.append("gasvormige brandstoffen (e-gas). Bij passagiersschepen varieert de stroombehoefte op de")
    thisalinea.textcontent.append("ligplaats naargelang de scheepscategorie, waardoor ook de investeringsbehoeften in havens")
    thisalinea.textcontent.append("verschillen. Een en ander moet worden afgestemd op de verschillende operationele")
    thisalinea.textcontent.append("kenmerken van havens, waaronder de indeling van terminals. Daarom wordt ten opzichte")
    thisalinea.textcontent.append("van het initiatief FuelEU Zeevaart een verder onderscheid gemaakt tussen categorieën")
    thisalinea.textcontent.append("passagiersschepen, namelijk tussen ro-ro-passagiersschepen en")
    thisalinea.textcontent.append("hogesnelheidspassagiersschepen enerzijds en cruiseschepen anderzijds. Samen met FuelEU")
    thisalinea.textcontent.append('Zeevaart wordt hiermee een antwoord geboden op het huidige “kip of het ei"-dilemma,')
    thisalinea.textcontent.append("waarbij de zeer geringe vraag van scheepsexploitanten naar een elektriciteitsaansluiting op")
    thisalinea.textcontent.append("de ligplaats het voor havens minder aantrekkelijk maakt om in walstroom te investeren. De")
    thisalinea.textcontent.append("beperkte uitrol van walstroom (On-shore power supply- OPS) in havens dreigt de")
    thisalinea.textcontent.append("concurrentie tussen havens te verstoren, met name voor vroege investeerders. Het gevaar")
    thisalinea.textcontent.append("bestaat dat reders van schepen die niet voor OPS zijn uitgerust, voor andere havens zullen")
    thisalinea.textcontent.append("kiezen. Daarom is het belangrijk dat er minimumeisen worden vastgesteld voor zeehavens")
    thisalinea.textcontent.append("op het hele TEN-T-netwerk.")
    thisalinea.textcontent.append("Het initiatief vormt ook een aanvulling op het initiatief ReFuelEU Luchtvaart. In aanvulling")
    thisalinea.textcontent.append("op het initiatief voor duurzame luchtvaartbrandstoffen waarvoor slechts beperkte aparte")
    thisalinea.textcontent.append("tankinfrastructuur vereist is, worden regels vastgesteld voor de elektriciteitsvoorziening voor")
    thisalinea.textcontent.append("stilstaande luchtvaartuigen, ter ondersteuning van de transitie naar een koolstofvrije")
    thisalinea.textcontent.append("luchtvaart.")
    thisalinea.textcontent.append("Naast het wetgevingsvoorstel zal de Commissie inspelen op de behoefte aan aanvullende")
    thisalinea.textcontent.append("onderzoeks- en innovatieactiviteiten (O&I), met name via het gezamenlijk geprogrammeerde")
    thisalinea.textcontent.append("partnerschap voor emissievrij vervoer over water dat is voorgesteld door het Waterborne")
    thisalinea.textcontent.append("Technology Platform in het kader van Horizon Europa, de Gemeenschappelijke")
    thisalinea.textcontent.append("Onderneming Clean Sky 2 en de Gemeenschappelijke Onderneming Schone waterstof, dat in")
    thisalinea.textcontent.append("synergie met deze twee vervoerspartnerschappen werkt.")
    thisalinea.textcontent.append("Dit initiatief spoort tevens met de herziening van de richtlijn hernieuwbare energie. Het")
    thisalinea.textcontent.append("doel is ervoor te zorgen dat het gebrek aan laad- en tankinfrastructuur, als er afzonderlijke")
    thisalinea.textcontent.append("infrastructuur vereist is, geen belemmering vormt voor de algemene omslag naar")
    thisalinea.textcontent.append("hernieuwbare en koolstofarme brandstoffen in de vervoerssector. Op EU-niveau is er geen")
    thisalinea.textcontent.append("beleidsinstrument dat gelijkwaardig is aan de richtlijn betreffende de uitrol van")
    thisalinea.textcontent.append("infrastructuur voor alternatieve brandstoffen dat de uitrol van openbaar toegankelijke laad-")
    thisalinea.textcontent.append("en tankinfrastructuur voor alle vervoerswijzen op equivalente wijze kan waarborgen. Dit")
    thisalinea.textcontent.append("initiatief houdt ook nauw verband met het geplande voorstel tot herziening van de")
    thisalinea.textcontent.append("verordening betreffende de richtsnoeren voor het trans-Europees vervoersnetwerk16. De")
    thisalinea.textcontent.append("geplande herziening van die verordening zal voortbouwen op en een aanvulling vormen op")
    thisalinea.textcontent.append("de infrastructuur voor alternatieve brandstoffen die reeds is aangelegd via afzonderlijke")
    thisalinea.textcontent.append("projecten op de TEN-T-netwerkcorridors. Door consequent naar de bepalingen van dit")
    thisalinea.textcontent.append("initiatief te verwijzen zal de herziening van die verordening een toereikende dekking van")
    thisalinea.textcontent.append("het TEN-T-kernnetwerk en het uitgebreide netwerk waarborgen.")
    thisalinea.textcontent.append("Dit initiatief zal de beschikbaarheid van de nodige infrastructuur voor emissievrije en")
    thisalinea.textcontent.append("emissiearme voertuigen en vaartuigen waarborgen en vormt daarmee ook een aanvulling op")
    thisalinea.textcontent.append("een reeks andere beleidsinitiatieven in het kader van het “Fit for 55”-pakket die de vraag")
    thisalinea.textcontent.append("naar dergelijke voertuigen stimuleren middels prijssignalen die rekening houden met de")
    thisalinea.textcontent.append("externe klimaat- en milieueffecten van fossiele brandstoffen, zoals de herziening van het")
    thisalinea.textcontent.append("emissiehandelssysteem17 en de herziening van de energiebelastingrichtlijn18 van de EU.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1.3. Verenigbaarheid met andere beleidsterreinen van de Unie"
    thisalinea.nativeID = 6
    thisalinea.parentID = 3
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "Dit initiatief moet in synergie werken met de richtlijn energieprestatie van gebouwen19 (EPBD), die betrekking heeft op particuliere laadinfrastructuur en voorziet in voorschriften voor de uitrol van laadinfrastructuur in gebouwen. In de effectbeoordeling ter ondersteuning van dit beleidsinitiatief is uitvoerig ingegaan op de wisselwerking tussen openbare en particuliere laadinfrastructuur. Door ervoor te zorgen dat de nodige infrastructuur voor emissievrije en emissiearme voertuigen en vaartuigen beschikbaar is, vormt dit initiatief ook een aanvulling op de beleidsinspanningen op het gebied van tolheffing, die ook tot doel hebben de vraag naar schonere voertuigen te stimuleren. De Eurovignet-richtlijn20 wordt eveneens herzien om de externe "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Dit initiatief moet in synergie werken met de richtlijn energieprestatie van gebouwen19")
    thisalinea.textcontent.append("(EPBD), die betrekking heeft op particuliere laadinfrastructuur en voorziet in voorschriften")
    thisalinea.textcontent.append("voor de uitrol van laadinfrastructuur in gebouwen. In de effectbeoordeling ter")
    thisalinea.textcontent.append("ondersteuning van dit beleidsinitiatief is uitvoerig ingegaan op de wisselwerking tussen")
    thisalinea.textcontent.append("openbare en particuliere laadinfrastructuur.")
    thisalinea.textcontent.append("Door ervoor te zorgen dat de nodige infrastructuur voor emissievrije en emissiearme")
    thisalinea.textcontent.append("voertuigen en vaartuigen beschikbaar is, vormt dit initiatief ook een aanvulling op de")
    thisalinea.textcontent.append("beleidsinspanningen op het gebied van tolheffing, die ook tot doel hebben de vraag naar")
    thisalinea.textcontent.append("schonere voertuigen te stimuleren. De Eurovignet-richtlijn20 wordt eveneens herzien om de")
    thisalinea.textcontent.append("externe klimaat- en milieu-effecten van fossiele brandstoffen beter in aanmerking te nemen.")
    thisalinea.textcontent.append("Ook de richtlijn schone voertuigen21 is erop gericht de uitrol van emissiearme en")
    thisalinea.textcontent.append("emissievrije voertuigen te versnellen. Een bredere beschikbaarheid van infrastructuur en")
    thisalinea.textcontent.append("een snellere uitrol van emissievrije en emissiearme voertuigen zullen de uitrol van schone")
    thisalinea.textcontent.append("voertuigen in openbare wagenparken indirect faciliteren. Openbare wagenparken (met")
    thisalinea.textcontent.append("name bussen) maken doorgaans echter gebruik van eigen laad- en tankpunten in plaats van")
    thisalinea.textcontent.append("openbaar toegankelijke infrastructuur. De interactie met de richtlijn bestaat er vooral in dat")
    thisalinea.textcontent.append("via normalisatie de interoperabiliteit wordt gewaarborgd.")
    thisalinea.textcontent.append("De uitrol van meer elektrische waterstof- en batterijvoertuigen in het wagenpark van de EU")
    thisalinea.textcontent.append("is ook een belangrijk onderdeel van de waterstofstrategie22 en de strategie van de")
    thisalinea.textcontent.append("Commissie voor de slimme integratie van energiesystemen23. Een te beperkte")
    thisalinea.textcontent.append("beschikbaarheid van de overeenkomstige infrastructuur voor voertuigen kan deze ambities")
    thisalinea.textcontent.append("in gevaar brengen.")
    thisalinea.textcontent.append("Door de invoering van steeds meer emissievrije en emissiearme voertuigen te")
    thisalinea.textcontent.append("vergemakkelijken, draagt dit initiatief ook bij aan de ambitie van de Europese Green Deal")
    thisalinea.textcontent.append("om de vervuiling tot nul terug te brengen, als aanvulling op de Euro 6-emissienormen (voor")
    thisalinea.textcontent.append("auto’s en bestelwagens)24 en Euro VI (voor bussen en vrachtwagens)25, waarin voor alle")
    thisalinea.textcontent.append("voertuigen emissiegrenswaarden zijn vastgesteld.")
    thisalinea.textcontent.append("Tot slot hangt dit initiatief samen met de richtlijn intelligente vervoerssystemen 26, waarvoor")
    thisalinea.textcontent.append("de Commissie voornemens is later dit jaar een voorstel tot herziening in te dienen, en met")
    thisalinea.textcontent.append("de gedelegeerde handelingen daarvan, met name de gedelegeerde verordening betreffende")
    thisalinea.textcontent.append("EU-wijde realtimeverkeersinformatiediensten27. Gezien de snel veranderende dataomgeving")
    thisalinea.textcontent.append("voor alternatieve brandstoffen moet in dit initiatief worden gespecificeerd welke relevante")
    thisalinea.textcontent.append("soorten gegevens beschikbaar moeten worden gesteld, in synergie met het algemene kader")
    thisalinea.textcontent.append("dat is vastgesteld in de ITS-richtlijn.")
    thisalinea.textcontent.append("Horizon Europa is het nieuwe belangrijkste EU-financieringsprogramma voor onderzoek en")
    thisalinea.textcontent.append("innovatie28. Het focust op klimaatverandering, draagt bij tot de verwezenlijking van de")
    thisalinea.textcontent.append("duurzameontwikkelingsdoelstellingen van de VN en stimuleert het concurrentievermogen")
    thisalinea.textcontent.append("en de groei van de EU. Cluster 5: Klimaat, energie en mobiliteit, heeft tot doel de")
    thisalinea.textcontent.append("klimaatverandering te bestrijden door de energie- en vervoersector klimaat- en")
    thisalinea.textcontent.append("milieuvriendelijker, efficiënter en concurrerender, slimmer, veiliger en veerkrachtiger te")
    thisalinea.textcontent.append("maken. Europees onderzoek en innovatie kunnen de transformatieve Green Deal-agenda")
    thisalinea.textcontent.append("aansturen, focussen en versnellen door de richting te bepalen, oplossingen te testen en te")
    thisalinea.textcontent.append("demonstreren, afwegingen te maken en ervoor te zorgen dat het beleid coherent,")
    thisalinea.textcontent.append("innovatievriendelijk en empirisch onderbouwd is. De partnerschappen inzake emissievrij")
    thisalinea.textcontent.append("wegvervoer (2Zero), geconnecteerde, coöperatieve en geautomatiseerde mobiliteit")
    thisalinea.textcontent.append("(CCAM), de Europese waardeketen voor industriële batterijen (Batt4EU), schone waterstof,")
    thisalinea.textcontent.append("de overgang naar schone energie en de stedelijke transitie voor een duurzame toekomst")
    thisalinea.textcontent.append("zullen een belangrijke rol spelen bij de omslag naar een klimaatneutrale en")
    thisalinea.textcontent.append("milieuvriendelijke mobiliteit. De missie voor klimaatneutrale en slimme steden van")
    thisalinea.textcontent.append("Horizon Europa29 heeft tot doel 100 Europese steden tegen 2030 te ondersteunen en te")
    thisalinea.textcontent.append("promoten bij hun systemische transformatie naar klimaatneutraliteit.")
    thisalinea.textcontent.append("Het cohesiebeleid zal een centrale rol spelen bij het helpen van alle regio’s bij hun transitie")
    thisalinea.textcontent.append("naar een groener, klimaatneutraal Europa. Het Europees Fonds voor Regionale")
    thisalinea.textcontent.append("Ontwikkeling en het Cohesiefonds zijn beschikbaar om investeringen in innovatie en uitrol")
    thisalinea.textcontent.append("te ondersteunen, met name in achtergestelde lidstaten en regio’s. Het cohesiebeleid zal")
    thisalinea.textcontent.append("steun bieden voor een duurzaam, slim en veerkrachtig vervoerssysteem dat alle")
    thisalinea.textcontent.append("vervoerswijzen en alle niveaus van het vervoerssysteem bestrijkt, conform de specifieke in")
    thisalinea.textcontent.append("de nationale en regionale programma’s vastgestelde eisen en prioriteiten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "2. RECHTSGRONDSLAG, SUBSIDIARITEIT EN EVENREDIGHEID"
    thisalinea.nativeID = 7
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "Om de goede werking van de interne markt te waarborgen, is de Unie bij het Verdrag betreffende de werking van de Europese Unie (VWEU) gemachtigd bepalingen vast te stellen inzake het gemeenschappelijk vervoerbeleid, titel VI (artikelen 90-91), en de trans- Europese netwerken, titel XVI (artikelen 170-171). Met dit rechtskader in gedachten biedt een optreden op EU-niveau de mogelijkheid de gelijkmatige en algemene uitrol van infrastructuur voor alternatieve brandstoffen beter te coördineren dan wanneer de lidstaten die opdracht alleen zouden moeten vervullen. Dit maakt het zowel voor particuliere gebruikers als voor bedrijven gemakkelijker om zich met een voertuig op alternatieve brandstoffen "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2.1. Rechtsgrondslag"
    thisalinea.nativeID = 8
    thisalinea.parentID = 7
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "Om de goede werking van de interne markt te waarborgen, is de Unie bij het Verdrag betreffende de werking van de Europese Unie (VWEU) gemachtigd bepalingen vast te stellen inzake het gemeenschappelijk vervoerbeleid, titel VI (artikelen 90-91), en de trans- Europese netwerken, titel XVI (artikelen 170-171). Met dit rechtskader in gedachten biedt een optreden op EU-niveau de mogelijkheid de gelijkmatige en algemene uitrol van infrastructuur voor alternatieve brandstoffen beter te coördineren dan wanneer de lidstaten die opdracht alleen zouden moeten vervullen. Dit maakt het zowel voor particuliere gebruikers als voor bedrijven gemakkelijker om zich met een voertuig op alternatieve brandstoffen "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Om de goede werking van de interne markt te waarborgen, is de Unie bij het Verdrag")
    thisalinea.textcontent.append("betreffende de werking van de Europese Unie (VWEU) gemachtigd bepalingen vast te")
    thisalinea.textcontent.append("stellen inzake het gemeenschappelijk vervoerbeleid, titel VI (artikelen 90-91), en de trans-")
    thisalinea.textcontent.append("Europese netwerken, titel XVI (artikelen 170-171). Met dit rechtskader in gedachten biedt")
    thisalinea.textcontent.append("een optreden op EU-niveau de mogelijkheid de gelijkmatige en algemene uitrol van")
    thisalinea.textcontent.append("infrastructuur voor alternatieve brandstoffen beter te coördineren dan wanneer de lidstaten")
    thisalinea.textcontent.append("die opdracht alleen zouden moeten vervullen. Dit maakt het zowel voor particuliere")
    thisalinea.textcontent.append("gebruikers als voor bedrijven gemakkelijker om zich met een voertuig op alternatieve")
    thisalinea.textcontent.append("brandstoffen in de Unie te verplaatsen. Het helpt ook om te voorkomen dat een gebrek aan")
    thisalinea.textcontent.append("of een versnipperde uitrol van infrastructuur voor alternatieve brandstoffen een potentiële")
    thisalinea.textcontent.append("belemmering voor de voltooiing van de interne markt zou worden en de productie van")
    thisalinea.textcontent.append("emissiearme en emissievrije voertuigen door de automobielindustrie zou ontmoedigen.")
    thisalinea.textcontent.append("Om in de Europese Green Deal voor vervoer vastgestelde emissiereductiedoelstellingen te")
    thisalinea.textcontent.append("halen (zoals bekrachtigd door de strategie voor duurzame en slimme mobiliteit), moet het")
    thisalinea.textcontent.append("marktaandeel van emissiearme en emissievrije voertuigen en vaartuigen aanzienlijk")
    thisalinea.textcontent.append("toenemen. Dit zal niet gebeuren zonder de uitrol van een samenhangend en omvattend")
    thisalinea.textcontent.append("netwerk van volledig interoperabele infrastructuur voor alternatieve brandstoffen die het")
    thisalinea.textcontent.append("mogelijk maakt om met een voertuig op alternatieve brandstof door de Unie te reizen. Zoals")
    thisalinea.textcontent.append("bij de vaststelling van de huidige richtlijn is opgemerkt, kan een dergelijk netwerk niet op")
    thisalinea.textcontent.append("adequate wijze door de lidstaten afzonderlijk worden ontwikkeld en is het derhalve")
    thisalinea.textcontent.append("noodzakelijk dat de Unie initiatief neemt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2.2. Subsidiariteit (bij niet-exclusieve bevoegdheid)"
    thisalinea.nativeID = 9
    thisalinea.parentID = 7
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "De toegevoegde waarde van dit EU-initiatief in termen van doeltreffendheid, efficiëntie en synergieën wordt benadrukt in de evaluatie van de huidige richtlijn, in samenhang met de beoordeling van de door de lidstaten ingediende nationale uitvoeringsverslagen. Uit de evaluatie is gebleken dat de ontwikkeling van een gemeenschappelijk EU-kader in zekere mate heeft geholpen om versnippering te voorkomen. Dat kader heeft de ontwikkeling van nationaal beleid voor de ontwikkeling van infrastructuur voor alternatieve brandstoffen in alle lidstaten en de totstandbrenging van een gelijker speelveld binnen de sector ondersteund. Door interoperabiliteit, relevante technische normen en de vaststelling van doelstellingen met vergelijkbare tijdschema’s aan "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("De toegevoegde waarde van dit EU-initiatief in termen van doeltreffendheid, efficiëntie en")
    thisalinea.textcontent.append("synergieën wordt benadrukt in de evaluatie van de huidige richtlijn, in samenhang met de")
    thisalinea.textcontent.append("beoordeling van de door de lidstaten ingediende nationale uitvoeringsverslagen. Uit de")
    thisalinea.textcontent.append("evaluatie is gebleken dat de ontwikkeling van een gemeenschappelijk EU-kader in zekere")
    thisalinea.textcontent.append("mate heeft geholpen om versnippering te voorkomen. Dat kader heeft de ontwikkeling van")
    thisalinea.textcontent.append("nationaal beleid voor de ontwikkeling van infrastructuur voor alternatieve brandstoffen in")
    thisalinea.textcontent.append("alle lidstaten en de totstandbrenging van een gelijker speelveld binnen de sector")
    thisalinea.textcontent.append("ondersteund. Door interoperabiliteit, relevante technische normen en de vaststelling van")
    thisalinea.textcontent.append("doelstellingen met vergelijkbare tijdschema’s aan te moedigen, heeft het beleid van de Unie")
    thisalinea.textcontent.append("voor besparingen en een betere prijs-kwaliteitsverhouding gezorgd. Dat gebeurde door")
    thisalinea.textcontent.append("schaalvoordelen te faciliteren, te vermijden dat naast elkaar werd gewerkt en door middelen")
    thisalinea.textcontent.append("uit te trekken voor de financiering van infrastructuur. De uitvoering van de richtlijn (en van")
    thisalinea.textcontent.append("de ondersteunende activiteiten in dat verband) heeft de samenwerking en de uitwisseling")
    thisalinea.textcontent.append("van informatie over alternatieve brandstoffen tussen de betrokken industrie en publieke")
    thisalinea.textcontent.append("actoren vergemakkelijkt. Zonder de richtlijn zou een dergelijke samenwerking wellicht niet")
    thisalinea.textcontent.append("tot stand zijn gekomen.")
    thisalinea.textcontent.append("Zonder optreden van de Unie zou het zeer onwaarschijnlijk zijn dat in alle lidstaten een")
    thisalinea.textcontent.append("samenhangend en volledig netwerk van volledig interoperabele infrastructuur voor")
    thisalinea.textcontent.append("alternatieve brandstoffen ontstaat, dat gebruikers in staat stelt met een voertuig op")
    thisalinea.textcontent.append("alternatieve brandstof door de Unie te reizen. Dit is op zijn beurt een voorwaarde voor de")
    thisalinea.textcontent.append("uitrol van dergelijke voertuigen in de hele Unie, wat voor de EU van vitaal belang is om")
    thisalinea.textcontent.append("haar verhoogde klimaatambitie voor 2030 te halen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2.3. Evenredigheid"
    thisalinea.nativeID = 10
    thisalinea.parentID = 7
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "Overeenkomstig het evenredigheidsbeginsel gaat dit voorstel niet verder dan wat nodig is om de geformuleerde doelstellingen te verwezenlijken. Alle maatregelen worden geacht evenredig te zijn wat hun effect betreft, zoals blijkt uit de effectbeoordeling bij dit initiatief1. De voorgestelde maatregel voorziet in meer bindende voorschriften voor de lidstaten om te zorgen dat er in de hele Unie voldoende openbaar toegankelijke infrastructuur beschikbaar is voor het opladen en bijtanken van voertuigen op alternatieve brandstoffen. Dit is noodzakelijk voor de EU om haar aangescherpte klimaat- en energieambitie voor 2030 te verwezenlijken en te voldoen aan de algemene doelstelling om uiterlijk in 2050 "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Overeenkomstig het evenredigheidsbeginsel gaat dit voorstel niet verder dan wat nodig is")
    thisalinea.textcontent.append("om de geformuleerde doelstellingen te verwezenlijken. Alle maatregelen worden geacht")
    thisalinea.textcontent.append("evenredig te zijn wat hun effect betreft, zoals blijkt uit de effectbeoordeling bij dit")
    thisalinea.textcontent.append("initiatief1. De voorgestelde maatregel voorziet in meer bindende voorschriften voor de")
    thisalinea.textcontent.append("lidstaten om te zorgen dat er in de hele Unie voldoende openbaar toegankelijke")
    thisalinea.textcontent.append("infrastructuur beschikbaar is voor het opladen en bijtanken van voertuigen op alternatieve")
    thisalinea.textcontent.append("brandstoffen. Dit is noodzakelijk voor de EU om haar aangescherpte klimaat- en")
    thisalinea.textcontent.append("energieambitie voor 2030 te verwezenlijken en te voldoen aan de algemene doelstelling om")
    thisalinea.textcontent.append("uiterlijk in 2050 klimaatneutraal te zijn, een doelstelling die onder meer tot uiting komt in")
    thisalinea.textcontent.append("de CO2-normen voor auto’s en bestelwagens, en om de grensoverschrijdende connectiviteit")
    thisalinea.textcontent.append("voor dergelijke voertuigen op het TEN-T-kernnetwerk en het uitgebreide netwerk te")
    thisalinea.textcontent.append("waarborgen.")
    thisalinea.textcontent.append("Uit de ervaring met de uitvoering van de huidige richtlijn blijkt dat deze herziene maatregel")
    thisalinea.textcontent.append("noodzakelijk is. De uitvoering van de huidige richtlijn leidt tot een ongelijke spreiding van")
    thisalinea.textcontent.append("infrastructuur in de lidstaten, waardoor geen dicht en omvattend netwerk van infrastructuur")
    thisalinea.textcontent.append("voor alternatieve brandstoffen ontstaat. Dit is volledig aangetoond in het verslag van de")
    thisalinea.textcontent.append("Commissie aan het Europees Parlement en de Raad over de toepassing van Richtlijn")
    thisalinea.textcontent.append("2014/94/EU betreffende de uitrol van infrastructuur voor alternatieve brandstoffen2 en in de")
    thisalinea.textcontent.append("effectbeoordeling ter ondersteuning van het huidige initiatief. De aard en de omvang van")
    thisalinea.textcontent.append("het probleem zijn in alle lidstaten vergelijkbaar en er zijn aanwijzingen dat")
    thisalinea.textcontent.append("grensoverschrijdende connectiviteit voor voertuigen op alternatieve brandstoffen in de Unie")
    thisalinea.textcontent.append("noodzakelijk is en een meerwaarde biedt, en dat een optreden van de Unie dus")
    thisalinea.textcontent.append("gerechtvaardigd is.")
    thisalinea.textcontent.append("Dit initiatief zorgt voor een stabiel en transparant beleidskader om bij te dragen tot de")
    thisalinea.textcontent.append("ontwikkeling van open en concurrerende markten en zo investeringen in laad- en")
    thisalinea.textcontent.append("tankinfrastructuur voor alle vervoerswijzen te stimuleren. Er wordt een gemeenschappelijk")
    thisalinea.textcontent.append("minimum vastgesteld op basis waarvan markten de infrastructuur verder kunnen uitrollen")
    thisalinea.textcontent.append("om tegemoet te komen aan de marktvraag naar voertuigen, op basis van een mechanisme")
    thisalinea.textcontent.append("met duidelijke en transparante streefcijfers, dat in de hele Unie van toepassing is.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2.4. Keuze van het instrument"
    thisalinea.nativeID = 11
    thisalinea.parentID = 7
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "Hoewel een richtlijn in de effectbeoordeling als voorkeursoptie naar voren kwam, heeft de Commissie ervoor geopteerd een verordening voor te stellen. De keuze voor een verordening zorgt voor een snelle en coherente ontwikkeling van een dicht en omvattend netwerk van volledig interoperabele laadinfrastructuur in alle lidstaten. Het besluit is met name gerechtvaardigd in het licht van de noodzakelijke snelle en coherente uitvoering van de op het nationale wagenpark gebaseerde minimumstreefcijfers voor de uitrol op lidstaatniveau en van de verplichte op afstand gebaseerde streefcijfers voor het TEN-T- netwerk, aangezien de eerste voorgestelde doelstellingen reeds tegen 2025 zouden moeten worden bereikt. Gezien "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Hoewel een richtlijn in de effectbeoordeling als voorkeursoptie naar voren kwam, heeft de")
    thisalinea.textcontent.append("Commissie ervoor geopteerd een verordening voor te stellen. De keuze voor een")
    thisalinea.textcontent.append("verordening zorgt voor een snelle en coherente ontwikkeling van een dicht en omvattend")
    thisalinea.textcontent.append("netwerk van volledig interoperabele laadinfrastructuur in alle lidstaten. Het besluit is met")
    thisalinea.textcontent.append("name gerechtvaardigd in het licht van de noodzakelijke snelle en coherente uitvoering van")
    thisalinea.textcontent.append("de op het nationale wagenpark gebaseerde minimumstreefcijfers voor de uitrol op")
    thisalinea.textcontent.append("lidstaatniveau en van de verplichte op afstand gebaseerde streefcijfers voor het TEN-T-")
    thisalinea.textcontent.append("netwerk, aangezien de eerste voorgestelde doelstellingen reeds tegen 2025 zouden moeten")
    thisalinea.textcontent.append("worden bereikt. Gezien die tijdspanne is het van het grootste belang dat in de hele Unie een")
    thisalinea.textcontent.append("voldoende fijnmazig en omvattend netwerk van laad- en tankinfrastructuur voor")
    thisalinea.textcontent.append("emissievrije en emissiearme voertuigen wordt uitgerold aan hetzelfde tempo en onder")
    thisalinea.textcontent.append("dezelfde voorwaarden, om de hoognodige versnelde marktintroductie van emissiearme en")
    thisalinea.textcontent.append("emissievrije voertuigen te ondersteunen. Daartoe moeten de plannen en maatregelen van de")
    thisalinea.textcontent.append("lidstaten om de doelstellingen te verwezenlijken reeds vóór 2025 worden ontwikkeld. Een")
    thisalinea.textcontent.append("nieuwe verordening voorziet in duidelijk bindende en rechtstreeks toepasselijke")
    thisalinea.textcontent.append("verplichtingen voor de lidstaten en waarborgt tegelijk een coherente en tijdige toepassing")
    thisalinea.textcontent.append("en uitvoering daarvan in de hele EU. Ze voorkomt het risico op vertragingen en")
    thisalinea.textcontent.append("inconsistenties in de nationale omzettingsprocessen, waardoor ook een duidelijk gelijk")
    thisalinea.textcontent.append("speelveld voor de markten ontstaat, hetgeen zal bijdragen tot de uitrol van oplaad- en")
    thisalinea.textcontent.append("tankinfrastructuur in de hele Unie. De verordening voorziet in een robuuster")
    thisalinea.textcontent.append("governancemechanisme om de vooruitgang van de lidstaten bij de verwezenlijking van de")
    thisalinea.textcontent.append("doelstellingen te monitoren; dit mechanisme stelt de lidstaten in staat de juiste stimulansen")
    thisalinea.textcontent.append("te geven zodat concurrerende oplaadmarkten zich kunnen ontwikkelen. Duidelijke")
    thisalinea.textcontent.append("tijdschema’s voor het ontwerp en de ontwikkeling van de nationale beleidskaders van de")
    thisalinea.textcontent.append("lidstaten om de streefcijfers te halen, robuuste monitoring- en rapportagemechanismen,")
    thisalinea.textcontent.append("alsmede bepalingen voor corrigerende maatregelen van de lidstaten, creëren mogelijkheden")
    thisalinea.textcontent.append("voor een efficiënte algemene monitoring en sturing van de inspanningen van de lidstaten")
    thisalinea.textcontent.append("om de doelstellingen te bereiken. Dit initiatief garandeert een dergelijke aanpak.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "3. EX-POSTEVALUATIE, RAADPLEGING VAN BELANGHEBBENDEN EN EFFECTBEOORDELING"
    thisalinea.nativeID = 12
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "Een REFIT-evaluatie ex post heeft aangetoond dat de richtlijn heeft bijgedragen tot de ontwikkeling van beleidslijnen en maatregelen voor de uitrol van infrastructuur voor alternatieve brandstoffen in de lidstaten, met name door de verplichting om nationale beleidskaders1 te ontwikkelen. De evaluatie heeft echter ook een aantal tekortkomingen in het huidige beleidskader aan het licht gebracht. Bovendien is de belangrijkste doelstelling van de richtlijn, namelijk een coherente ontwikkeling in de EU waarborgen, niet gehaald. De tekortkomingen situeren zich op de volgende drie gebieden: i) het ontbreken van een volledig infrastructuurnetwerk dat naadloos reizen in de hele EU mogelijk maakt; ii) de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3.1. Evaluatie van de bestaande wetgeving en controle van de resultaatgerichtheid ervan"
    thisalinea.nativeID = 13
    thisalinea.parentID = 12
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "Een REFIT-evaluatie ex post heeft aangetoond dat de richtlijn heeft bijgedragen tot de ontwikkeling van beleidslijnen en maatregelen voor de uitrol van infrastructuur voor alternatieve brandstoffen in de lidstaten, met name door de verplichting om nationale beleidskaders1 te ontwikkelen. De evaluatie heeft echter ook een aantal tekortkomingen in het huidige beleidskader aan het licht gebracht. Bovendien is de belangrijkste doelstelling van de richtlijn, namelijk een coherente ontwikkeling in de EU waarborgen, niet gehaald. De tekortkomingen situeren zich op de volgende drie gebieden: i) het ontbreken van een volledig infrastructuurnetwerk dat naadloos reizen in de hele EU mogelijk maakt; ii) de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Een REFIT-evaluatie ex post heeft aangetoond dat de richtlijn heeft bijgedragen tot de")
    thisalinea.textcontent.append("ontwikkeling van beleidslijnen en maatregelen voor de uitrol van infrastructuur voor")
    thisalinea.textcontent.append("alternatieve brandstoffen in de lidstaten, met name door de verplichting om nationale")
    thisalinea.textcontent.append("beleidskaders1 te ontwikkelen.")
    thisalinea.textcontent.append("De evaluatie heeft echter ook een aantal tekortkomingen in het huidige beleidskader aan het")
    thisalinea.textcontent.append("licht gebracht. Bovendien is de belangrijkste doelstelling van de richtlijn, namelijk een")
    thisalinea.textcontent.append("coherente ontwikkeling in de EU waarborgen, niet gehaald. De tekortkomingen situeren")
    thisalinea.textcontent.append("zich op de volgende drie gebieden: i) het ontbreken van een volledig infrastructuurnetwerk")
    thisalinea.textcontent.append("dat naadloos reizen in de hele EU mogelijk maakt; ii) de behoefte aan nadere")
    thisalinea.textcontent.append("gemeenschappelijke technische specificaties om de interoperabiliteit van opkomende")
    thisalinea.textcontent.append("technologieën te waarborgen; en iii) het ontbreken van volledige gebruikersinformatie,")
    thisalinea.textcontent.append("uniforme en gebruiksvriendelijke betalingsmethoden en volledige prijstransparantie in de")
    thisalinea.textcontent.append("hele Unie.")
    thisalinea.textcontent.append("De conclusie van de evaluatie luidde dat de algemene Europese markt voor infrastructuur")
    thisalinea.textcontent.append("voor alternatieve brandstoffen zich zes jaar na de vaststelling van de richtlijn nog in een vrij")
    thisalinea.textcontent.append("vroeg ontwikkelingsstadium bevindt, hoewel de markten in sommige delen van de EU")
    thisalinea.textcontent.append("maturiteit bereiken. Aangezien het in het algemeen van belang is om voor voldoende")
    thisalinea.textcontent.append("infrastructuur te zorgen om de vereiste introductie van voertuigen en vaartuigen te")
    thisalinea.textcontent.append("ondersteunen in het licht van de verhoogde klimaatambitie voor 2030, werd in de evaluatie")
    thisalinea.textcontent.append("van de richtlijn aanbevolen de regelgeving te herzien in plaats van ze te behouden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3.2. Raadpleging van belanghebbenden"
    thisalinea.nativeID = 14
    thisalinea.parentID = 12
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "In het kader van de effectbeoordeling zijn de belanghebbenden op verschillende manieren geraadpleegd. Van 6 april tot 4 mei 2020 vond een openbare raadpleging plaats over de aanvangseffectbeoordeling (IIA)2 voor dit initiatief. De Commissie ontving 86 reacties, waarvan het merendeel (61) afkomstig was van bedrijven en ondernemersverenigingen. Ook ngo’s en burgers hebben op de IIA gereageerd, net als één netwerk van steden. Tussen 6 april 2020 en 29 juni 2020 organiseerde de Commissie een openbare raadpleging. In het kader daarvan werden alle burgers en organisaties uitgenodigd om te reageren op zowel de evaluatie als de effectbeoordeling3. In totaal ontving de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("In het kader van de effectbeoordeling zijn de belanghebbenden op verschillende manieren")
    thisalinea.textcontent.append("geraadpleegd.")
    thisalinea.textcontent.append("Van 6 april tot 4 mei 2020 vond een openbare raadpleging plaats over de")
    thisalinea.textcontent.append("aanvangseffectbeoordeling (IIA)2 voor dit initiatief. De Commissie ontving 86 reacties,")
    thisalinea.textcontent.append("waarvan het merendeel (61) afkomstig was van bedrijven en ondernemersverenigingen.")
    thisalinea.textcontent.append("Ook ngo’s en burgers hebben op de IIA gereageerd, net als één netwerk van steden.")
    thisalinea.textcontent.append("Tussen 6 april 2020 en 29 juni 2020 organiseerde de Commissie een openbare raadpleging.")
    thisalinea.textcontent.append("In het kader daarvan werden alle burgers en organisaties uitgenodigd om te reageren op")
    thisalinea.textcontent.append("zowel de evaluatie als de effectbeoordeling3. In totaal ontving de Commissie 324 reacties.")
    thisalinea.textcontent.append("Tussen oktober 2020 en januari 2021 vonden gerichte interviews en enquêtes met")
    thisalinea.textcontent.append("belanghebbenden plaats. De Commissie voerde verkennende gesprekken met")
    thisalinea.textcontent.append("vertegenwoordigers van de belangrijkste belanghebbenden op EU-niveau, met name om de")
    thisalinea.textcontent.append("algemene probleemstelling en mogelijke beleidsopties te onderbouwen en te verfijnen. Er")
    thisalinea.textcontent.append("werden verdere interviews gehouden en er werd een online-enquête verspreid onder")
    thisalinea.textcontent.append("belanghebbende vertegenwoordigers van autoriteiten en overheidsinstanties (nationale,")
    thisalinea.textcontent.append("regionale en lokale overheden, EU-organen), vertegenwoordigers van het bedrijfsleven")
    thisalinea.textcontent.append("(m.i.v. representatieve verenigingen) en het maatschappelijk middenveld (ngo’s,")
    thisalinea.textcontent.append("consumentenorganisaties).")
    thisalinea.textcontent.append("De consultant die belast is met de externe ondersteunende studie voor de effectbeoordeling")
    thisalinea.textcontent.append("organiseerde tussen december 2020 en februari 2021 een gerichte raadpleging van de")
    thisalinea.textcontent.append("belanghebbenden. Die omvatte gerichte enquêtes onder de belangrijkste belanghebbenden")
    thisalinea.textcontent.append("en gerichte interviews en verzoeken om specifieke gegevens, met name als input voor de")
    thisalinea.textcontent.append("ontwikkeling van een methode om te bepalen of er voldoende infrastructuur wordt voorzien")
    thisalinea.textcontent.append("en ter ondersteuning van de effectbeoordeling van mogelijke beleidsmaatregelen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3.3. Bijeenbrengen en gebruik van expertise"
    thisalinea.nativeID = 15
    thisalinea.parentID = 12
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "Bij de voorbereiding van dit initiatief heeft de Commissie gebruikgemaakt van de bevindingen van de ex-postevaluatie4 van de richtlijn. De belanghebbenden hebben uitvoerige informatie verstrekt in het kader van de raadplegingsactiviteiten. Daarnaast ontving de Commissie extra informatie op ad-hocbasis. De effectbeoordeling is voor een groot deel gebaseerd op een begeleidende externe ondersteunende studie5, die door een consultant is uitgevoerd. De Commissie heeft ook gebruikgemaakt van een brede raadpleging van het Forum voor duurzaam vervoer, de deskundigengroep van de Commissie op het gebied van alternatieve brandstoffen. De raadpleging van het Forum voor duurzaam vervoer vond plaats van oktober 2018 tot november "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Bij de voorbereiding van dit initiatief heeft de Commissie gebruikgemaakt van de")
    thisalinea.textcontent.append("bevindingen van de ex-postevaluatie4 van de richtlijn. De belanghebbenden hebben")
    thisalinea.textcontent.append("uitvoerige informatie verstrekt in het kader van de raadplegingsactiviteiten. Daarnaast")
    thisalinea.textcontent.append("ontving de Commissie extra informatie op ad-hocbasis. De effectbeoordeling is voor een")
    thisalinea.textcontent.append("groot deel gebaseerd op een begeleidende externe ondersteunende studie5, die door een")
    thisalinea.textcontent.append("consultant is uitgevoerd. De Commissie heeft ook gebruikgemaakt van een brede")
    thisalinea.textcontent.append("raadpleging van het Forum voor duurzaam vervoer, de deskundigengroep van de")
    thisalinea.textcontent.append("Commissie op het gebied van alternatieve brandstoffen. De raadpleging van het Forum")
    thisalinea.textcontent.append("voor duurzaam vervoer vond plaats van oktober 2018 tot november 2019 en focuste op de")
    thisalinea.textcontent.append("knelpunten en toekomstige beleidsbehoeften op het gebied van infrastructuur voor")
    thisalinea.textcontent.append("alternatieve brandstoffen6. In het algemeen werden in het kader van de effectbeoordeling")
    thisalinea.textcontent.append("een groot aantal bronnen geraadpleegd die grotendeels exhaustief en representatief waren")
    thisalinea.textcontent.append("voor de diverse groepen belanghebbenden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3.4. Effectbeoordeling"
    thisalinea.nativeID = 16
    thisalinea.parentID = 12
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "De Raad voor regelgevingstoetsing heeft de ontwerpversie van het effectbeoordelingsverslag op 7 april 2021 ontvangen en op 7 mei 2021 een positief advies uitgebracht. De raad was van oordeel dat het verslag nog kon worden verbeterd door: a) het verschil tussen de opties en de wijze waarop deze verband houden met de vastgestelde problemen beter te omschrijven; en b) in het verslag een nuancering op te nemen om te verduidelijken of de verwachte effecten voortvloeien uit dit specifieke initiatief, uit ander beleid, dan wel uit een combinatie van beide. Het definitieve effectbeoordelingsverslag bevat een uitgebreide beschrijving en beoordeling van de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("De Raad voor regelgevingstoetsing heeft de ontwerpversie van het")
    thisalinea.textcontent.append("effectbeoordelingsverslag op 7 april 2021 ontvangen en op 7 mei 2021 een positief advies")
    thisalinea.textcontent.append("uitgebracht. De raad was van oordeel dat het verslag nog kon worden verbeterd door: a) het")
    thisalinea.textcontent.append("verschil tussen de opties en de wijze waarop deze verband houden met de vastgestelde")
    thisalinea.textcontent.append("problemen beter te omschrijven; en b) in het verslag een nuancering op te nemen om te")
    thisalinea.textcontent.append("verduidelijken of de verwachte effecten voortvloeien uit dit specifieke initiatief, uit ander")
    thisalinea.textcontent.append("beleid, dan wel uit een combinatie van beide.")
    thisalinea.textcontent.append("Het definitieve effectbeoordelingsverslag bevat een uitgebreide beschrijving en beoordeling")
    thisalinea.textcontent.append("van de toegevoegde waarde van het initiatief en het verband met andere beleidsinitiatieven.")
    thisalinea.textcontent.append("Die zijn opgenomen in de punten 1.3, 3.3 en 8.1 van het beoordelingsrapport. Een")
    thisalinea.textcontent.append("gedetailleerde beschrijving van de beleidsopties is opgenomen in punt 5, terwijl de effecten")
    thisalinea.textcontent.append("van alle opties uitvoerig zijn geanalyseerd in punt 6. De geanalyseerde beleidsopties")
    thisalinea.textcontent.append("kunnen als volgt worden samengevat:")
    thisalinea.textcontent.append("Omdat ze een optimaal evenwicht biedt tussen de bereikte doelstellingen en de")
    thisalinea.textcontent.append("uitvoeringskosten, is optie 2 als de beste beleidsoptie geselecteerd. Beleidsoptie 2 kan")
    thisalinea.textcontent.append("echter ook de vorm van een verordening aannemen, die een snellere impact heeft op de")
    thisalinea.textcontent.append("uitvoering van de regels. De effectbeoordeling omvat een gedetailleerde beschrijving van")
    thisalinea.textcontent.append("de regelgevende maatregelen die in de verschillende beleidsopties zijn opgenomen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Beleidsoptie 1: inhoudelijke wijzigingen van ..."
    thisalinea.nativeID = 17
    thisalinea.parentID = 16
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "– Beleidsoptie 1: inhoudelijke wijzigingen van de richtlijn. De vaststelling van nationale streefcijfers en verslaglegging in het kader van de nationale beleidskaders zouden een belangrijke pijler blijven, versterkt door verplichte op de omvang van het wagenpark gebaseerde doelstellingen voor elektrische laadpunten voor lichte voertuigen (LDV’s). Voor zware bedrijfsvoertuigen zouden verplichte streefcijfers op basis van afstand worden ingevoerd voor elektrische laadpunten en waterstoftankpunten op het TEN-T-netwerk, aangevuld met beperkte regels voor waterstoftankpunten in stedelijke knooppunten. Er zouden ook verplichte streefcijfers worden ingevoerd voor stilstaande luchtvaartuigen en walstroomvoorzieningen in zee- en binnenhavens. Daarnaast zouden enkele kwaliteitsproblemen van de infrastructuur worden aangepakt om "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Beleidsoptie 1: inhoudelijke wijzigingen van de richtlijn. De vaststelling van")
    thisalinea.textcontent.append("nationale streefcijfers en verslaglegging in het kader van de nationale beleidskaders")
    thisalinea.textcontent.append("zouden een belangrijke pijler blijven, versterkt door verplichte op de omvang van het")
    thisalinea.textcontent.append("wagenpark gebaseerde doelstellingen voor elektrische laadpunten voor lichte")
    thisalinea.textcontent.append("voertuigen (LDV’s). Voor zware bedrijfsvoertuigen zouden verplichte streefcijfers")
    thisalinea.textcontent.append("op basis van afstand worden ingevoerd voor elektrische laadpunten en")
    thisalinea.textcontent.append("waterstoftankpunten op het TEN-T-netwerk, aangevuld met beperkte regels voor")
    thisalinea.textcontent.append("waterstoftankpunten in stedelijke knooppunten. Er zouden ook verplichte")
    thisalinea.textcontent.append("streefcijfers worden ingevoerd voor stilstaande luchtvaartuigen en")
    thisalinea.textcontent.append("walstroomvoorzieningen in zee- en binnenhavens. Daarnaast zouden enkele")
    thisalinea.textcontent.append("kwaliteitsproblemen van de infrastructuur worden aangepakt om de interoperabiliteit")
    thisalinea.textcontent.append("en de gebruikersinformatie te verbeteren.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Beleidsoptie 2: een meer ingrijpende ..."
    thisalinea.nativeID = 18
    thisalinea.parentID = 16
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "– Beleidsoptie 2: een meer ingrijpende inhoudelijke wijziging van de richtlijn dan in optie 1. Bovenop de verplichte, op de omvang van het wagenpark gebaseerde streefcijfers voor elektrische laadpunten voor lichte voertuigen, zouden op afstand gebaseerde normen worden vastgesteld voor alle infrastructuur voor wegvoertuigen op het TEN-T-netwerk, ook voor zware bedrijfsvoertuigen in stedelijke knooppunten. Deze optie omvat ook meer gedetailleerde bepalingen voor havens en luchthavens op het TEN-T-netwerk en een sterkere harmonisatie van de betalingsopties, fysieke en communicatienormen en consumentenrechten inzake betaling. De bepalingen inzake prijstransparantie en andere gebruikersinformatie zouden worden aangescherpt, m.i.v. fysieke bewegwijzering van oplaad- en tankinfrastructuur. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Beleidsoptie 2: een meer ingrijpende inhoudelijke wijziging van de richtlijn dan")
    thisalinea.textcontent.append("in optie 1. Bovenop de verplichte, op de omvang van het wagenpark gebaseerde")
    thisalinea.textcontent.append("streefcijfers voor elektrische laadpunten voor lichte voertuigen, zouden op afstand")
    thisalinea.textcontent.append("gebaseerde normen worden vastgesteld voor alle infrastructuur voor wegvoertuigen")
    thisalinea.textcontent.append("op het TEN-T-netwerk, ook voor zware bedrijfsvoertuigen in stedelijke")
    thisalinea.textcontent.append("knooppunten. Deze optie omvat ook meer gedetailleerde bepalingen voor havens en")
    thisalinea.textcontent.append("luchthavens op het TEN-T-netwerk en een sterkere harmonisatie van de")
    thisalinea.textcontent.append("betalingsopties, fysieke en communicatienormen en consumentenrechten inzake")
    thisalinea.textcontent.append("betaling. De bepalingen inzake prijstransparantie en andere gebruikersinformatie")
    thisalinea.textcontent.append("zouden worden aangescherpt, m.i.v. fysieke bewegwijzering van oplaad- en")
    thisalinea.textcontent.append("tankinfrastructuur.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Beleidsoptie 3: de richtlijn vervangen ..."
    thisalinea.nativeID = 19
    thisalinea.parentID = 16
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "– Beleidsoptie 3: de richtlijn vervangen door een verordening (het meest ingrijpende bindende rechtsinstrument). Bovenop de verplichte vlootgerelateerde en op afstand gebaseerde streefcijfers in optie 2, worden in deze optie verdere locatiespecifieke streefcijfers voor elektrische lichte bedrijfsvoertuigen en streefcijfers voor zware bedrijfsvoertuigen toegevoegd. De optie zou ook een aanzienlijke ambitie voor haveninfrastructuur toevoegen en van verplichte terminalbetalingen bij nieuwe snelladers de enige betaaloptie maken. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Beleidsoptie 3: de richtlijn vervangen door een verordening (het meest")
    thisalinea.textcontent.append("ingrijpende bindende rechtsinstrument). Bovenop de verplichte vlootgerelateerde en")
    thisalinea.textcontent.append("op afstand gebaseerde streefcijfers in optie 2, worden in deze optie verdere")
    thisalinea.textcontent.append("locatiespecifieke streefcijfers voor elektrische lichte bedrijfsvoertuigen en")
    thisalinea.textcontent.append("streefcijfers voor zware bedrijfsvoertuigen toegevoegd. De optie zou ook een")
    thisalinea.textcontent.append("aanzienlijke ambitie voor haveninfrastructuur toevoegen en van verplichte")
    thisalinea.textcontent.append("terminalbetalingen bij nieuwe snelladers de enige betaaloptie maken.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3.5. Resultaatgerichtheid en vereenvoudiging"
    thisalinea.nativeID = 20
    thisalinea.parentID = 12
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "Er moet veel meer ambitie aan de dag worden gelegd voor de uitrol van voldoende en volledig interoperabele laad- en tankinfrastructuur om de vereiste marktpenetratie van emissiearme en emissievrije voertuigen te ondersteunen, conform de algemene beleidsambitie van het “Fit for 55”-pakket en de bijbehorende beleidsinitiatieven. Gezonde regelgeving wordt bereikt door de vaststelling van de nodige minimumvereisten voor overheidsinstanties en marktdeelnemers. De daarmee gepaard gaande hogere kosten voor overheidsinstanties om de uitrol van infrastructuur te ondersteunen, met name op delen van het vervoersnetwerk waar de vraag laag is, moeten worden afgezet tegen de aanzienlijk gestegen vraag van de gebruikers en de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Er moet veel meer ambitie aan de dag worden gelegd voor de uitrol van voldoende en")
    thisalinea.textcontent.append("volledig interoperabele laad- en tankinfrastructuur om de vereiste marktpenetratie van")
    thisalinea.textcontent.append("emissiearme en emissievrije voertuigen te ondersteunen, conform de algemene")
    thisalinea.textcontent.append("beleidsambitie van het “Fit for 55”-pakket en de bijbehorende beleidsinitiatieven. Gezonde")
    thisalinea.textcontent.append("regelgeving wordt bereikt door de vaststelling van de nodige minimumvereisten voor")
    thisalinea.textcontent.append("overheidsinstanties en marktdeelnemers. De daarmee gepaard gaande hogere kosten voor")
    thisalinea.textcontent.append("overheidsinstanties om de uitrol van infrastructuur te ondersteunen, met name op delen van")
    thisalinea.textcontent.append("het vervoersnetwerk waar de vraag laag is, moeten worden afgezet tegen de aanzienlijk")
    thisalinea.textcontent.append("gestegen vraag van de gebruikers en de grootschalige kansen voor marktgroei. De")
    thisalinea.textcontent.append("herziening van het beleid in het kader van “Fit for 55”-pakket zal de marktintroductie van")
    thisalinea.textcontent.append("emissievrije voertuigen en de afhandeling van schepen met walstroomvoorziening mogelijk")
    thisalinea.textcontent.append("maken. De effectbeoordeling bevat een gedetailleerde analyse van de kosten en baten,")
    thisalinea.textcontent.append("m.i.v. een samenvatting in bijlage 3.")
    thisalinea.textcontent.append("Hoewel de herziening de algemene beleidsambitie aanscherpt, voorziet zij ook in enkele")
    thisalinea.textcontent.append("belangrijke vereenvoudigingen, die vooral exploitanten van laadpunten en aanbieders van")
    thisalinea.textcontent.append("mobiliteitsdiensten ten goede zullen komen. Het vaststellen van duidelijke en")
    thisalinea.textcontent.append("gemeenschappelijke minimumeisen die in alle lidstaten gelden, zal hun bedrijfsvoering")
    thisalinea.textcontent.append("vereenvoudigen. Door die eisen wordt het voor particuliere en zakelijke consumenten (die")
    thisalinea.textcontent.append("momenteel met een veelvoud aan gebruiksmethoden worden geconfronteerd) eenvoudiger")
    thisalinea.textcontent.append("om de infrastructuur te gebruiken en ontstaan kansen voor innovatie van de zakelijke")
    thisalinea.textcontent.append("dienstverlening. Het vertrouwen van de consument in de robuustheid van een pan-Europees")
    thisalinea.textcontent.append("netwerk van laad- en tankinfrastructuur zal toenemen, wat de algemene rendabiliteit van")
    thisalinea.textcontent.append("laad- en tankpunten zal bevorderen en bijdraagt tot een stabiele business case. Alle")
    thisalinea.textcontent.append("marktdeelnemers en gebruikersgroepen zullen profiteren van lagere informatiekosten en, in")
    thisalinea.textcontent.append("het geval van marktdeelnemers, lagere nalevingskosten op middellange termijn, die het")
    thisalinea.textcontent.append("resultaat zijn van een verdere harmonisering van de infrastructuureisen in het kader van de")
    thisalinea.textcontent.append("verordening. Overheidsinstanties kunnen ook profiteren van een coherent EU-kader dat de")
    thisalinea.textcontent.append("coördinatie met publieke en private marktdeelnemers zal vereenvoudigen.")
    thisalinea.textcontent.append("In de effectbeoordeling was geen sprake van aanzienlijke en onevenredige kosten van dit")
    thisalinea.textcontent.append("initiatief voor kmo’s ten opzichte van andere ondernemingen. Dit initiatief creëert")
    thisalinea.textcontent.append("marktzekerheid op lange termijn voor investeringen in laad- en tankinfrastructuur en legt de")
    thisalinea.textcontent.append("basis voor de ontwikkeling van een open data-ecosysteem dat ondernemingen kunnen")
    thisalinea.textcontent.append("gebruiken om nieuwe marktdiensten te ontwikkelen, wat innovatieve kmo’s ten goede zal")
    thisalinea.textcontent.append("komen. Het initiatief heeft over het algemeen een positief effect op het")
    thisalinea.textcontent.append("concurrentievermogen van ondernemingen die laad- en tankinfrastructuur installeren en")
    thisalinea.textcontent.append("exploiteren, en op het concurrentievermogen van de automobielsector. Dit komt doordat de")
    thisalinea.textcontent.append("beschikbaarheid van voldoende infrastructuur een impact heeft op de marktintroductie van")
    thisalinea.textcontent.append("emissievrije voertuigen, een belangrijk aspect voor het toekomstige concurrentievermogen")
    thisalinea.textcontent.append("van de automobielsector. Dit is nader toegelicht in de effectbeoordeling die ten grondslag")
    thisalinea.textcontent.append("ligt aan het voorstel tot herziening van de CO2-normen voor auto’s en bestelwagens7.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3.6. Grondrechten"
    thisalinea.nativeID = 21
    thisalinea.parentID = 12
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "Het voorstel heeft geen gevolgen voor de grondrechten. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Het voorstel heeft geen gevolgen voor de grondrechten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "4. GEVOLGEN VOOR DE BEGROTING"
    thisalinea.nativeID = 22
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "Het voorstel heeft geen gevolgen voor de begroting van de Europese Unie. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Het voorstel heeft geen gevolgen voor de begroting van de Europese Unie.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "5. OVERIGE ELEMENTEN"
    thisalinea.nativeID = 23
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "De uitvoering van de herziene verordening zal worden gemonitord aan de hand van indicatoren betreffende de fysieke uitrol van laad- en tankinfrastructuur in de EU. Er zullen beproefde monitoringinstrumenten worden gebruikt om de uitrol te monitoren. De lidstaten zullen een herzien nationaal beleidskader moeten vaststellen om de markt voor alternatieve brandstoffen in de vervoerssector te ontwikkelen en de relevante infrastructuur uit te rollen conform de voorgestelde aangescherpte regels. Dit zal hen in staat stellen op coherente en consistente wijze aan de Commissie verslag uit te brengen over de uitvoering. Bij de gegevensverstrekking aan de nationale en gemeenschappelijke toegangspunten van de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5.1. Uitvoeringsplanning en regelingen betreffende controle, evaluatie en rapportage"
    thisalinea.nativeID = 24
    thisalinea.parentID = 23
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "De uitvoering van de herziene verordening zal worden gemonitord aan de hand van indicatoren betreffende de fysieke uitrol van laad- en tankinfrastructuur in de EU. Er zullen beproefde monitoringinstrumenten worden gebruikt om de uitrol te monitoren. De lidstaten zullen een herzien nationaal beleidskader moeten vaststellen om de markt voor alternatieve brandstoffen in de vervoerssector te ontwikkelen en de relevante infrastructuur uit te rollen conform de voorgestelde aangescherpte regels. Dit zal hen in staat stellen op coherente en consistente wijze aan de Commissie verslag uit te brengen over de uitvoering. Bij de gegevensverstrekking aan de nationale en gemeenschappelijke toegangspunten van de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("De uitvoering van de herziene verordening zal worden gemonitord aan de hand van")
    thisalinea.textcontent.append("indicatoren betreffende de fysieke uitrol van laad- en tankinfrastructuur in de EU. Er zullen")
    thisalinea.textcontent.append("beproefde monitoringinstrumenten worden gebruikt om de uitrol te monitoren.")
    thisalinea.textcontent.append("De lidstaten zullen een herzien nationaal beleidskader moeten vaststellen om de markt voor")
    thisalinea.textcontent.append("alternatieve brandstoffen in de vervoerssector te ontwikkelen en de relevante infrastructuur")
    thisalinea.textcontent.append("uit te rollen conform de voorgestelde aangescherpte regels. Dit zal hen in staat stellen op")
    thisalinea.textcontent.append("coherente en consistente wijze aan de Commissie verslag uit te brengen over de uitvoering.")
    thisalinea.textcontent.append("Bij de gegevensverstrekking aan de nationale en gemeenschappelijke toegangspunten van")
    thisalinea.textcontent.append("de lidstaten worden gezamenlijk overeengekomen kwaliteitsnormen1 voor gegevens")
    thisalinea.textcontent.append("gehanteerd. Het Europees Waarnemingscentrum voor alternatieve brandstoffen zal voorts")
    thisalinea.textcontent.append("worden opgewaardeerd en blijft gegevens over de uitrol van voertuigen en infrastructuur in")
    thisalinea.textcontent.append("alle lidstaten2verzamelen en zal die regelmatig bijwerken. De Commissie zal ook blijven")
    thisalinea.textcontent.append("samenwerken met haar deskundigengroep, het Forum voor duurzaam vervoer (en zijn")
    thisalinea.textcontent.append("specifieke subgroepen), om de marktontwikkelingen te volgen en de daarmee")
    thisalinea.textcontent.append("samenhangende beleidsbehoeften te bepalen.")
    thisalinea.textcontent.append("Een volledige herziening van de verordening is gepland voor eind 2026 en moet eventuele")
    thisalinea.textcontent.append("tekortkomingen aan het licht brengen en een beeld geven van de toekomstige behoeften aan")
    thisalinea.textcontent.append("wetgevende maatregelen op het gebied van opkomende technologieën. Zie bijlage 9 bij het")
    thisalinea.textcontent.append("werkdocument van de diensten van de Commissie over de effectbeoordeling bij dit initiatief")
    thisalinea.textcontent.append("voor een overzicht van de operationele doelstellingen, indicatoren en gegevensbronnen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5.2. Artikelsgewijze toelichting"
    thisalinea.nativeID = 25
    thisalinea.parentID = 23
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "Dit voorstel voorziet in een nieuwe verordening tot intrekking van Richtlijn 2014/94/EU betreffende de uitrol van infrastructuur voor alternatieve brandstoffen. De structuur van de nieuwe verordening is als volgt: Het voorstel bevat bijlagen: 2021/0223 (COD) Voorstel voor een – Artikel 1 omschrijft het onderwerp van de verordening en bevat specifieke maar geen inhoudelijke wijzigingen van het onderwerp van de huidige richtlijn. – Artikel 2 bevat een lijst van definities, voortbouwend op de lijst van definities van de huidige richtlijn: waar nodig worden die definities aangevuld in het licht van de algemene wijzigingen van het toepassingsgebied en de bepalingen van de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Dit voorstel voorziet in een nieuwe verordening tot intrekking van Richtlijn 2014/94/EU")
    thisalinea.textcontent.append("betreffende de uitrol van infrastructuur voor alternatieve brandstoffen. De structuur van de")
    thisalinea.textcontent.append("nieuwe verordening is als volgt:")
    thisalinea.textcontent.append("Het voorstel bevat bijlagen:")
    thisalinea.textcontent.append("2021/0223 (COD)")
    thisalinea.textcontent.append("Voorstel voor een")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 1 omschrijft het onderwerp ..."
    thisalinea.nativeID = 26
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "– Artikel 1 omschrijft het onderwerp van de verordening en bevat specifieke maar geen inhoudelijke wijzigingen van het onderwerp van de huidige richtlijn. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 1 omschrijft het onderwerp van de verordening en bevat specifieke maar geen")
    thisalinea.textcontent.append("inhoudelijke wijzigingen van het onderwerp van de huidige richtlijn.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 2 bevat een lijst ..."
    thisalinea.nativeID = 27
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "– Artikel 2 bevat een lijst van definities, voortbouwend op de lijst van definities van de huidige richtlijn: waar nodig worden die definities aangevuld in het licht van de algemene wijzigingen van het toepassingsgebied en de bepalingen van de nieuwe verordening. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 2 bevat een lijst van definities, voortbouwend op de lijst van definities van de")
    thisalinea.textcontent.append("huidige richtlijn: waar nodig worden die definities aangevuld in het licht van de")
    thisalinea.textcontent.append("algemene wijzigingen van het toepassingsgebied en de bepalingen van de nieuwe")
    thisalinea.textcontent.append("verordening.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– De artikelen 3 tot en ..."
    thisalinea.nativeID = 28
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "– De artikelen 3 tot en met 12 bevatten bepalingen inzake de uitrol van laad- en tankinfrastructuur voor lichte en zware wegvoertuigen, schepen en luchtvaartuigen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– De artikelen 3 tot en met 12 bevatten bepalingen inzake de uitrol van laad- en")
    thisalinea.textcontent.append("tankinfrastructuur voor lichte en zware wegvoertuigen, schepen en luchtvaartuigen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Op grond van de artikelen ..."
    thisalinea.nativeID = 29
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "– Op grond van de artikelen 3 en 4 moeten de lidstaten op hun grondgebied, m.i.v. het TEN-T-kernnetwerk en het uitgebreide netwerk, voor een minimale dekking van openbaar toegankelijke laadpunten voor lichte en zware wegvoertuigen zorgen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Op grond van de artikelen 3 en 4 moeten de lidstaten op hun grondgebied, m.i.v. het")
    thisalinea.textcontent.append("TEN-T-kernnetwerk en het uitgebreide netwerk, voor een minimale dekking van")
    thisalinea.textcontent.append("openbaar toegankelijke laadpunten voor lichte en zware wegvoertuigen zorgen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 5 bevat nadere bepalingen ..."
    thisalinea.nativeID = 30
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "– Artikel 5 bevat nadere bepalingen om de gebruiksvriendelijkheid van oplaadinfrastructuur te waarborgen. Het gaat onder meer om bepalingen over betalingsmogelijkheden, prijstransparantie en consumenteninformatie, niet- discriminerende praktijken, slim opladen en regels inzake de bewegwijzering van elektriciteitsvoorzieningen en laadpunten. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 5 bevat nadere bepalingen om de gebruiksvriendelijkheid van")
    thisalinea.textcontent.append("oplaadinfrastructuur te waarborgen. Het gaat onder meer om bepalingen over")
    thisalinea.textcontent.append("betalingsmogelijkheden, prijstransparantie en consumenteninformatie, niet-")
    thisalinea.textcontent.append("discriminerende praktijken, slim opladen en regels inzake de bewegwijzering van")
    thisalinea.textcontent.append("elektriciteitsvoorzieningen en laadpunten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 6 bevat bepalingen op ..."
    thisalinea.nativeID = 31
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "– Artikel 6 bevat bepalingen op grond waarvan de lidstaten op hun grondgebied, m.i.v. het kernnetwerk en het uitgebreide netwerk van het TEN-T, voor een minimale dekking van openbaar toegankelijke waterstoftankpunten voor lichte en zware wegvoertuigen moeten zorgen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 6 bevat bepalingen op grond waarvan de lidstaten op hun grondgebied, m.i.v.")
    thisalinea.textcontent.append("het kernnetwerk en het uitgebreide netwerk van het TEN-T, voor een minimale")
    thisalinea.textcontent.append("dekking van openbaar toegankelijke waterstoftankpunten voor lichte en zware")
    thisalinea.textcontent.append("wegvoertuigen moeten zorgen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 7 bevat nadere bepalingen ..."
    thisalinea.nativeID = 32
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "– Artikel 7 bevat nadere bepalingen om de gebruiksvriendelijkheid van de waterstoftankinfrastructuur te waarborgen, met onder meer minimumeisen inzake betaalmogelijkheden, prijstransparantie en contractuele keuze. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 7 bevat nadere bepalingen om de gebruiksvriendelijkheid van de")
    thisalinea.textcontent.append("waterstoftankinfrastructuur te waarborgen, met onder meer minimumeisen inzake")
    thisalinea.textcontent.append("betaalmogelijkheden, prijstransparantie en contractuele keuze.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 8 bevat bepalingen op ..."
    thisalinea.nativeID = 33
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "– Artikel 8 bevat bepalingen op grond waarvan de lidstaten tot en met 1 januari 2025 op het kernnetwerk en het uitgebreide netwerk van het TEN-T voor een minimumdekking van openbaar toegankelijke tankpunten voor vloeibaar aardgas voor zware bedrijfsvoertuigen moeten zorgen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 8 bevat bepalingen op grond waarvan de lidstaten tot en met 1 januari 2025")
    thisalinea.textcontent.append("op het kernnetwerk en het uitgebreide netwerk van het TEN-T voor een")
    thisalinea.textcontent.append("minimumdekking van openbaar toegankelijke tankpunten voor vloeibaar aardgas")
    thisalinea.textcontent.append("voor zware bedrijfsvoertuigen moeten zorgen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– De artikelen 9 en 10 ..."
    thisalinea.nativeID = 34
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "– De artikelen 9 en 10 bevatten bepalingen inzake de installatie van minimale walstroomvoorzieningen voor bepaalde zeeschepen in zeehavens en voor binnenschepen. In deze artikelen worden ook de criteria voor de vrijstelling van bepaalde havens nader omschreven en worden eisen vastgesteld om een minimale walstroomvoorziening te waarborgen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– De artikelen 9 en 10 bevatten bepalingen inzake de installatie van minimale")
    thisalinea.textcontent.append("walstroomvoorzieningen voor bepaalde zeeschepen in zeehavens en voor")
    thisalinea.textcontent.append("binnenschepen. In deze artikelen worden ook de criteria voor de vrijstelling van")
    thisalinea.textcontent.append("bepaalde havens nader omschreven en worden eisen vastgesteld om een minimale")
    thisalinea.textcontent.append("walstroomvoorziening te waarborgen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Op grond van artikel 11 ..."
    thisalinea.nativeID = 35
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 9
    thisalinea.summary = "– Op grond van artikel 11 moeten de lidstaten zorgen voor een passend aantal LNG- tankpunten in maritieme TEN-T-havens en in hun nationale beleidskaders relevante havens selecteren. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Op grond van artikel 11 moeten de lidstaten zorgen voor een passend aantal LNG-")
    thisalinea.textcontent.append("tankpunten in maritieme TEN-T-havens en in hun nationale beleidskaders relevante")
    thisalinea.textcontent.append("havens selecteren.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 12 heeft betrekking op ..."
    thisalinea.nativeID = 36
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 10
    thisalinea.summary = "– Artikel 12 heeft betrekking op minimumvoorzieningen voor de elektriciteitsaansluitingen voor alle stilstaande luchtvaartuigen op luchthavens op het TEN-T-kernnetwerk en het uitgebreide TEN-T. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 12 heeft betrekking op minimumvoorzieningen voor de")
    thisalinea.textcontent.append("elektriciteitsaansluitingen voor alle stilstaande luchtvaartuigen op luchthavens op het")
    thisalinea.textcontent.append("TEN-T-kernnetwerk en het uitgebreide TEN-T.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– In artikel 13 zijn de ..."
    thisalinea.nativeID = 37
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 11
    thisalinea.summary = "– In artikel 13 zijn de bepalingen inzake de nationale beleidskaders van de lidstaten geherformuleerd. Het voorziet in een iteratief proces tussen de lidstaten en de Commissie om een elementaire planning voor de uitrol van infrastructuur op te stellen en de in de verordening vastgestelde streefcijfers te halen. Het bevat ook nieuwe bepalingen over de ontwikkeling van een strategie voor de uitrol van alternatieve brandstoffen in andere vervoerswijzen, in samenwerking met belangrijke sectorale en regionale/lokale belanghebbenden. Het gaat om gevallen waarin in de verordening geen dwingende eisen zijn vastgesteld maar waarin een antwoord moet worden geformuleerd op nieuwe beleidsbehoeften in "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– In artikel 13 zijn de bepalingen inzake de nationale beleidskaders van de lidstaten")
    thisalinea.textcontent.append("geherformuleerd. Het voorziet in een iteratief proces tussen de lidstaten en de")
    thisalinea.textcontent.append("Commissie om een elementaire planning voor de uitrol van infrastructuur op te")
    thisalinea.textcontent.append("stellen en de in de verordening vastgestelde streefcijfers te halen. Het bevat ook")
    thisalinea.textcontent.append("nieuwe bepalingen over de ontwikkeling van een strategie voor de uitrol van")
    thisalinea.textcontent.append("alternatieve brandstoffen in andere vervoerswijzen, in samenwerking met belangrijke")
    thisalinea.textcontent.append("sectorale en regionale/lokale belanghebbenden. Het gaat om gevallen waarin in de")
    thisalinea.textcontent.append("verordening geen dwingende eisen zijn vastgesteld maar waarin een antwoord moet")
    thisalinea.textcontent.append("worden geformuleerd op nieuwe beleidsbehoeften in verband met de ontwikkeling")
    thisalinea.textcontent.append("van technologieën voor alternatieve brandstoffen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– In de artikelen 14, 15 ..."
    thisalinea.nativeID = 38
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 12
    thisalinea.summary = "– In de artikelen 14, 15 en 16 wordt de governance-aanpak uiteengezet. Dit omvat rapportageverplichtingen overeenkomstig de bepalingen inzake de nationale beleidskaders en nationale voortgangsverslagen van de lidstaten, als onderdeel van een interactief proces met de Commissie. De artikelen bevatten ook voorschriften voor de Commissie om verslag uit te brengen over de nationale beleidskaders en voortgangsverslagen van de lidstaten. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– In de artikelen 14, 15 en 16 wordt de governance-aanpak uiteengezet. Dit omvat")
    thisalinea.textcontent.append("rapportageverplichtingen overeenkomstig de bepalingen inzake de nationale")
    thisalinea.textcontent.append("beleidskaders en nationale voortgangsverslagen van de lidstaten, als onderdeel van")
    thisalinea.textcontent.append("een interactief proces met de Commissie. De artikelen bevatten ook voorschriften")
    thisalinea.textcontent.append("voor de Commissie om verslag uit te brengen over de nationale beleidskaders en")
    thisalinea.textcontent.append("voortgangsverslagen van de lidstaten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 17 heeft betrekking op ..."
    thisalinea.nativeID = 39
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 13
    thisalinea.summary = "– Artikel 17 heeft betrekking op de eisen inzake gebruikersinformatie in de vorm van brandstoflabels en informatievereisten inzake de vergelijking van de brandstofprijzen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 17 heeft betrekking op de eisen inzake gebruikersinformatie in de vorm van")
    thisalinea.textcontent.append("brandstoflabels en informatievereisten inzake de vergelijking van de")
    thisalinea.textcontent.append("brandstofprijzen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– In artikel 18 is bepaald ..."
    thisalinea.nativeID = 40
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 14
    thisalinea.summary = "– In artikel 18 is bepaald aan welke gegevensvereisten exploitanten of eigenaars van openbaar toegankelijke laad- of tankpunten moeten voldoen met betrekking tot de beschikbaarheid en toegankelijkheid van bepaalde soorten statische en dynamische gegevens, m.i.v. de oprichting van een organisatie voor identificatieregistratie (IDRO) voor de afgifte van identificatiecodes. Dit artikel verleent de Commissie ook de bevoegdheid om gedelegeerde handelingen vast te stellen om nadere elementen te specificeren. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– In artikel 18 is bepaald aan welke gegevensvereisten exploitanten of eigenaars van")
    thisalinea.textcontent.append("openbaar toegankelijke laad- of tankpunten moeten voldoen met betrekking tot de")
    thisalinea.textcontent.append("beschikbaarheid en toegankelijkheid van bepaalde soorten statische en dynamische")
    thisalinea.textcontent.append("gegevens, m.i.v. de oprichting van een organisatie voor identificatieregistratie")
    thisalinea.textcontent.append("(IDRO) voor de afgifte van identificatiecodes. Dit artikel verleent de Commissie ook")
    thisalinea.textcontent.append("de bevoegdheid om gedelegeerde handelingen vast te stellen om nadere elementen te")
    thisalinea.textcontent.append("specificeren.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 19 bevat bepalingen voor ..."
    thisalinea.nativeID = 41
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 15
    thisalinea.summary = "– Artikel 19 bevat bepalingen voor gemeenschappelijke technische specificaties; de bestaande gemeenschappelijke technische specificaties worden aangevuld met een reeks nieuwe gebieden waarvoor de Commissie gedelegeerde handelingen kan vaststellen. Deze zullen, waar nodig, voortbouwen op normen die zijn ontwikkeld door de Europese normalisatieorganisaties (ENO’s). "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 19 bevat bepalingen voor gemeenschappelijke technische specificaties; de")
    thisalinea.textcontent.append("bestaande gemeenschappelijke technische specificaties worden aangevuld met een")
    thisalinea.textcontent.append("reeks nieuwe gebieden waarvoor de Commissie gedelegeerde handelingen kan")
    thisalinea.textcontent.append("vaststellen. Deze zullen, waar nodig, voortbouwen op normen die zijn ontwikkeld")
    thisalinea.textcontent.append("door de Europese normalisatieorganisaties (ENO’s).")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 20 heeft betrekking op ..."
    thisalinea.nativeID = 42
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 16
    thisalinea.summary = "– Artikel 20 heeft betrekking op de bevoegdheidsdelegatie inzake gegevensverstrekking en gemeenschappelijke technische specificaties. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 20 heeft betrekking op de bevoegdheidsdelegatie inzake")
    thisalinea.textcontent.append("gegevensverstrekking en gemeenschappelijke technische specificaties.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Artikel 21 betreft de voortzetting ..."
    thisalinea.nativeID = 43
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 17
    thisalinea.summary = "– Artikel 21 betreft de voortzetting van de comitéprocedure in het kader van de nieuwe verordening. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Artikel 21 betreft de voortzetting van de comitéprocedure in het kader van de nieuwe")
    thisalinea.textcontent.append("verordening.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– In de artikelen 22, 23 ..."
    thisalinea.nativeID = 44
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 18
    thisalinea.summary = "– In de artikelen 22, 23 en 24 worden de voorwaarden voor herziening en inwerkingtreding van deze verordening vastgesteld. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– In de artikelen 22, 23 en 24 worden de voorwaarden voor herziening en")
    thisalinea.textcontent.append("inwerkingtreding van deze verordening vastgesteld.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Bijlage I bevat gedetailleerde bepalingen ..."
    thisalinea.nativeID = 45
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 19
    thisalinea.summary = "– Bijlage I bevat gedetailleerde bepalingen over de nationale rapportage door de lidstaten. Die waarborgen een consistente en vergelijkbare verslaglegging om de uitvoering van deze verordening te ondersteunen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Bijlage I bevat gedetailleerde bepalingen over de nationale rapportage door de")
    thisalinea.textcontent.append("lidstaten. Die waarborgen een consistente en vergelijkbare verslaglegging om de")
    thisalinea.textcontent.append("uitvoering van deze verordening te ondersteunen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Bijlage II betreft de lijst ..."
    thisalinea.nativeID = 46
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 20
    thisalinea.summary = "– Bijlage II betreft de lijst van gebieden waarvoor op de interne markt krachtens deze verordening gemeenschappelijke technische specificaties gelden waarvoor die op grond van deze verordening moeten worden vastgesteld door middel van gedelegeerde handelingen betreffende nieuwe technologische ontwikkelingen waarvoor gemeenschappelijke technische specificaties nodig zijn. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Bijlage II betreft de lijst van gebieden waarvoor op de interne markt krachtens deze")
    thisalinea.textcontent.append("verordening gemeenschappelijke technische specificaties gelden waarvoor die op")
    thisalinea.textcontent.append("grond van deze verordening moeten worden vastgesteld door middel van")
    thisalinea.textcontent.append("gedelegeerde handelingen betreffende nieuwe technologische ontwikkelingen")
    thisalinea.textcontent.append("waarvoor gemeenschappelijke technische specificaties nodig zijn.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– Bijlage III bevat categoriseringsvoorschriften voor ..."
    thisalinea.nativeID = 47
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 21
    thisalinea.summary = "– Bijlage III bevat categoriseringsvoorschriften voor de verslaglegging door de lidstaten over de uitrol van elektrische voertuigen en laadinfrastructuur. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Bijlage III bevat categoriseringsvoorschriften voor de verslaglegging door de")
    thisalinea.textcontent.append("lidstaten over de uitrol van elektrische voertuigen en laadinfrastructuur.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– De concordantietabel is opgenomen in ..."
    thisalinea.nativeID = 48
    thisalinea.parentID = 25
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 22
    thisalinea.summary = "– De concordantietabel is opgenomen in bijlage IV. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– De concordantietabel is opgenomen in bijlage IV.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "VERORDENING VAN HET EUROPEES PARLEMENT EN DE RAAD betreffende de uitrol van infrastructuur voor alternatieve brandstoffen en tot intrekking van Richtlijn 2014/94/EU van het Europees Parlement en de Raad"
    thisalinea.nativeID = 49
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "(Voor de EER relevante tekst) HET EUROPEES PARLEMENT EN DE RAAD VAN DE EUROPESE UNIE, Gezien het Verdrag betreffende de werking van de Europese Unie, en met name artikel 91, Gezien het voorstel van de Europese Commissie, Na toezending van het ontwerp van wetgevingshandeling aan de nationale parlementen, Gezien het advies van het Europees Economisch en Sociaal Comité3, Gezien het advies van het Comité van de Regio's4, Handelend volgens de gewone wetgevingsprocedure, Overwegende hetgeen volgt: laadpunt kunnen laden dan bij een normaal laadpunt. Bij die methode moet ook rekening worden gehouden met het verschillende laadpatroon tussen batterij- en plug- in "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(Voor de EER relevante tekst)")
    thisalinea.textcontent.append("HET EUROPEES PARLEMENT EN DE RAAD VAN DE EUROPESE UNIE,")
    thisalinea.textcontent.append("Gezien het Verdrag betreffende de werking van de Europese Unie, en met name artikel 91,")
    thisalinea.textcontent.append("Gezien het voorstel van de Europese Commissie,")
    thisalinea.textcontent.append("Na toezending van het ontwerp van wetgevingshandeling aan de nationale parlementen,")
    thisalinea.textcontent.append("Gezien het advies van het Europees Economisch en Sociaal Comité3,")
    thisalinea.textcontent.append("Gezien het advies van het Comité van de Regio's4,")
    thisalinea.textcontent.append("Handelend volgens de gewone wetgevingsprocedure,")
    thisalinea.textcontent.append("Overwegende hetgeen volgt:")
    thisalinea.textcontent.append("laadpunt kunnen laden dan bij een normaal laadpunt. Bij die methode moet ook")
    thisalinea.textcontent.append("rekening worden gehouden met het verschillende laadpatroon tussen batterij- en plug-")
    thisalinea.textcontent.append("in hybridevoertuigen. Een methode waarmee de nationale vloot wordt")
    thisalinea.textcontent.append("gestandaardiseerd op basis van het totale maximale laadvermogen van de openbaar")
    thisalinea.textcontent.append("toegankelijke laadinfrastructuur, moet ruimte bieden voor flexibiliteit bij de uitrol van")
    thisalinea.textcontent.append("verschillende laadtechnologieën in de lidstaten.")
    thisalinea.textcontent.append("behoeften van kleine en middelgrote ondernemingen. Daarnaast moeten in de herziene")
    thisalinea.textcontent.append("kaders het algemene nationale kader voor de planning, vergunningverlening en")
    thisalinea.textcontent.append("aanbesteding van die infrastructuur worden beschreven, met inbegrip van de")
    thisalinea.textcontent.append("vastgestelde belemmeringen en maatregelen om die weg te nemen, zodat de")
    thisalinea.textcontent.append("infrastructuur sneller kan worden uitgerold.")
    thisalinea.textcontent.append("HEBBEN DE VOLGENDE VERORDENING VASTGESTELD:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(1) Bij Richtlijn 2014/94/EU5 van het ..."
    thisalinea.nativeID = 50
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(1) Bij Richtlijn 2014/94/EU5 van het Europees Parlement en de Raad van 22 oktober 2014 heeft de EU een kader voor de uitrol van infrastructuur voor alternatieve brandstoffen vastgesteld. In haar mededeling over de toepassing van die richtlijn6 heeft de Commissie gewezen op de ongelijke uitrol van laad- en tankinfrastructuur in de Unie en op het gebrek aan interoperabiliteit en gebruikersvriendelijkheid. Voorts heeft ze opgemerkt dat het ambitieniveau bij de vaststelling van streefcijfers en ondersteunend beleid, door het ontbreken van een heldere gemeenschappelijke methode voor de vaststelling van streefcijfers en maatregelen in de op grond van Richtlijn 2014/94/EU vereiste nationale "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(1) Bij Richtlijn 2014/94/EU5 van het Europees Parlement en de Raad van 22 oktober")
    thisalinea.textcontent.append("2014 heeft de EU een kader voor de uitrol van infrastructuur voor alternatieve")
    thisalinea.textcontent.append("brandstoffen vastgesteld. In haar mededeling over de toepassing van die richtlijn6 heeft")
    thisalinea.textcontent.append("de Commissie gewezen op de ongelijke uitrol van laad- en tankinfrastructuur in de")
    thisalinea.textcontent.append("Unie en op het gebrek aan interoperabiliteit en gebruikersvriendelijkheid. Voorts heeft")
    thisalinea.textcontent.append("ze opgemerkt dat het ambitieniveau bij de vaststelling van streefcijfers en")
    thisalinea.textcontent.append("ondersteunend beleid, door het ontbreken van een heldere gemeenschappelijke")
    thisalinea.textcontent.append("methode voor de vaststelling van streefcijfers en maatregelen in de op grond van")
    thisalinea.textcontent.append("Richtlijn 2014/94/EU vereiste nationale beleidskaders, sterk verschilt van lidstaat tot")
    thisalinea.textcontent.append("lidstaat.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(2) In verschillende rechtsinstrumenten van de ..."
    thisalinea.nativeID = 51
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(2) In verschillende rechtsinstrumenten van de Unie zijn reeds streefcijfers voor hernieuwbare brandstoffen vastgesteld. In Richtlijn 2018/2001/EG7 van het Europees Parlement en de Raad is voor het marktaandeel van hernieuwbare energie in vervoersbrandstoffen een streefdoel van 14 % opgenomen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(2) In verschillende rechtsinstrumenten van de Unie zijn reeds streefcijfers voor")
    thisalinea.textcontent.append("hernieuwbare brandstoffen vastgesteld. In Richtlijn 2018/2001/EG7 van het Europees")
    thisalinea.textcontent.append("Parlement en de Raad is voor het marktaandeel van hernieuwbare energie in")
    thisalinea.textcontent.append("vervoersbrandstoffen een streefdoel van 14 % opgenomen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(3) Bij Verordening (EU) 2019/6318 van ..."
    thisalinea.nativeID = 52
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(3) Bij Verordening (EU) 2019/6318 van het Europees Parlement en de Raad en Verordening (EU) 2019/12429 van het Europees Parlement ende Raad zijn reeds CO2- emissienormen vastgesteld voor nieuwe personenauto’s, nieuwe lichte bedrijfsvoertuigen en bepaalde zware bedrijfsvoertuigen. Die instrumenten moeten de omslag naar met name emissievrije voertuigen versnellen en zo vraag naar laad- en tankinfrastructuur creëren. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(3) Bij Verordening (EU) 2019/6318 van het Europees Parlement en de Raad en")
    thisalinea.textcontent.append("Verordening (EU) 2019/12429 van het Europees Parlement ende Raad zijn reeds CO2-")
    thisalinea.textcontent.append("emissienormen vastgesteld voor nieuwe personenauto’s, nieuwe lichte")
    thisalinea.textcontent.append("bedrijfsvoertuigen en bepaalde zware bedrijfsvoertuigen. Die instrumenten moeten de")
    thisalinea.textcontent.append("omslag naar met name emissievrije voertuigen versnellen en zo vraag naar laad- en")
    thisalinea.textcontent.append("tankinfrastructuur creëren.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(4) De initiatieven ReFuelEU Luchtvaart10 en ..."
    thisalinea.nativeID = 53
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "(4) De initiatieven ReFuelEU Luchtvaart10 en FuelEU Zeevaart11 moeten de productie en het gebruik van duurzame alternatieve brandstoffen in de lucht- en zeevaart een boost geven. Hoewel voor de eisen inzake het gebruik van duurzame luchtvaartbrandstoffen grotendeels gebruik kan worden gemaakt van de bestaande tankinfrastructuur, zijn investeringen nodig voor de elektriciteitsvoorziening van stilstaande luchtvaartuigen. In het kader van FuelEU Zeevaart worden met name eisen gesteld inzake het gebruik van walstroom, waaraan alleen kan worden voldaan als in TEN-T-havens een toereikende walstroomvoorziening wordt aangelegd. Die initiatieven bevatten echter geen bepalingen over de vereiste brandstofinfrastructuur, die een randvoorwaarde is om de doelstellingen "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(4) De initiatieven ReFuelEU Luchtvaart10 en FuelEU Zeevaart11 moeten de productie en")
    thisalinea.textcontent.append("het gebruik van duurzame alternatieve brandstoffen in de lucht- en zeevaart een boost")
    thisalinea.textcontent.append("geven. Hoewel voor de eisen inzake het gebruik van duurzame luchtvaartbrandstoffen")
    thisalinea.textcontent.append("grotendeels gebruik kan worden gemaakt van de bestaande tankinfrastructuur, zijn")
    thisalinea.textcontent.append("investeringen nodig voor de elektriciteitsvoorziening van stilstaande luchtvaartuigen.")
    thisalinea.textcontent.append("In het kader van FuelEU Zeevaart worden met name eisen gesteld inzake het gebruik")
    thisalinea.textcontent.append("van walstroom, waaraan alleen kan worden voldaan als in TEN-T-havens een")
    thisalinea.textcontent.append("toereikende walstroomvoorziening wordt aangelegd. Die initiatieven bevatten echter")
    thisalinea.textcontent.append("geen bepalingen over de vereiste brandstofinfrastructuur, die een randvoorwaarde is")
    thisalinea.textcontent.append("om de doelstellingen te kunnen halen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(5) Daarom moet dit instrument op ..."
    thisalinea.nativeID = 54
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "(5) Daarom moet dit instrument op alle vervoerswijzen gericht zijn, rekening houdend met de verscheidenheid aan alternatieve brandstoffen. Het gebruik van emissievrije aandrijftechnologieën bevindt zich in de verschillende vervoerswijzen in verschillende stadia van ontwikkeling. Met name in het wegvervoer winnen elektrische voertuigen op batterijen en plug-in-hybride voertuigen snel terrein. Ook wegvoertuigen op waterstof zijn beschikbaar. Bovendien worden in het kader van verschillende projecten en eerste commerciële activiteiten momenteel compactere waterstof- en batterijschepen en waterstoftreinen geëxploiteerd; de volledige commerciële uitrol wordt de volgende jaren verwacht. De lucht- en scheepvaart blijven daarentegen afhankelijk van vloeibare en gasvormige brandstoffen, aangezien emissievrije en emissiearme "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(5) Daarom moet dit instrument op alle vervoerswijzen gericht zijn, rekening houdend met")
    thisalinea.textcontent.append("de verscheidenheid aan alternatieve brandstoffen. Het gebruik van emissievrije")
    thisalinea.textcontent.append("aandrijftechnologieën bevindt zich in de verschillende vervoerswijzen in verschillende")
    thisalinea.textcontent.append("stadia van ontwikkeling. Met name in het wegvervoer winnen elektrische voertuigen")
    thisalinea.textcontent.append("op batterijen en plug-in-hybride voertuigen snel terrein. Ook wegvoertuigen op")
    thisalinea.textcontent.append("waterstof zijn beschikbaar. Bovendien worden in het kader van verschillende projecten")
    thisalinea.textcontent.append("en eerste commerciële activiteiten momenteel compactere waterstof- en")
    thisalinea.textcontent.append("batterijschepen en waterstoftreinen geëxploiteerd; de volledige commerciële uitrol")
    thisalinea.textcontent.append("wordt de volgende jaren verwacht. De lucht- en scheepvaart blijven daarentegen")
    thisalinea.textcontent.append("afhankelijk van vloeibare en gasvormige brandstoffen, aangezien emissievrije en")
    thisalinea.textcontent.append("emissiearme aandrijfsystemen naar verwachting pas rond 2030, en in de")
    thisalinea.textcontent.append("luchtvaartsector zelfs nog later, op de markt zullen komen en de volledige")
    thisalinea.textcontent.append("commercialisering tijd vergt. Het gebruik van fossiele gasvormige of vloeibare")
    thisalinea.textcontent.append("brandstoffen is alleen mogelijk indien ingebed in een duidelijk decarbonisatietraject")
    thisalinea.textcontent.append("conform de langetermijndoelstelling van klimaatneutraliteit in de Unie, die een")
    thisalinea.textcontent.append("toename van de vermenging met of vervanging door hernieuwbare brandstoffen zoals")
    thisalinea.textcontent.append("biomethaan, geavanceerde biobrandstoffen of hernieuwbare en koolstofarme")
    thisalinea.textcontent.append("synthetische gasvormige en vloeibare brandstoffen vereist.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(6) Dergelijke biobrandstoffen en synthetische brandstoffen ..."
    thisalinea.nativeID = 55
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "(6) Dergelijke biobrandstoffen en synthetische brandstoffen ter vervanging van diesel, benzine en kerosine kunnen uit verschillende grondstoffen worden geproduceerd en in hoge bijmengpercentages in fossiele brandstoffen worden gemengd. Zij kunnen technisch worden gebruikt met de huidige voertuigtechnologie, die slechts in beperkte mate moet worden aangepast. Hernieuwbare methanol kan ook worden gebruikt voor de binnenvaart en de kustvaart. Synthetische en paraffinehoudende brandstoffen bieden potentieel om het gebruik van fossiele brandstoffen voor de energievoorziening van de vervoerssector terug te dringen. Al deze brandstoffen kunnen worden gedistribueerd, opgeslagen en gebruikt met de bestaande infrastructuur of, indien nodig, met soortgelijke infrastructuur. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(6) Dergelijke biobrandstoffen en synthetische brandstoffen ter vervanging van diesel,")
    thisalinea.textcontent.append("benzine en kerosine kunnen uit verschillende grondstoffen worden geproduceerd en in")
    thisalinea.textcontent.append("hoge bijmengpercentages in fossiele brandstoffen worden gemengd. Zij kunnen")
    thisalinea.textcontent.append("technisch worden gebruikt met de huidige voertuigtechnologie, die slechts in beperkte")
    thisalinea.textcontent.append("mate moet worden aangepast. Hernieuwbare methanol kan ook worden gebruikt voor")
    thisalinea.textcontent.append("de binnenvaart en de kustvaart. Synthetische en paraffinehoudende brandstoffen")
    thisalinea.textcontent.append("bieden potentieel om het gebruik van fossiele brandstoffen voor de energievoorziening")
    thisalinea.textcontent.append("van de vervoerssector terug te dringen. Al deze brandstoffen kunnen worden")
    thisalinea.textcontent.append("gedistribueerd, opgeslagen en gebruikt met de bestaande infrastructuur of, indien")
    thisalinea.textcontent.append("nodig, met soortgelijke infrastructuur.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(7) LNG zal waarschijnlijk een rol ..."
    thisalinea.nativeID = 56
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "(7) LNG zal waarschijnlijk een rol blijven spelen in de zeevaart, waarvoor momenteel nog geen economisch levensvatbare emissievrije aandrijftechnologie beschikbaar is. Volgens de mededeling over de strategie voor slimme en duurzame mobiliteit zouden emissievrije zeeschepen tegen 2030 klaar zijn voor marktintroductie. Gezien de lange levensduur van schepen, moet de omschakeling van de vloot stapsgewijs gebeuren. In vergelijking met de zeevaart, zijn de schepen en afstanden in de binnenvaart doorgaans kleiner en zouden emissievrije aandrijftechnologieën, zoals waterstof en elektriciteit, sneller op de markt kunnen komen. Men verwacht niet dat LNG in die sector nog een belangrijke rol zal spelen. Vervoersbrandstoffen zoals "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(7) LNG zal waarschijnlijk een rol blijven spelen in de zeevaart, waarvoor momenteel nog")
    thisalinea.textcontent.append("geen economisch levensvatbare emissievrije aandrijftechnologie beschikbaar is.")
    thisalinea.textcontent.append("Volgens de mededeling over de strategie voor slimme en duurzame mobiliteit zouden")
    thisalinea.textcontent.append("emissievrije zeeschepen tegen 2030 klaar zijn voor marktintroductie. Gezien de lange")
    thisalinea.textcontent.append("levensduur van schepen, moet de omschakeling van de vloot stapsgewijs gebeuren. In")
    thisalinea.textcontent.append("vergelijking met de zeevaart, zijn de schepen en afstanden in de binnenvaart doorgaans")
    thisalinea.textcontent.append("kleiner en zouden emissievrije aandrijftechnologieën, zoals waterstof en elektriciteit,")
    thisalinea.textcontent.append("sneller op de markt kunnen komen. Men verwacht niet dat LNG in die sector nog een")
    thisalinea.textcontent.append("belangrijke rol zal spelen. Vervoersbrandstoffen zoals LNG moeten in toenemende")
    thisalinea.textcontent.append("mate koolstofvrij worden gemaakt door ze bijvoorbeeld te mengen met of te")
    thisalinea.textcontent.append("vervangen door vloeibaar biomethaan (bio-LNG) of hernieuwbare en koolstofarme")
    thisalinea.textcontent.append("synthetische gasvormige e-brandstoffen (e-gas). Die koolstofvrije brandstoffen kunnen")
    thisalinea.textcontent.append("in dezelfde infrastructuur worden gebruikt als gasvormige fossiele brandstoffen,")
    thisalinea.textcontent.append("waardoor geleidelijk kan worden overgeschakeld op koolstofvrije brandstoffen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(8) De technologie voor zware vrachtwagens ..."
    thisalinea.nativeID = 57
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "(8) De technologie voor zware vrachtwagens op LNG is intussen helemaal matuur. De gemeenschappelijke scenario’s die aan de strategie voor duurzame en slimme mobiliteit en het klimaatdoelplan ten grondslag liggen, alsook de herziene Fit for 55- modelscenario’s wijzen op een beperkte rol van gasvormige brandstoffen, die in toenemende mate koolstofvrij zullen worden, voor zwaar wegvervoer over langere afstand. Voorts wordt verwacht dat voertuigen op LPG en CNG, waarvoor in de Unie reeds een toereikend infrastructuurnet bestaat, geleidelijk zullen worden vervangen door emissievrije voertuigen; daarom wordt geoordeeld dat de inspanningen voor de uitrol van LNG-infrastructuur die ook koolstofvrije brandstoffen kan leveren, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(8) De technologie voor zware vrachtwagens op LNG is intussen helemaal matuur. De")
    thisalinea.textcontent.append("gemeenschappelijke scenario’s die aan de strategie voor duurzame en slimme")
    thisalinea.textcontent.append("mobiliteit en het klimaatdoelplan ten grondslag liggen, alsook de herziene Fit for 55-")
    thisalinea.textcontent.append("modelscenario’s wijzen op een beperkte rol van gasvormige brandstoffen, die in")
    thisalinea.textcontent.append("toenemende mate koolstofvrij zullen worden, voor zwaar wegvervoer over langere")
    thisalinea.textcontent.append("afstand. Voorts wordt verwacht dat voertuigen op LPG en CNG, waarvoor in de Unie")
    thisalinea.textcontent.append("reeds een toereikend infrastructuurnet bestaat, geleidelijk zullen worden vervangen")
    thisalinea.textcontent.append("door emissievrije voertuigen; daarom wordt geoordeeld dat de inspanningen voor de")
    thisalinea.textcontent.append("uitrol van LNG-infrastructuur die ook koolstofvrije brandstoffen kan leveren, beperkt")
    thisalinea.textcontent.append("kunnen blijven tot het wegwerken van de resterende leemten op de hoofdnetten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(9) De uitrol van openbaar toegankelijke ..."
    thisalinea.nativeID = 58
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "(9) De uitrol van openbaar toegankelijke laadinfrastructuur voor lichte elektrische voertuigen is in de Unie niet gelijk verlopen. Een aanhoudende ongelijke spreiding zou een belemmering vormen voor het gebruik van dergelijke voertuigen, waardoor de connectiviteit in de hele Unie zou worden beperkt. Aanhoudende verschillen in de beleidsambities en -benaderingen tussen de lidstaten staan haaks op de voor substantiële marktinvesteringen vereiste zekerheid op lange termijn. Verplichte nationale minimumstreefcijfers voor de lidstaten moeten daarom de beleidsrichting bepalen en de nationale beleidskaders aanvullen. In die aanpak moeten nationale streefcijfers op basis van de omvang van de vloot worden gecombineerd met op afstand gebaseerde "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(9) De uitrol van openbaar toegankelijke laadinfrastructuur voor lichte elektrische")
    thisalinea.textcontent.append("voertuigen is in de Unie niet gelijk verlopen. Een aanhoudende ongelijke spreiding")
    thisalinea.textcontent.append("zou een belemmering vormen voor het gebruik van dergelijke voertuigen, waardoor de")
    thisalinea.textcontent.append("connectiviteit in de hele Unie zou worden beperkt. Aanhoudende verschillen in de")
    thisalinea.textcontent.append("beleidsambities en -benaderingen tussen de lidstaten staan haaks op de voor")
    thisalinea.textcontent.append("substantiële marktinvesteringen vereiste zekerheid op lange termijn. Verplichte")
    thisalinea.textcontent.append("nationale minimumstreefcijfers voor de lidstaten moeten daarom de beleidsrichting")
    thisalinea.textcontent.append("bepalen en de nationale beleidskaders aanvullen. In die aanpak moeten nationale")
    thisalinea.textcontent.append("streefcijfers op basis van de omvang van de vloot worden gecombineerd met op")
    thisalinea.textcontent.append("afstand gebaseerde doelstellingen voor het trans-Europese vervoersnetwerk (TEN-T).")
    thisalinea.textcontent.append("Nationale vlootstreefcijfers moeten ervoor zorgen dat de uitrol van voldoende")
    thisalinea.textcontent.append("openbaar toegankelijke laadinfrastructuur gelijke tred houdt met de toename van")
    thisalinea.textcontent.append("voertuigen in elke lidstaat. De op afstand gebaseerde doelstellingen voor het TEN-T-")
    thisalinea.textcontent.append("netwerk moeten een volledige dekking van de hoofdwegennetten van de Unie met")
    thisalinea.textcontent.append("elektrische laadpunten waarborgen en naadloos vervoer doorheen de Unie mogelijk")
    thisalinea.textcontent.append("maken.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(10) Er moeten nationale streefcijfers op ..."
    thisalinea.nativeID = 59
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 9
    thisalinea.summary = "(10) Er moeten nationale streefcijfers op basis van het wagenpark worden vastgesteld op basis van het totale aantal ingeschreven elektrische voertuigen in die lidstaat, aan de hand van een gemeenschappelijke methode die rekening houdt met de technologische ontwikkelingen, zoals de grotere autonomie van elektrische voertuigen of de toenemende marktpenetratie van snelladers, waaraan een groter aantal voertuigen per "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(10) Er moeten nationale streefcijfers op basis van het wagenpark worden vastgesteld op")
    thisalinea.textcontent.append("basis van het totale aantal ingeschreven elektrische voertuigen in die lidstaat, aan de")
    thisalinea.textcontent.append("hand van een gemeenschappelijke methode die rekening houdt met de technologische")
    thisalinea.textcontent.append("ontwikkelingen, zoals de grotere autonomie van elektrische voertuigen of de")
    thisalinea.textcontent.append("toenemende marktpenetratie van snelladers, waaraan een groter aantal voertuigen per")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(11) Bij de uitvoering door de ..."
    thisalinea.nativeID = 60
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 10
    thisalinea.summary = "(11) Bij de uitvoering door de lidstaten moet worden gezorgd voor voldoende openbaar toegankelijke laadpunten, met name bij openbaarvervoerstations, zoals passagiersterminals in havens, luchthavens of treinstations. Om het de consument gemakkelijker te maken, moeten voldoende openbaar toegankelijke snellaadpunten voor lichte voertuigen worden geïnstalleerd, met name op het TEN-T-netwerk, teneinde volledige grensoverschrijdende connectiviteit te waarborgen en het verkeer van elektrische voertuigen in de hele Unie mogelijk te maken. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(11) Bij de uitvoering door de lidstaten moet worden gezorgd voor voldoende openbaar")
    thisalinea.textcontent.append("toegankelijke laadpunten, met name bij openbaarvervoerstations, zoals")
    thisalinea.textcontent.append("passagiersterminals in havens, luchthavens of treinstations. Om het de consument")
    thisalinea.textcontent.append("gemakkelijker te maken, moeten voldoende openbaar toegankelijke snellaadpunten")
    thisalinea.textcontent.append("voor lichte voertuigen worden geïnstalleerd, met name op het TEN-T-netwerk,")
    thisalinea.textcontent.append("teneinde volledige grensoverschrijdende connectiviteit te waarborgen en het verkeer")
    thisalinea.textcontent.append("van elektrische voertuigen in de hele Unie mogelijk te maken.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(12) Eigenaars van elektrische voertuigen moeten ..."
    thisalinea.nativeID = 61
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 11
    thisalinea.summary = "(12) Eigenaars van elektrische voertuigen moeten grotendeels gebruik maken van laadpunten in hun eigen gebouw of op collectieve parkeerplaatsen in residentiële en niet-residentiële gebouwen. Hoewel de uitrol van infrastructuur voor leidingen en laadpunten in die gebouwen geregeld is bij Richtlijn 2010/31/EU12 van het Europees Parlement en de Raad, moeten de lidstaten bij de uitrolplanning van openbaar toegankelijke laadpunten rekening houden met de beschikbaarheid van dergelijke particuliere infrastructuur. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(12) Eigenaars van elektrische voertuigen moeten grotendeels gebruik maken van")
    thisalinea.textcontent.append("laadpunten in hun eigen gebouw of op collectieve parkeerplaatsen in residentiële en")
    thisalinea.textcontent.append("niet-residentiële gebouwen. Hoewel de uitrol van infrastructuur voor leidingen en")
    thisalinea.textcontent.append("laadpunten in die gebouwen geregeld is bij Richtlijn 2010/31/EU12 van het Europees")
    thisalinea.textcontent.append("Parlement en de Raad, moeten de lidstaten bij de uitrolplanning van openbaar")
    thisalinea.textcontent.append("toegankelijke laadpunten rekening houden met de beschikbaarheid van dergelijke")
    thisalinea.textcontent.append("particuliere infrastructuur.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(13) Elektrische zware bedrijfsvoertuigen vergen andere ..."
    thisalinea.nativeID = 62
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 12
    thisalinea.summary = "(13) Elektrische zware bedrijfsvoertuigen vergen andere laadinfrastructuur dan lichte voertuigen. Op dit moment is er echter bijna nergens in de Unie openbaar toegankelijke infrastructuur voor elektrische zware bedrijfsvoertuigen beschikbaar. Een aanpak met een combinatie van op afstand gebaseerde doelstellingen voor het TEN-T-netwerk, streefcijfers voor infrastructuur voor nachtelijk opladen en streefcijfers voor stedelijke knooppunten moet in de hele Unie zorgen voor een toereikende dekking van openbaar toegankelijke laadinfrastructuur voor elektrische zware bedrijfsvoertuigen om de verwachte marktpenetratie van zware bedrijfsvoertuigen op batterijen te ondersteunen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(13) Elektrische zware bedrijfsvoertuigen vergen andere laadinfrastructuur dan lichte")
    thisalinea.textcontent.append("voertuigen. Op dit moment is er echter bijna nergens in de Unie openbaar")
    thisalinea.textcontent.append("toegankelijke infrastructuur voor elektrische zware bedrijfsvoertuigen beschikbaar.")
    thisalinea.textcontent.append("Een aanpak met een combinatie van op afstand gebaseerde doelstellingen voor het")
    thisalinea.textcontent.append("TEN-T-netwerk, streefcijfers voor infrastructuur voor nachtelijk opladen en")
    thisalinea.textcontent.append("streefcijfers voor stedelijke knooppunten moet in de hele Unie zorgen voor een")
    thisalinea.textcontent.append("toereikende dekking van openbaar toegankelijke laadinfrastructuur voor elektrische")
    thisalinea.textcontent.append("zware bedrijfsvoertuigen om de verwachte marktpenetratie van zware")
    thisalinea.textcontent.append("bedrijfsvoertuigen op batterijen te ondersteunen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(14) Op het TEN-T-netwerk moeten voldoende ..."
    thisalinea.nativeID = 63
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 13
    thisalinea.summary = "(14) Op het TEN-T-netwerk moeten voldoende openbaar toegankelijke snellaadpunten voor zware bedrijfsvoertuigen worden geïnstalleerd om de volledige grensoverschrijdende connectiviteit te waarborgen en naadloos verkeer van elektrische voertuigen in de hele Unie mogelijk te maken. Die infrastructuur moet over voldoende vermogen beschikken om het voertuig binnen de wettelijke rusttijd van de bestuurder te kunnen opladen. Om de elektrificatie van het langeafstandsvervoer te ondersteunen, moeten zware bedrijfsvoertuigen niet alleen gebruik kunnen maken van snelle laadpunten maar op het hoofdwegennet ook toegang hebben tot openbaar toegankelijke laadinfrastructuur voor nachtelijk opladen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(14) Op het TEN-T-netwerk moeten voldoende openbaar toegankelijke snellaadpunten")
    thisalinea.textcontent.append("voor zware bedrijfsvoertuigen worden geïnstalleerd om de volledige")
    thisalinea.textcontent.append("grensoverschrijdende connectiviteit te waarborgen en naadloos verkeer van elektrische")
    thisalinea.textcontent.append("voertuigen in de hele Unie mogelijk te maken. Die infrastructuur moet over voldoende")
    thisalinea.textcontent.append("vermogen beschikken om het voertuig binnen de wettelijke rusttijd van de bestuurder")
    thisalinea.textcontent.append("te kunnen opladen. Om de elektrificatie van het langeafstandsvervoer te ondersteunen,")
    thisalinea.textcontent.append("moeten zware bedrijfsvoertuigen niet alleen gebruik kunnen maken van snelle")
    thisalinea.textcontent.append("laadpunten maar op het hoofdwegennet ook toegang hebben tot openbaar")
    thisalinea.textcontent.append("toegankelijke laadinfrastructuur voor nachtelijk opladen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(15) De laadinfrastructuur op het TEN-T-netwerk ..."
    thisalinea.nativeID = 64
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 14
    thisalinea.summary = "(15) De laadinfrastructuur op het TEN-T-netwerk moet worden aangevuld met openbaar toegankelijke snellaadinfrastructuur in stedelijke knooppunten. Er is met name infrastructuur nodig om laadmogelijkheden te bieden voor distributievrachtwagens en om vrachtwagens die langeafstandsvervoer verrichten de kans te geven op hun bestemming te laden; het nationale streefcijfer op basis van het wagenpark moet ook in steden voorzien in laadpunten voor lichte bedrijfsvoertuigen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(15) De laadinfrastructuur op het TEN-T-netwerk moet worden aangevuld met openbaar")
    thisalinea.textcontent.append("toegankelijke snellaadinfrastructuur in stedelijke knooppunten. Er is met name")
    thisalinea.textcontent.append("infrastructuur nodig om laadmogelijkheden te bieden voor distributievrachtwagens en")
    thisalinea.textcontent.append("om vrachtwagens die langeafstandsvervoer verrichten de kans te geven op hun")
    thisalinea.textcontent.append("bestemming te laden; het nationale streefcijfer op basis van het wagenpark moet ook")
    thisalinea.textcontent.append("in steden voorzien in laadpunten voor lichte bedrijfsvoertuigen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(16) De uitrol van laadinfrastructuur is ..."
    thisalinea.nativeID = 65
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 15
    thisalinea.summary = "(16) De uitrol van laadinfrastructuur is even belangrijk op particuliere locaties, zoals in particuliere garages en in logistieke centra om laden tijdens de nacht en op de bestemming mogelijk te maken. Overheidsinstanties moeten in het kader van de ontwikkeling van hun herziene nationale beleidskaders maatregelen nemen om ervoor te zorgen dat er adequate infrastructuur om tijdens de nacht of op de bestemming te laden beschikbaar is. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(16) De uitrol van laadinfrastructuur is even belangrijk op particuliere locaties, zoals in")
    thisalinea.textcontent.append("particuliere garages en in logistieke centra om laden tijdens de nacht en op de")
    thisalinea.textcontent.append("bestemming mogelijk te maken. Overheidsinstanties moeten in het kader van de")
    thisalinea.textcontent.append("ontwikkeling van hun herziene nationale beleidskaders maatregelen nemen om ervoor")
    thisalinea.textcontent.append("te zorgen dat er adequate infrastructuur om tijdens de nacht of op de bestemming te")
    thisalinea.textcontent.append("laden beschikbaar is.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(17) Tot de openbaar toegankelijke laad- ..."
    thisalinea.nativeID = 66
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 16
    thisalinea.summary = "(17) Tot de openbaar toegankelijke laad- of tankpunten behoren bijvoorbeeld particuliere publiek toegankelijke laad- of tankpunten die zich op openbaar of privéterrein bevinden, zoals openbare parkeerplaatsen of parkeerplaatsen van supermarkten. Een laad- of tankpunt op privéterrein dat voor het grote publiek toegankelijk is, moet als openbaar toegankelijk worden beschouwd, zelfs als de toegang beperkt is tot een specifieke algemene groep gebruikers, bijvoorbeeld klanten. Laad- of tankpunten voor autodeelsystemen mogen alleen als openbaar toegankelijk worden beschouwd als zij uitdrukkelijk toegankelijk zijn voor derden. Laad- of tankpunten op privéterrein waarvan de toegang beperkt is tot een beperkte, specifieke groep personen, zoals parkeerplaatsen "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(17) Tot de openbaar toegankelijke laad- of tankpunten behoren bijvoorbeeld particuliere")
    thisalinea.textcontent.append("publiek toegankelijke laad- of tankpunten die zich op openbaar of privéterrein")
    thisalinea.textcontent.append("bevinden, zoals openbare parkeerplaatsen of parkeerplaatsen van supermarkten. Een")
    thisalinea.textcontent.append("laad- of tankpunt op privéterrein dat voor het grote publiek toegankelijk is, moet als")
    thisalinea.textcontent.append("openbaar toegankelijk worden beschouwd, zelfs als de toegang beperkt is tot een")
    thisalinea.textcontent.append("specifieke algemene groep gebruikers, bijvoorbeeld klanten. Laad- of tankpunten voor")
    thisalinea.textcontent.append("autodeelsystemen mogen alleen als openbaar toegankelijk worden beschouwd als zij")
    thisalinea.textcontent.append("uitdrukkelijk toegankelijk zijn voor derden. Laad- of tankpunten op privéterrein")
    thisalinea.textcontent.append("waarvan de toegang beperkt is tot een beperkte, specifieke groep personen, zoals")
    thisalinea.textcontent.append("parkeerplaatsen in kantoorgebouwen die alleen toegankelijk zijn voor werknemers of")
    thisalinea.textcontent.append("gemachtigde personen, mogen niet als openbaar toegankelijke laad- of tankpunten")
    thisalinea.textcontent.append("worden beschouwd.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(18) Een laadstation is de enige ..."
    thisalinea.nativeID = 67
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 17
    thisalinea.summary = "(18) Een laadstation is de enige fysieke installatie voor het opladen van elektrische voertuigen. Elk station heeft een theoretisch maximumvermogen, uitgedrukt in kW. Elk station omvat ten minste één laadpunt dat slechts één voertuig tegelijk kan bedienen. Het aantal laadpunten in een laadstation bepaalt hoeveel voertuigen op een bepaald moment in dat station kunnen worden opgeladen. Wanneer op een laadstation op een bepaald moment meer dan één voertuig wordt opgeladen, wordt het maximumvermogen over de verschillende laadpunten verdeeld, waardoor het op elk laadpunt geleverde vermogen lager is dan het laadvermogen van dat station. Een laadpool bestaat uit een of meer "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(18) Een laadstation is de enige fysieke installatie voor het opladen van elektrische")
    thisalinea.textcontent.append("voertuigen. Elk station heeft een theoretisch maximumvermogen, uitgedrukt in kW.")
    thisalinea.textcontent.append("Elk station omvat ten minste één laadpunt dat slechts één voertuig tegelijk kan")
    thisalinea.textcontent.append("bedienen. Het aantal laadpunten in een laadstation bepaalt hoeveel voertuigen op een")
    thisalinea.textcontent.append("bepaald moment in dat station kunnen worden opgeladen. Wanneer op een laadstation")
    thisalinea.textcontent.append("op een bepaald moment meer dan één voertuig wordt opgeladen, wordt het")
    thisalinea.textcontent.append("maximumvermogen over de verschillende laadpunten verdeeld, waardoor het op elk")
    thisalinea.textcontent.append("laadpunt geleverde vermogen lager is dan het laadvermogen van dat station. Een")
    thisalinea.textcontent.append("laadpool bestaat uit een of meer laadstations op één specifieke locatie, met inbegrip")
    thisalinea.textcontent.append("van, in voorkomend geval, de voor het laden bestemde parkeerplaatsen. Voor het")
    thisalinea.textcontent.append("behalen van de in deze verordening vastgestelde streefcijfers voor laadpools kan het")
    thisalinea.textcontent.append("minimale laadvermogen dat voor die pools vereist is, door een of meer laadstations")
    thisalinea.textcontent.append("worden geleverd.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(19) De mogelijkheid om geavanceerde digitale ..."
    thisalinea.nativeID = 68
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 18
    thisalinea.summary = "(19) De mogelijkheid om geavanceerde digitale diensten te ontwikkelen, met inbegrip van aan een contract gekoppelde betaaloplossingen, en om met digitale middelen transparante gebruikersinformatie te verstrekken, hangt af van de uitrol van digitaal geconnecteerde en slimme laadpunten die de ontwikkeling van een digitaal verbonden en interoperabele infrastructuur13 ondersteunen. Die slimme laadpunten moeten bepaalde fysieke kenmerken en technische specificaties (hard- en software) bezitten om gegevens in real time te kunnen verzenden en ontvangen, zodat informatie kan worden uitgewisseld tussen marktdeelnemers die van deze gegevens afhankelijk zijn voor de volledige ontwikkeling van de oplaadervaring, zoals exploitanten van laadpunten, aanbieders van mobiliteitsdiensten, e-roamingplatforms, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(19) De mogelijkheid om geavanceerde digitale diensten te ontwikkelen, met inbegrip van")
    thisalinea.textcontent.append("aan een contract gekoppelde betaaloplossingen, en om met digitale middelen")
    thisalinea.textcontent.append("transparante gebruikersinformatie te verstrekken, hangt af van de uitrol van digitaal")
    thisalinea.textcontent.append("geconnecteerde en slimme laadpunten die de ontwikkeling van een digitaal verbonden")
    thisalinea.textcontent.append("en interoperabele infrastructuur13 ondersteunen. Die slimme laadpunten moeten")
    thisalinea.textcontent.append("bepaalde fysieke kenmerken en technische specificaties (hard- en software) bezitten")
    thisalinea.textcontent.append("om gegevens in real time te kunnen verzenden en ontvangen, zodat informatie kan")
    thisalinea.textcontent.append("worden uitgewisseld tussen marktdeelnemers die van deze gegevens afhankelijk zijn")
    thisalinea.textcontent.append("voor de volledige ontwikkeling van de oplaadervaring, zoals exploitanten van")
    thisalinea.textcontent.append("laadpunten, aanbieders van mobiliteitsdiensten, e-roamingplatforms,")
    thisalinea.textcontent.append("distributiesysteembeheerders en uiteindelijk eindgebruikers.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(20) Slimme metersystemen als gedefinieerd in ..."
    thisalinea.nativeID = 69
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 19
    thisalinea.summary = "(20) Slimme metersystemen als gedefinieerd in Richtlijn (EU) 2019/944 van het Europees Parlement en de Raad14 leveren de realtimegegevens die nodig zijn om de stabiliteit van het net te garanderen en aan te zetten tot een rationeel gebruik van laaddiensten. Door in realtime nauwkeurige en transparante kostprijsinformatie te verstrekken, moedigen zij de gebruiker, in combinatie met slimme laadpunten, aan op te laden op tijdstippen waarop de algemene elektriciteitsvraag en de energieprijzen laag zijn. Het gebruik van slimme metersystemen in combinatie met slimme laadpunten kan het laden optimaliseren, hetgeen voordelen biedt voor het elektriciteitssysteem en de eindgebruiker. De lidstaten moeten het "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(20) Slimme metersystemen als gedefinieerd in Richtlijn (EU) 2019/944 van het Europees")
    thisalinea.textcontent.append("Parlement en de Raad14 leveren de realtimegegevens die nodig zijn om de stabiliteit")
    thisalinea.textcontent.append("van het net te garanderen en aan te zetten tot een rationeel gebruik van laaddiensten.")
    thisalinea.textcontent.append("Door in realtime nauwkeurige en transparante kostprijsinformatie te verstrekken,")
    thisalinea.textcontent.append("moedigen zij de gebruiker, in combinatie met slimme laadpunten, aan op te laden op")
    thisalinea.textcontent.append("tijdstippen waarop de algemene elektriciteitsvraag en de energieprijzen laag zijn. Het")
    thisalinea.textcontent.append("gebruik van slimme metersystemen in combinatie met slimme laadpunten kan het")
    thisalinea.textcontent.append("laden optimaliseren, hetgeen voordelen biedt voor het elektriciteitssysteem en de")
    thisalinea.textcontent.append("eindgebruiker. De lidstaten moeten het gebruik van slimme metersystemen voor het")
    thisalinea.textcontent.append("opladen van elektrische voertuigen op openbaar toegankelijke laadpunten")
    thisalinea.textcontent.append("aanmoedigen, voor zover dit technisch haalbaar en economisch redelijk is, en ervoor")
    thisalinea.textcontent.append("zorgen dat die systemen voldoen aan de eisen van artikel 20 van Richtlijn (EU)")
    thisalinea.textcontent.append("2019/944.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(21) Om in te spelen om ..."
    thisalinea.nativeID = 70
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 20
    thisalinea.summary = "(21) Om in te spelen om de behoeften van het toenemende aantal elektrische voertuigen in onder meer het wegvervoer, bij het spoor en in de zeevaart zal het oplaadproces moeten worden geoptimaliseerd en beheerd op een manier die geen congestie veroorzaakt en waarbij de beschikbaarheid van hernieuwbare elektriciteit en lage elektriciteitsprijzen in het systeem optimaal worden benut. Met name slim opladen, waarbij gebruik wordt gemaakt van aggregatie en vraagrespons op basis van de prijs, kan de integratie van elektrische voertuigen in het elektriciteitssysteem verder faciliteren. Systeemintegratie kan verder worden vergemakkelijkt door bidirectioneel laden (tussen voertuig en net). Slim laden moet "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(21) Om in te spelen om de behoeften van het toenemende aantal elektrische voertuigen in")
    thisalinea.textcontent.append("onder meer het wegvervoer, bij het spoor en in de zeevaart zal het oplaadproces")
    thisalinea.textcontent.append("moeten worden geoptimaliseerd en beheerd op een manier die geen congestie")
    thisalinea.textcontent.append("veroorzaakt en waarbij de beschikbaarheid van hernieuwbare elektriciteit en lage")
    thisalinea.textcontent.append("elektriciteitsprijzen in het systeem optimaal worden benut. Met name slim opladen,")
    thisalinea.textcontent.append("waarbij gebruik wordt gemaakt van aggregatie en vraagrespons op basis van de prijs,")
    thisalinea.textcontent.append("kan de integratie van elektrische voertuigen in het elektriciteitssysteem verder")
    thisalinea.textcontent.append("faciliteren. Systeemintegratie kan verder worden vergemakkelijkt door bidirectioneel")
    thisalinea.textcontent.append("laden (tussen voertuig en net). Slim laden moet daarom worden ondersteund door alle")
    thisalinea.textcontent.append("normale laadpunten waarop geparkeerde voertuigen gewoonlijk voor een langere")
    thisalinea.textcontent.append("periode worden aangesloten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(22) De ontwikkeling van infrastructuur voor ..."
    thisalinea.nativeID = 71
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 21
    thisalinea.summary = "(22) De ontwikkeling van infrastructuur voor elektrische voertuigen, de interactie van die infrastructuur met het elektriciteitssysteem en de aan de verschillende actoren op de markt voor elektrische mobiliteit toegekende rechten en verantwoordelijkheden moeten in overeenstemming zijn met de beginselen van Richtlijn (EU) 2019/944. In die zin moeten distributiesysteembeheerders op niet-discriminerende basis samenwerken met iedereen die een openbaar toegankelijk laadpunt installeert of exploiteert, en de lidstaten moeten ervoor zorgen dat voor de elektriciteitsvoorziening van een laadpunt een contract kan worden gesloten met een andere leverancier dan de entiteit die elektriciteit levert aan het huishouden of het gebouw waar dat laadpunt zich "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(22) De ontwikkeling van infrastructuur voor elektrische voertuigen, de interactie van die")
    thisalinea.textcontent.append("infrastructuur met het elektriciteitssysteem en de aan de verschillende actoren op de")
    thisalinea.textcontent.append("markt voor elektrische mobiliteit toegekende rechten en verantwoordelijkheden")
    thisalinea.textcontent.append("moeten in overeenstemming zijn met de beginselen van Richtlijn (EU) 2019/944. In")
    thisalinea.textcontent.append("die zin moeten distributiesysteembeheerders op niet-discriminerende basis")
    thisalinea.textcontent.append("samenwerken met iedereen die een openbaar toegankelijk laadpunt installeert of")
    thisalinea.textcontent.append("exploiteert, en de lidstaten moeten ervoor zorgen dat voor de elektriciteitsvoorziening")
    thisalinea.textcontent.append("van een laadpunt een contract kan worden gesloten met een andere leverancier dan de")
    thisalinea.textcontent.append("entiteit die elektriciteit levert aan het huishouden of het gebouw waar dat laadpunt zich")
    thisalinea.textcontent.append("bevindt. De toegang van EU-elektriciteitsleveranciers tot laadpunten mag geen afbreuk")
    thisalinea.textcontent.append("doen aan de ontheffingen uit hoofde van artikel 66 van Richtlijn (EU) 2019/944.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(23) De installatie en het beheer ..."
    thisalinea.nativeID = 72
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 22
    thisalinea.summary = "(23) De installatie en het beheer van laadpunten voor elektrische voertuigen moeten op basis van een concurrerende marktwerking worden ontwikkeld, waarbij die markt vrij toegankelijk moet zijn voor alle partijen die laadinfrastructuur willen aanleggen of beheren. Gezien de beperkte alternatieve locaties op de snelwegen vormen de bestaande snelwegconcessies, bijvoorbeeld voor conventionele tankstations of rustplaatsen, een bijzonder punt van zorg, aangezien die concessies soms een zeer lange looptijd hebben en in sommige gevallen zelfs geen exacte einddatum hebben. Voor laadstations op of in de buurt van bestaande rustplaatsen op de snelwegen moeten de lidstaten ernaar streven om, voor zover mogelijk en "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(23) De installatie en het beheer van laadpunten voor elektrische voertuigen moeten op")
    thisalinea.textcontent.append("basis van een concurrerende marktwerking worden ontwikkeld, waarbij die markt vrij")
    thisalinea.textcontent.append("toegankelijk moet zijn voor alle partijen die laadinfrastructuur willen aanleggen of")
    thisalinea.textcontent.append("beheren. Gezien de beperkte alternatieve locaties op de snelwegen vormen de")
    thisalinea.textcontent.append("bestaande snelwegconcessies, bijvoorbeeld voor conventionele tankstations of")
    thisalinea.textcontent.append("rustplaatsen, een bijzonder punt van zorg, aangezien die concessies soms een zeer")
    thisalinea.textcontent.append("lange looptijd hebben en in sommige gevallen zelfs geen exacte einddatum hebben.")
    thisalinea.textcontent.append("Voor laadstations op of in de buurt van bestaande rustplaatsen op de snelwegen")
    thisalinea.textcontent.append("moeten de lidstaten ernaar streven om, voor zover mogelijk en in overeenstemming")
    thisalinea.textcontent.append("met Richtlijn 2014/23/EU15 van het Europees Parlement en de Raad, nieuwe")
    thisalinea.textcontent.append("concessies te gunnen teneinde de uitrolkosten te beperken en kansen te bieden aan")
    thisalinea.textcontent.append("nieuwkomers op de markt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(24) Prijstransparantie is van cruciaal belang ..."
    thisalinea.nativeID = 73
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 23
    thisalinea.summary = "(24) Prijstransparantie is van cruciaal belang voor naadloos en eenvoudig opladen en bijtanken. Gebruikers van voertuigen op alternatieve brandstof moeten vóór het begin van de laad- of tankbeurt nauwkeurige prijsinformatie krijgen. De prijs moet op een duidelijk gestructureerde wijze worden meegedeeld zodat eindgebruikers inzicht krijgen in de verschillende kostencomponenten. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(24) Prijstransparantie is van cruciaal belang voor naadloos en eenvoudig opladen en")
    thisalinea.textcontent.append("bijtanken. Gebruikers van voertuigen op alternatieve brandstof moeten vóór het begin")
    thisalinea.textcontent.append("van de laad- of tankbeurt nauwkeurige prijsinformatie krijgen. De prijs moet op een")
    thisalinea.textcontent.append("duidelijk gestructureerde wijze worden meegedeeld zodat eindgebruikers inzicht")
    thisalinea.textcontent.append("krijgen in de verschillende kostencomponenten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(25) Er ontstaan nieuwe diensten die ..."
    thisalinea.nativeID = 74
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 24
    thisalinea.summary = "(25) Er ontstaan nieuwe diensten die het gebruik van elektrische voertuigen ondersteunen. Entiteiten die deze diensten aanbieden, zoals aanbieders van mobiliteitsdiensten, moeten onder eerlijke marktvoorwaarden kunnen werken. Exploitanten van laadpunten mogen dergelijke dienstverleners geen ongeoorloofde voorkeursbehandeling geven, bijvoorbeeld door ongerechtvaardigde prijsdifferentiatie die de concurrentie kan belemmeren en uiteindelijk kan leiden tot hogere consumentenprijzen. De Commissie moet toezicht houden op de ontwikkeling van de oplaadmarkt. Bij de herziening van de verordening zal de Commissie maatregelen nemen wanneer marktontwikkelingen dit vereisen, bijvoorbeeld als er sprake zou zijn van beperkingen van diensten voor eindgebruikers of handelspraktijken die de mededinging kunnen beperken. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(25) Er ontstaan nieuwe diensten die het gebruik van elektrische voertuigen ondersteunen.")
    thisalinea.textcontent.append("Entiteiten die deze diensten aanbieden, zoals aanbieders van mobiliteitsdiensten,")
    thisalinea.textcontent.append("moeten onder eerlijke marktvoorwaarden kunnen werken. Exploitanten van")
    thisalinea.textcontent.append("laadpunten mogen dergelijke dienstverleners geen ongeoorloofde")
    thisalinea.textcontent.append("voorkeursbehandeling geven, bijvoorbeeld door ongerechtvaardigde prijsdifferentiatie")
    thisalinea.textcontent.append("die de concurrentie kan belemmeren en uiteindelijk kan leiden tot hogere")
    thisalinea.textcontent.append("consumentenprijzen. De Commissie moet toezicht houden op de ontwikkeling van de")
    thisalinea.textcontent.append("oplaadmarkt. Bij de herziening van de verordening zal de Commissie maatregelen")
    thisalinea.textcontent.append("nemen wanneer marktontwikkelingen dit vereisen, bijvoorbeeld als er sprake zou zijn")
    thisalinea.textcontent.append("van beperkingen van diensten voor eindgebruikers of handelspraktijken die de")
    thisalinea.textcontent.append("mededinging kunnen beperken.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(26) Het marktaandeel van motorvoertuigen op ..."
    thisalinea.nativeID = 75
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 25
    thisalinea.summary = "(26) Het marktaandeel van motorvoertuigen op waterstof is momenteel zeer klein. De uitrol van toereikende infrastructuur voor het tanken van waterstof is echter essentieel om een grootschalige uitrol van motorvoertuigen op waterstof mogelijk te maken, zoals beoogd in de waterstofstrategie van de Commissie voor een klimaatneutraal Europa 16. Momenteel zijn er slechts in enkele lidstaten waterstoftankpunten en zijn de meeste daarvan niet geschikt voor zware bedrijfsvoertuigen, waardoor waterstofvoertuigen niet in de hele Unie kunnen rijden. Bindende streefcijfers voor de uitrol van openbaar toegankelijke waterstoftankpunten moeten ervoor zorgen dat op het TEN-T- kernnetwerk een voldoende dicht netwerk van waterstoftankpunten wordt uitgerold "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(26) Het marktaandeel van motorvoertuigen op waterstof is momenteel zeer klein. De uitrol")
    thisalinea.textcontent.append("van toereikende infrastructuur voor het tanken van waterstof is echter essentieel om")
    thisalinea.textcontent.append("een grootschalige uitrol van motorvoertuigen op waterstof mogelijk te maken, zoals")
    thisalinea.textcontent.append("beoogd in de waterstofstrategie van de Commissie voor een klimaatneutraal Europa 16.")
    thisalinea.textcontent.append("Momenteel zijn er slechts in enkele lidstaten waterstoftankpunten en zijn de meeste")
    thisalinea.textcontent.append("daarvan niet geschikt voor zware bedrijfsvoertuigen, waardoor waterstofvoertuigen")
    thisalinea.textcontent.append("niet in de hele Unie kunnen rijden. Bindende streefcijfers voor de uitrol van openbaar")
    thisalinea.textcontent.append("toegankelijke waterstoftankpunten moeten ervoor zorgen dat op het TEN-T-")
    thisalinea.textcontent.append("kernnetwerk een voldoende dicht netwerk van waterstoftankpunten wordt uitgerold")
    thisalinea.textcontent.append("om in de hele Unie naadloos vervoer met lichte en zware bedrijfsvoertuigen op")
    thisalinea.textcontent.append("waterstof mogelijk te maken.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(27) Voertuigen op waterstof moeten kunnen ..."
    thisalinea.nativeID = 76
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 26
    thisalinea.summary = "(27) Voertuigen op waterstof moeten kunnen tanken op of dichtbij hun bestemming, die gewoonlijk in een stedelijk gebied ligt. Om ervoor te zorgen dat er op zijn minst in de belangrijkste steden openbaar toegankelijke tankpunten zijn, moeten er waterstoftankstations komen in alle stedelijke knooppunten zoals gedefinieerd in Verordening (EU) nr. 1315/201317 van het Europees Parlement en de Raad. Overheden moeten onderzoeken of die stations in stedelijke knooppunten kunnen worden voorzien in multimodale goederenterminals, aangezien dat niet alleen typische bestemmingen zijn voor zware bedrijfsvoertuigen zijn, maar ook andere vervoerswijzen, zoals het spoor en de binnenvaart, daar waterstof zouden kunnen tanken. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(27) Voertuigen op waterstof moeten kunnen tanken op of dichtbij hun bestemming, die")
    thisalinea.textcontent.append("gewoonlijk in een stedelijk gebied ligt. Om ervoor te zorgen dat er op zijn minst in de")
    thisalinea.textcontent.append("belangrijkste steden openbaar toegankelijke tankpunten zijn, moeten er")
    thisalinea.textcontent.append("waterstoftankstations komen in alle stedelijke knooppunten zoals gedefinieerd in")
    thisalinea.textcontent.append("Verordening (EU) nr. 1315/201317 van het Europees Parlement en de Raad.")
    thisalinea.textcontent.append("Overheden moeten onderzoeken of die stations in stedelijke knooppunten kunnen")
    thisalinea.textcontent.append("worden voorzien in multimodale goederenterminals, aangezien dat niet alleen typische")
    thisalinea.textcontent.append("bestemmingen zijn voor zware bedrijfsvoertuigen zijn, maar ook andere")
    thisalinea.textcontent.append("vervoerswijzen, zoals het spoor en de binnenvaart, daar waterstof zouden kunnen")
    thisalinea.textcontent.append("tanken.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(28) In een vroeg stadium van ..."
    thisalinea.nativeID = 77
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 27
    thisalinea.summary = "(28) In een vroeg stadium van marktintroductie bestaat er nog steeds een zekere mate van onzekerheid over het soort voertuigen dat op de markt zal komen en over het soort technologieën dat op grote schaal zal worden gebruikt. Zoals uiteengezet in de mededeling van de Commissie “Een waterstofstrategie voor een klimaatneutraal Europa”18 werd het segment van de zware bedrijfsvoertuigen aangemerkt als het meest kansrijke segment voor een snelle grootschalige uitrol van waterstofvoertuigen. Daarom moet de infrastructuur voor het tanken van waterstof voorlopig op dat segment focussen en moeten lichte voertuigen ook gebruik kunnen maken van openbaar toegankelijke waterstoftankstations. Met het "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(28) In een vroeg stadium van marktintroductie bestaat er nog steeds een zekere mate van")
    thisalinea.textcontent.append("onzekerheid over het soort voertuigen dat op de markt zal komen en over het soort")
    thisalinea.textcontent.append("technologieën dat op grote schaal zal worden gebruikt. Zoals uiteengezet in de")
    thisalinea.textcontent.append("mededeling van de Commissie “Een waterstofstrategie voor een klimaatneutraal")
    thisalinea.textcontent.append("Europa”18 werd het segment van de zware bedrijfsvoertuigen aangemerkt als het meest")
    thisalinea.textcontent.append("kansrijke segment voor een snelle grootschalige uitrol van waterstofvoertuigen.")
    thisalinea.textcontent.append("Daarom moet de infrastructuur voor het tanken van waterstof voorlopig op dat")
    thisalinea.textcontent.append("segment focussen en moeten lichte voertuigen ook gebruik kunnen maken van")
    thisalinea.textcontent.append("openbaar toegankelijke waterstoftankstations. Met het oog op de interoperabiliteit")
    thisalinea.textcontent.append("moeten alle openbaar toegankelijke waterstofstations een druk van ten minste 700 bar")
    thisalinea.textcontent.append("leveren. Bij de uitrol van infrastructuur moet ook rekening worden gehouden met de")
    thisalinea.textcontent.append("opkomst van nieuwe technologieën, zoals vloeibare waterstof, die zware")
    thisalinea.textcontent.append("bedrijfsvoertuigen een grotere autonomie bieden en die de voorkeur genieten van")
    thisalinea.textcontent.append("sommige voertuigfabrikanten. Daartoe moet bij een minimumaantal")
    thisalinea.textcontent.append("waterstoftankstations vloeibaar waterstof kunnen worden getankt met een druk van")
    thisalinea.textcontent.append("700 bar.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(29) De Unie beschikt over een ..."
    thisalinea.nativeID = 78
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 28
    thisalinea.summary = "(29) De Unie beschikt over een aantal LNG-tankpunten, die een ruggengraat vormen voor het verkeer van zware bedrijfsvoertuigen op LNG. Het TEN-T-kernnetwerk moet de basis blijven voor de uitrol van LNG-infrastructuur en geleidelijk aan voor bio-LNG, aangezien het de belangrijkste verkeersstromen verwerkt en grensoverschrijdende verbindingen in de hele Unie mogelijk maakt. In Richtlijn 2014/94/EU werd aanbevolen dat dergelijke tankpunten om de 400 km op het TEN-T-kernnetwerk zouden worden geïnstalleerd, maar het netwerk vertoont nog enkele kleine lacunes om die doelstelling te bereiken. De lidstaten moeten die doelstelling uiterlijk in 2025 bereiken en de resterende leemten opvullen, waarna de doelstelling vervalt. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(29) De Unie beschikt over een aantal LNG-tankpunten, die een ruggengraat vormen voor")
    thisalinea.textcontent.append("het verkeer van zware bedrijfsvoertuigen op LNG. Het TEN-T-kernnetwerk moet de")
    thisalinea.textcontent.append("basis blijven voor de uitrol van LNG-infrastructuur en geleidelijk aan voor bio-LNG,")
    thisalinea.textcontent.append("aangezien het de belangrijkste verkeersstromen verwerkt en grensoverschrijdende")
    thisalinea.textcontent.append("verbindingen in de hele Unie mogelijk maakt. In Richtlijn 2014/94/EU werd")
    thisalinea.textcontent.append("aanbevolen dat dergelijke tankpunten om de 400 km op het TEN-T-kernnetwerk")
    thisalinea.textcontent.append("zouden worden geïnstalleerd, maar het netwerk vertoont nog enkele kleine lacunes om")
    thisalinea.textcontent.append("die doelstelling te bereiken. De lidstaten moeten die doelstelling uiterlijk in 2025")
    thisalinea.textcontent.append("bereiken en de resterende leemten opvullen, waarna de doelstelling vervalt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(30) Gebruikers van voertuigen op alternatieve ..."
    thisalinea.nativeID = 79
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 29
    thisalinea.summary = "(30) Gebruikers van voertuigen op alternatieve brandstoffen moeten vlot en gemakkelijk kunnen betalen bij alle openbaar toegankelijke laad- en tankpunten, zonder de verplichting een contract te sluiten met de exploitant van het laad- of tankpunt of een aanbieder van mobiliteitsdiensten. Daarom moeten alle openbaar toegankelijke laad- en tankpunten op ad-hocbasis de in de Unie gangbare betaalmiddelen aanvaarden, met name elektronische betalingen via terminals en apparatuur voor betalingsdiensten. Die ad-hocbetalingsmethode moet altijd beschikbaar zijn voor consumenten, zelfs als bij het laad- of tankpunt op basis van een contract kan worden betaald. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(30) Gebruikers van voertuigen op alternatieve brandstoffen moeten vlot en gemakkelijk")
    thisalinea.textcontent.append("kunnen betalen bij alle openbaar toegankelijke laad- en tankpunten, zonder de")
    thisalinea.textcontent.append("verplichting een contract te sluiten met de exploitant van het laad- of tankpunt of een")
    thisalinea.textcontent.append("aanbieder van mobiliteitsdiensten. Daarom moeten alle openbaar toegankelijke laad-")
    thisalinea.textcontent.append("en tankpunten op ad-hocbasis de in de Unie gangbare betaalmiddelen aanvaarden, met")
    thisalinea.textcontent.append("name elektronische betalingen via terminals en apparatuur voor betalingsdiensten. Die")
    thisalinea.textcontent.append("ad-hocbetalingsmethode moet altijd beschikbaar zijn voor consumenten, zelfs als bij")
    thisalinea.textcontent.append("het laad- of tankpunt op basis van een contract kan worden betaald.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(31) De vervoersinfrastructuur moet alle gebruikers ..."
    thisalinea.nativeID = 80
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 30
    thisalinea.summary = "(31) De vervoersinfrastructuur moet alle gebruikers naadloze mobiliteit en toegankelijkheid bieden, ook aan personen met een handicap en ouderen. In beginsel moeten de plaats van alle laad- en tankstations en die stations zelf zodanig worden ontworpen dat zij door zoveel mogelijk mensen kunnen worden gebruikt, ook door ouderen, personen met beperkte mobiliteit en personen met een handicap. Er moet bijvoorbeeld voldoende ruimte worden voorzien rond de parkeerplaats, het laadstation moet zonder drempel bereikbaar zijn, de knoppen en het scherm van het laadstation moeten op een passende hoogte staan en de laad- en tankkabels mogen niet te zwaar zijn zodat ze "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(31) De vervoersinfrastructuur moet alle gebruikers naadloze mobiliteit en toegankelijkheid")
    thisalinea.textcontent.append("bieden, ook aan personen met een handicap en ouderen. In beginsel moeten de plaats")
    thisalinea.textcontent.append("van alle laad- en tankstations en die stations zelf zodanig worden ontworpen dat zij")
    thisalinea.textcontent.append("door zoveel mogelijk mensen kunnen worden gebruikt, ook door ouderen, personen")
    thisalinea.textcontent.append("met beperkte mobiliteit en personen met een handicap. Er moet bijvoorbeeld")
    thisalinea.textcontent.append("voldoende ruimte worden voorzien rond de parkeerplaats, het laadstation moet zonder")
    thisalinea.textcontent.append("drempel bereikbaar zijn, de knoppen en het scherm van het laadstation moeten op een")
    thisalinea.textcontent.append("passende hoogte staan en de laad- en tankkabels mogen niet te zwaar zijn zodat ze ook")
    thisalinea.textcontent.append("hanteerbaar zijn voor mensen met beperkte spierkracht. Bovendien moet de")
    thisalinea.textcontent.append("gebruikersinterface van de laadpunten toegankelijk zijn. In die zin moeten de")
    thisalinea.textcontent.append("toegankelijkheidseisen van de bijlagen I en III bij Richtlijn 2019/88219 van toepassing")
    thisalinea.textcontent.append("zijn op laad- en tankinfrastructuur.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(32) Walstroomvoorzieningen kunnen schone stroom leveren ..."
    thisalinea.nativeID = 81
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 31
    thisalinea.summary = "(32) Walstroomvoorzieningen kunnen schone stroom leveren aan de zee- en binnenvaart en helpen om de milieu-impact van zee- en binnenschepen te beperken. In het kader van FuelEU Zeevaart worden exploitanten van container- en passagiersschepen verplicht de emissies op de ligplaats te verminderen. Bindende uitrolstreefcijfers moeten ervoor zorgen dat in de zeehavens van het kernnetwerk en uitgebreid netwerk van het TEN-T voldoende walstroomvoorzieningen komen om de sector in staat te stellen zijn verplichtingen na te leven. De toepassing van deze doelstellingen op alle TEN-T- zeehavens moet zorgen voor een gelijk speelveld tussen havens. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(32) Walstroomvoorzieningen kunnen schone stroom leveren aan de zee- en binnenvaart en")
    thisalinea.textcontent.append("helpen om de milieu-impact van zee- en binnenschepen te beperken. In het kader van")
    thisalinea.textcontent.append("FuelEU Zeevaart worden exploitanten van container- en passagiersschepen verplicht")
    thisalinea.textcontent.append("de emissies op de ligplaats te verminderen. Bindende uitrolstreefcijfers moeten ervoor")
    thisalinea.textcontent.append("zorgen dat in de zeehavens van het kernnetwerk en uitgebreid netwerk van het TEN-T")
    thisalinea.textcontent.append("voldoende walstroomvoorzieningen komen om de sector in staat te stellen zijn")
    thisalinea.textcontent.append("verplichtingen na te leven. De toepassing van deze doelstellingen op alle TEN-T-")
    thisalinea.textcontent.append("zeehavens moet zorgen voor een gelijk speelveld tussen havens.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(33) Containerschepen en passagiersschepen, de twee ..."
    thisalinea.nativeID = 82
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 32
    thisalinea.summary = "(33) Containerschepen en passagiersschepen, de twee categorieën schepen die op de ligplaats de meeste emissies per schip veroorzaken, moeten bij voorrang van walstroom worden voorzien. Om rekening te houden met de kenmerken van de elektriciteitsbehoeften van verschillende passagiersschepen op de ligplaats en met de operationele kenmerken van de haven, moet voor passagiersschepen een onderscheid worden gemaakt tussen de eisen voor enerzijds ro-ro-passagiersschepen en hogesnelheidspassagiersschepen en anderzijds de overige types passagiersschepen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(33) Containerschepen en passagiersschepen, de twee categorieën schepen die op de")
    thisalinea.textcontent.append("ligplaats de meeste emissies per schip veroorzaken, moeten bij voorrang van")
    thisalinea.textcontent.append("walstroom worden voorzien. Om rekening te houden met de kenmerken van de")
    thisalinea.textcontent.append("elektriciteitsbehoeften van verschillende passagiersschepen op de ligplaats en met de")
    thisalinea.textcontent.append("operationele kenmerken van de haven, moet voor passagiersschepen een onderscheid")
    thisalinea.textcontent.append("worden gemaakt tussen de eisen voor enerzijds ro-ro-passagiersschepen en")
    thisalinea.textcontent.append("hogesnelheidspassagiersschepen en anderzijds de overige types passagiersschepen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(34) In de streefcijfers moet rekening ..."
    thisalinea.nativeID = 83
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 33
    thisalinea.summary = "(34) In de streefcijfers moet rekening worden gehouden met de soorten schepen die van stroom worden voorzien en met hun respectieve verkeersvolumes. Zeehavens met een bescheiden verkeersvolume van bepaalde scheepscategorieën moeten op basis van een minimumverkeersvolume worden vrijgesteld van de verplichte eisen voor de overeenkomstige categorieën, om te voorkomen dat capaciteit wordt geïnstalleerd die daarna onderbenut blijft. Evenzo mogen de verplichte streefcijfers niet gericht zijn op de maximale vraag, maar op een voldoende hoog volume, om een onderbenutting van de capaciteit te voorkomen en rekening te houden met de operationele kenmerken van de haven. Zeevervoer is belangrijk voor de cohesie "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(34) In de streefcijfers moet rekening worden gehouden met de soorten schepen die van")
    thisalinea.textcontent.append("stroom worden voorzien en met hun respectieve verkeersvolumes. Zeehavens met een")
    thisalinea.textcontent.append("bescheiden verkeersvolume van bepaalde scheepscategorieën moeten op basis van een")
    thisalinea.textcontent.append("minimumverkeersvolume worden vrijgesteld van de verplichte eisen voor de")
    thisalinea.textcontent.append("overeenkomstige categorieën, om te voorkomen dat capaciteit wordt geïnstalleerd die")
    thisalinea.textcontent.append("daarna onderbenut blijft. Evenzo mogen de verplichte streefcijfers niet gericht zijn op")
    thisalinea.textcontent.append("de maximale vraag, maar op een voldoende hoog volume, om een onderbenutting van")
    thisalinea.textcontent.append("de capaciteit te voorkomen en rekening te houden met de operationele kenmerken van")
    thisalinea.textcontent.append("de haven. Zeevervoer is belangrijk voor de cohesie en de economische ontwikkeling")
    thisalinea.textcontent.append("van eilanden in de Unie. De energieproductiecapaciteit op die eilanden is niet altijd")
    thisalinea.textcontent.append("toereikend om tegemoet te komen aan de vraag naar energie die met de levering van")
    thisalinea.textcontent.append("walstroom gepaard gaat. In dergelijke gevallen moeten eilanden van die eis worden")
    thisalinea.textcontent.append("vrijgesteld, tenzij en totdat een elektrische verbinding met het vasteland is gerealiseerd")
    thisalinea.textcontent.append("of tot er ter plaatse voldoende productiecapaciteit uit schone energiebronnen")
    thisalinea.textcontent.append("beschikbaar is.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(35) Tegen 2025 moet in de ..."
    thisalinea.nativeID = 84
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 34
    thisalinea.summary = "(35) Tegen 2025 moet in de zeehavens een kernnetwerk van LNG-tankpunten beschikbaar zijn. LNG-tankpunten bestaan uit terminals, tanks en mobiele containers voor LNG, en LNG-bunkerstations en -bunkerschepen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(35) Tegen 2025 moet in de zeehavens een kernnetwerk van LNG-tankpunten beschikbaar")
    thisalinea.textcontent.append("zijn. LNG-tankpunten bestaan uit terminals, tanks en mobiele containers voor LNG, en")
    thisalinea.textcontent.append("LNG-bunkerstations en -bunkerschepen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(36) De elektriciteitsvoorziening aan stilstaande luchtvaartuigen ..."
    thisalinea.nativeID = 85
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 35
    thisalinea.summary = "(36) De elektriciteitsvoorziening aan stilstaande luchtvaartuigen op luchthavens moet het verbruik van vloeibare brandstof vervangen door een schonere energiebron voor luchtvaartuigen (gebruik van hulpaggregaten) of grondgroepen (GPU’s). Dit moet het lawaai en de uitstoot van verontreinigende stoffen verminderen, de luchtkwaliteit verbeteren en de impact op de klimaatverandering beperken. Daarom moet voor alle commerciële vluchtuitvoeringen gebruik kunnen worden gemaakt van externe stroomvoorzieningen als het toestel op een TEN-T-luchthaven geparkeerd is bij de gates of op een buitenstandplaats. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(36) De elektriciteitsvoorziening aan stilstaande luchtvaartuigen op luchthavens moet het")
    thisalinea.textcontent.append("verbruik van vloeibare brandstof vervangen door een schonere energiebron voor")
    thisalinea.textcontent.append("luchtvaartuigen (gebruik van hulpaggregaten) of grondgroepen (GPU’s). Dit moet het")
    thisalinea.textcontent.append("lawaai en de uitstoot van verontreinigende stoffen verminderen, de luchtkwaliteit")
    thisalinea.textcontent.append("verbeteren en de impact op de klimaatverandering beperken. Daarom moet voor alle")
    thisalinea.textcontent.append("commerciële vluchtuitvoeringen gebruik kunnen worden gemaakt van externe")
    thisalinea.textcontent.append("stroomvoorzieningen als het toestel op een TEN-T-luchthaven geparkeerd is bij de")
    thisalinea.textcontent.append("gates of op een buitenstandplaats.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(37) Overeenkomstig artikel 3 van Richtlijn ..."
    thisalinea.nativeID = 86
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 36
    thisalinea.summary = "(37) Overeenkomstig artikel 3 van Richtlijn 2014/94/EU hebben de lidstaten nationale beleidskaders vastgesteld met hun plannen en doelstellingen om te waarborgen dat die doelstellingen worden bereikt. Zowel uit de beoordeling van het nationale beleidskader als uit de evaluatie van Richtlijn 2014/94/EU is gebleken dat er behoefte is aan meer ambitie en een beter gecoördineerde aanpak over de lidstaatgrenzen heen om de verwachte groei van het gebruik van voertuigen op alternatieve brandstoffen, met name elektrische voertuigen, op te vangen. Bovendien zullen voor alle vervoerswijzen alternatieven voor fossiele brandstoffen nodig zijn om de ambities van de Europese Green Deal te verwezenlijken. De "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(37) Overeenkomstig artikel 3 van Richtlijn 2014/94/EU hebben de lidstaten nationale")
    thisalinea.textcontent.append("beleidskaders vastgesteld met hun plannen en doelstellingen om te waarborgen dat die")
    thisalinea.textcontent.append("doelstellingen worden bereikt. Zowel uit de beoordeling van het nationale")
    thisalinea.textcontent.append("beleidskader als uit de evaluatie van Richtlijn 2014/94/EU is gebleken dat er behoefte")
    thisalinea.textcontent.append("is aan meer ambitie en een beter gecoördineerde aanpak over de lidstaatgrenzen heen")
    thisalinea.textcontent.append("om de verwachte groei van het gebruik van voertuigen op alternatieve brandstoffen,")
    thisalinea.textcontent.append("met name elektrische voertuigen, op te vangen. Bovendien zullen voor alle")
    thisalinea.textcontent.append("vervoerswijzen alternatieven voor fossiele brandstoffen nodig zijn om de ambities van")
    thisalinea.textcontent.append("de Europese Green Deal te verwezenlijken. De bestaande nationale beleidskaders")
    thisalinea.textcontent.append("moeten worden herzien om duidelijk aan te geven hoe de lidstaten zullen voldoen aan")
    thisalinea.textcontent.append("de veel grotere behoefte aan openbaar toegankelijke laad- en tankinfrastructuur, zoals")
    thisalinea.textcontent.append("uitgedrukt in de bindende streefcijfers. De herziene kaders moeten in gelijke mate")
    thisalinea.textcontent.append("betrekking hebben op alle vervoerswijzen, m.i.v. de vervoerswijzen waarvoor geen")
    thisalinea.textcontent.append("bindende uitrolstreefcijfers zijn vastgesteld.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(38) In de herziene nationale beleidskaders ..."
    thisalinea.nativeID = 87
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 37
    thisalinea.summary = "(38) In de herziene nationale beleidskaders van de lidstaten moeten ondersteunende acties worden opgenomen om de markt voor alternatieve brandstoffen te ontwikkelen, met inbegrip van de uitrol van de nodige infrastructuur, in nauwe samenwerking met de regionale en lokale autoriteiten en de betrokken sectoren, en met inachtneming van de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(38) In de herziene nationale beleidskaders van de lidstaten moeten ondersteunende acties")
    thisalinea.textcontent.append("worden opgenomen om de markt voor alternatieve brandstoffen te ontwikkelen, met")
    thisalinea.textcontent.append("inbegrip van de uitrol van de nodige infrastructuur, in nauwe samenwerking met de")
    thisalinea.textcontent.append("regionale en lokale autoriteiten en de betrokken sectoren, en met inachtneming van de")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(39) De Commissie moet de ontwikkeling ..."
    thisalinea.nativeID = 88
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 38
    thisalinea.summary = "(39) De Commissie moet de ontwikkeling en implementatie van de herziene nationale beleidskaders van de lidstaten faciliteren door middel van de uitwisseling van informatie en beste praktijken tussen de lidstaten. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(39) De Commissie moet de ontwikkeling en implementatie van de herziene nationale")
    thisalinea.textcontent.append("beleidskaders van de lidstaten faciliteren door middel van de uitwisseling van")
    thisalinea.textcontent.append("informatie en beste praktijken tussen de lidstaten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(40) Om alternatieve brandstoffen te promoten ..."
    thisalinea.nativeID = 89
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 39
    thisalinea.summary = "(40) Om alternatieve brandstoffen te promoten en de relevante infrastructuur te ontwikkelen, moeten de nationale beleidskaders bestaan uit gedetailleerde strategieën om het gebruik die brandstoffen te bevorderen in sectoren die moeilijk koolstofvrij kunnen worden gemaakt, zoals de luchtvaart, de zee- en binnenvaart en het spoorvervoer over lijnen die niet kunnen worden geëlektrificeerd. De lidstaten moeten met name duidelijke strategieën ontwikkelen om de binnenvaart over de TEN-T- waterwegen koolstofvrij te maken, in nauwe samenwerking met de andere betrokken lidstaten. Er moeten ook langetermijnstrategieën voor decarbonisatie worden ontwikkeld voor TEN-T-havens en -luchthavens, met bijzondere aandacht voor de uitrol van infrastructuur voor emissiearme "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(40) Om alternatieve brandstoffen te promoten en de relevante infrastructuur te")
    thisalinea.textcontent.append("ontwikkelen, moeten de nationale beleidskaders bestaan uit gedetailleerde strategieën")
    thisalinea.textcontent.append("om het gebruik die brandstoffen te bevorderen in sectoren die moeilijk koolstofvrij")
    thisalinea.textcontent.append("kunnen worden gemaakt, zoals de luchtvaart, de zee- en binnenvaart en het")
    thisalinea.textcontent.append("spoorvervoer over lijnen die niet kunnen worden geëlektrificeerd. De lidstaten moeten")
    thisalinea.textcontent.append("met name duidelijke strategieën ontwikkelen om de binnenvaart over de TEN-T-")
    thisalinea.textcontent.append("waterwegen koolstofvrij te maken, in nauwe samenwerking met de andere betrokken")
    thisalinea.textcontent.append("lidstaten. Er moeten ook langetermijnstrategieën voor decarbonisatie worden")
    thisalinea.textcontent.append("ontwikkeld voor TEN-T-havens en -luchthavens, met bijzondere aandacht voor de")
    thisalinea.textcontent.append("uitrol van infrastructuur voor emissiearme en emissievrije schepen en luchtvaartuigen")
    thisalinea.textcontent.append("en voor spoorlijnen die niet worden geëlektrificeerd. Op basis van die strategieën moet")
    thisalinea.textcontent.append("de Commissie deze verordening herzien teneinde voor die sectoren meer bindende")
    thisalinea.textcontent.append("doelstellingen vast te stellen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(41) De lidstaten moeten gebruikmaken van ..."
    thisalinea.nativeID = 90
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 40
    thisalinea.summary = "(41) De lidstaten moeten gebruikmaken van een breed scala aan regelgevende en niet- regelgevende stimulansen en maatregelen om de bindende streefcijfers te halen en hun nationale beleidskaders uit te voeren; dat moet gebeuren in nauwe samenwerking met actoren uit de particuliere sector, die een sleutelrol moeten spelen bij de ondersteuning van de ontwikkeling van infrastructuur voor alternatieve brandstoffen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(41) De lidstaten moeten gebruikmaken van een breed scala aan regelgevende en niet-")
    thisalinea.textcontent.append("regelgevende stimulansen en maatregelen om de bindende streefcijfers te halen en hun")
    thisalinea.textcontent.append("nationale beleidskaders uit te voeren; dat moet gebeuren in nauwe samenwerking met")
    thisalinea.textcontent.append("actoren uit de particuliere sector, die een sleutelrol moeten spelen bij de ondersteuning")
    thisalinea.textcontent.append("van de ontwikkeling van infrastructuur voor alternatieve brandstoffen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(42) Overeenkomstig Richtlijn 2009/33/EG20 van het ..."
    thisalinea.nativeID = 91
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 41
    thisalinea.summary = "(42) Overeenkomstig Richtlijn 2009/33/EG20 van het Europees Parlement en de Raad zijn nationale minimumstreefcijfers vastgesteld voor overheidsaankopen van schone en emissievrije bussen, d.w.z. schone bussen die alternatieve brandstoffen gebruiken zoals gedefinieerd in artikel 2, punt 3), van deze verordening. Nu steeds meer OV- autoriteiten en -exploitanten overschakelen op schone en emissievrije bussen om die doelstellingen te halen, moeten de lidstaten de gerichte bevordering en ontwikkeling van de noodzakelijke infrastructuur voor bussen als essentieel onderdeel opnemen in hun nationale beleidskaders. Zij moeten passende instrumenten invoeren en in stand houden om ook voor eigen wagenparken de uitrol van laad- en tankinfrastructuur te "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(42) Overeenkomstig Richtlijn 2009/33/EG20 van het Europees Parlement en de Raad zijn")
    thisalinea.textcontent.append("nationale minimumstreefcijfers vastgesteld voor overheidsaankopen van schone en")
    thisalinea.textcontent.append("emissievrije bussen, d.w.z. schone bussen die alternatieve brandstoffen gebruiken")
    thisalinea.textcontent.append("zoals gedefinieerd in artikel 2, punt 3), van deze verordening. Nu steeds meer OV-")
    thisalinea.textcontent.append("autoriteiten en -exploitanten overschakelen op schone en emissievrije bussen om die")
    thisalinea.textcontent.append("doelstellingen te halen, moeten de lidstaten de gerichte bevordering en ontwikkeling")
    thisalinea.textcontent.append("van de noodzakelijke infrastructuur voor bussen als essentieel onderdeel opnemen in")
    thisalinea.textcontent.append("hun nationale beleidskaders. Zij moeten passende instrumenten invoeren en in stand")
    thisalinea.textcontent.append("houden om ook voor eigen wagenparken de uitrol van laad- en tankinfrastructuur te")
    thisalinea.textcontent.append("bevorderen en met name voor schone en emissievrije stads- en streekbussen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(43) In het licht van de ..."
    thisalinea.nativeID = 92
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 42
    thisalinea.summary = "(43) In het licht van de toenemende diversiteit van de soorten brandstof voor motorvoertuigen, in combinatie met de nog steeds groeiende wegmobiliteit van burgers in de hele Unie, moeten voertuiggebruikers op een duidelijke en gemakkelijk te begrijpen manier worden geïnformeerd over de brandstoffen die bij tankstations te koop zijn en over de compatibiliteit van hun voertuigen met de verschillende brandstoffen of laadpunten op de EU-markt. De lidstaten moeten kunnen besluiten deze informatiemaatregelen ook in te voeren ten aanzien van voertuigen die vóór 18 november 2016 op de markt gebracht zijn. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(43) In het licht van de toenemende diversiteit van de soorten brandstof voor")
    thisalinea.textcontent.append("motorvoertuigen, in combinatie met de nog steeds groeiende wegmobiliteit van")
    thisalinea.textcontent.append("burgers in de hele Unie, moeten voertuiggebruikers op een duidelijke en gemakkelijk")
    thisalinea.textcontent.append("te begrijpen manier worden geïnformeerd over de brandstoffen die bij tankstations te")
    thisalinea.textcontent.append("koop zijn en over de compatibiliteit van hun voertuigen met de verschillende")
    thisalinea.textcontent.append("brandstoffen of laadpunten op de EU-markt. De lidstaten moeten kunnen besluiten")
    thisalinea.textcontent.append("deze informatiemaatregelen ook in te voeren ten aanzien van voertuigen die vóór 18")
    thisalinea.textcontent.append("november 2016 op de markt gebracht zijn.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(44) Eenvoudige en gemakkelijk te vergelijken ..."
    thisalinea.nativeID = 93
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 43
    thisalinea.summary = "(44) Eenvoudige en gemakkelijk te vergelijken informatie over de prijzen van verschillende brandstoffen kan voor de voertuiggebruikers van belang zijn om de relatieve kosten van de in de handel verkrijgbare brandstoffen beter te kunnen beoordelen. Daarom moet in alle relevante tankstations ter informatie een vergelijking van eenheidsprijzen van bepaalde alternatieve brandstoffen en conventionele brandstoffen, uitgedrukt als “brandstofprijs per 100 km”, worden getoond. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(44) Eenvoudige en gemakkelijk te vergelijken informatie over de prijzen van verschillende")
    thisalinea.textcontent.append("brandstoffen kan voor de voertuiggebruikers van belang zijn om de relatieve kosten")
    thisalinea.textcontent.append("van de in de handel verkrijgbare brandstoffen beter te kunnen beoordelen. Daarom")
    thisalinea.textcontent.append("moet in alle relevante tankstations ter informatie een vergelijking van eenheidsprijzen")
    thisalinea.textcontent.append("van bepaalde alternatieve brandstoffen en conventionele brandstoffen, uitgedrukt als")
    thisalinea.textcontent.append("“brandstofprijs per 100 km”, worden getoond.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(45) Consumenten moeten voldoende informatie krijgen ..."
    thisalinea.nativeID = 94
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 44
    thisalinea.summary = "(45) Consumenten moeten voldoende informatie krijgen over de geografische ligging, kenmerken en diensten die worden aangeboden bij openbaar toegankelijke laad- en tankpunten voor alternatieve brandstoffen die onder deze verordening vallen. Daarom moeten de lidstaten exploitanten of eigenaars van openbaar toegankelijke laad- en tankpunten verplichten relevante statische en dynamische gegevens beschikbaar te stellen. Er moeten eisen worden vastgesteld met betrekking tot de beschikbaarheid en toegankelijkheid van relevante laad- en tankgegevens, voortbouwend op de resultaten van de programmaondersteunende actie inzake “Gegevensvergaring met betrekking tot laad- en tankpunten voor alternatieve brandstoffen en unieke identificatiecodes voor e- mobiliteitsactoren” (“IDACS”). "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(45) Consumenten moeten voldoende informatie krijgen over de geografische ligging,")
    thisalinea.textcontent.append("kenmerken en diensten die worden aangeboden bij openbaar toegankelijke laad- en")
    thisalinea.textcontent.append("tankpunten voor alternatieve brandstoffen die onder deze verordening vallen. Daarom")
    thisalinea.textcontent.append("moeten de lidstaten exploitanten of eigenaars van openbaar toegankelijke laad- en")
    thisalinea.textcontent.append("tankpunten verplichten relevante statische en dynamische gegevens beschikbaar te")
    thisalinea.textcontent.append("stellen. Er moeten eisen worden vastgesteld met betrekking tot de beschikbaarheid en")
    thisalinea.textcontent.append("toegankelijkheid van relevante laad- en tankgegevens, voortbouwend op de resultaten")
    thisalinea.textcontent.append("van de programmaondersteunende actie inzake “Gegevensvergaring met betrekking tot")
    thisalinea.textcontent.append("laad- en tankpunten voor alternatieve brandstoffen en unieke identificatiecodes voor e-")
    thisalinea.textcontent.append("mobiliteitsactoren” (“IDACS”).")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(46) Gegevens moeten een fundamentele rol ..."
    thisalinea.nativeID = 95
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 45
    thisalinea.summary = "(46) Gegevens moeten een fundamentele rol spelen bij de goede werking van de laad- en tankinfrastructuur. Het formaat, de frequentie en de kwaliteit waarin de gegevens beschikbaar en toegankelijk moeten worden gemaakt, moeten bepalend zijn voor de algemene kwaliteit van een infrastructuurecosysteem voor alternatieve brandstoffen dat aan de behoeften van de gebruikers beantwoordt. Bovendien moeten die gegevens in alle lidstaten op coherente wijze toegankelijk zijn. Daarom moeten de gegevens worden verstrekt overeenkomstig de in Richtlijn 2010/40/EU21 van het Europees Parlement en de Raad voor nationale toegangspunten (NAP's) vastgestelde regels. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(46) Gegevens moeten een fundamentele rol spelen bij de goede werking van de laad- en")
    thisalinea.textcontent.append("tankinfrastructuur. Het formaat, de frequentie en de kwaliteit waarin de gegevens")
    thisalinea.textcontent.append("beschikbaar en toegankelijk moeten worden gemaakt, moeten bepalend zijn voor de")
    thisalinea.textcontent.append("algemene kwaliteit van een infrastructuurecosysteem voor alternatieve brandstoffen")
    thisalinea.textcontent.append("dat aan de behoeften van de gebruikers beantwoordt. Bovendien moeten die gegevens")
    thisalinea.textcontent.append("in alle lidstaten op coherente wijze toegankelijk zijn. Daarom moeten de gegevens")
    thisalinea.textcontent.append("worden verstrekt overeenkomstig de in Richtlijn 2010/40/EU21 van het Europees")
    thisalinea.textcontent.append("Parlement en de Raad voor nationale toegangspunten (NAP's) vastgestelde regels.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(47) Het is van cruciaal belang ..."
    thisalinea.nativeID = 96
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 46
    thisalinea.summary = "(47) Het is van cruciaal belang dat alle actoren in het ecosysteem voor elektrische mobiliteit vlot met digitale middelen kunnen interageren zodat ze de eindgebruiker een optimale dienstverlening kunnen bieden. Dit vereist unieke identificatiecodes van de relevante actoren in de waardeketen. Daartoe moeten de lidstaten een organisatie voor de identificatie van registraties (IDRO) aanwijzen, die belast wordt met de afgifte en het beheer van unieke identificatiecodes (ID's) om, ten minste, exploitanten van laadpunten en aanbieders van mobiliteitsdiensten te identificeren. De IDRO moet informatie verzamelen over e-mobiliteitsidentificatiecodes die reeds worden gebruikt in de betrokken lidstaat; waar nodig, nieuwe e-mobiliteitscodes toekennen aan "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(47) Het is van cruciaal belang dat alle actoren in het ecosysteem voor elektrische")
    thisalinea.textcontent.append("mobiliteit vlot met digitale middelen kunnen interageren zodat ze de eindgebruiker een")
    thisalinea.textcontent.append("optimale dienstverlening kunnen bieden. Dit vereist unieke identificatiecodes van de")
    thisalinea.textcontent.append("relevante actoren in de waardeketen. Daartoe moeten de lidstaten een organisatie voor")
    thisalinea.textcontent.append("de identificatie van registraties (IDRO) aanwijzen, die belast wordt met de afgifte en")
    thisalinea.textcontent.append("het beheer van unieke identificatiecodes (ID's) om, ten minste, exploitanten van")
    thisalinea.textcontent.append("laadpunten en aanbieders van mobiliteitsdiensten te identificeren. De IDRO moet")
    thisalinea.textcontent.append("informatie verzamelen over e-mobiliteitsidentificatiecodes die reeds worden gebruikt")
    thisalinea.textcontent.append("in de betrokken lidstaat; waar nodig, nieuwe e-mobiliteitscodes toekennen aan")
    thisalinea.textcontent.append("exploitanten van laadpunten en aanbieders van mobiliteitsdiensten conform een voor")
    thisalinea.textcontent.append("de hele Unie vastgestelde gemeenschappelijke logica voor de formattering van")
    thisalinea.textcontent.append("elektronische mobiliteitsidentificatiecodes; en ervoor zorgen dat die e-mobiliteitscodes")
    thisalinea.textcontent.append("kunnen worden uitgewisseld en geverifieerd via een mogelijk toekomstig")
    thisalinea.textcontent.append("gemeenschappelijk register van identificatiegegevens (IDRR). De Commissie moet")
    thisalinea.textcontent.append("technische richtsnoeren opstellen voor de oprichting van een dergelijke organisatie,")
    thisalinea.textcontent.append("voortbouwend op de programmaondersteunende actie inzake “Gegevensvergaring met")
    thisalinea.textcontent.append("betrekking tot laad- en tankpunten voor alternatieve brandstoffen en unieke")
    thisalinea.textcontent.append("identificatiecodes voor e-mobiliteitsactoren” (IDACS).")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(48) Om de toegang tot de ..."
    thisalinea.nativeID = 97
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 47
    thisalinea.summary = "(48) Om de toegang tot de markt van alternatieve brandstoffen te vergemakkelijken en te consolideren, moeten voor de zee- en binnenvaart nieuwe normen worden vastgesteld met betrekking tot de elektriciteitsvoorziening en het bunkeren van waterstof, methanol en ammoniak, naast normen voor de communicatie tussen schepen en infrastructuur. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(48) Om de toegang tot de markt van alternatieve brandstoffen te vergemakkelijken en te")
    thisalinea.textcontent.append("consolideren, moeten voor de zee- en binnenvaart nieuwe normen worden vastgesteld")
    thisalinea.textcontent.append("met betrekking tot de elektriciteitsvoorziening en het bunkeren van waterstof,")
    thisalinea.textcontent.append("methanol en ammoniak, naast normen voor de communicatie tussen schepen en")
    thisalinea.textcontent.append("infrastructuur.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(49) De Internationale Maritieme Organisatie (IMO) ..."
    thisalinea.nativeID = 98
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 48
    thisalinea.summary = "(49) De Internationale Maritieme Organisatie (IMO) werkt aan uniforme en internationaal erkende veiligheids- en milieunormen voor vervoer over zee. Conflicten met internationale normen moeten worden voorkomen omdat vervoer over zee van nature een mondiale dimensie heeft. Daarom moet de Europese Unie ervoor zorgen dat technische specificaties voor vervoer over zee die op grond van deze verordening worden vastgesteld conform zijn met de internationale regels van de IMO. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(49) De Internationale Maritieme Organisatie (IMO) werkt aan uniforme en internationaal")
    thisalinea.textcontent.append("erkende veiligheids- en milieunormen voor vervoer over zee. Conflicten met")
    thisalinea.textcontent.append("internationale normen moeten worden voorkomen omdat vervoer over zee van nature")
    thisalinea.textcontent.append("een mondiale dimensie heeft. Daarom moet de Europese Unie ervoor zorgen dat")
    thisalinea.textcontent.append("technische specificaties voor vervoer over zee die op grond van deze verordening")
    thisalinea.textcontent.append("worden vastgesteld conform zijn met de internationale regels van de IMO.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(50) De technische specificaties voor de ..."
    thisalinea.nativeID = 99
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 49
    thisalinea.summary = "(50) De technische specificaties voor de interoperabiliteit van laad- en tankpunten moeten worden vastgesteld aan de hand van Europese of internationale normen. De Europese normalisatieorganisaties (ENO’s) moeten Europese normen vaststellen overeenkomstig artikel 10 van Verordening (EU) nr. 1025/201222 van het Europees Parlement en de Raad. Die normen moeten gebaseerd zijn op bestaande internationale normen of lopende internationale normalisatiewerkzaamheden, indien van toepassing. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(50) De technische specificaties voor de interoperabiliteit van laad- en tankpunten moeten")
    thisalinea.textcontent.append("worden vastgesteld aan de hand van Europese of internationale normen. De Europese")
    thisalinea.textcontent.append("normalisatieorganisaties (ENO’s) moeten Europese normen vaststellen")
    thisalinea.textcontent.append("overeenkomstig artikel 10 van Verordening (EU) nr. 1025/201222 van het Europees")
    thisalinea.textcontent.append("Parlement en de Raad. Die normen moeten gebaseerd zijn op bestaande internationale")
    thisalinea.textcontent.append("normen of lopende internationale normalisatiewerkzaamheden, indien van toepassing.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(51) De in bijlage II bij ..."
    thisalinea.nativeID = 100
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 50
    thisalinea.summary = "(51) De in bijlage II bij Richtlijn 2014/94/EU van het Europees Parlement en de Raad gespecificeerde technische specificaties moeten van toepassing blijven zoals gespecificeerd in die richtlijn. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(51) De in bijlage II bij Richtlijn 2014/94/EU van het Europees Parlement en de Raad")
    thisalinea.textcontent.append("gespecificeerde technische specificaties moeten van toepassing blijven zoals")
    thisalinea.textcontent.append("gespecificeerd in die richtlijn.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(52) Bij de toepassing van deze ..."
    thisalinea.nativeID = 101
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 51
    thisalinea.summary = "(52) Bij de toepassing van deze verordening moet de Commissie relevante deskundigengroepen raadplegen, met name het Forum voor duurzaam vervoer (STF) en het Europees Forum voor duurzame scheepvaart (ESSF). Deze raadpleging van deskundigen is uitermate belangrijk als de Commissie voornemens is gedelegeerde of uitvoeringshandelingen uit hoofde van deze verordening vast te stellen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(52) Bij de toepassing van deze verordening moet de Commissie relevante")
    thisalinea.textcontent.append("deskundigengroepen raadplegen, met name het Forum voor duurzaam vervoer (STF)")
    thisalinea.textcontent.append("en het Europees Forum voor duurzame scheepvaart (ESSF). Deze raadpleging van")
    thisalinea.textcontent.append("deskundigen is uitermate belangrijk als de Commissie voornemens is gedelegeerde of")
    thisalinea.textcontent.append("uitvoeringshandelingen uit hoofde van deze verordening vast te stellen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(53) De ontwikkelingen op het gebied ..."
    thisalinea.nativeID = 102
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 52
    thisalinea.summary = "(53) De ontwikkelingen op het gebied van infrastructuur voor alternatieve brandstoffen gaan snel. Het ontbreken van gemeenschappelijke technische specificaties vormt een belemmering voor de totstandbrenging van een interne markt voor infrastructuur voor alternatieve brandstoffen. Daarom moet aan de Commissie de bevoegdheid worden verleend om overeenkomstig artikel 290 VWEU technische specificaties vast te stellen met betrekking tot gebieden waarvoor nog geen technische specificaties bestaan maar wel nodig zijn. Het gaat onder meer om communicatie tussen elektrische voertuigen en de laadpunten, communicatie tussen laadpunten en het managementsysteem voor de laadsoftware (back-end); communicatie in verband met roaming door elektrische voertuigen en communicatie met "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(53) De ontwikkelingen op het gebied van infrastructuur voor alternatieve brandstoffen")
    thisalinea.textcontent.append("gaan snel. Het ontbreken van gemeenschappelijke technische specificaties vormt een")
    thisalinea.textcontent.append("belemmering voor de totstandbrenging van een interne markt voor infrastructuur voor")
    thisalinea.textcontent.append("alternatieve brandstoffen. Daarom moet aan de Commissie de bevoegdheid worden")
    thisalinea.textcontent.append("verleend om overeenkomstig artikel 290 VWEU technische specificaties vast te stellen")
    thisalinea.textcontent.append("met betrekking tot gebieden waarvoor nog geen technische specificaties bestaan maar")
    thisalinea.textcontent.append("wel nodig zijn. Het gaat onder meer om communicatie tussen elektrische voertuigen")
    thisalinea.textcontent.append("en de laadpunten, communicatie tussen laadpunten en het managementsysteem voor de")
    thisalinea.textcontent.append("laadsoftware (back-end); communicatie in verband met roaming door elektrische")
    thisalinea.textcontent.append("voertuigen en communicatie met het elektriciteitsnet. Voorts moet een passend")
    thisalinea.textcontent.append("governancekader worden gedefinieerd en moeten de rollen worden beschreven van de")
    thisalinea.textcontent.append("verschillende actoren die bij het ecosysteem voor communicatie tussen voertuigen en")
    thisalinea.textcontent.append("netten zijn betrokken. Bovendien moet rekening worden gehouden met opkomende")
    thisalinea.textcontent.append("technologische ontwikkelingen, zoals elektrische wegsystemen (ERS). Wat de")
    thisalinea.textcontent.append("verstrekking van gegevens betreft, moet worden voorzien in aanvullende soorten")
    thisalinea.textcontent.append("gegevens en technische specificaties met betrekking tot de frequentie waarmee en het")
    thisalinea.textcontent.append("formaat en de kwaliteit waarin die gegevens beschikbaar en toegankelijk moeten")
    thisalinea.textcontent.append("worden gemaakt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(54) De markt voor alternatieve brandstoffen ..."
    thisalinea.nativeID = 103
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 53
    thisalinea.summary = "(54) De markt voor alternatieve brandstoffen en met name voor emissievrije brandstoffen bevindt zich nog in een pril ontwikkelingsstadium en de technologie evolueert snel. Dit zal waarschijnlijk van invloed zijn op de vraag naar alternatieve brandstoffen en bijgevolg op de infrastructuur voor alternatieve brandstoffen voor alle vervoerswijzen. Daarom moet de Commissie deze verordening uiterlijk eind 2026 herzien, met name wat betreft de streefcijfers voor elektrische laadpunten voor zware bedrijfsvoertuigen en de streefcijfers voor infrastructuur voor alternatieve brandstoffen voor emissievrije schepen en luchtvaartuigen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(54) De markt voor alternatieve brandstoffen en met name voor emissievrije brandstoffen")
    thisalinea.textcontent.append("bevindt zich nog in een pril ontwikkelingsstadium en de technologie evolueert snel.")
    thisalinea.textcontent.append("Dit zal waarschijnlijk van invloed zijn op de vraag naar alternatieve brandstoffen en")
    thisalinea.textcontent.append("bijgevolg op de infrastructuur voor alternatieve brandstoffen voor alle vervoerswijzen.")
    thisalinea.textcontent.append("Daarom moet de Commissie deze verordening uiterlijk eind 2026 herzien, met name")
    thisalinea.textcontent.append("wat betreft de streefcijfers voor elektrische laadpunten voor zware bedrijfsvoertuigen")
    thisalinea.textcontent.append("en de streefcijfers voor infrastructuur voor alternatieve brandstoffen voor emissievrije")
    thisalinea.textcontent.append("schepen en luchtvaartuigen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(55) Daar de doelstelling van deze ..."
    thisalinea.nativeID = 104
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 54
    thisalinea.summary = "(55) Daar de doelstelling van deze verordening, namelijk een brede ontwikkeling van de markt voor alternatieve brandstoffen bevorderen, niet voldoende door de lidstaten kan worden verwezenlijkt maar, omdat er maatregelen nodig zijn om tegemoet te komen aan de vraag naar een kritische massa van voertuigen op alternatieve brandstof en naar kostenefficiënte ontwikkelingen door de Europese industrie, en om de mobiliteit van voertuigen op alternatieve brandstoffen in de hele Unie mogelijk te maken, beter door de Unie kan worden verwezenlijkt, kan de Unie maatregelen vaststellen overeenkomstig het subsidiariteitsbeginsel zoals vastgelegd in artikel 5 van het Verdrag betreffende de Europese Unie. Overeenkomstig "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(55) Daar de doelstelling van deze verordening, namelijk een brede ontwikkeling van de")
    thisalinea.textcontent.append("markt voor alternatieve brandstoffen bevorderen, niet voldoende door de lidstaten kan")
    thisalinea.textcontent.append("worden verwezenlijkt maar, omdat er maatregelen nodig zijn om tegemoet te komen")
    thisalinea.textcontent.append("aan de vraag naar een kritische massa van voertuigen op alternatieve brandstof en naar")
    thisalinea.textcontent.append("kostenefficiënte ontwikkelingen door de Europese industrie, en om de mobiliteit van")
    thisalinea.textcontent.append("voertuigen op alternatieve brandstoffen in de hele Unie mogelijk te maken, beter door")
    thisalinea.textcontent.append("de Unie kan worden verwezenlijkt, kan de Unie maatregelen vaststellen")
    thisalinea.textcontent.append("overeenkomstig het subsidiariteitsbeginsel zoals vastgelegd in artikel 5 van het")
    thisalinea.textcontent.append("Verdrag betreffende de Europese Unie. Overeenkomstig het in hetzelfde artikel")
    thisalinea.textcontent.append("neergelegde evenredigheidsbeginsel gaat deze verordening niet verder dan nodig is om")
    thisalinea.textcontent.append("deze doelstelling te verwezenlijken,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(56) Richtlijn 2014/94/EU moet daarom worden ..."
    thisalinea.nativeID = 105
    thisalinea.parentID = 49
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 55
    thisalinea.summary = "(56) Richtlijn 2014/94/EU moet daarom worden ingetrokken, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(56) Richtlijn 2014/94/EU moet daarom worden ingetrokken,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 1"
    thisalinea.nativeID = 106
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "Onderwerp 1. Bij deze verordening worden bindende nationale streefcijfers vastgesteld voor de EU-brede uitrol van voldoende infrastructuur voor alternatieve brandstoffen voor wegvoertuigen, vaartuigen en stilstaande luchtvaartuigen. Er worden gemeenschappelijke technische specificaties en eisen vastgesteld inzake de gebruikersinformatie, gegevensverstrekking en betalingsmodaliteiten voor infrastructuur voor alternatieve brandstoffen. 2. Deze verordening bevat regels voor de nationale beleidskaders die de lidstaten dienen vast te stellen, met inbegrip van de uitrol van infrastructuur voor alternatieve brandstoffen in gebieden waarvoor geen bindende EU-doelstellingen zijn vastgesteld, en inzake de verslaglegging over de uitrol van die infrastructuur. 3. Bij deze verordening wordt een rapportagemechanisme ingesteld om samenwerking te "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Onderwerp")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Bij deze verordening worden bindende ..."
    thisalinea.nativeID = 107
    thisalinea.parentID = 106
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Bij deze verordening worden bindende nationale streefcijfers vastgesteld voor de EU-brede uitrol van voldoende infrastructuur voor alternatieve brandstoffen voor wegvoertuigen, vaartuigen en stilstaande luchtvaartuigen. Er worden gemeenschappelijke technische specificaties en eisen vastgesteld inzake de gebruikersinformatie, gegevensverstrekking en betalingsmodaliteiten voor infrastructuur voor alternatieve brandstoffen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Bij deze verordening worden bindende nationale streefcijfers vastgesteld voor de")
    thisalinea.textcontent.append("EU-brede uitrol van voldoende infrastructuur voor alternatieve brandstoffen voor")
    thisalinea.textcontent.append("wegvoertuigen, vaartuigen en stilstaande luchtvaartuigen. Er worden")
    thisalinea.textcontent.append("gemeenschappelijke technische specificaties en eisen vastgesteld inzake de")
    thisalinea.textcontent.append("gebruikersinformatie, gegevensverstrekking en betalingsmodaliteiten voor")
    thisalinea.textcontent.append("infrastructuur voor alternatieve brandstoffen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Deze verordening bevat regels voor ..."
    thisalinea.nativeID = 108
    thisalinea.parentID = 106
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Deze verordening bevat regels voor de nationale beleidskaders die de lidstaten dienen vast te stellen, met inbegrip van de uitrol van infrastructuur voor alternatieve brandstoffen in gebieden waarvoor geen bindende EU-doelstellingen zijn vastgesteld, en inzake de verslaglegging over de uitrol van die infrastructuur. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Deze verordening bevat regels voor de nationale beleidskaders die de lidstaten")
    thisalinea.textcontent.append("dienen vast te stellen, met inbegrip van de uitrol van infrastructuur voor alternatieve")
    thisalinea.textcontent.append("brandstoffen in gebieden waarvoor geen bindende EU-doelstellingen zijn vastgesteld,")
    thisalinea.textcontent.append("en inzake de verslaglegging over de uitrol van die infrastructuur.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Bij deze verordening wordt een ..."
    thisalinea.nativeID = 109
    thisalinea.parentID = 106
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Bij deze verordening wordt een rapportagemechanisme ingesteld om samenwerking te stimuleren en een degelijke monitoring van de voortgang te waarborgen. Dat mechanisme voorziet in een gestructureerd, transparant en iteratief proces tussen de Commissie en de lidstaten dat gericht is op de ontwikkeling van de nationale beleidskaders, op de daaropvolgende uitvoering daarvan en op de overeenkomstige maatregelen van de Commissie. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Bij deze verordening wordt een rapportagemechanisme ingesteld om samenwerking")
    thisalinea.textcontent.append("te stimuleren en een degelijke monitoring van de voortgang te waarborgen. Dat")
    thisalinea.textcontent.append("mechanisme voorziet in een gestructureerd, transparant en iteratief proces tussen de")
    thisalinea.textcontent.append("Commissie en de lidstaten dat gericht is op de ontwikkeling van de nationale")
    thisalinea.textcontent.append("beleidskaders, op de daaropvolgende uitvoering daarvan en op de overeenkomstige")
    thisalinea.textcontent.append("maatregelen van de Commissie.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 2"
    thisalinea.nativeID = 110
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 9
    thisalinea.summary = "Definities Voor de toepassing van deze verordening wordt verstaan onder: (1) “toegankelijkheid van de gegevens”: de mogelijkheid om de gegevens te allen tijde in een machineleesbaar formaat op te vragen en te verkrijgen, als gedefinieerd in artikel 2, punt 5, van Gedelegeerde Verordening (EU) 2015/96223 van de Commissie; (2) “ad-hocprijs”: de prijs die een exploitant van een laad- of tankpunt aan een eindgebruiker aanrekent om op ad-hocbasis te laden of te tanken; (3) “alternatieve brandstoffen”: brandstoffen of energiebronnen die, althans gedeeltelijk, dienen als vervanging van fossiele oliebronnen in de energievoorziening voor vervoer en die kunnen bijdragen tot de decarbonisatie van "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Definities")
    thisalinea.textcontent.append("Voor de toepassing van deze verordening wordt verstaan onder:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(1) “toegankelijkheid van de gegevens”: de ..."
    thisalinea.nativeID = 111
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(1) “toegankelijkheid van de gegevens”: de mogelijkheid om de gegevens te allen tijde in een machineleesbaar formaat op te vragen en te verkrijgen, als gedefinieerd in artikel 2, punt 5, van Gedelegeerde Verordening (EU) 2015/96223 van de Commissie; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(1) “toegankelijkheid van de gegevens”: de mogelijkheid om de gegevens te allen tijde")
    thisalinea.textcontent.append("in een machineleesbaar formaat op te vragen en te verkrijgen, als gedefinieerd in")
    thisalinea.textcontent.append("artikel 2, punt 5, van Gedelegeerde Verordening (EU) 2015/96223 van de Commissie;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(2) “ad-hocprijs”: de prijs die een ..."
    thisalinea.nativeID = 112
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(2) “ad-hocprijs”: de prijs die een exploitant van een laad- of tankpunt aan een eindgebruiker aanrekent om op ad-hocbasis te laden of te tanken; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(2) “ad-hocprijs”: de prijs die een exploitant van een laad- of tankpunt aan een")
    thisalinea.textcontent.append("eindgebruiker aanrekent om op ad-hocbasis te laden of te tanken;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(3) “alternatieve brandstoffen”: brandstoffen of energiebronnen ..."
    thisalinea.nativeID = 113
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(3) “alternatieve brandstoffen”: brandstoffen of energiebronnen die, althans gedeeltelijk, dienen als vervanging van fossiele oliebronnen in de energievoorziening voor vervoer en die kunnen bijdragen tot de decarbonisatie van de energievoorziening en tot betere milieuprestaties van de vervoerssector, met inbegrip van: (a) “alternatieve brandstoffen voor emissievrije voertuigen”: – elektriciteit, – waterstof, – ammoniak, (b) “hernieuwbare brandstoffen”: biomassabrandstoffen en biobrandstoffen als gedefinieerd in artikel 2, punten 27 en 33, van Richtlijn (EU) 2018/2001, uit hernieuwbare energiebronnen geproduceerde synthetische en paraffinehoudende brandstoffen, waaronder ammoniak, (c) “alternatieve fossiele brandstoffen” voor een overgangsfase: – aardgas, in gasvorm (Compressed Natural Gas — CNG) en in vloeibare "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(3) “alternatieve brandstoffen”: brandstoffen of energiebronnen die, althans gedeeltelijk,")
    thisalinea.textcontent.append("dienen als vervanging van fossiele oliebronnen in de energievoorziening voor")
    thisalinea.textcontent.append("vervoer en die kunnen bijdragen tot de decarbonisatie van de energievoorziening en")
    thisalinea.textcontent.append("tot betere milieuprestaties van de vervoerssector, met inbegrip van:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) “alternatieve brandstoffen voor emissievrije voertuigen”: "
    thisalinea.nativeID = 114
    thisalinea.parentID = 113
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) “alternatieve brandstoffen voor emissievrije voertuigen”: – elektriciteit, – waterstof, – ammoniak, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) “alternatieve brandstoffen voor emissievrije voertuigen”:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– elektriciteit, "
    thisalinea.nativeID = 115
    thisalinea.parentID = 114
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "– elektriciteit, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– elektriciteit,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– waterstof, "
    thisalinea.nativeID = 116
    thisalinea.parentID = 114
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "– waterstof, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– waterstof,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– ammoniak, "
    thisalinea.nativeID = 117
    thisalinea.parentID = 114
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "– ammoniak, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– ammoniak,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) “hernieuwbare brandstoffen”: biomassabrandstoffen en biobrandstoffen ..."
    thisalinea.nativeID = 118
    thisalinea.parentID = 113
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) “hernieuwbare brandstoffen”: biomassabrandstoffen en biobrandstoffen als gedefinieerd in artikel 2, punten 27 en 33, van Richtlijn (EU) 2018/2001, uit hernieuwbare energiebronnen geproduceerde synthetische en paraffinehoudende brandstoffen, waaronder ammoniak, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) “hernieuwbare brandstoffen”: biomassabrandstoffen en biobrandstoffen als")
    thisalinea.textcontent.append("gedefinieerd in artikel 2, punten 27 en 33, van Richtlijn (EU) 2018/2001, uit")
    thisalinea.textcontent.append("hernieuwbare energiebronnen geproduceerde synthetische en")
    thisalinea.textcontent.append("paraffinehoudende brandstoffen, waaronder ammoniak,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– "
    thisalinea.nativeID = 119
    thisalinea.parentID = 118
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = ""
    thisalinea.sum_CanbeEmpty = True
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("–")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– "
    thisalinea.nativeID = 120
    thisalinea.parentID = 118
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = ""
    thisalinea.sum_CanbeEmpty = True
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("–")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(c) “alternatieve fossiele brandstoffen” voor een ..."
    thisalinea.nativeID = 121
    thisalinea.parentID = 113
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(c) “alternatieve fossiele brandstoffen” voor een overgangsfase: – aardgas, in gasvorm (Compressed Natural Gas — CNG) en in vloeibare vorm (Liquefied Natural Gas — LNG), – vloeibaar gemaakt petroleumgas (LPG), en – uit niet-hernieuwbare energiebronnen geproduceerde synthetische en paraffinehoudende brandstoffen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(c) “alternatieve fossiele brandstoffen” voor een overgangsfase:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– aardgas, in gasvorm (Compressed Natural ..."
    thisalinea.nativeID = 122
    thisalinea.parentID = 121
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "– aardgas, in gasvorm (Compressed Natural Gas — CNG) en in vloeibare vorm (Liquefied Natural Gas — LNG), "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– aardgas, in gasvorm (Compressed Natural Gas — CNG) en in vloeibare vorm")
    thisalinea.textcontent.append("(Liquefied Natural Gas — LNG),")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– vloeibaar gemaakt petroleumgas (LPG), en "
    thisalinea.nativeID = 123
    thisalinea.parentID = 121
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "– vloeibaar gemaakt petroleumgas (LPG), en "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– vloeibaar gemaakt petroleumgas (LPG), en")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– uit niet-hernieuwbare energiebronnen geproduceerde synthetische ..."
    thisalinea.nativeID = 124
    thisalinea.parentID = 121
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "– uit niet-hernieuwbare energiebronnen geproduceerde synthetische en paraffinehoudende brandstoffen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– uit niet-hernieuwbare energiebronnen geproduceerde synthetische en")
    thisalinea.textcontent.append("paraffinehoudende brandstoffen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(4) “luchthaven van het TEN-T-kernnetwerk en ..."
    thisalinea.nativeID = 125
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "(4) “luchthaven van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk”: een luchthaven als genoemd en gecategoriseerd in bijlage II bij Verordening (EU) nr. 1315/2013; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(4) “luchthaven van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk”: een")
    thisalinea.textcontent.append("luchthaven als genoemd en gecategoriseerd in bijlage II bij Verordening (EU) nr.")
    thisalinea.textcontent.append("1315/2013;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(5) “luchthavenbeheerder”: als gedefinieerd in artikel ..."
    thisalinea.nativeID = 126
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "(5) “luchthavenbeheerder”: als gedefinieerd in artikel 2, punt 2, van Richtlijn 2009/12/EG24 van het Europees Parlement en de Raad; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(5) “luchthavenbeheerder”: als gedefinieerd in artikel 2, punt 2, van Richtlijn")
    thisalinea.textcontent.append("2009/12/EG24 van het Europees Parlement en de Raad;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(6) “automatische authenticatie”: de authenticatie van ..."
    thisalinea.nativeID = 127
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "(6) “automatische authenticatie”: de authenticatie van een voertuig bij een laadpunt via de laadconnector of telematica; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(6) “automatische authenticatie”: de authenticatie van een voertuig bij een laadpunt via")
    thisalinea.textcontent.append("de laadconnector of telematica;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(7) “beschikbaarheid van gegevens”: het bestaan ..."
    thisalinea.nativeID = 128
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "(7) “beschikbaarheid van gegevens”: het bestaan van gegevens in een digitaal machineleesbaar formaat; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(7) “beschikbaarheid van gegevens”: het bestaan van gegevens in een digitaal")
    thisalinea.textcontent.append("machineleesbaar formaat;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(8) “batterijvoertuig”: een elektrisch voertuig dat ..."
    thisalinea.nativeID = 129
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "(8) “batterijvoertuig”: een elektrisch voertuig dat uitsluitend op de elektromotor rijdt, zonder secundaire voortstuwingsbron; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(8) “batterijvoertuig”: een elektrisch voertuig dat uitsluitend op de elektromotor rijdt,")
    thisalinea.textcontent.append("zonder secundaire voortstuwingsbron;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(9) “bidirectioneel laden”: een slim laadproces ..."
    thisalinea.nativeID = 130
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "(9) “bidirectioneel laden”: een slim laadproces waarbij de richting van de elektriciteitsstroom kan worden omgekeerd, waardoor elektriciteit ook van de batterij naar het laadpunt waarop zij is aangesloten kan stromen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(9) “bidirectioneel laden”: een slim laadproces waarbij de richting van de")
    thisalinea.textcontent.append("elektriciteitsstroom kan worden omgekeerd, waardoor elektriciteit ook van de batterij")
    thisalinea.textcontent.append("naar het laadpunt waarop zij is aangesloten kan stromen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(10) “connector”: de fysieke interface tussen ..."
    thisalinea.nativeID = 131
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 9
    thisalinea.summary = "(10) “connector”: de fysieke interface tussen het laadpunt en het elektrische voertuig via dewelke de elektrische energie wordt uitgewisseld; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(10) “connector”: de fysieke interface tussen het laadpunt en het elektrische voertuig via")
    thisalinea.textcontent.append("dewelke de elektrische energie wordt uitgewisseld;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(11) “commercieel luchtvervoer”: luchtvervoer als gedefinieerd ..."
    thisalinea.nativeID = 132
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 10
    thisalinea.summary = "(11) “commercieel luchtvervoer”: luchtvervoer als gedefinieerd in artikel 3, punt 24), van Verordening (EU) 2018/113925 van het Europees Parlement en de Raad; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(11) “commercieel luchtvervoer”: luchtvervoer als gedefinieerd in artikel 3, punt 24), van")
    thisalinea.textcontent.append("Verordening (EU) 2018/113925 van het Europees Parlement en de Raad;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(12) “containerschip”: een schip dat uitsluitend ..."
    thisalinea.nativeID = 133
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 11
    thisalinea.summary = "(12) “containerschip”: een schip dat uitsluitend is ontworpen voor het vervoer van containers in ruimen en op het dek; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(12) “containerschip”: een schip dat uitsluitend is ontworpen voor het vervoer van")
    thisalinea.textcontent.append("containers in ruimen en op het dek;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(13) “betaling op basis van een ..."
    thisalinea.nativeID = 134
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 12
    thisalinea.summary = "(13) “betaling op basis van een contract”: een betaling door de eindgebruiker van een laad- of tankdienst aan een aanbieder van mobiliteitsdiensten op basis van een contract tussen de eindgebruiker en de aanbieder van mobiliteitsdiensten; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(13) “betaling op basis van een contract”: een betaling door de eindgebruiker van een")
    thisalinea.textcontent.append("laad- of tankdienst aan een aanbieder van mobiliteitsdiensten op basis van een")
    thisalinea.textcontent.append("contract tussen de eindgebruiker en de aanbieder van mobiliteitsdiensten;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(14) “digitaal verbonden laadpunt”: een laadpunt ..."
    thisalinea.nativeID = 135
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 13
    thisalinea.summary = "(14) “digitaal verbonden laadpunt”: een laadpunt dat in realtime informatie kan verzenden en ontvangen, dat in twee richtingen met het elektriciteitsnet en met het elektrisch voertuig kan communiceren, en dat op afstand kan worden gemonitord en beheerd, onder meer om de laadsessie te starten en te stoppen en om de elektriciteitsstromen te meten; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(14) “digitaal verbonden laadpunt”: een laadpunt dat in realtime informatie kan verzenden")
    thisalinea.textcontent.append("en ontvangen, dat in twee richtingen met het elektriciteitsnet en met het elektrisch")
    thisalinea.textcontent.append("voertuig kan communiceren, en dat op afstand kan worden gemonitord en beheerd,")
    thisalinea.textcontent.append("onder meer om de laadsessie te starten en te stoppen en om de elektriciteitsstromen te")
    thisalinea.textcontent.append("meten;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(15) “distributiesysteembeheerder”: een beheerder als gedefinieerd ..."
    thisalinea.nativeID = 136
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 14
    thisalinea.summary = "(15) “distributiesysteembeheerder”: een beheerder als gedefinieerd in artikel 2, punt 29, van Richtlijn (EU) 2019/944; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(15) “distributiesysteembeheerder”: een beheerder als gedefinieerd in artikel 2, punt 29,")
    thisalinea.textcontent.append("van Richtlijn (EU) 2019/944;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(16) “dynamische gegevens”: gegevens die vaak ..."
    thisalinea.nativeID = 137
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 15
    thisalinea.summary = "(16) “dynamische gegevens”: gegevens die vaak of op regelmatige basis wijzigen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(16) “dynamische gegevens”: gegevens die vaak of op regelmatige basis wijzigen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(17) “elektrisch wegsysteem”: een fysieke installatie ..."
    thisalinea.nativeID = 138
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 16
    thisalinea.summary = "(17) “elektrisch wegsysteem”: een fysieke installatie op een weg waarmee elektriciteit kan worden verstrekt aan een rijdend elektrisch voertuig; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(17) “elektrisch wegsysteem”: een fysieke installatie op een weg waarmee elektriciteit")
    thisalinea.textcontent.append("kan worden verstrekt aan een rijdend elektrisch voertuig;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(18) “elektrisch voertuig”: een motorvoertuig, uitgerust ..."
    thisalinea.nativeID = 139
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 17
    thisalinea.summary = "(18) “elektrisch voertuig”: een motorvoertuig, uitgerust met een aandrijving die bestaat uit ten minste één niet-perifere elektromotor als energieomzetter met een elektrisch oplaadbaar energieopslagsysteem, dat extern kan worden opgeladen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(18) “elektrisch voertuig”: een motorvoertuig, uitgerust met een aandrijving die bestaat uit")
    thisalinea.textcontent.append("ten minste één niet-perifere elektromotor als energieomzetter met een elektrisch")
    thisalinea.textcontent.append("oplaadbaar energieopslagsysteem, dat extern kan worden opgeladen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(19) “elektriciteitsvoorziening aan stilstaande luchtvaartuigen”: de ..."
    thisalinea.nativeID = 140
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 18
    thisalinea.summary = "(19) “elektriciteitsvoorziening aan stilstaande luchtvaartuigen”: de levering van elektriciteit via een gestandaardiseerde vaste of mobiele interface aan luchtvaartuigen die aan de gate of op een buitenstandplaats van een luchthaven zijn geparkeerd; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(19) “elektriciteitsvoorziening aan stilstaande luchtvaartuigen”: de levering van")
    thisalinea.textcontent.append("elektriciteit via een gestandaardiseerde vaste of mobiele interface aan luchtvaartuigen")
    thisalinea.textcontent.append("die aan de gate of op een buitenstandplaats van een luchthaven zijn geparkeerd;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(20) “eindgebruiker”: een natuurlijke of rechtspersoon ..."
    thisalinea.nativeID = 141
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 19
    thisalinea.summary = "(20) “eindgebruiker”: een natuurlijke of rechtspersoon die alternatieve brandstof koopt voor direct gebruik in een voertuig; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(20) “eindgebruiker”: een natuurlijke of rechtspersoon die alternatieve brandstof koopt")
    thisalinea.textcontent.append("voor direct gebruik in een voertuig;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(21) “e-roaming”: de uitwisseling van gegevens ..."
    thisalinea.nativeID = 142
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 20
    thisalinea.summary = "(21) “e-roaming”: de uitwisseling van gegevens en betalingen tussen de exploitant van een laad- of tankpunt en een aanbieder van mobiliteitsdiensten van wie een eindgebruiker een laaddienst koopt; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(21) “e-roaming”: de uitwisseling van gegevens en betalingen tussen de exploitant van")
    thisalinea.textcontent.append("een laad- of tankpunt en een aanbieder van mobiliteitsdiensten van wie een")
    thisalinea.textcontent.append("eindgebruiker een laaddienst koopt;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(22) “elektronisch roamingplatform”: een platform dat ..."
    thisalinea.nativeID = 143
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 21
    thisalinea.summary = "(22) “elektronisch roamingplatform”: een platform dat marktspelers, met name aanbieders van mobiliteitsdiensten en exploitanten van laad- of tankpunten, met elkaar verbindt om hen in staat te stellen aan elkaar diensten te verlenen, met inbegrip van e- roaming; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(22) “elektronisch roamingplatform”: een platform dat marktspelers, met name aanbieders")
    thisalinea.textcontent.append("van mobiliteitsdiensten en exploitanten van laad- of tankpunten, met elkaar verbindt")
    thisalinea.textcontent.append("om hen in staat te stellen aan elkaar diensten te verlenen, met inbegrip van e-")
    thisalinea.textcontent.append("roaming;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(23) “Europese norm”: een Europese norm ..."
    thisalinea.nativeID = 144
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 22
    thisalinea.summary = "(23) “Europese norm”: een Europese norm als gedefinieerd in artikel 2, punt 1, c), van Verordening (EU) nr. 1025/2012; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(23) “Europese norm”: een Europese norm als gedefinieerd in artikel 2, punt 1, c), van")
    thisalinea.textcontent.append("Verordening (EU) nr. 1025/2012;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(24) “goederenterminal”: een goederenterminal als gedefinieerd ..."
    thisalinea.nativeID = 145
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 23
    thisalinea.summary = "(24) “goederenterminal”: een goederenterminal als gedefinieerd in artikel 3, punt s), van Verordening (EU) nr. 1315/2013; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(24) “goederenterminal”: een goederenterminal als gedefinieerd in artikel 3, punt s), van")
    thisalinea.textcontent.append("Verordening (EU) nr. 1315/2013;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(25) “brutotonnage (GT)”: brutotonnage als gedefinieerd ..."
    thisalinea.nativeID = 146
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 24
    thisalinea.summary = "(25) “brutotonnage (GT)”: brutotonnage als gedefinieerd in artikel 3, punt e), van Verordening (EU) 2015/75726 van het Europees Parlement en de Raad; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(25) “brutotonnage (GT)”: brutotonnage als gedefinieerd in artikel 3, punt e), van")
    thisalinea.textcontent.append("Verordening (EU) 2015/75726 van het Europees Parlement en de Raad;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(26) “zwaar bedrijfsvoertuig”: een motorvoertuig van ..."
    thisalinea.nativeID = 147
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 25
    thisalinea.summary = "(26) “zwaar bedrijfsvoertuig”: een motorvoertuig van de categorieën M2, M3, N2 of N3 zoals gedefinieerd in bijlage II bij Richtlijn 2007/46/EG27; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(26) “zwaar bedrijfsvoertuig”: een motorvoertuig van de categorieën M2, M3, N2 of N3")
    thisalinea.textcontent.append("zoals gedefinieerd in bijlage II bij Richtlijn 2007/46/EG27;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(27) “laadpunt voor hoog vermogen”: een ..."
    thisalinea.nativeID = 148
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 26
    thisalinea.summary = "(27) “laadpunt voor hoog vermogen”: een laadpunt met een vermogen van meer dan 22 kW waarmee elektriciteit kan worden verstrekt aan een elektrisch voertuig; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(27) “laadpunt voor hoog vermogen”: een laadpunt met een vermogen van meer dan")
    thisalinea.textcontent.append("22 kW waarmee elektriciteit kan worden verstrekt aan een elektrisch voertuig;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(28) “hogesnelheidspassagiersvaartuig”: een vaartuig als omschreven ..."
    thisalinea.nativeID = 149
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 27
    thisalinea.summary = "(28) “hogesnelheidspassagiersvaartuig”: een vaartuig als omschreven in hoofdstuk X, voorschrift 1, van het SOLAS-verdrag van 1974, en dat bestemd is voor het vervoer van meer dan twaalf passagiers; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(28) “hogesnelheidspassagiersvaartuig”: een vaartuig als omschreven in hoofdstuk X,")
    thisalinea.textcontent.append("voorschrift 1, van het SOLAS-verdrag van 1974, en dat bestemd is voor het vervoer")
    thisalinea.textcontent.append("van meer dan twaalf passagiers;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(29) “licht voertuig”: een motorvoertuig van ..."
    thisalinea.nativeID = 150
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 28
    thisalinea.summary = "(29) “licht voertuig”: een motorvoertuig van de categorieën M1 of N1 zoals gedefinieerd in bijlage II bij Richtlijn 2007/46/EG; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(29) “licht voertuig”: een motorvoertuig van de categorieën M1 of N1 zoals gedefinieerd")
    thisalinea.textcontent.append("in bijlage II bij Richtlijn 2007/46/EG;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(30) “aanbieder van mobiliteitsdiensten”: een rechtspersoon ..."
    thisalinea.nativeID = 151
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 29
    thisalinea.summary = "(30) “aanbieder van mobiliteitsdiensten”: een rechtspersoon die tegen vergoeding diensten verleent aan eindgebruikers, met inbegrip van de verkoop van laaddiensten; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(30) “aanbieder van mobiliteitsdiensten”: een rechtspersoon die tegen vergoeding")
    thisalinea.textcontent.append("diensten verleent aan eindgebruikers, met inbegrip van de verkoop van laaddiensten;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(31) “laadpunt voor normaal vermogen”: een ..."
    thisalinea.nativeID = 152
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 30
    thisalinea.summary = "(31) “laadpunt voor normaal vermogen”: een laadpunt met een vermogen van maximaal 22 kW waarmee elektriciteit kan worden overgebracht naar een elektrisch voertuig;s "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(31) “laadpunt voor normaal vermogen”: een laadpunt met een vermogen van maximaal")
    thisalinea.textcontent.append("22 kW waarmee elektriciteit kan worden overgebracht naar een elektrisch voertuig;s")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(32) “nationaal toegangspunt”: een digitale interface ..."
    thisalinea.nativeID = 153
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 31
    thisalinea.summary = "(32) “nationaal toegangspunt”: een digitale interface waarbij bepaalde statische en dynamische gegevens toegankelijk worden gemaakt voor hergebruik door gebruikers, zoals door de lidstaten geïmplementeerd in overeenstemming met artikel 3 van Gedelegeerde Verordening (EU) 2015/962 van de Commissie; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(32) “nationaal toegangspunt”: een digitale interface waarbij bepaalde statische en")
    thisalinea.textcontent.append("dynamische gegevens toegankelijk worden gemaakt voor hergebruik door")
    thisalinea.textcontent.append("gebruikers, zoals door de lidstaten geïmplementeerd in overeenstemming met artikel")
    thisalinea.textcontent.append("3 van Gedelegeerde Verordening (EU) 2015/962 van de Commissie;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(33) “exploitant van een laadpunt”: de ..."
    thisalinea.nativeID = 154
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 32
    thisalinea.summary = "(33) “exploitant van een laadpunt”: de entiteit die verantwoordelijk is voor het beheer en de exploitatie van een laadpunt dat een laaddienst levert aan eindgebruikers, onder meer namens en voor rekening van een aanbieder van mobiliteitsdiensten; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(33) “exploitant van een laadpunt”: de entiteit die verantwoordelijk is voor het beheer en")
    thisalinea.textcontent.append("de exploitatie van een laadpunt dat een laaddienst levert aan eindgebruikers, onder")
    thisalinea.textcontent.append("meer namens en voor rekening van een aanbieder van mobiliteitsdiensten;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(34) “exploitant van een tankpunt”: de ..."
    thisalinea.nativeID = 155
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 33
    thisalinea.summary = "(34) “exploitant van een tankpunt”: de entiteit die verantwoordelijk is voor het beheer en de werking van een tankpunt dat een tankdienst levert aan eindgebruikers, onder meer namens en voor rekening van een aanbieder van mobiliteitsdiensten; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(34) “exploitant van een tankpunt”: de entiteit die verantwoordelijk is voor het beheer en")
    thisalinea.textcontent.append("de werking van een tankpunt dat een tankdienst levert aan eindgebruikers, onder")
    thisalinea.textcontent.append("meer namens en voor rekening van een aanbieder van mobiliteitsdiensten;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(35) “passagiersschip”: een schip dat meer ..."
    thisalinea.nativeID = 156
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 34
    thisalinea.summary = "(35) “passagiersschip”: een schip dat meer dan 12 passagiers vervoert, met inbegrip van cruiseschepen, hogesnelheidspassagiersvaartuigen en schepen met voorzieningen om weg- of spoorvoertuigen in staat te stellen op en van het schip te rijden (“ro-ro- passagiersschepen”); "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(35) “passagiersschip”: een schip dat meer dan 12 passagiers vervoert, met inbegrip van")
    thisalinea.textcontent.append("cruiseschepen, hogesnelheidspassagiersvaartuigen en schepen met voorzieningen om")
    thisalinea.textcontent.append("weg- of spoorvoertuigen in staat te stellen op en van het schip te rijden (“ro-ro-")
    thisalinea.textcontent.append("passagiersschepen”);")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(36) “plug-in hybride voertuig”: elektrisch voertuig ..."
    thisalinea.nativeID = 157
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 35
    thisalinea.summary = "(36) “plug-in hybride voertuig”: elektrisch voertuig waarbij een conventionele verbrandingsmotor wordt gecombineerd met een elektrisch aandrijfsysteem, dat via een externe elektrische energiebron kan worden opgeladen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(36) “plug-in hybride voertuig”: elektrisch voertuig waarbij een conventionele")
    thisalinea.textcontent.append("verbrandingsmotor wordt gecombineerd met een elektrisch aandrijfsysteem, dat via")
    thisalinea.textcontent.append("een externe elektrische energiebron kan worden opgeladen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(37) “laadvermogen”: het theoretische maximumvermogen, uitgedrukt ..."
    thisalinea.nativeID = 158
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 36
    thisalinea.summary = "(37) “laadvermogen”: het theoretische maximumvermogen, uitgedrukt in kW, dat door een laadpunt, -station, -pool of walstroomvoorziening kan worden geleverd aan een voertuig of vaartuig dat is aangesloten op dat punt, dat station, die pool of die voorziening; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(37) “laadvermogen”: het theoretische maximumvermogen, uitgedrukt in kW, dat door")
    thisalinea.textcontent.append("een laadpunt, -station, -pool of walstroomvoorziening kan worden geleverd aan een")
    thisalinea.textcontent.append("voertuig of vaartuig dat is aangesloten op dat punt, dat station, die pool of die")
    thisalinea.textcontent.append("voorziening;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(38) “openbaar toegankelijke infrastructuur voor alternatieve ..."
    thisalinea.nativeID = 159
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 37
    thisalinea.summary = "(38) “openbaar toegankelijke infrastructuur voor alternatieve brandstoffen”: infrastructuur voor alternatieve brandstoffen op een locatie of in een ruimte die toegankelijk is voor het grote publiek, ongeacht of die infrastructuur zich op een openbaar dan wel op een privéterrein bevindt, ongeacht de eventuele beperkingen of voorwaarden voor de toegang tot de locatie of ruimte en ongeacht de gebruiksvoorwaarden van die infrastructuur; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(38) “openbaar toegankelijke infrastructuur voor alternatieve brandstoffen”: infrastructuur")
    thisalinea.textcontent.append("voor alternatieve brandstoffen op een locatie of in een ruimte die toegankelijk is voor")
    thisalinea.textcontent.append("het grote publiek, ongeacht of die infrastructuur zich op een openbaar dan wel op een")
    thisalinea.textcontent.append("privéterrein bevindt, ongeacht de eventuele beperkingen of voorwaarden voor de")
    thisalinea.textcontent.append("toegang tot de locatie of ruimte en ongeacht de gebruiksvoorwaarden van die")
    thisalinea.textcontent.append("infrastructuur;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(39) “Quick-responscode (QR-code)”: een ISO 18004-conforme ..."
    thisalinea.nativeID = 160
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 38
    thisalinea.summary = "(39) “Quick-responscode (QR-code)”: een ISO 18004-conforme codering en visualisatie van gegevens; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(39) “Quick-responscode (QR-code)”: een ISO 18004-conforme codering en visualisatie")
    thisalinea.textcontent.append("van gegevens;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(40) “adhoc-laadbeurt”: een door een eindgebruiker ..."
    thisalinea.nativeID = 161
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 39
    thisalinea.summary = "(40) “adhoc-laadbeurt”: een door een eindgebruiker aangekochte laaddienst waarvoor hij niet verplicht is zich te registreren, een schriftelijke overeenkomst te sluiten of een commerciële relatie met de exploitant van een laadpunt aan te gaan voor een langere periode dan de aankoop van de dienst; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(40) “adhoc-laadbeurt”: een door een eindgebruiker aangekochte laaddienst waarvoor hij")
    thisalinea.textcontent.append("niet verplicht is zich te registreren, een schriftelijke overeenkomst te sluiten of een")
    thisalinea.textcontent.append("commerciële relatie met de exploitant van een laadpunt aan te gaan voor een langere")
    thisalinea.textcontent.append("periode dan de aankoop van de dienst;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(41) “laadpunt”: een vaste of mobiele ..."
    thisalinea.nativeID = 162
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 40
    thisalinea.summary = "(41) “laadpunt”: een vaste of mobiele interface die het mogelijk maakt elektriciteit over te brengen naar een elektrisch voertuig en dat weliswaar over een of meer connectoren voor verschillende types stekker kan beschikken maar waaraan slechts één elektrisch voertuig tegelijk kan opladen, met uitzondering van apparaten met een uitgangsvermogen van ten hoogste 3,7 kW die niet in de eerste plaats voor het opladen van elektrische voertuigen zijn bestemd; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(41) “laadpunt”: een vaste of mobiele interface die het mogelijk maakt elektriciteit over te")
    thisalinea.textcontent.append("brengen naar een elektrisch voertuig en dat weliswaar over een of meer connectoren")
    thisalinea.textcontent.append("voor verschillende types stekker kan beschikken maar waaraan slechts één elektrisch")
    thisalinea.textcontent.append("voertuig tegelijk kan opladen, met uitzondering van apparaten met een")
    thisalinea.textcontent.append("uitgangsvermogen van ten hoogste 3,7 kW die niet in de eerste plaats voor het")
    thisalinea.textcontent.append("opladen van elektrische voertuigen zijn bestemd;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(42) “laadpunt, -station of -pool voor ..."
    thisalinea.nativeID = 163
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 41
    thisalinea.summary = "(42) “laadpunt, -station of -pool voor lichte voertuigen”: een laadpunt, -station of -pool dat of die bestemd is voor het opladen van lichte voertuigen, hetzij vanwege het specifieke ontwerp van de connectoren/stekkers, hetzij vanwege de inrichting van de parkeerplaats naast het laadpunt, het station en/of de pool; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(42) “laadpunt, -station of -pool voor lichte voertuigen”: een laadpunt, -station of -pool")
    thisalinea.textcontent.append("dat of die bestemd is voor het opladen van lichte voertuigen, hetzij vanwege het")
    thisalinea.textcontent.append("specifieke ontwerp van de connectoren/stekkers, hetzij vanwege de inrichting van de")
    thisalinea.textcontent.append("parkeerplaats naast het laadpunt, het station en/of de pool;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(43) “laadpunt, station of pool voor ..."
    thisalinea.nativeID = 164
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 42
    thisalinea.summary = "(43) “laadpunt, station of pool voor zware bedrijfsvoertuigen”: een laadpunt, station of pool dat of die bestemd is voor het opladen van zware bedrijfsvoertuigen, hetzij vanwege het specifieke ontwerp van de connectoren/stekkers, hetzij vanwege het ontwerp van de parkeerplaats naast het laadpunt, het station en/of de pool; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(43) “laadpunt, station of pool voor zware bedrijfsvoertuigen”: een laadpunt, station of")
    thisalinea.textcontent.append("pool dat of die bestemd is voor het opladen van zware bedrijfsvoertuigen, hetzij")
    thisalinea.textcontent.append("vanwege het specifieke ontwerp van de connectoren/stekkers, hetzij vanwege het")
    thisalinea.textcontent.append("ontwerp van de parkeerplaats naast het laadpunt, het station en/of de pool;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(44) “laadpool”: een of meer laadstations ..."
    thisalinea.nativeID = 165
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 43
    thisalinea.summary = "(44) “laadpool”: een of meer laadstations op een specifieke locatie; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(44) “laadpool”: een of meer laadstations op een specifieke locatie;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(45) “laadstation”: een enkele fysieke installatie ..."
    thisalinea.nativeID = 166
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 44
    thisalinea.summary = "(45) “laadstation”: een enkele fysieke installatie op een specifieke locatie, bestaande uit een of meer laadpunten; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(45) “laadstation”: een enkele fysieke installatie op een specifieke locatie, bestaande uit")
    thisalinea.textcontent.append("een of meer laadpunten;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(46) “laaddienst”: de verkoop of levering ..."
    thisalinea.nativeID = 167
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 45
    thisalinea.summary = "(46) “laaddienst”: de verkoop of levering van elektriciteit, met inbegrip van aanverwante diensten, via een openbaar toegankelijk laadpunt; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(46) “laaddienst”: de verkoop of levering van elektriciteit, met inbegrip van aanverwante")
    thisalinea.textcontent.append("diensten, via een openbaar toegankelijk laadpunt;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(47) “laadsessie”: het volledige proces van ..."
    thisalinea.nativeID = 168
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 46
    thisalinea.summary = "(47) “laadsessie”: het volledige proces van het opladen van een voertuig op een openbaar toegankelijk laadpunt vanaf het moment waarop het voertuig wordt aangesloten tot het moment waarop het wordt losgekoppeld; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(47) “laadsessie”: het volledige proces van het opladen van een voertuig op een openbaar")
    thisalinea.textcontent.append("toegankelijk laadpunt vanaf het moment waarop het voertuig wordt aangesloten tot")
    thisalinea.textcontent.append("het moment waarop het wordt losgekoppeld;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(48) “ad-hoctankbeurt”: een door een eindgebruiker ..."
    thisalinea.nativeID = 169
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 47
    thisalinea.summary = "(48) “ad-hoctankbeurt”: een door een eindgebruiker aangekochte tankdienst waarvoor hij niet verplicht is zich te registreren, een schriftelijke overeenkomst te sluiten of een commerciële relatie met de exploitant van dat tankpunt aan te gaan voor een langere periode dan de aankoop van de dienst; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(48) “ad-hoctankbeurt”: een door een eindgebruiker aangekochte tankdienst waarvoor hij")
    thisalinea.textcontent.append("niet verplicht is zich te registreren, een schriftelijke overeenkomst te sluiten of een")
    thisalinea.textcontent.append("commerciële relatie met de exploitant van dat tankpunt aan te gaan voor een langere")
    thisalinea.textcontent.append("periode dan de aankoop van de dienst;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(49) “tankpunt”: een tankfaciliteit voor de ..."
    thisalinea.nativeID = 170
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 48
    thisalinea.summary = "(49) “tankpunt”: een tankfaciliteit voor de levering van een vloeibare of gasvormige alternatieve brandstof via een vaste of mobiele installatie, waaraan slechts één voertuig tegelijk kan worden bijgetankt; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(49) “tankpunt”: een tankfaciliteit voor de levering van een vloeibare of gasvormige")
    thisalinea.textcontent.append("alternatieve brandstof via een vaste of mobiele installatie, waaraan slechts één")
    thisalinea.textcontent.append("voertuig tegelijk kan worden bijgetankt;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(50) “tankdienst”: de verkoop of levering ..."
    thisalinea.nativeID = 171
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 49
    thisalinea.summary = "(50) “tankdienst”: de verkoop of levering van een vloeibare of gasvormige alternatieve brandstof via een openbaar toegankelijk tankpunt; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(50) “tankdienst”: de verkoop of levering van een vloeibare of gasvormige alternatieve")
    thisalinea.textcontent.append("brandstof via een openbaar toegankelijk tankpunt;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(51) “tanksessie”: het volledige proces van ..."
    thisalinea.nativeID = 172
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 50
    thisalinea.summary = "(51) “tanksessie”: het volledige proces van het tanken van een voertuig op een openbaar toegankelijk tankpunt vanaf het moment waarop het voertuig wordt aangesloten tot het moment waarop het wordt losgekoppeld; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(51) “tanksessie”: het volledige proces van het tanken van een voertuig op een openbaar")
    thisalinea.textcontent.append("toegankelijk tankpunt vanaf het moment waarop het voertuig wordt aangesloten tot")
    thisalinea.textcontent.append("het moment waarop het wordt losgekoppeld;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(52) “tankstation”: één fysieke installatie op ..."
    thisalinea.nativeID = 173
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 51
    thisalinea.summary = "(52) “tankstation”: één fysieke installatie op een specifieke locatie, bestaande uit een of meer tankpunten; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(52) “tankstation”: één fysieke installatie op een specifieke locatie, bestaande uit een of")
    thisalinea.textcontent.append("meer tankpunten;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = '(53) "regulerende instantie": de door elke ...'
    thisalinea.nativeID = 174
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 52
    thisalinea.summary = '(53) "regulerende instantie": de door elke lidstaat krachtens artikel 57, lid 1, van Richtlijn (EU) 2019/944 aangewezen regulerende instantie; '
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append('(53) "regulerende instantie": de door elke lidstaat krachtens artikel 57, lid 1, van Richtlijn')
    thisalinea.textcontent.append("(EU) 2019/944 aangewezen regulerende instantie;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(54) “hernieuwbare energie”: energie uit hernieuwbare ..."
    thisalinea.nativeID = 175
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 53
    thisalinea.summary = "(54) “hernieuwbare energie”: energie uit hernieuwbare niet-fossiele bronnen als gedefinieerd in artikel 2, punt 1, van Richtlijn (EU) 2018/2001; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(54) “hernieuwbare energie”: energie uit hernieuwbare niet-fossiele bronnen als")
    thisalinea.textcontent.append("gedefinieerd in artikel 2, punt 1, van Richtlijn (EU) 2018/2001;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(55) “ro-ro-passagiersschip”: een schip dat over ..."
    thisalinea.nativeID = 176
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 54
    thisalinea.summary = "(55) “ro-ro-passagiersschip”: een schip dat over de nodige voorzieningen beschikt om weg- of spoorvoertuigen het vaartuig op en af te laten rijden en dat bestemd is voor het vervoer van meer dan twaalf passagiers; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(55) “ro-ro-passagiersschip”: een schip dat over de nodige voorzieningen beschikt om")
    thisalinea.textcontent.append("weg- of spoorvoertuigen het vaartuig op en af te laten rijden en dat bestemd is voor")
    thisalinea.textcontent.append("het vervoer van meer dan twaalf passagiers;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(56) “veilig en beveiligd parkeerterrein”: een ..."
    thisalinea.nativeID = 177
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 55
    thisalinea.summary = "(56) “veilig en beveiligd parkeerterrein”: een parkeer- en rustplaats als bedoeld in artikel 17, lid 1, punt b), die bestemd is voor nachtelijk parkeren van zware bedrijfsvoertuigen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(56) “veilig en beveiligd parkeerterrein”: een parkeer- en rustplaats als bedoeld in")
    thisalinea.textcontent.append("artikel 17, lid 1, punt b), die bestemd is voor nachtelijk parkeren van zware")
    thisalinea.textcontent.append("bedrijfsvoertuigen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(57) “schip op zijn ligplaats”: een ..."
    thisalinea.nativeID = 178
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 56
    thisalinea.summary = "(57) “schip op zijn ligplaats”: een schip op zijn ligplaats als gedefinieerd in artikel 3, punt 1, c), van Verordening (EU) 2015/757; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(57) “schip op zijn ligplaats”: een schip op zijn ligplaats als gedefinieerd in artikel 3,")
    thisalinea.textcontent.append("punt 1, c), van Verordening (EU) 2015/757;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(58) “walstroomvoorziening”: de voorziening van walstroom ..."
    thisalinea.nativeID = 179
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 57
    thisalinea.summary = "(58) “walstroomvoorziening”: de voorziening van walstroom aan zeeschepen of binnenschepen die op de ligplaats liggen door middel van een gestandaardiseerde aansluiting; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(58) “walstroomvoorziening”: de voorziening van walstroom aan zeeschepen of")
    thisalinea.textcontent.append("binnenschepen die op de ligplaats liggen door middel van een gestandaardiseerde")
    thisalinea.textcontent.append("aansluiting;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(59) “slim opladen”: een laadbeurt waarbij ..."
    thisalinea.nativeID = 180
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 58
    thisalinea.summary = "(59) “slim opladen”: een laadbeurt waarbij de intensiteit van de aan de batterij geleverde elektriciteit in realtime wordt aangepast op basis van via elektronische communicatie ontvangen informatie; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(59) “slim opladen”: een laadbeurt waarbij de intensiteit van de aan de batterij geleverde")
    thisalinea.textcontent.append("elektriciteit in realtime wordt aangepast op basis van via elektronische communicatie")
    thisalinea.textcontent.append("ontvangen informatie;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(60) “statische gegevens”: gegevens die niet ..."
    thisalinea.nativeID = 181
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 59
    thisalinea.summary = "(60) “statische gegevens”: gegevens die niet vaak of niet op regelmatige basis wijzigen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(60) “statische gegevens”: gegevens die niet vaak of niet op regelmatige basis wijzigen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(61) “uitgebreid TEN-T-netwerk”: een netwerk als ..."
    thisalinea.nativeID = 182
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 60
    thisalinea.summary = "(61) “uitgebreid TEN-T-netwerk”: een netwerk als gedefinieerd in artikel 9 van Verordening (EU) nr. 1315/2013; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(61) “uitgebreid TEN-T-netwerk”: een netwerk als gedefinieerd in artikel 9 van")
    thisalinea.textcontent.append("Verordening (EU) nr. 1315/2013;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(62) “TEN-T-kernnetwerk”: een netwerk als gedefinieerd ..."
    thisalinea.nativeID = 183
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 61
    thisalinea.summary = "(62) “TEN-T-kernnetwerk”: een netwerk als gedefinieerd in artikel 38 van Verordening (EU) nr. 1315/2013; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(62) “TEN-T-kernnetwerk”: een netwerk als gedefinieerd in artikel 38 van Verordening")
    thisalinea.textcontent.append("(EU) nr. 1315/2013;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(63) “binnenhaven op het TEN-T-kernnetwerk en ..."
    thisalinea.nativeID = 184
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 62
    thisalinea.summary = "(63) “binnenhaven op het TEN-T-kernnetwerk en op het uitgebreide TEN-T-netwerk”: een binnenhaven van het TEN-T-kernnetwerk of uitgebreide TEN-T-netwerk, als genoemd en gecategoriseerd in bijlage II bij Verordening (EU) nr. 1315/2013; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(63) “binnenhaven op het TEN-T-kernnetwerk en op het uitgebreide TEN-T-netwerk”:")
    thisalinea.textcontent.append("een binnenhaven van het TEN-T-kernnetwerk of uitgebreide TEN-T-netwerk, als")
    thisalinea.textcontent.append("genoemd en gecategoriseerd in bijlage II bij Verordening (EU) nr. 1315/2013;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(64) “zeehaven op het TEN-T-kernnetwerk en ..."
    thisalinea.nativeID = 185
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 63
    thisalinea.summary = "(64) “zeehaven op het TEN-T-kernnetwerk en op het uitgebreide TEN-T-netwerk”: een zeehaven van het TEN-T-kernnetwerk of uitgebreide TEN-T-netwerk, als genoemd en gecategoriseerd in bijlage II bij Verordening (EU) nr. 1315/2013; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(64) “zeehaven op het TEN-T-kernnetwerk en op het uitgebreide TEN-T-netwerk”: een")
    thisalinea.textcontent.append("zeehaven van het TEN-T-kernnetwerk of uitgebreide TEN-T-netwerk, als genoemd")
    thisalinea.textcontent.append("en gecategoriseerd in bijlage II bij Verordening (EU) nr. 1315/2013;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(65) “transmissiesysteembeheerder”: een systeembeheerder als gedefinieerd ..."
    thisalinea.nativeID = 186
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 64
    thisalinea.summary = "(65) “transmissiesysteembeheerder”: een systeembeheerder als gedefinieerd in artikel 2, punt 35, van Richtlijn (EU) 2019/944; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(65) “transmissiesysteembeheerder”: een systeembeheerder als gedefinieerd in artikel 2,")
    thisalinea.textcontent.append("punt 35, van Richtlijn (EU) 2019/944;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(66) “stedelijk knooppunt”: een stedelijk knooppunt ..."
    thisalinea.nativeID = 187
    thisalinea.parentID = 110
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 65
    thisalinea.summary = "(66) “stedelijk knooppunt”: een stedelijk knooppunt als gedefinieerd in artikel 3, punt p), van Verordening (EU) nr. 1315/2013. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(66) “stedelijk knooppunt”: een stedelijk knooppunt als gedefinieerd in artikel 3, punt p),")
    thisalinea.textcontent.append("van Verordening (EU) nr. 1315/2013.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 3"
    thisalinea.nativeID = 188
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 10
    thisalinea.summary = "Streefcijfers voor laadinfrastructuur voor lichte elektrische voertuigen Daartoe zorgen de lidstaten ervoor dat aan het einde van elk jaar, met ingang van het in artikel 24 bedoelde jaar, de volgende streefcijfers voor het beschikbare laadvermogen cumulatief worden gehaald: 1. De lidstaten zien er op toe dat: – de uitrol van openbaar toegankelijke laadstations voor lichte voertuigen gelijke tred houdt met de toename van het aantal elektrische lichte voertuigen; – dat de op hun grondgebied geïnstalleerde openbaar toegankelijke laadstations voor lichte voertuigen voldoende vermogen leveren voor die voertuigen. (a) voor elk op hun grondgebied ingeschreven licht batterijvoertuig wordt via openbaar toegankelijke "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Streefcijfers voor laadinfrastructuur voor lichte elektrische voertuigen")
    thisalinea.textcontent.append("Daartoe zorgen de lidstaten ervoor dat aan het einde van elk jaar, met ingang van het")
    thisalinea.textcontent.append("in artikel 24 bedoelde jaar, de volgende streefcijfers voor het beschikbare")
    thisalinea.textcontent.append("laadvermogen cumulatief worden gehaald:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. De lidstaten zien er op ..."
    thisalinea.nativeID = 189
    thisalinea.parentID = 188
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. De lidstaten zien er op toe dat: – de uitrol van openbaar toegankelijke laadstations voor lichte voertuigen gelijke tred houdt met de toename van het aantal elektrische lichte voertuigen; – dat de op hun grondgebied geïnstalleerde openbaar toegankelijke laadstations voor lichte voertuigen voldoende vermogen leveren voor die voertuigen. (a) voor elk op hun grondgebied ingeschreven licht batterijvoertuig wordt via openbaar toegankelijke laadstations een totaal laadvermogen geleverd van ten minste 1 kW; en (b) voor elk op hun grondgebied ingeschreven licht plug-in hybride voertuig wordt via openbaar toegankelijke laadstations een totaal laadvermogen geleverd van ten minste 0,66 kW. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. De lidstaten zien er op toe dat:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– de uitrol van openbaar toegankelijke ..."
    thisalinea.nativeID = 190
    thisalinea.parentID = 189
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "– de uitrol van openbaar toegankelijke laadstations voor lichte voertuigen gelijke tred houdt met de toename van het aantal elektrische lichte voertuigen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– de uitrol van openbaar toegankelijke laadstations voor lichte voertuigen gelijke")
    thisalinea.textcontent.append("tred houdt met de toename van het aantal elektrische lichte voertuigen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "– dat de op hun grondgebied ..."
    thisalinea.nativeID = 191
    thisalinea.parentID = 189
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "– dat de op hun grondgebied geïnstalleerde openbaar toegankelijke laadstations voor lichte voertuigen voldoende vermogen leveren voor die voertuigen. (a) voor elk op hun grondgebied ingeschreven licht batterijvoertuig wordt via openbaar toegankelijke laadstations een totaal laadvermogen geleverd van ten minste 1 kW; en (b) voor elk op hun grondgebied ingeschreven licht plug-in hybride voertuig wordt via openbaar toegankelijke laadstations een totaal laadvermogen geleverd van ten minste 0,66 kW. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– dat de op hun grondgebied geïnstalleerde openbaar toegankelijke laadstations")
    thisalinea.textcontent.append("voor lichte voertuigen voldoende vermogen leveren voor die voertuigen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "(a) voor elk op hun grondgebied ..."
    thisalinea.nativeID = 192
    thisalinea.parentID = 191
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) voor elk op hun grondgebied ingeschreven licht batterijvoertuig wordt via openbaar toegankelijke laadstations een totaal laadvermogen geleverd van ten minste 1 kW; en "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) voor elk op hun grondgebied ingeschreven licht batterijvoertuig wordt via")
    thisalinea.textcontent.append("openbaar toegankelijke laadstations een totaal laadvermogen geleverd van ten")
    thisalinea.textcontent.append("minste 1 kW; en")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "(b) voor elk op hun grondgebied ..."
    thisalinea.nativeID = 193
    thisalinea.parentID = 191
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) voor elk op hun grondgebied ingeschreven licht plug-in hybride voertuig wordt via openbaar toegankelijke laadstations een totaal laadvermogen geleverd van ten minste 0,66 kW. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) voor elk op hun grondgebied ingeschreven licht plug-in hybride voertuig wordt")
    thisalinea.textcontent.append("via openbaar toegankelijke laadstations een totaal laadvermogen geleverd van")
    thisalinea.textcontent.append("ten minste 0,66 kW.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. De lidstaten zorgen op hun ..."
    thisalinea.nativeID = 194
    thisalinea.parentID = 188
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. De lidstaten zorgen op hun wegennet voor een minimumdekking van openbaar toegankelijke laadpunten voor lichte voertuigen. Met het oog daarop zorgen de lidstaten ervoor dat: (a) op het TEN-T-kernnetwerk in elke rijrichting op onderlinge afstanden van maximaal 60 km openbaar toegankelijke laadpools voor lichte voertuigen worden geïnstalleerd die voldoen aan de volgende eisen: i) uiterlijk op 31 december 2025 levert elke laadpool een laadvermogen van ten minste 300 kW en omvat hij ten minste één laadstation met een individueel laadvermogen van ten minste 150 kW; ii) uiterlijk op 31 december 2030 levert elke laadpool een laadvermogen van ten minste "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. De lidstaten zorgen op hun wegennet voor een minimumdekking van openbaar")
    thisalinea.textcontent.append("toegankelijke laadpunten voor lichte voertuigen. Met het oog daarop zorgen de")
    thisalinea.textcontent.append("lidstaten ervoor dat:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "(a) op het TEN-T-kernnetwerk in elke ..."
    thisalinea.nativeID = 195
    thisalinea.parentID = 194
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) op het TEN-T-kernnetwerk in elke rijrichting op onderlinge afstanden van maximaal 60 km openbaar toegankelijke laadpools voor lichte voertuigen worden geïnstalleerd die voldoen aan de volgende eisen: i) uiterlijk op 31 december 2025 levert elke laadpool een laadvermogen van ten minste 300 kW en omvat hij ten minste één laadstation met een individueel laadvermogen van ten minste 150 kW; ii) uiterlijk op 31 december 2030 levert elke laadpool een laadvermogen van ten minste 600 kW en omvat hij ten minste twee laadstations met een individueel laadvermogen van ten minste 150 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) op het TEN-T-kernnetwerk in elke rijrichting op onderlinge afstanden van")
    thisalinea.textcontent.append("maximaal 60 km openbaar toegankelijke laadpools voor lichte voertuigen")
    thisalinea.textcontent.append("worden geïnstalleerd die voldoen aan de volgende eisen:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 5
    thisalinea.texttitle = "i) uiterlijk op 31 december 2025 ..."
    thisalinea.nativeID = 196
    thisalinea.parentID = 195
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i) uiterlijk op 31 december 2025 levert elke laadpool een laadvermogen van ten minste 300 kW en omvat hij ten minste één laadstation met een individueel laadvermogen van ten minste 150 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i) uiterlijk op 31 december 2025 levert elke laadpool een")
    thisalinea.textcontent.append("laadvermogen van ten minste 300 kW en omvat hij ten minste één")
    thisalinea.textcontent.append("laadstation met een individueel laadvermogen van ten minste")
    thisalinea.textcontent.append("150 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 5
    thisalinea.texttitle = "ii) uiterlijk op 31 december 2030 ..."
    thisalinea.nativeID = 197
    thisalinea.parentID = 195
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii) uiterlijk op 31 december 2030 levert elke laadpool een laadvermogen van ten minste 600 kW en omvat hij ten minste twee laadstations met een individueel laadvermogen van ten minste 150 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii) uiterlijk op 31 december 2030 levert elke laadpool een")
    thisalinea.textcontent.append("laadvermogen van ten minste 600 kW en omvat hij ten minste twee")
    thisalinea.textcontent.append("laadstations met een individueel laadvermogen van ten minste")
    thisalinea.textcontent.append("150 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "(b) op het uitgebreide TEN-T-netwerk in ..."
    thisalinea.nativeID = 198
    thisalinea.parentID = 194
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) op het uitgebreide TEN-T-netwerk in elke rijrichting op onderlinge afstanden van maximaal 60 km openbaar toegankelijke laadpools voor lichte voertuigen worden geïnstalleerd die voldoen aan de volgende eisen: i) uiterlijk op 31 december 2030 levert elke laadpool een vermogen van ten minste 300 kW en omvat hij ten minste één laadstation met een individueel vermogen van ten minste 150 kW; ii) uiterlijk op 31 december 2035 levert elke laadpool een laadvermogen van ten minste 600 kW en omvat hij ten minste twee laadstations met een individueel laadvermogen van ten minste 150 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) op het uitgebreide TEN-T-netwerk in elke rijrichting op onderlinge afstanden")
    thisalinea.textcontent.append("van maximaal 60 km openbaar toegankelijke laadpools voor lichte voertuigen")
    thisalinea.textcontent.append("worden geïnstalleerd die voldoen aan de volgende eisen:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 5
    thisalinea.texttitle = "i) uiterlijk op 31 december 2030 ..."
    thisalinea.nativeID = 199
    thisalinea.parentID = 198
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i) uiterlijk op 31 december 2030 levert elke laadpool een vermogen van ten minste 300 kW en omvat hij ten minste één laadstation met een individueel vermogen van ten minste 150 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i) uiterlijk op 31 december 2030 levert elke laadpool een vermogen")
    thisalinea.textcontent.append("van ten minste 300 kW en omvat hij ten minste één laadstation met")
    thisalinea.textcontent.append("een individueel vermogen van ten minste 150 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 5
    thisalinea.texttitle = "ii) uiterlijk op 31 december 2035 ..."
    thisalinea.nativeID = 200
    thisalinea.parentID = 198
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii) uiterlijk op 31 december 2035 levert elke laadpool een laadvermogen van ten minste 600 kW en omvat hij ten minste twee laadstations met een individueel laadvermogen van ten minste 150 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii) uiterlijk op 31 december 2035 levert elke laadpool een")
    thisalinea.textcontent.append("laadvermogen van ten minste 600 kW en omvat hij ten minste twee")
    thisalinea.textcontent.append("laadstations met een individueel laadvermogen van ten minste")
    thisalinea.textcontent.append("150 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Naburige lidstaten zorgen ervoor dat ..."
    thisalinea.nativeID = 201
    thisalinea.parentID = 188
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Naburige lidstaten zorgen ervoor dat de in de punten a) en b) bedoelde maximumafstanden op grensoverschrijdende wegen van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk niet worden overschreden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Naburige lidstaten zorgen ervoor dat de in de punten a) en b) bedoelde")
    thisalinea.textcontent.append("maximumafstanden op grensoverschrijdende wegen van het TEN-T-kernnetwerk en")
    thisalinea.textcontent.append("het uitgebreide TEN-T-netwerk niet worden overschreden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 4"
    thisalinea.nativeID = 202
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 11
    thisalinea.summary = "Streefcijfers voor laadinfrastructuur voor zware elektrische bedrijfsvoertuigen 1. De lidstaten zorgen op hun grondgebied voor een minimumdekking van openbaar toegankelijke laadpunten voor zware bedrijfsvoertuigen. Met het oog daarop zorgen de lidstaten ervoor dat: (a) op het TEN-T-kernnetwerk in elke rijrichting op onderlinge afstanden van maximaal 60 km openbaar toegankelijke laadpools voor zware bedrijfsvoertuigen worden geïnstalleerd die voldoen aan de volgende eisen: i) uiterlijk op 31 december 2025 levert elke laadpool een laadvermogen van ten minste 1400 kW en omvat hij ten minste één laadstation met een individueel laadvermogen van ten minste 350 kW; ii) uiterlijk op 31 december 2030 levert "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Streefcijfers voor laadinfrastructuur voor zware elektrische bedrijfsvoertuigen")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. De lidstaten zorgen op hun ..."
    thisalinea.nativeID = 203
    thisalinea.parentID = 202
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. De lidstaten zorgen op hun grondgebied voor een minimumdekking van openbaar toegankelijke laadpunten voor zware bedrijfsvoertuigen. Met het oog daarop zorgen de lidstaten ervoor dat: (a) op het TEN-T-kernnetwerk in elke rijrichting op onderlinge afstanden van maximaal 60 km openbaar toegankelijke laadpools voor zware bedrijfsvoertuigen worden geïnstalleerd die voldoen aan de volgende eisen: i) uiterlijk op 31 december 2025 levert elke laadpool een laadvermogen van ten minste 1400 kW en omvat hij ten minste één laadstation met een individueel laadvermogen van ten minste 350 kW; ii) uiterlijk op 31 december 2030 levert elke laadpool een laadvermogen van ten minste "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. De lidstaten zorgen op hun grondgebied voor een minimumdekking van openbaar")
    thisalinea.textcontent.append("toegankelijke laadpunten voor zware bedrijfsvoertuigen. Met het oog daarop zorgen")
    thisalinea.textcontent.append("de lidstaten ervoor dat:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) op het TEN-T-kernnetwerk in elke ..."
    thisalinea.nativeID = 204
    thisalinea.parentID = 203
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) op het TEN-T-kernnetwerk in elke rijrichting op onderlinge afstanden van maximaal 60 km openbaar toegankelijke laadpools voor zware bedrijfsvoertuigen worden geïnstalleerd die voldoen aan de volgende eisen: i) uiterlijk op 31 december 2025 levert elke laadpool een laadvermogen van ten minste 1400 kW en omvat hij ten minste één laadstation met een individueel laadvermogen van ten minste 350 kW; ii) uiterlijk op 31 december 2030 levert elke laadpool een laadvermogen van ten minste 3500 kW en omvat hij ten minste twee laadstations met een individueel vermogen van ten minste 350 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) op het TEN-T-kernnetwerk in elke rijrichting op onderlinge afstanden van")
    thisalinea.textcontent.append("maximaal 60 km openbaar toegankelijke laadpools voor zware")
    thisalinea.textcontent.append("bedrijfsvoertuigen worden geïnstalleerd die voldoen aan de volgende eisen:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "i) uiterlijk op 31 december 2025 ..."
    thisalinea.nativeID = 205
    thisalinea.parentID = 204
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i) uiterlijk op 31 december 2025 levert elke laadpool een laadvermogen van ten minste 1400 kW en omvat hij ten minste één laadstation met een individueel laadvermogen van ten minste 350 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i) uiterlijk op 31 december 2025 levert elke laadpool een")
    thisalinea.textcontent.append("laadvermogen van ten minste 1400 kW en omvat hij ten minste één")
    thisalinea.textcontent.append("laadstation met een individueel laadvermogen van ten minste")
    thisalinea.textcontent.append("350 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "ii) uiterlijk op 31 december 2030 ..."
    thisalinea.nativeID = 206
    thisalinea.parentID = 204
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii) uiterlijk op 31 december 2030 levert elke laadpool een laadvermogen van ten minste 3500 kW en omvat hij ten minste twee laadstations met een individueel vermogen van ten minste 350 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii) uiterlijk op 31 december 2030 levert elke laadpool een")
    thisalinea.textcontent.append("laadvermogen van ten minste 3500 kW en omvat hij ten minste")
    thisalinea.textcontent.append("twee laadstations met een individueel vermogen van ten minste")
    thisalinea.textcontent.append("350 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) op het uitgebreide TEN-T-netwerk worden ..."
    thisalinea.nativeID = 207
    thisalinea.parentID = 203
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) op het uitgebreide TEN-T-netwerk worden in elke rijrichting op onderlinge afstanden van maximaal 100 km openbaar toegankelijke laadpools voor zware bedrijfsvoertuigen geïnstalleerd die voldoen aan de volgende eisen: i) uiterlijk op 31 december 2030 levert elke laadpool een laadvermogen van ten minste 1400 kW en omvat hij ten minste één laadstation met een individueel laadvermogen van ten minste 350 kW; ii) uiterlijk op 31 december 2035 levert elke laadpool een laadvermogen van ten minste 3500 kW en omvat hij ten minste twee laadstations met een individueel laadvermogen van ten minste 350 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) op het uitgebreide TEN-T-netwerk worden in elke rijrichting op onderlinge")
    thisalinea.textcontent.append("afstanden van maximaal 100 km openbaar toegankelijke laadpools voor zware")
    thisalinea.textcontent.append("bedrijfsvoertuigen geïnstalleerd die voldoen aan de volgende eisen:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "i) uiterlijk op 31 december 2030 ..."
    thisalinea.nativeID = 208
    thisalinea.parentID = 207
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i) uiterlijk op 31 december 2030 levert elke laadpool een laadvermogen van ten minste 1400 kW en omvat hij ten minste één laadstation met een individueel laadvermogen van ten minste 350 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i) uiterlijk op 31 december 2030 levert elke laadpool een")
    thisalinea.textcontent.append("laadvermogen van ten minste 1400 kW en omvat hij ten minste één")
    thisalinea.textcontent.append("laadstation met een individueel laadvermogen van ten minste")
    thisalinea.textcontent.append("350 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "ii) uiterlijk op 31 december 2035 ..."
    thisalinea.nativeID = 209
    thisalinea.parentID = 207
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii) uiterlijk op 31 december 2035 levert elke laadpool een laadvermogen van ten minste 3500 kW en omvat hij ten minste twee laadstations met een individueel laadvermogen van ten minste 350 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii) uiterlijk op 31 december 2035 levert elke laadpool een")
    thisalinea.textcontent.append("laadvermogen van ten minste 3500 kW en omvat hij ten minste")
    thisalinea.textcontent.append("twee laadstations met een individueel laadvermogen van ten minste")
    thisalinea.textcontent.append("350 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(c) elk veilig en beveiligd parkeerterrein ..."
    thisalinea.nativeID = 210
    thisalinea.parentID = 203
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(c) elk veilig en beveiligd parkeerterrein uiterlijk op 31 december 2030 is uitgerust met ten minste één laadstation voor zware bedrijfsvoertuigen met een laadvermogen van ten minste 100 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(c) elk veilig en beveiligd parkeerterrein uiterlijk op 31 december 2030 is uitgerust")
    thisalinea.textcontent.append("met ten minste één laadstation voor zware bedrijfsvoertuigen met een")
    thisalinea.textcontent.append("laadvermogen van ten minste 100 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(d) elk stedelijk knooppunt uiterlijk op ..."
    thisalinea.nativeID = 211
    thisalinea.parentID = 203
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "(d) elk stedelijk knooppunt uiterlijk op 31 december 2025 beschikt over openbaar toegankelijke laadpunten voor zware bedrijfsvoertuigen met een totaal laadvermogen van ten minste 600 kW, geleverd door laadstations met een individueel laadvermogen van ten minste 150 kW; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(d) elk stedelijk knooppunt uiterlijk op 31 december 2025 beschikt over openbaar")
    thisalinea.textcontent.append("toegankelijke laadpunten voor zware bedrijfsvoertuigen met een totaal")
    thisalinea.textcontent.append("laadvermogen van ten minste 600 kW, geleverd door laadstations met een")
    thisalinea.textcontent.append("individueel laadvermogen van ten minste 150 kW;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(e) elk stedelijk knooppunt uiterlijk op ..."
    thisalinea.nativeID = 212
    thisalinea.parentID = 203
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "(e) elk stedelijk knooppunt uiterlijk op 31 december 2030 beschikt over openbaar toegankelijke laadpunten voor zware bedrijfsvoertuigen met een totaal laadvermogen van ten minste 1 200 kW, geleverd door laadstations met een individueel laadvermogen van ten minste 150 kW. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(e) elk stedelijk knooppunt uiterlijk op 31 december 2030 beschikt over openbaar")
    thisalinea.textcontent.append("toegankelijke laadpunten voor zware bedrijfsvoertuigen met een totaal")
    thisalinea.textcontent.append("laadvermogen van ten minste 1 200 kW, geleverd door laadstations met een")
    thisalinea.textcontent.append("individueel laadvermogen van ten minste 150 kW.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Naburige lidstaten zorgen ervoor dat ..."
    thisalinea.nativeID = 213
    thisalinea.parentID = 202
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Naburige lidstaten zorgen ervoor dat de onder a) en b) bedoelde maximumafstanden op grensoverschrijdende wegen van het TEN-T-kernnetwerk en het uitgebreide TEN- T-netwerk niet worden overschreden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Naburige lidstaten zorgen ervoor dat de onder a) en b) bedoelde maximumafstanden")
    thisalinea.textcontent.append("op grensoverschrijdende wegen van het TEN-T-kernnetwerk en het uitgebreide TEN-")
    thisalinea.textcontent.append("T-netwerk niet worden overschreden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 5"
    thisalinea.nativeID = 214
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 12
    thisalinea.summary = "Laadinfrastructuur Met ingang van 1 januari 2027 zorgen exploitanten van laadpunten ervoor dat alle door hen geëxploiteerde openbaar toegankelijke laadstations met een laadvermogen van 50 kW of meer voldoen aan de eis van punt b). De in de punten a) en b) vastgestelde eisen zijn niet van toepassing op openbaar toegankelijke laadpunten waarbij de laaddienst gratis wordt verleend. 1. Exploitanten van openbaar toegankelijke laadstations kunnen kiezen van welke elektriciteitsleverancier uit de Unie zij elektriciteit afnemen, mits de leverancier daarmee instemt. 2. Exploitanten van laadpunten bieden eindgebruikers op de door hen geëxploiteerde openbaar toegankelijke laadpunten de mogelijkheid om hun elektrisch voertuig "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Laadinfrastructuur")
    thisalinea.textcontent.append("Met ingang van 1 januari 2027 zorgen exploitanten van laadpunten ervoor dat alle")
    thisalinea.textcontent.append("door hen geëxploiteerde openbaar toegankelijke laadstations met een laadvermogen")
    thisalinea.textcontent.append("van 50 kW of meer voldoen aan de eis van punt b).")
    thisalinea.textcontent.append("De in de punten a) en b) vastgestelde eisen zijn niet van toepassing op openbaar")
    thisalinea.textcontent.append("toegankelijke laadpunten waarbij de laaddienst gratis wordt verleend.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Exploitanten van openbaar toegankelijke laadstations ..."
    thisalinea.nativeID = 215
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Exploitanten van openbaar toegankelijke laadstations kunnen kiezen van welke elektriciteitsleverancier uit de Unie zij elektriciteit afnemen, mits de leverancier daarmee instemt. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Exploitanten van openbaar toegankelijke laadstations kunnen kiezen van welke")
    thisalinea.textcontent.append("elektriciteitsleverancier uit de Unie zij elektriciteit afnemen, mits de leverancier")
    thisalinea.textcontent.append("daarmee instemt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Exploitanten van laadpunten bieden eindgebruikers ..."
    thisalinea.nativeID = 216
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Exploitanten van laadpunten bieden eindgebruikers op de door hen geëxploiteerde openbaar toegankelijke laadpunten de mogelijkheid om hun elektrisch voertuig op ad-hocbasis te herladen met behulp van een in de Unie gangbaar betaalinstrument. Daartoe: (a) aanvaarden exploitanten van laadpunten in openbaar toegankelijke laadstations met een laadvermogen van minder dan 50 kW die vanaf de in artikel 24 bedoelde datum worden geïnstalleerd, elektronische betalingen via terminals en apparatuur die voor betalingsdiensten worden gebruikt, met inbegrip van ten minste een van de volgende elementen: i) betaalkaartlezers; ii) apparatuur voor contactloos betalen die ten minste in staat is betaalkaarten te lezen; iii) apparaten "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Exploitanten van laadpunten bieden eindgebruikers op de door hen geëxploiteerde")
    thisalinea.textcontent.append("openbaar toegankelijke laadpunten de mogelijkheid om hun elektrisch voertuig op")
    thisalinea.textcontent.append("ad-hocbasis te herladen met behulp van een in de Unie gangbaar betaalinstrument.")
    thisalinea.textcontent.append("Daartoe:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) aanvaarden exploitanten van laadpunten in ..."
    thisalinea.nativeID = 217
    thisalinea.parentID = 216
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) aanvaarden exploitanten van laadpunten in openbaar toegankelijke laadstations met een laadvermogen van minder dan 50 kW die vanaf de in artikel 24 bedoelde datum worden geïnstalleerd, elektronische betalingen via terminals en apparatuur die voor betalingsdiensten worden gebruikt, met inbegrip van ten minste een van de volgende elementen: i) betaalkaartlezers; ii) apparatuur voor contactloos betalen die ten minste in staat is betaalkaarten te lezen; iii) apparaten met een internetverbinding, die bijvoorbeeld een specifieke QR-code kunnen genereren die voor de betaaltransactie kan worden gebruikt; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) aanvaarden exploitanten van laadpunten in openbaar toegankelijke laadstations")
    thisalinea.textcontent.append("met een laadvermogen van minder dan 50 kW die vanaf de in artikel 24")
    thisalinea.textcontent.append("bedoelde datum worden geïnstalleerd, elektronische betalingen via terminals en")
    thisalinea.textcontent.append("apparatuur die voor betalingsdiensten worden gebruikt, met inbegrip van ten")
    thisalinea.textcontent.append("minste een van de volgende elementen:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "i) betaalkaartlezers; "
    thisalinea.nativeID = 218
    thisalinea.parentID = 217
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i) betaalkaartlezers; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i) betaalkaartlezers;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "ii) apparatuur voor contactloos betalen die ..."
    thisalinea.nativeID = 219
    thisalinea.parentID = 217
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii) apparatuur voor contactloos betalen die ten minste in staat is betaalkaarten te lezen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii) apparatuur voor contactloos betalen die ten minste in staat is")
    thisalinea.textcontent.append("betaalkaarten te lezen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "iii) apparaten met een internetverbinding, die ..."
    thisalinea.nativeID = 220
    thisalinea.parentID = 217
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "iii) apparaten met een internetverbinding, die bijvoorbeeld een specifieke QR-code kunnen genereren die voor de betaaltransactie kan worden gebruikt; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("iii) apparaten met een internetverbinding, die bijvoorbeeld een specifieke")
    thisalinea.textcontent.append("QR-code kunnen genereren die voor de betaaltransactie kan worden")
    thisalinea.textcontent.append("gebruikt;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) aanvaarden exploitanten van laadpunten in ..."
    thisalinea.nativeID = 221
    thisalinea.parentID = 216
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) aanvaarden exploitanten van laadpunten in openbaar toegankelijke laadstations met een laadvermogen van 50 kW of meer die vanaf de in artikel 24 bedoelde datum worden geïnstalleerd, elektronische betalingen via terminals en apparatuur die voor betalingsdiensten worden gebruikt, met inbegrip van ten minste een van de volgende elementen: i) betaalkaartlezers; ii) apparatuur voor contactloos betalen die ten minste in staat is betaalkaarten te lezen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) aanvaarden exploitanten van laadpunten in openbaar toegankelijke laadstations")
    thisalinea.textcontent.append("met een laadvermogen van 50 kW of meer die vanaf de in artikel 24 bedoelde")
    thisalinea.textcontent.append("datum worden geïnstalleerd, elektronische betalingen via terminals en")
    thisalinea.textcontent.append("apparatuur die voor betalingsdiensten worden gebruikt, met inbegrip van ten")
    thisalinea.textcontent.append("minste een van de volgende elementen:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "i) betaalkaartlezers; "
    thisalinea.nativeID = 222
    thisalinea.parentID = 221
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i) betaalkaartlezers; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i) betaalkaartlezers;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "ii) apparatuur voor contactloos betalen die ..."
    thisalinea.nativeID = 223
    thisalinea.parentID = 221
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii) apparatuur voor contactloos betalen die ten minste in staat is betaalkaarten te lezen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii) apparatuur voor contactloos betalen die ten minste in staat is")
    thisalinea.textcontent.append("betaalkaarten te lezen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Wanneer exploitanten van laadpunten op ..."
    thisalinea.nativeID = 224
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Wanneer exploitanten van laadpunten op een door hen geëxploiteerd openbaar toegankelijk laadpunt automatische authenticatie aanbieden, dienen zij eindgebruikers de mogelijkheid te bieden geen gebruik te maken van de automatische authenticatie; in dat geval moeten eindgebruikers de mogelijkheid krijgen hun voertuig op ad-hocbasis op te laden, zoals bepaald in lid 3, of gebruik te maken van een andere contractuele laadoplossing die op dat laadpunt wordt aangeboden. Op elk openbaar toegankelijk laadpunt dat zij exploiteren en waar zij automatische authenticatie beschikbaar stellen, duiden exploitanten van laadpunten op transparante wijze aan dat die optie beschikbaar is en bieden zij deze op een "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Wanneer exploitanten van laadpunten op een door hen geëxploiteerd openbaar")
    thisalinea.textcontent.append("toegankelijk laadpunt automatische authenticatie aanbieden, dienen zij")
    thisalinea.textcontent.append("eindgebruikers de mogelijkheid te bieden geen gebruik te maken van de")
    thisalinea.textcontent.append("automatische authenticatie; in dat geval moeten eindgebruikers de mogelijkheid")
    thisalinea.textcontent.append("krijgen hun voertuig op ad-hocbasis op te laden, zoals bepaald in lid 3, of gebruik te")
    thisalinea.textcontent.append("maken van een andere contractuele laadoplossing die op dat laadpunt wordt")
    thisalinea.textcontent.append("aangeboden. Op elk openbaar toegankelijk laadpunt dat zij exploiteren en waar zij")
    thisalinea.textcontent.append("automatische authenticatie beschikbaar stellen, duiden exploitanten van laadpunten")
    thisalinea.textcontent.append("op transparante wijze aan dat die optie beschikbaar is en bieden zij deze op een")
    thisalinea.textcontent.append("handige manier aan de eindgebruiker aan.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. De prijzen die exploitanten van ..."
    thisalinea.nativeID = 225
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. De prijzen die exploitanten van openbaar toegankelijke laadpunten in rekening brengen, moeten redelijk, gemakkelijk en duidelijk vergelijkbaar, transparant en niet- discriminerend zijn. Exploitanten van openbaar toegankelijke laadpunten mogen geen onderscheid maken tussen de prijzen die worden aangerekend aan eindgebruikers en aan aanbieders van mobiliteitsdiensten, noch tussen de prijzen die aan verschillende aanbieders van mobiliteitsdiensten worden aangerekend. In voorkomend geval mag het prijsniveau alleen op evenredige wijze worden gedifferentieerd, op basis van een objectieve rechtvaardiging. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. De prijzen die exploitanten van openbaar toegankelijke laadpunten in rekening")
    thisalinea.textcontent.append("brengen, moeten redelijk, gemakkelijk en duidelijk vergelijkbaar, transparant en niet-")
    thisalinea.textcontent.append("discriminerend zijn. Exploitanten van openbaar toegankelijke laadpunten mogen")
    thisalinea.textcontent.append("geen onderscheid maken tussen de prijzen die worden aangerekend aan")
    thisalinea.textcontent.append("eindgebruikers en aan aanbieders van mobiliteitsdiensten, noch tussen de prijzen die")
    thisalinea.textcontent.append("aan verschillende aanbieders van mobiliteitsdiensten worden aangerekend. In")
    thisalinea.textcontent.append("voorkomend geval mag het prijsniveau alleen op evenredige wijze worden")
    thisalinea.textcontent.append("gedifferentieerd, op basis van een objectieve rechtvaardiging.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5. Exploitanten van laadpunten vermelden de ..."
    thisalinea.nativeID = 226
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "5. Exploitanten van laadpunten vermelden de ad-hocprijs en alle componenten daarvan duidelijk op alle door hen geëxploiteerde openbaar toegankelijke laadpunten, zodat de eindgebruikers die tarieven kennen alvorens zij een laadsessie beginnen. Ten minste de volgende prijscomponenten, indien van toepassing op het laadstation, moeten duidelijk worden weergegeven: – de prijs per sessie, – de prijs per minuut, – de prijs per kWh. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("5. Exploitanten van laadpunten vermelden de ad-hocprijs en alle componenten daarvan")
    thisalinea.textcontent.append("duidelijk op alle door hen geëxploiteerde openbaar toegankelijke laadpunten, zodat")
    thisalinea.textcontent.append("de eindgebruikers die tarieven kennen alvorens zij een laadsessie beginnen. Ten")
    thisalinea.textcontent.append("minste de volgende prijscomponenten, indien van toepassing op het laadstation,")
    thisalinea.textcontent.append("moeten duidelijk worden weergegeven:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 5
    thisalinea.texttitle = "– de prijs per sessie, "
    thisalinea.nativeID = 227
    thisalinea.parentID = 226
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "– de prijs per sessie, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– de prijs per sessie,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 5
    thisalinea.texttitle = "– de prijs per minuut, "
    thisalinea.nativeID = 228
    thisalinea.parentID = 226
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "– de prijs per minuut, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– de prijs per minuut,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 5
    thisalinea.texttitle = "– de prijs per kWh. "
    thisalinea.nativeID = 229
    thisalinea.parentID = 226
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "– de prijs per kWh. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– de prijs per kWh.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "6. De prijzen die aanbieders van ..."
    thisalinea.nativeID = 230
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "6. De prijzen die aanbieders van mobiliteitsdiensten aan eindgebruikers in rekening brengen, moeten redelijk, transparant en niet-discriminerend zijn. Aanbieders van mobiliteitsdiensten stellen eindgebruikers vóór het begin van een laadsessie via vrij toegankelijke, breed ondersteunde elektronische middelen alle prijsinformatie ter beschikking die op hun geplande laadsessie van toepassing is; daarbij wordt duidelijk onderscheid gemaakt tussen de prijscomponenten die de exploitant van het laadpunt in rekening brengt, de toepasselijke e-roamingkosten en andere door de aanbieder van mobiliteitsdiensten aangerekende vergoedingen of kosten. De vergoedingen moeten redelijk, transparant en niet-discriminerend zijn. Er mogen geen extra kosten voor grensoverschrijdende e-roaming worden aangerekend. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("6. De prijzen die aanbieders van mobiliteitsdiensten aan eindgebruikers in rekening")
    thisalinea.textcontent.append("brengen, moeten redelijk, transparant en niet-discriminerend zijn. Aanbieders van")
    thisalinea.textcontent.append("mobiliteitsdiensten stellen eindgebruikers vóór het begin van een laadsessie via vrij")
    thisalinea.textcontent.append("toegankelijke, breed ondersteunde elektronische middelen alle prijsinformatie ter")
    thisalinea.textcontent.append("beschikking die op hun geplande laadsessie van toepassing is; daarbij wordt duidelijk")
    thisalinea.textcontent.append("onderscheid gemaakt tussen de prijscomponenten die de exploitant van het laadpunt")
    thisalinea.textcontent.append("in rekening brengt, de toepasselijke e-roamingkosten en andere door de aanbieder")
    thisalinea.textcontent.append("van mobiliteitsdiensten aangerekende vergoedingen of kosten. De vergoedingen")
    thisalinea.textcontent.append("moeten redelijk, transparant en niet-discriminerend zijn. Er mogen geen extra kosten")
    thisalinea.textcontent.append("voor grensoverschrijdende e-roaming worden aangerekend.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "7. Vanaf de in artikel 24 ..."
    thisalinea.nativeID = 231
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "7. Vanaf de in artikel 24 bedoelde datum zorgen exploitanten van laadpunten ervoor dat alle door hen geëxploiteerde openbaar toegankelijke laadpunten digitaal geconnecteerd zijn. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("7. Vanaf de in artikel 24 bedoelde datum zorgen exploitanten van laadpunten ervoor dat")
    thisalinea.textcontent.append("alle door hen geëxploiteerde openbaar toegankelijke laadpunten digitaal")
    thisalinea.textcontent.append("geconnecteerd zijn.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "8. Vanaf de in artikel 24 ..."
    thisalinea.nativeID = 232
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "8. Vanaf de in artikel 24 bedoelde datum zorgen exploitanten van laadpunten ervoor dat alle door hen geëxploiteerde openbaar toegankelijke laadpunten voor normaal vermogen uitgerust zijn om slim te kunnen laden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("8. Vanaf de in artikel 24 bedoelde datum zorgen exploitanten van laadpunten ervoor dat")
    thisalinea.textcontent.append("alle door hen geëxploiteerde openbaar toegankelijke laadpunten voor normaal")
    thisalinea.textcontent.append("vermogen uitgerust zijn om slim te kunnen laden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "9. De lidstaten nemen de nodige ..."
    thisalinea.nativeID = 233
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "9. De lidstaten nemen de nodige maatregelen om ervoor te zorgen dat op parkeer- en rustplaatsen op het TEN-T-wegennet waar infrastructuur voor alternatieve brandstoffen is geïnstalleerd passende bewegwijzering wordt aangebracht, zodat gebruikers de exacte plaats van de infrastructuur voor alternatieve brandstoffen gemakkelijk kunnen vinden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("9. De lidstaten nemen de nodige maatregelen om ervoor te zorgen dat op parkeer- en")
    thisalinea.textcontent.append("rustplaatsen op het TEN-T-wegennet waar infrastructuur voor alternatieve")
    thisalinea.textcontent.append("brandstoffen is geïnstalleerd passende bewegwijzering wordt aangebracht, zodat")
    thisalinea.textcontent.append("gebruikers de exacte plaats van de infrastructuur voor alternatieve brandstoffen")
    thisalinea.textcontent.append("gemakkelijk kunnen vinden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "10. Exploitanten van openbaar toegankelijke laadpunten ..."
    thisalinea.nativeID = 234
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 9
    thisalinea.summary = "10. Exploitanten van openbaar toegankelijke laadpunten zorgen ervoor dat alle door hen geëxploiteerde openbaar toegankelijke laadpunten met gelijkstroom (DC) uitgerust zijn met een vaste laadkabel. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("10. Exploitanten van openbaar toegankelijke laadpunten zorgen ervoor dat alle door hen")
    thisalinea.textcontent.append("geëxploiteerde openbaar toegankelijke laadpunten met gelijkstroom (DC) uitgerust")
    thisalinea.textcontent.append("zijn met een vaste laadkabel.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "11. Als de exploitant van een ..."
    thisalinea.nativeID = 235
    thisalinea.parentID = 214
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 10
    thisalinea.summary = "11. Als de exploitant van een laadpunt niet de eigenaar is van dat punt, stelt de eigenaar de exploitant, overeenkomstig de tussen beide getroffen regelingen, een laadpunt ter beschikking waarvan de technische kenmerken hem in staat stellen te voldoen aan de in de leden 1, 3, 7, 8 en 10 vastgestelde eisen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("11. Als de exploitant van een laadpunt niet de eigenaar is van dat punt, stelt de eigenaar")
    thisalinea.textcontent.append("de exploitant, overeenkomstig de tussen beide getroffen regelingen, een laadpunt ter")
    thisalinea.textcontent.append("beschikking waarvan de technische kenmerken hem in staat stellen te voldoen aan de")
    thisalinea.textcontent.append("in de leden 1, 3, 7, 8 en 10 vastgestelde eisen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 6"
    thisalinea.nativeID = 236
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 13
    thisalinea.summary = "Streefcijfers voor waterstoftankinfrastructuur voor wegvoertuigen Daartoe zorgen de lidstaten ervoor dat het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk uiterlijk op 31 december 2030 worden uitgerust met openbaar toegankelijke waterstoftankstations met een minimumcapaciteit van 2 t/dag en met een dispenser van ten minste 700 bar; de onderlinge afstand tussen die tankstations bedraagt maximaal 150 km. Vloeibare waterstof moet beschikbaar worden gesteld in openbaar toegankelijke tankstations, waartussen de onderlinge afstand maximaal 450 km bedraagt. Zij zorgen ervoor dat uiterlijk op 31 december 2030 in elk stedelijk knooppunt ten minste één openbaar toegankelijk waterstoftankstation beschikbaar is. Voor de installatie van die tankstations wordt een "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Streefcijfers voor waterstoftankinfrastructuur voor wegvoertuigen")
    thisalinea.textcontent.append("Daartoe zorgen de lidstaten ervoor dat het TEN-T-kernnetwerk en het uitgebreide")
    thisalinea.textcontent.append("TEN-T-netwerk uiterlijk op 31 december 2030 worden uitgerust met openbaar")
    thisalinea.textcontent.append("toegankelijke waterstoftankstations met een minimumcapaciteit van 2 t/dag en met")
    thisalinea.textcontent.append("een dispenser van ten minste 700 bar; de onderlinge afstand tussen die tankstations")
    thisalinea.textcontent.append("bedraagt maximaal 150 km. Vloeibare waterstof moet beschikbaar worden gesteld in")
    thisalinea.textcontent.append("openbaar toegankelijke tankstations, waartussen de onderlinge afstand maximaal")
    thisalinea.textcontent.append("450 km bedraagt.")
    thisalinea.textcontent.append("Zij zorgen ervoor dat uiterlijk op 31 december 2030 in elk stedelijk knooppunt ten")
    thisalinea.textcontent.append("minste één openbaar toegankelijk waterstoftankstation beschikbaar is. Voor de")
    thisalinea.textcontent.append("installatie van die tankstations wordt een analyse gemaakt van de beste locatie,")
    thisalinea.textcontent.append("rekening houdend met de uitrol van dergelijke stations in multimodale knooppunten")
    thisalinea.textcontent.append("waar ook waterstof aan andere vervoerswijzen kan worden geleverd.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. De lidstaten zorgen ervoor dat ..."
    thisalinea.nativeID = 237
    thisalinea.parentID = 236
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. De lidstaten zorgen ervoor dat op hun grondgebied uiterlijk op 31 december 2030 een minimumaantal openbaar toegankelijke waterstoftankstations zijn geïnstalleerd. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. De lidstaten zorgen ervoor dat op hun grondgebied uiterlijk op 31 december 2030")
    thisalinea.textcontent.append("een minimumaantal openbaar toegankelijke waterstoftankstations zijn geïnstalleerd.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Naburige lidstaten zorgen ervoor dat ..."
    thisalinea.nativeID = 238
    thisalinea.parentID = 236
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Naburige lidstaten zorgen ervoor dat de in de in lid 1, tweede alinea, bedoelde maximumafstand op grensoverschrijdende wegen van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk niet wordt overschreden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Naburige lidstaten zorgen ervoor dat de in de in lid 1, tweede alinea, bedoelde")
    thisalinea.textcontent.append("maximumafstand op grensoverschrijdende wegen van het TEN-T-kernnetwerk en het")
    thisalinea.textcontent.append("uitgebreide TEN-T-netwerk niet wordt overschreden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. De exploitant van een openbaar ..."
    thisalinea.nativeID = 239
    thisalinea.parentID = 236
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. De exploitant van een openbaar toegankelijk tankstation of, indien hij niet de eigenaar is, de eigenaar van dat tankstation zorgt er, overeenkomstig regelingen tussen beide, voor dat het station kan worden gebruikt door zowel lichte voertuigen als zware bedrijfsvoertuigen. In goederenterminals zorgen de exploitanten of eigenaars van openbaar toegankelijke waterstoftankstations ervoor dat in die stations ook vloeibare waterstof kan worden getankt. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. De exploitant van een openbaar toegankelijk tankstation of, indien hij niet de")
    thisalinea.textcontent.append("eigenaar is, de eigenaar van dat tankstation zorgt er, overeenkomstig regelingen")
    thisalinea.textcontent.append("tussen beide, voor dat het station kan worden gebruikt door zowel lichte voertuigen")
    thisalinea.textcontent.append("als zware bedrijfsvoertuigen. In goederenterminals zorgen de exploitanten of")
    thisalinea.textcontent.append("eigenaars van openbaar toegankelijke waterstoftankstations ervoor dat in die stations")
    thisalinea.textcontent.append("ook vloeibare waterstof kan worden getankt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 7"
    thisalinea.nativeID = 240
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 14
    thisalinea.summary = "Infrastructuur voor het tanken van waterstof Indien de exploitant van het waterstoftankpunt niet de eigenaar is van dat punt, stelt de eigenaar de exploitant, overeenkomstig de tussen beide getroffen regelingen, waterstoftankpunten ter beschikking waarvan de technische kenmerken de exploitant in staat stellen te voldoen aan de in dit lid vastgestelde verplichting. 1. Vanaf de in artikel 24 bedoelde datum bieden alle exploitanten van openbaar toegankelijke waterstoftankstations eindgebruikers in de door hen geëxploiteerde stations de mogelijkheid om op ad-hocbasis te tanken middels een in de Unie gangbaar betaalinstrument. Daartoe zorgen exploitanten van waterstoftankstations ervoor dat in alle door hen geëxploiteerde waterstoftankstations "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Infrastructuur voor het tanken van waterstof")
    thisalinea.textcontent.append("Indien de exploitant van het waterstoftankpunt niet de eigenaar is van dat punt, stelt")
    thisalinea.textcontent.append("de eigenaar de exploitant, overeenkomstig de tussen beide getroffen regelingen,")
    thisalinea.textcontent.append("waterstoftankpunten ter beschikking waarvan de technische kenmerken de exploitant")
    thisalinea.textcontent.append("in staat stellen te voldoen aan de in dit lid vastgestelde verplichting.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Vanaf de in artikel 24 ..."
    thisalinea.nativeID = 241
    thisalinea.parentID = 240
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Vanaf de in artikel 24 bedoelde datum bieden alle exploitanten van openbaar toegankelijke waterstoftankstations eindgebruikers in de door hen geëxploiteerde stations de mogelijkheid om op ad-hocbasis te tanken middels een in de Unie gangbaar betaalinstrument. Daartoe zorgen exploitanten van waterstoftankstations ervoor dat in alle door hen geëxploiteerde waterstoftankstations elektronisch kan worden betaald via terminals en apparatuur voor betaaldiensten, waaronder ten minste een van de volgende: (a) betaalkaartlezers; (b) apparatuur voor contactloos betalen die ten minste in staat is betaalkaarten te lezen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Vanaf de in artikel 24 bedoelde datum bieden alle exploitanten van openbaar")
    thisalinea.textcontent.append("toegankelijke waterstoftankstations eindgebruikers in de door hen geëxploiteerde")
    thisalinea.textcontent.append("stations de mogelijkheid om op ad-hocbasis te tanken middels een in de Unie")
    thisalinea.textcontent.append("gangbaar betaalinstrument. Daartoe zorgen exploitanten van waterstoftankstations")
    thisalinea.textcontent.append("ervoor dat in alle door hen geëxploiteerde waterstoftankstations elektronisch kan")
    thisalinea.textcontent.append("worden betaald via terminals en apparatuur voor betaaldiensten, waaronder ten")
    thisalinea.textcontent.append("minste een van de volgende:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) betaalkaartlezers; "
    thisalinea.nativeID = 242
    thisalinea.parentID = 241
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) betaalkaartlezers; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) betaalkaartlezers;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) apparatuur voor contactloos betalen die ..."
    thisalinea.nativeID = 243
    thisalinea.parentID = 241
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) apparatuur voor contactloos betalen die ten minste in staat is betaalkaarten te lezen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) apparatuur voor contactloos betalen die ten minste in staat is")
    thisalinea.textcontent.append("betaalkaarten te lezen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. De prijzen die exploitanten van ..."
    thisalinea.nativeID = 244
    thisalinea.parentID = 240
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. De prijzen die exploitanten van openbaar toegankelijke waterstoftankpunten in rekening brengen, moeten redelijk, gemakkelijk en duidelijk vergelijkbaar, transparant en niet-discriminerend zijn. Exploitanten van openbaar toegankelijke waterstoftankpunten mogen geen onderscheid maken tussen de prijzen die aan eindgebruikers en aan aanbieders van mobiliteitsdiensten worden aangerekend, noch tussen de prijzen die aan de verschillende aanbieders van mobiliteitsdiensten worden aangerekend. In voorkomend geval mag het prijsniveau alleen worden gedifferentieerd op basis van een objectieve rechtvaardiging. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. De prijzen die exploitanten van openbaar toegankelijke waterstoftankpunten in")
    thisalinea.textcontent.append("rekening brengen, moeten redelijk, gemakkelijk en duidelijk vergelijkbaar,")
    thisalinea.textcontent.append("transparant en niet-discriminerend zijn. Exploitanten van openbaar toegankelijke")
    thisalinea.textcontent.append("waterstoftankpunten mogen geen onderscheid maken tussen de prijzen die aan")
    thisalinea.textcontent.append("eindgebruikers en aan aanbieders van mobiliteitsdiensten worden aangerekend, noch")
    thisalinea.textcontent.append("tussen de prijzen die aan de verschillende aanbieders van mobiliteitsdiensten worden")
    thisalinea.textcontent.append("aangerekend. In voorkomend geval mag het prijsniveau alleen worden")
    thisalinea.textcontent.append("gedifferentieerd op basis van een objectieve rechtvaardiging.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Exploitanten van waterstoftankpunten stellen prijsinformatie ..."
    thisalinea.nativeID = 245
    thisalinea.parentID = 240
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Exploitanten van waterstoftankpunten stellen prijsinformatie beschikbaar vóór het begin van een tankbeurt in de door hen geëxploiteerde tankstations. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Exploitanten van waterstoftankpunten stellen prijsinformatie beschikbaar vóór het")
    thisalinea.textcontent.append("begin van een tankbeurt in de door hen geëxploiteerde tankstations.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. Exploitanten van openbaar toegankelijke tankstations ..."
    thisalinea.nativeID = 246
    thisalinea.parentID = 240
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. Exploitanten van openbaar toegankelijke tankstations kunnen op contractbasis waterstoftankdiensten verlenen aan klanten, onder meer namens en voor rekening van andere aanbieders van mobiliteitsdiensten. Aanbieders van mobiliteitsdiensten rekenen aan eindgebruikers redelijke, transparante en niet-discriminerende prijzen aan. Aanbieders van mobiliteitsdiensten stellen eindgebruikers vóór het begin van de tankbeurt via vrij toegankelijke, breed ondersteunde elektronische middelen alle op hun geplande tankbeurt toepasselijke prijsinformatie ter beschikking; daarbij wordt een duidelijk onderscheid gemaakt tussen de prijscomponenten die de exploitant van het waterstoftankpunt in rekening brengt, de toepasselijke e-roamingkosten en andere door de aanbieder van mobiliteitsdiensten aangerekende vergoedingen of kosten. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. Exploitanten van openbaar toegankelijke tankstations kunnen op contractbasis")
    thisalinea.textcontent.append("waterstoftankdiensten verlenen aan klanten, onder meer namens en voor rekening")
    thisalinea.textcontent.append("van andere aanbieders van mobiliteitsdiensten. Aanbieders van mobiliteitsdiensten")
    thisalinea.textcontent.append("rekenen aan eindgebruikers redelijke, transparante en niet-discriminerende prijzen")
    thisalinea.textcontent.append("aan. Aanbieders van mobiliteitsdiensten stellen eindgebruikers vóór het begin van de")
    thisalinea.textcontent.append("tankbeurt via vrij toegankelijke, breed ondersteunde elektronische middelen alle op")
    thisalinea.textcontent.append("hun geplande tankbeurt toepasselijke prijsinformatie ter beschikking; daarbij wordt")
    thisalinea.textcontent.append("een duidelijk onderscheid gemaakt tussen de prijscomponenten die de exploitant van")
    thisalinea.textcontent.append("het waterstoftankpunt in rekening brengt, de toepasselijke e-roamingkosten en andere")
    thisalinea.textcontent.append("door de aanbieder van mobiliteitsdiensten aangerekende vergoedingen of kosten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 8"
    thisalinea.nativeID = 247
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 15
    thisalinea.summary = "LNG-infrastructuur voor wegvoertuigen Tot 1 januari 2025 zien de lidstaten erop toe dat er minstens op het TEN-T-kernnetwerk een passend aantal openbaar toegankelijke LNG-tankpunten beschikbaar zijn om ervoor te zorgen dat zware bedrijfsvoertuigen op LNG in de hele Unie kunnen rijden, voor zover daar vraag naar is en tenzij de kosten buitensporig zijn ten opzichte van de baten, waaronder de voordelen voor het milieu. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("LNG-infrastructuur voor wegvoertuigen")
    thisalinea.textcontent.append("Tot 1 januari 2025 zien de lidstaten erop toe dat er minstens op het TEN-T-kernnetwerk een")
    thisalinea.textcontent.append("passend aantal openbaar toegankelijke LNG-tankpunten beschikbaar zijn om ervoor te zorgen")
    thisalinea.textcontent.append("dat zware bedrijfsvoertuigen op LNG in de hele Unie kunnen rijden, voor zover daar vraag")
    thisalinea.textcontent.append("naar is en tenzij de kosten buitensporig zijn ten opzichte van de baten, waaronder de")
    thisalinea.textcontent.append("voordelen voor het milieu.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 9"
    thisalinea.nativeID = 248
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 16
    thisalinea.summary = "Streefcijfers voor walstroomvoorzieningen in zeehavens aangedaan over voldoende vermogen aan walstroom beschikken om aan ten minste 90 % van de vraag van die schepen te voldoen; 1. De lidstaten zorgen ervoor dat in zeehavens minimale walstroomvoorzieningen voor zeeschepen voor container- of passagiersvervoer beschikbaar zijn. De lidstaten nemen de nodige maatregelen om ervoor te zorgen dat uiterlijk 1 januari 2030: (a) de zeehavens van het TEN-T-kernnetwerk en uitgebreide TEN-T-netwerk die de jongste drie jaar gemiddeld door meer dan 50 containerzeeschepen van meer dan 5 000 brutoton werden aangedaan over voldoende vermogen aan walstroom beschikken om aan ten minste 90 % van "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Streefcijfers voor walstroomvoorzieningen in zeehavens")
    thisalinea.textcontent.append("aangedaan over voldoende vermogen aan walstroom beschikken om aan ten")
    thisalinea.textcontent.append("minste 90 % van de vraag van die schepen te voldoen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. De lidstaten zorgen ervoor dat ..."
    thisalinea.nativeID = 249
    thisalinea.parentID = 248
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. De lidstaten zorgen ervoor dat in zeehavens minimale walstroomvoorzieningen voor zeeschepen voor container- of passagiersvervoer beschikbaar zijn. De lidstaten nemen de nodige maatregelen om ervoor te zorgen dat uiterlijk 1 januari 2030: (a) de zeehavens van het TEN-T-kernnetwerk en uitgebreide TEN-T-netwerk die de jongste drie jaar gemiddeld door meer dan 50 containerzeeschepen van meer dan 5 000 brutoton werden aangedaan over voldoende vermogen aan walstroom beschikken om aan ten minste 90 % van de vraag van die schepen te voldoen; (b) de zeehavens van het TEN-T-kernnetwerk en uitgebreide TEN-T-netwerk die de jongste drie jaar gemiddeld door meer van 40 "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. De lidstaten zorgen ervoor dat in zeehavens minimale walstroomvoorzieningen voor")
    thisalinea.textcontent.append("zeeschepen voor container- of passagiersvervoer beschikbaar zijn. De lidstaten")
    thisalinea.textcontent.append("nemen de nodige maatregelen om ervoor te zorgen dat uiterlijk 1 januari 2030:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) de zeehavens van het TEN-T-kernnetwerk ..."
    thisalinea.nativeID = 250
    thisalinea.parentID = 249
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) de zeehavens van het TEN-T-kernnetwerk en uitgebreide TEN-T-netwerk die de jongste drie jaar gemiddeld door meer dan 50 containerzeeschepen van meer dan 5 000 brutoton werden aangedaan over voldoende vermogen aan walstroom beschikken om aan ten minste 90 % van de vraag van die schepen te voldoen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) de zeehavens van het TEN-T-kernnetwerk en uitgebreide TEN-T-netwerk die")
    thisalinea.textcontent.append("de jongste drie jaar gemiddeld door meer dan 50 containerzeeschepen van meer")
    thisalinea.textcontent.append("dan 5 000 brutoton werden aangedaan over voldoende vermogen aan")
    thisalinea.textcontent.append("walstroom beschikken om aan ten minste 90 % van de vraag van die schepen te")
    thisalinea.textcontent.append("voldoen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) de zeehavens van het TEN-T-kernnetwerk ..."
    thisalinea.nativeID = 251
    thisalinea.parentID = 249
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) de zeehavens van het TEN-T-kernnetwerk en uitgebreide TEN-T-netwerk die de jongste drie jaar gemiddeld door meer van 40 ro-ro-passagierszeeschepen en hogesnelheidspassagiersvaartuigen van meer dan 5 000 brutoton werden "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) de zeehavens van het TEN-T-kernnetwerk en uitgebreide TEN-T-netwerk die")
    thisalinea.textcontent.append("de jongste drie jaar gemiddeld door meer van 40 ro-ro-passagierszeeschepen en")
    thisalinea.textcontent.append("hogesnelheidspassagiersvaartuigen van meer dan 5 000 brutoton werden")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(c) de zeehavens van het TEN-T-kernnetwerk ..."
    thisalinea.nativeID = 252
    thisalinea.parentID = 249
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(c) de zeehavens van het TEN-T-kernnetwerk en uitgebreide TEN-T-netwerk die de jongste drie jaar gemiddeld door meer van 25 passagiersschepen van andere types dan ro-ro-passagiersschepen en hogesnelheidspassagiersvaartuigen van meer dan 5 000 brutoton werden aangedaan over voldoende vermogen aan walstroom beschikken om aan ten minste 90 % van de vraag van die schepen te voldoen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(c) de zeehavens van het TEN-T-kernnetwerk en uitgebreide TEN-T-netwerk die")
    thisalinea.textcontent.append("de jongste drie jaar gemiddeld door meer van 25 passagiersschepen van andere")
    thisalinea.textcontent.append("types dan ro-ro-passagiersschepen en hogesnelheidspassagiersvaartuigen van")
    thisalinea.textcontent.append("meer dan 5 000 brutoton werden aangedaan over voldoende vermogen aan")
    thisalinea.textcontent.append("walstroom beschikken om aan ten minste 90 % van de vraag van die schepen te")
    thisalinea.textcontent.append("voldoen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Voor de bepaling van het ..."
    thisalinea.nativeID = 253
    thisalinea.parentID = 248
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Voor de bepaling van het aantal havenaanlopen wordt geen rekening gehouden met: (a) schepen die minder dan twee uur aangelegd blijven, berekend op basis van het uur van vertrek en aankomst dat wordt gemonitord overeenkomstig artikel 14 van het voorstel voor een verordening COM (2021)562; (b) havenaanlopen door schepen die emissievrije technologieën gebruiken, zoals gespecificeerd in bijlage III bij het voorstel voor een verordening COM(2021)562; (c) niet-geplande havenaanlopen om veiligheidsredenen of om mensenlevens op zee te redden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Voor de bepaling van het aantal havenaanlopen wordt geen rekening gehouden met:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) schepen die minder dan twee ..."
    thisalinea.nativeID = 254
    thisalinea.parentID = 253
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) schepen die minder dan twee uur aangelegd blijven, berekend op basis van het uur van vertrek en aankomst dat wordt gemonitord overeenkomstig artikel 14 van het voorstel voor een verordening COM (2021)562; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) schepen die minder dan twee uur aangelegd blijven, berekend op basis van het")
    thisalinea.textcontent.append("uur van vertrek en aankomst dat wordt gemonitord overeenkomstig artikel 14")
    thisalinea.textcontent.append("van het voorstel voor een verordening COM (2021)562;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) havenaanlopen door schepen die emissievrije ..."
    thisalinea.nativeID = 255
    thisalinea.parentID = 253
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) havenaanlopen door schepen die emissievrije technologieën gebruiken, zoals gespecificeerd in bijlage III bij het voorstel voor een verordening COM(2021)562; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) havenaanlopen door schepen die emissievrije technologieën gebruiken, zoals")
    thisalinea.textcontent.append("gespecificeerd in bijlage III bij het voorstel voor een verordening")
    thisalinea.textcontent.append("COM(2021)562;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(c) niet-geplande havenaanlopen om veiligheidsredenen of ..."
    thisalinea.nativeID = 256
    thisalinea.parentID = 253
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(c) niet-geplande havenaanlopen om veiligheidsredenen of om mensenlevens op zee te redden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(c) niet-geplande havenaanlopen om veiligheidsredenen of om mensenlevens op")
    thisalinea.textcontent.append("zee te redden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Wanneer de zeehaven van het ..."
    thisalinea.nativeID = 257
    thisalinea.parentID = 248
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Wanneer de zeehaven van het TEN-T-kernnetwerk en het uitgebreide TEN-T- netwerk gelegen zijn op een eiland dat niet rechtstreeks op het elektriciteitsnet is aangesloten, is lid 1 niet van toepassing tot een dergelijke verbinding tot stand is gebracht of tot er ter plaatse voldoende vermogen uit schone energiebronnen kan worden opgewekt. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Wanneer de zeehaven van het TEN-T-kernnetwerk en het uitgebreide TEN-T-")
    thisalinea.textcontent.append("netwerk gelegen zijn op een eiland dat niet rechtstreeks op het elektriciteitsnet is")
    thisalinea.textcontent.append("aangesloten, is lid 1 niet van toepassing tot een dergelijke verbinding tot stand is")
    thisalinea.textcontent.append("gebracht of tot er ter plaatse voldoende vermogen uit schone energiebronnen kan")
    thisalinea.textcontent.append("worden opgewekt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 10"
    thisalinea.nativeID = 258
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 17
    thisalinea.summary = "Streefcijfers voor walstroomvoorzieningen in binnenhavens De lidstaten zien er op toe dat: (a) uiterlijk 1 januari 2025 ten minste één walstroominstallatie voor binnenschepen beschikbaar is in alle binnenhavens van het TEN-T-kernnetwerk; (b) uiterlijk 1 januari 2030 ten minste één walstroominstallatie voor binnenschepen beschikbaar is in alle binnenhavens van het uitgebreide TEN-T-netwerk. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Streefcijfers voor walstroomvoorzieningen in binnenhavens")
    thisalinea.textcontent.append("De lidstaten zien er op toe dat:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(a) uiterlijk 1 januari 2025 ten ..."
    thisalinea.nativeID = 259
    thisalinea.parentID = 258
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) uiterlijk 1 januari 2025 ten minste één walstroominstallatie voor binnenschepen beschikbaar is in alle binnenhavens van het TEN-T-kernnetwerk; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) uiterlijk 1 januari 2025 ten minste één walstroominstallatie voor binnenschepen")
    thisalinea.textcontent.append("beschikbaar is in alle binnenhavens van het TEN-T-kernnetwerk;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "(b) uiterlijk 1 januari 2030 ten ..."
    thisalinea.nativeID = 260
    thisalinea.parentID = 258
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) uiterlijk 1 januari 2030 ten minste één walstroominstallatie voor binnenschepen beschikbaar is in alle binnenhavens van het uitgebreide TEN-T-netwerk. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) uiterlijk 1 januari 2030 ten minste één walstroominstallatie voor binnenschepen")
    thisalinea.textcontent.append("beschikbaar is in alle binnenhavens van het uitgebreide TEN-T-netwerk.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 11"
    thisalinea.nativeID = 261
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 18
    thisalinea.summary = "Streefcijfers voor de levering van LNG in zeehavens 1. De lidstaten zorgen ervoor dat in de in lid 2 bedoelde zeehavens van het TEN-T- kernnetwerk een passend aantal LNG-tankpunten wordt geïnstalleerd, zodat zeeschepen uiterlijk 1 januari 2025 over het volledige TEN-T-kernnetwerk kunnen varen. Indien nodig werken lidstaten met naburige lidstaten samen om een adequate dekking van het TEN-T-kernnetwerk te waarborgen. 2. De lidstaten wijzen in hun nationale beleidskaders de zeehavens van het TEN-T- kernnetwerk aan waar de LNG-tankpunten als bedoeld in lid 1 beschikbaar zullen zijn, rekening houdend met werkelijke marktbehoeften en ontwikkelingen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Streefcijfers voor de levering van LNG in zeehavens")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. De lidstaten zorgen ervoor dat ..."
    thisalinea.nativeID = 262
    thisalinea.parentID = 261
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. De lidstaten zorgen ervoor dat in de in lid 2 bedoelde zeehavens van het TEN-T- kernnetwerk een passend aantal LNG-tankpunten wordt geïnstalleerd, zodat zeeschepen uiterlijk 1 januari 2025 over het volledige TEN-T-kernnetwerk kunnen varen. Indien nodig werken lidstaten met naburige lidstaten samen om een adequate dekking van het TEN-T-kernnetwerk te waarborgen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. De lidstaten zorgen ervoor dat in de in lid 2 bedoelde zeehavens van het TEN-T-")
    thisalinea.textcontent.append("kernnetwerk een passend aantal LNG-tankpunten wordt geïnstalleerd, zodat")
    thisalinea.textcontent.append("zeeschepen uiterlijk 1 januari 2025 over het volledige TEN-T-kernnetwerk kunnen")
    thisalinea.textcontent.append("varen. Indien nodig werken lidstaten met naburige lidstaten samen om een adequate")
    thisalinea.textcontent.append("dekking van het TEN-T-kernnetwerk te waarborgen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. De lidstaten wijzen in hun ..."
    thisalinea.nativeID = 263
    thisalinea.parentID = 261
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. De lidstaten wijzen in hun nationale beleidskaders de zeehavens van het TEN-T- kernnetwerk aan waar de LNG-tankpunten als bedoeld in lid 1 beschikbaar zullen zijn, rekening houdend met werkelijke marktbehoeften en ontwikkelingen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. De lidstaten wijzen in hun nationale beleidskaders de zeehavens van het TEN-T-")
    thisalinea.textcontent.append("kernnetwerk aan waar de LNG-tankpunten als bedoeld in lid 1 beschikbaar zullen")
    thisalinea.textcontent.append("zijn, rekening houdend met werkelijke marktbehoeften en ontwikkelingen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 12"
    thisalinea.nativeID = 264
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 19
    thisalinea.summary = "Streefcijfers voor de levering van elektriciteit aan stilstaande luchtvaartuigen 1. De lidstaten zien erop toe dat beheerders van luchthavens van het TEN-T- kernnetwerk en het uitgebreide TEN-T-netwerk ervoor zorgen dat elektriciteit kan worden geleverd aan stilstaande luchtvaartuigen: (a) tegen 1 januari 2025: aan alle voor commerciële vluchtuitvoeringen gebruikte gates; (b) tegen 1 januari 2030: op alle voor commerciële vluchtuitvoeringen gebruikte buitenstandplaatsen. 2. Uiterlijk 1 januari 2030 nemen de lidstaten de nodige maatregelen om ervoor te zorgen dat de overeenkomstig lid 1 geleverde elektriciteit afkomstig is van het elektriciteitsnet of ter plaatse uit hernieuwbare energie wordt opgewekt. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Streefcijfers voor de levering van elektriciteit aan stilstaande luchtvaartuigen")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. De lidstaten zien erop toe ..."
    thisalinea.nativeID = 265
    thisalinea.parentID = 264
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. De lidstaten zien erop toe dat beheerders van luchthavens van het TEN-T- kernnetwerk en het uitgebreide TEN-T-netwerk ervoor zorgen dat elektriciteit kan worden geleverd aan stilstaande luchtvaartuigen: (a) tegen 1 januari 2025: aan alle voor commerciële vluchtuitvoeringen gebruikte gates; (b) tegen 1 januari 2030: op alle voor commerciële vluchtuitvoeringen gebruikte buitenstandplaatsen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. De lidstaten zien erop toe dat beheerders van luchthavens van het TEN-T-")
    thisalinea.textcontent.append("kernnetwerk en het uitgebreide TEN-T-netwerk ervoor zorgen dat elektriciteit kan")
    thisalinea.textcontent.append("worden geleverd aan stilstaande luchtvaartuigen:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) tegen 1 januari 2025: aan ..."
    thisalinea.nativeID = 266
    thisalinea.parentID = 265
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) tegen 1 januari 2025: aan alle voor commerciële vluchtuitvoeringen gebruikte gates; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) tegen 1 januari 2025: aan alle voor commerciële vluchtuitvoeringen")
    thisalinea.textcontent.append("gebruikte gates;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) tegen 1 januari 2030: op ..."
    thisalinea.nativeID = 267
    thisalinea.parentID = 265
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) tegen 1 januari 2030: op alle voor commerciële vluchtuitvoeringen gebruikte buitenstandplaatsen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) tegen 1 januari 2030: op alle voor commerciële vluchtuitvoeringen")
    thisalinea.textcontent.append("gebruikte buitenstandplaatsen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Uiterlijk 1 januari 2030 nemen ..."
    thisalinea.nativeID = 268
    thisalinea.parentID = 264
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Uiterlijk 1 januari 2030 nemen de lidstaten de nodige maatregelen om ervoor te zorgen dat de overeenkomstig lid 1 geleverde elektriciteit afkomstig is van het elektriciteitsnet of ter plaatse uit hernieuwbare energie wordt opgewekt. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Uiterlijk 1 januari 2030 nemen de lidstaten de nodige maatregelen om ervoor te")
    thisalinea.textcontent.append("zorgen dat de overeenkomstig lid 1 geleverde elektriciteit afkomstig is van het")
    thisalinea.textcontent.append("elektriciteitsnet of ter plaatse uit hernieuwbare energie wordt opgewekt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 13"
    thisalinea.nativeID = 269
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 20
    thisalinea.summary = "Nationale beleidskaders De nationale beleidskaders omvatten minstens de volgende elementen: 1. Tegen 1 januari 2024 stellen de lidstaten een ontwerp van nationaal beleidskader op voor de ontwikkeling van de markt van alternatieve brandstoffen in de vervoerssector en de uitrol van de betreffende infrastructuur en dienen zij dat ontwerp in bij de Commissie. (a) een beoordeling van de huidige stand en de toekomstige ontwikkeling van de markt voor alternatieve brandstoffen in de vervoerssector, en van de ontwikkeling van de infrastructuur voor alternatieve brandstoffen, rekening houdend met de intermodale toegang tot die infrastructuur en, desgevallend, de grensoverschrijdende continuïteit; (b) de nationale streefcijfers "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Nationale beleidskaders")
    thisalinea.textcontent.append("De nationale beleidskaders omvatten minstens de volgende elementen:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Tegen 1 januari 2024 stellen ..."
    thisalinea.nativeID = 270
    thisalinea.parentID = 269
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Tegen 1 januari 2024 stellen de lidstaten een ontwerp van nationaal beleidskader op voor de ontwikkeling van de markt van alternatieve brandstoffen in de vervoerssector en de uitrol van de betreffende infrastructuur en dienen zij dat ontwerp in bij de Commissie. (a) een beoordeling van de huidige stand en de toekomstige ontwikkeling van de markt voor alternatieve brandstoffen in de vervoerssector, en van de ontwikkeling van de infrastructuur voor alternatieve brandstoffen, rekening houdend met de intermodale toegang tot die infrastructuur en, desgevallend, de grensoverschrijdende continuïteit; (b) de nationale streefcijfers en doelstellingen overeenkomstig de artikelen 3, 4, 6, 8, 9, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Tegen 1 januari 2024 stellen de lidstaten een ontwerp van nationaal beleidskader op")
    thisalinea.textcontent.append("voor de ontwikkeling van de markt van alternatieve brandstoffen in de vervoerssector")
    thisalinea.textcontent.append("en de uitrol van de betreffende infrastructuur en dienen zij dat ontwerp in bij de")
    thisalinea.textcontent.append("Commissie.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) een beoordeling van de huidige ..."
    thisalinea.nativeID = 271
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) een beoordeling van de huidige stand en de toekomstige ontwikkeling van de markt voor alternatieve brandstoffen in de vervoerssector, en van de ontwikkeling van de infrastructuur voor alternatieve brandstoffen, rekening houdend met de intermodale toegang tot die infrastructuur en, desgevallend, de grensoverschrijdende continuïteit; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) een beoordeling van de huidige stand en de toekomstige ontwikkeling van de")
    thisalinea.textcontent.append("markt voor alternatieve brandstoffen in de vervoerssector, en van de")
    thisalinea.textcontent.append("ontwikkeling van de infrastructuur voor alternatieve brandstoffen, rekening")
    thisalinea.textcontent.append("houdend met de intermodale toegang tot die infrastructuur en, desgevallend, de")
    thisalinea.textcontent.append("grensoverschrijdende continuïteit;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) de nationale streefcijfers en doelstellingen ..."
    thisalinea.nativeID = 272
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) de nationale streefcijfers en doelstellingen overeenkomstig de artikelen 3, 4, 6, 8, 9, 10, 11 en 12, waarvoor in deze verordening bindende nationale streefcijfers zijn vastgesteld; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) de nationale streefcijfers en doelstellingen overeenkomstig de artikelen 3, 4, 6,")
    thisalinea.textcontent.append("8, 9, 10, 11 en 12, waarvoor in deze verordening bindende nationale")
    thisalinea.textcontent.append("streefcijfers zijn vastgesteld;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(c) de nationale streefcijfers en doelstellingen ..."
    thisalinea.nativeID = 273
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(c) de nationale streefcijfers en doelstellingen voor de uitrol van infrastructuur voor alternatieve brandstoffen met betrekking tot de punten l), m), n), o) en p) van dit lid, waarvoor in deze verordening geen bindende streefcijfers zijn vastgesteld; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(c) de nationale streefcijfers en doelstellingen voor de uitrol van infrastructuur")
    thisalinea.textcontent.append("voor alternatieve brandstoffen met betrekking tot de punten l), m), n), o) en p)")
    thisalinea.textcontent.append("van dit lid, waarvoor in deze verordening geen bindende streefcijfers zijn")
    thisalinea.textcontent.append("vastgesteld;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(d) de beleidslijnen en maatregelen die ..."
    thisalinea.nativeID = 274
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "(d) de beleidslijnen en maatregelen die nodig zijn om ervoor te zorgen dat de onder b) en c) van dit lid bedoelde bindende streefcijfers en doelstellingen worden bereikt; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(d) de beleidslijnen en maatregelen die nodig zijn om ervoor te zorgen dat de")
    thisalinea.textcontent.append("onder b) en c) van dit lid bedoelde bindende streefcijfers en doelstellingen")
    thisalinea.textcontent.append("worden bereikt;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(e) maatregelen ter bevordering van de ..."
    thisalinea.nativeID = 275
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "(e) maatregelen ter bevordering van de uitrol van infrastructuur voor alternatieve brandstoffen voor wagenparken die bijzonder geschikt zijn voor de invoering van dergelijke brandstoffen, met name elektrische laad- en waterstoftankstations voor OV-bussen en elektrische laadpunten voor deelauto's; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(e) maatregelen ter bevordering van de uitrol van infrastructuur voor alternatieve")
    thisalinea.textcontent.append("brandstoffen voor wagenparken die bijzonder geschikt zijn voor de invoering")
    thisalinea.textcontent.append("van dergelijke brandstoffen, met name elektrische laad- en")
    thisalinea.textcontent.append("waterstoftankstations voor OV-bussen en elektrische laadpunten voor")
    thisalinea.textcontent.append("deelauto's;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(f) maatregelen om de uitrol van ..."
    thisalinea.nativeID = 276
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "(f) maatregelen om de uitrol van laadpunten voor lichte en zware bedrijfsvoertuigen op particuliere niet voor het publiek toegankelijke locaties aan te moedigen en te faciliteren; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(f) maatregelen om de uitrol van laadpunten voor lichte en zware")
    thisalinea.textcontent.append("bedrijfsvoertuigen op particuliere niet voor het publiek toegankelijke locaties")
    thisalinea.textcontent.append("aan te moedigen en te faciliteren;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(g) maatregelen om de uitrol van ..."
    thisalinea.nativeID = 277
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "(g) maatregelen om de uitrol van infrastructuur voor alternatieve brandstoffen, met name openbaar toegankelijke laadpunten, te bevorderen in stedelijke knooppunten; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(g) maatregelen om de uitrol van infrastructuur voor alternatieve brandstoffen, met")
    thisalinea.textcontent.append("name openbaar toegankelijke laadpunten, te bevorderen in stedelijke")
    thisalinea.textcontent.append("knooppunten;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(h) maatregelen om een voldoende aantal ..."
    thisalinea.nativeID = 278
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "(h) maatregelen om een voldoende aantal openbaar toegankelijke laadpunten voor hoog vermogen te bevorderen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(h) maatregelen om een voldoende aantal openbaar toegankelijke laadpunten voor")
    thisalinea.textcontent.append("hoog vermogen te bevorderen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(i) de nodige maatregelen om ervoor ..."
    thisalinea.nativeID = 279
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "(i) de nodige maatregelen om ervoor te zorgen dat de uitrol en het beheer van laadpunten, met inbegrip van de geografische spreiding van tweerichtingslaadpunten, bijdragen tot de flexibiliteit van het energiesysteem en tot de penetratie van hernieuwbare elektriciteit in het elektriciteitssysteem; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(i) de nodige maatregelen om ervoor te zorgen dat de uitrol en het beheer van")
    thisalinea.textcontent.append("laadpunten, met inbegrip van de geografische spreiding van")
    thisalinea.textcontent.append("tweerichtingslaadpunten, bijdragen tot de flexibiliteit van het energiesysteem")
    thisalinea.textcontent.append("en tot de penetratie van hernieuwbare elektriciteit in het elektriciteitssysteem;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(j) maatregelen om ervoor te zorgen ..."
    thisalinea.nativeID = 280
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 9
    thisalinea.summary = "(j) maatregelen om ervoor te zorgen dat openbaar toegankelijke laad- en tankpunten toegankelijk zijn voor ouderen, personen met beperkte mobiliteit en personen met een handicap, overeenkomstig de toegankelijkheidseisen van de bijlagen I en III van Richtlijn 2019/882; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(j) maatregelen om ervoor te zorgen dat openbaar toegankelijke laad- en")
    thisalinea.textcontent.append("tankpunten toegankelijk zijn voor ouderen, personen met beperkte mobiliteit en")
    thisalinea.textcontent.append("personen met een handicap, overeenkomstig de toegankelijkheidseisen van de")
    thisalinea.textcontent.append("bijlagen I en III van Richtlijn 2019/882;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(k) maatregelen om mogelijke belemmeringen voor ..."
    thisalinea.nativeID = 281
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 10
    thisalinea.summary = "(k) maatregelen om mogelijke belemmeringen voor de planning, de afgifte van vergunningen en de aanschaf van infrastructuur voor alternatieve brandstoffen weg te nemen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(k) maatregelen om mogelijke belemmeringen voor de planning, de afgifte van")
    thisalinea.textcontent.append("vergunningen en de aanschaf van infrastructuur voor alternatieve brandstoffen")
    thisalinea.textcontent.append("weg te nemen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(l) een plan voor de uitrol ..."
    thisalinea.nativeID = 282
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 11
    thisalinea.summary = "(l) een plan voor de uitrol van infrastructuur voor alternatieve brandstoffen op luchthavens voor andere doelen dan de elektriciteitsvoorziening van stilstaande luchtvaartuigen, met name om luchtvaartuigen op te laden met elektriciteit of bij te tanken met waterstof; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(l) een plan voor de uitrol van infrastructuur voor alternatieve brandstoffen op")
    thisalinea.textcontent.append("luchthavens voor andere doelen dan de elektriciteitsvoorziening van stilstaande")
    thisalinea.textcontent.append("luchtvaartuigen, met name om luchtvaartuigen op te laden met elektriciteit of")
    thisalinea.textcontent.append("bij te tanken met waterstof;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(m) een plan voor de uitrol ..."
    thisalinea.nativeID = 283
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 12
    thisalinea.summary = "(m) een plan voor de uitrol van infrastructuur voor alternatieve brandstoffen in zeehavens, met name voor elektriciteit en waterstof, voor havendiensten als gedefinieerd in Verordening (EU) 2017/35228 van het Europees Parlement en de Raad; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(m) een plan voor de uitrol van infrastructuur voor alternatieve brandstoffen in")
    thisalinea.textcontent.append("zeehavens, met name voor elektriciteit en waterstof, voor havendiensten als")
    thisalinea.textcontent.append("gedefinieerd in Verordening (EU) 2017/35228 van het Europees Parlement en")
    thisalinea.textcontent.append("de Raad;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(n) een plan voor de uitrol ..."
    thisalinea.nativeID = 284
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 13
    thisalinea.summary = "(n) een plan voor de uitrol van infrastructuur voor alternatieve brandstoffen in zeehavens voor andere energie dan LNG of walstroom, met name om zeeschepen te voorzien van waterstof, ammoniak en elektriciteit; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(n) een plan voor de uitrol van infrastructuur voor alternatieve brandstoffen in")
    thisalinea.textcontent.append("zeehavens voor andere energie dan LNG of walstroom, met name om")
    thisalinea.textcontent.append("zeeschepen te voorzien van waterstof, ammoniak en elektriciteit;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(o) een plan voor de uitrol ..."
    thisalinea.nativeID = 285
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 14
    thisalinea.summary = "(o) een plan voor de uitrol van alternatieve brandstoffen in de binnenvaart, met name voor de levering van waterstof en elektriciteit; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(o) een plan voor de uitrol van alternatieve brandstoffen in de binnenvaart, met")
    thisalinea.textcontent.append("name voor de levering van waterstof en elektriciteit;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(p) een plan voor de introductie ..."
    thisalinea.nativeID = 286
    thisalinea.parentID = 270
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 15
    thisalinea.summary = "(p) een plan voor de introductie van waterstof- of batterijtreinen op lijnen die niet zullen worden geëlektrificeerd, met vermelding van de streefcijfers, mijlpalen en vereiste financiering. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(p) een plan voor de introductie van waterstof- of batterijtreinen op lijnen die niet")
    thisalinea.textcontent.append("zullen worden geëlektrificeerd, met vermelding van de streefcijfers, mijlpalen")
    thisalinea.textcontent.append("en vereiste financiering.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. De lidstaten zorgen ervoor dat ..."
    thisalinea.nativeID = 287
    thisalinea.parentID = 269
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. De lidstaten zorgen ervoor dat in de nationale beleidskaders rekening wordt gehouden met de behoeften van de verschillende vervoerswijzen op hun grondgebied, onder meer die waarvoor beperkte alternatieven voor fossiele brandstoffen beschikbaar zijn. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. De lidstaten zorgen ervoor dat in de nationale beleidskaders rekening wordt")
    thisalinea.textcontent.append("gehouden met de behoeften van de verschillende vervoerswijzen op hun")
    thisalinea.textcontent.append("grondgebied, onder meer die waarvoor beperkte alternatieven voor fossiele")
    thisalinea.textcontent.append("brandstoffen beschikbaar zijn.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. De lidstaten zorgen ervoor dat ..."
    thisalinea.nativeID = 288
    thisalinea.parentID = 269
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. De lidstaten zorgen ervoor dat in de nationale beleidskaders in voorkomend geval rekening wordt gehouden met de belangen van regionale en lokale autoriteiten, met name wat betreft laad- en tankinfrastructuur voor het openbaar vervoer, alsook met die van de betrokken belanghebbenden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. De lidstaten zorgen ervoor dat in de nationale beleidskaders in voorkomend geval")
    thisalinea.textcontent.append("rekening wordt gehouden met de belangen van regionale en lokale autoriteiten, met")
    thisalinea.textcontent.append("name wat betreft laad- en tankinfrastructuur voor het openbaar vervoer, alsook met")
    thisalinea.textcontent.append("die van de betrokken belanghebbenden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. De lidstaten werken waar nodig ..."
    thisalinea.nativeID = 289
    thisalinea.parentID = 269
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. De lidstaten werken waar nodig door middel van overleg of gezamenlijke beleidskaders samen om te waarborgen dat de maatregelen voor de verwezenlijking van de doelstellingen van deze verordening coherent en gecoördineerd zijn. De lidstaten werken met name samen aan de strategieën voor het gebruik van alternatieve brandstoffen en de uitrol van de bijbehorende infrastructuur in het vervoer over water. De Commissie ondersteunt de lidstaten bij dat samenwerkingsproces. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. De lidstaten werken waar nodig door middel van overleg of gezamenlijke")
    thisalinea.textcontent.append("beleidskaders samen om te waarborgen dat de maatregelen voor de verwezenlijking")
    thisalinea.textcontent.append("van de doelstellingen van deze verordening coherent en gecoördineerd zijn. De")
    thisalinea.textcontent.append("lidstaten werken met name samen aan de strategieën voor het gebruik van")
    thisalinea.textcontent.append("alternatieve brandstoffen en de uitrol van de bijbehorende infrastructuur in het")
    thisalinea.textcontent.append("vervoer over water. De Commissie ondersteunt de lidstaten bij dat")
    thisalinea.textcontent.append("samenwerkingsproces.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5. Steunmaatregelen voor infrastructuur voor alternatieve ..."
    thisalinea.nativeID = 290
    thisalinea.parentID = 269
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "5. Steunmaatregelen voor infrastructuur voor alternatieve brandstoffen moeten in overeenstemming zijn met de desbetreffende staatssteunregels van het VWEU. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("5. Steunmaatregelen voor infrastructuur voor alternatieve brandstoffen moeten in")
    thisalinea.textcontent.append("overeenstemming zijn met de desbetreffende staatssteunregels van het VWEU.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "6. Elke lidstaat maakt zijn ontwerp ..."
    thisalinea.nativeID = 291
    thisalinea.parentID = 269
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "6. Elke lidstaat maakt zijn ontwerp van nationaal beleidskader bekend en zorgt ervoor dat het publiek in een vroeg stadium reële inspraak krijgt bij de ontwikkeling van het ontwerp van nationaal beleidskader. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("6. Elke lidstaat maakt zijn ontwerp van nationaal beleidskader bekend en zorgt ervoor")
    thisalinea.textcontent.append("dat het publiek in een vroeg stadium reële inspraak krijgt bij de ontwikkeling van het")
    thisalinea.textcontent.append("ontwerp van nationaal beleidskader.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "7. De Commissie beoordeelt de ontwerpen ..."
    thisalinea.nativeID = 292
    thisalinea.parentID = 269
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "7. De Commissie beoordeelt de ontwerpen van nationale beleidskaders en kan uiterlijk zes maanden nadat een lidstaat zijn ontwerp van nationaal beleidskader als bedoeld in lid 1 heeft ingediend aanbevelingen doen aan die lidstaat. In deze aanbevelingen kan met name het volgende aan bod komen: (a) het ambitieniveau van de streefcijfers en doelstellingen om te voldoen aan de verplichtingen van de artikelen 3, 4, 6, 8, 9, 10, 11 en 12; (b) de beleidslijnen en maatregelen met betrekking tot de doelstellingen en streefcijfers van de lidstaten. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("7. De Commissie beoordeelt de ontwerpen van nationale beleidskaders en kan uiterlijk")
    thisalinea.textcontent.append("zes maanden nadat een lidstaat zijn ontwerp van nationaal beleidskader als bedoeld")
    thisalinea.textcontent.append("in lid 1 heeft ingediend aanbevelingen doen aan die lidstaat. In deze aanbevelingen")
    thisalinea.textcontent.append("kan met name het volgende aan bod komen:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) het ambitieniveau van de streefcijfers ..."
    thisalinea.nativeID = 293
    thisalinea.parentID = 292
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) het ambitieniveau van de streefcijfers en doelstellingen om te voldoen aan de verplichtingen van de artikelen 3, 4, 6, 8, 9, 10, 11 en 12; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) het ambitieniveau van de streefcijfers en doelstellingen om te voldoen")
    thisalinea.textcontent.append("aan de verplichtingen van de artikelen 3, 4, 6, 8, 9, 10, 11 en 12;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) de beleidslijnen en maatregelen met ..."
    thisalinea.nativeID = 294
    thisalinea.parentID = 292
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) de beleidslijnen en maatregelen met betrekking tot de doelstellingen en streefcijfers van de lidstaten. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) de beleidslijnen en maatregelen met betrekking tot de doelstellingen en")
    thisalinea.textcontent.append("streefcijfers van de lidstaten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "8. De lidstaten houden in hun ..."
    thisalinea.nativeID = 295
    thisalinea.parentID = 269
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "8. De lidstaten houden in hun nationale beleidskader rekening met de eventuele aanbevelingen van de Commissie. Een lidstaat die besluit geen gevolg te geven aan een aanbeveling of een aanzienlijk deel daarvan, dient de Commissie schriftelijk in kennis te stellen van de redenen die aan dat besluit ten grondslag liggen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("8. De lidstaten houden in hun nationale beleidskader rekening met de eventuele")
    thisalinea.textcontent.append("aanbevelingen van de Commissie. Een lidstaat die besluit geen gevolg te geven aan")
    thisalinea.textcontent.append("een aanbeveling of een aanzienlijk deel daarvan, dient de Commissie schriftelijk in")
    thisalinea.textcontent.append("kennis te stellen van de redenen die aan dat besluit ten grondslag liggen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "9. Uiterlijk 1 januari 2025 stelt ..."
    thisalinea.nativeID = 296
    thisalinea.parentID = 269
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "9. Uiterlijk 1 januari 2025 stelt elke lidstaat de Commissie in kennis van zijn definitieve nationale beleidskader. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("9. Uiterlijk 1 januari 2025 stelt elke lidstaat de Commissie in kennis van zijn definitieve")
    thisalinea.textcontent.append("nationale beleidskader.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 14"
    thisalinea.nativeID = 297
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 21
    thisalinea.summary = "Rapportage technologie en geografische spreiding om de gebruikers beter in staat te stellen hun elektrische voertuigen in het systeem te integreren. Die informatie wordt openbaar gemaakt. Op basis van de resultaten van die beoordeling nemen de lidstaten zo nodig passende maatregelen voor de uitrol van extra laadpunten en vermelden zij die maatregelen in hun voortgangsverslag als bedoeld in lid 1. De systeembeheerders houden rekening met de beoordeling en de maatregelen in de in artikel 32, lid 3, en artikel 51 van Richtlijn (EU) 2019/944 bedoelde netontwikkelingsplannen. 1. Elke lidstaat dient uiterlijk 1 januari 2027 en vervolgens om de twee jaar "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Rapportage")
    thisalinea.textcontent.append("technologie en geografische spreiding om de gebruikers beter in staat te stellen hun")
    thisalinea.textcontent.append("elektrische voertuigen in het systeem te integreren. Die informatie wordt openbaar")
    thisalinea.textcontent.append("gemaakt. Op basis van de resultaten van die beoordeling nemen de lidstaten zo nodig")
    thisalinea.textcontent.append("passende maatregelen voor de uitrol van extra laadpunten en vermelden zij die")
    thisalinea.textcontent.append("maatregelen in hun voortgangsverslag als bedoeld in lid 1. De systeembeheerders")
    thisalinea.textcontent.append("houden rekening met de beoordeling en de maatregelen in de in artikel 32, lid 3, en")
    thisalinea.textcontent.append("artikel 51 van Richtlijn (EU) 2019/944 bedoelde netontwikkelingsplannen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Elke lidstaat dient uiterlijk 1 ..."
    thisalinea.nativeID = 298
    thisalinea.parentID = 297
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Elke lidstaat dient uiterlijk 1 januari 2027 en vervolgens om de twee jaar een individueel voortgangsverslag in bij de Commissie over de uitvoering van zijn nationale beleidskader. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Elke lidstaat dient uiterlijk 1 januari 2027 en vervolgens om de twee jaar een")
    thisalinea.textcontent.append("individueel voortgangsverslag in bij de Commissie over de uitvoering van zijn")
    thisalinea.textcontent.append("nationale beleidskader.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Die voortgangsverslagen bevatten de in ..."
    thisalinea.nativeID = 299
    thisalinea.parentID = 297
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Die voortgangsverslagen bevatten de in bijlage I bedoelde informatie en, in voorkomend geval, een motivering betreffende mate waarin de in artikel 13 bedoelde nationale streefcijfers en doelen zijn verwezenlijkt. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Die voortgangsverslagen bevatten de in bijlage I bedoelde informatie en, in")
    thisalinea.textcontent.append("voorkomend geval, een motivering betreffende mate waarin de in artikel 13 bedoelde")
    thisalinea.textcontent.append("nationale streefcijfers en doelen zijn verwezenlijkt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Uiterlijk op 30 juni 2024 ..."
    thisalinea.nativeID = 300
    thisalinea.parentID = 297
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Uiterlijk op 30 juni 2024 en vervolgens om de drie jaar beoordelen de regulerende instanties van de lidstaten hoe de uitrol en exploitatie van laadpunten elektrische voertuigen in staat zouden kunnen stellen een grotere bijdrage te leveren aan de flexibiliteit van het energiesysteem, onder meer door hun deelname aan de balanceringsmarkt, en aan de verdere absorptie van hernieuwbare elektriciteit. In die beoordeling wordt rekening gehouden met alle types openbare en particuliere laadpunten en worden aanbevelingen gedaan in termen van type, ondersteunende "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Uiterlijk op 30 juni 2024 en vervolgens om de drie jaar beoordelen de regulerende")
    thisalinea.textcontent.append("instanties van de lidstaten hoe de uitrol en exploitatie van laadpunten elektrische")
    thisalinea.textcontent.append("voertuigen in staat zouden kunnen stellen een grotere bijdrage te leveren aan de")
    thisalinea.textcontent.append("flexibiliteit van het energiesysteem, onder meer door hun deelname aan de")
    thisalinea.textcontent.append("balanceringsmarkt, en aan de verdere absorptie van hernieuwbare elektriciteit. In die")
    thisalinea.textcontent.append("beoordeling wordt rekening gehouden met alle types openbare en particuliere")
    thisalinea.textcontent.append("laadpunten en worden aanbevelingen gedaan in termen van type, ondersteunende")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. Op basis van de input ..."
    thisalinea.nativeID = 301
    thisalinea.parentID = 297
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. Op basis van de input van transmissie- en distributiesysteembeheerders beoordeelt de regulerende instantie van een lidstaat uiterlijk op 30 juni 2024 en vervolgens om de drie jaar de potentiële bijdrage van bidirectioneel laden aan de integratie van hernieuwbare elektriciteit in het elektriciteitssysteem. Die beoordeling wordt openbaar gemaakt. Op basis van de resultaten van die beoordeling nemen de lidstaten zo nodig passende maatregelen om de beschikbaarheid en geografische spreiding van bidirectionele laadpunten op zowel openbare als particuliere plaatsen bij te sturen en nemen zij die maatregelen op in hun voortgangsverslag als bedoeld in lid 1. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. Op basis van de input van transmissie- en distributiesysteembeheerders beoordeelt de")
    thisalinea.textcontent.append("regulerende instantie van een lidstaat uiterlijk op 30 juni 2024 en vervolgens om de")
    thisalinea.textcontent.append("drie jaar de potentiële bijdrage van bidirectioneel laden aan de integratie van")
    thisalinea.textcontent.append("hernieuwbare elektriciteit in het elektriciteitssysteem. Die beoordeling wordt")
    thisalinea.textcontent.append("openbaar gemaakt. Op basis van de resultaten van die beoordeling nemen de lidstaten")
    thisalinea.textcontent.append("zo nodig passende maatregelen om de beschikbaarheid en geografische spreiding van")
    thisalinea.textcontent.append("bidirectionele laadpunten op zowel openbare als particuliere plaatsen bij te sturen en")
    thisalinea.textcontent.append("nemen zij die maatregelen op in hun voortgangsverslag als bedoeld in lid 1.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5. De Commissie stelt richtsnoeren en ..."
    thisalinea.nativeID = 302
    thisalinea.parentID = 297
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "5. De Commissie stelt richtsnoeren en modellen vast met betrekking tot de inhoud, structuur en het formaat van de nationale beleidskaders en de inhoud van de nationale voortgangsverslagen die de lidstaten zes maanden na de in artikel 24 bedoelde datum overeenkomstig artikel 13, lid 1, moeten indienen. De Commissie kan richtsnoeren en modellen vaststellen om de doeltreffende toepassing van alle andere bepalingen van deze verordening in de Unie te faciliteren. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("5. De Commissie stelt richtsnoeren en modellen vast met betrekking tot de inhoud,")
    thisalinea.textcontent.append("structuur en het formaat van de nationale beleidskaders en de inhoud van de")
    thisalinea.textcontent.append("nationale voortgangsverslagen die de lidstaten zes maanden na de in artikel 24")
    thisalinea.textcontent.append("bedoelde datum overeenkomstig artikel 13, lid 1, moeten indienen. De Commissie")
    thisalinea.textcontent.append("kan richtsnoeren en modellen vaststellen om de doeltreffende toepassing van alle")
    thisalinea.textcontent.append("andere bepalingen van deze verordening in de Unie te faciliteren.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 15"
    thisalinea.nativeID = 303
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 22
    thisalinea.summary = "Beoordeling van de nationale beleidskaders en voortgangsverslagen 1. Uiterlijk 1 januari 2026 beoordeelt de Commissie de door de lidstaten overeenkomstig artikel 13, lid 9, ingediende nationale beleidskaders en dient zij bij het Europees Parlement en de Raad een verslag in over de beoordeling van de nationale beleidskaders en de samenhang daarvan op het niveau van de Unie, inclusief een evaluatie van de mate waarin de in artikel 13, lid 1, bedoelde nationale streefcijfers en doelen zijn verwezenlijkt. 2. De Commissie beoordeelt de door de lidstaten overeenkomstig artikel 14, lid 1, ingediende voortgangsverslagen en doet in voorkomend geval aanbevelingen aan de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Beoordeling van de nationale beleidskaders en voortgangsverslagen")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Uiterlijk 1 januari 2026 beoordeelt ..."
    thisalinea.nativeID = 304
    thisalinea.parentID = 303
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Uiterlijk 1 januari 2026 beoordeelt de Commissie de door de lidstaten overeenkomstig artikel 13, lid 9, ingediende nationale beleidskaders en dient zij bij het Europees Parlement en de Raad een verslag in over de beoordeling van de nationale beleidskaders en de samenhang daarvan op het niveau van de Unie, inclusief een evaluatie van de mate waarin de in artikel 13, lid 1, bedoelde nationale streefcijfers en doelen zijn verwezenlijkt. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Uiterlijk 1 januari 2026 beoordeelt de Commissie de door de lidstaten")
    thisalinea.textcontent.append("overeenkomstig artikel 13, lid 9, ingediende nationale beleidskaders en dient zij bij")
    thisalinea.textcontent.append("het Europees Parlement en de Raad een verslag in over de beoordeling van de")
    thisalinea.textcontent.append("nationale beleidskaders en de samenhang daarvan op het niveau van de Unie,")
    thisalinea.textcontent.append("inclusief een evaluatie van de mate waarin de in artikel 13, lid 1, bedoelde nationale")
    thisalinea.textcontent.append("streefcijfers en doelen zijn verwezenlijkt.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. De Commissie beoordeelt de door ..."
    thisalinea.nativeID = 305
    thisalinea.parentID = 303
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. De Commissie beoordeelt de door de lidstaten overeenkomstig artikel 14, lid 1, ingediende voortgangsverslagen en doet in voorkomend geval aanbevelingen aan de lidstaten om ervoor te zorgen dat de in deze verordening vastgestelde doelstellingen en verplichtingen worden verwezenlijkt. Uiterlijk zes maanden na die aanbevelingen van de Commissie dienen de lidstaten bij de Commissie een actualisering van hun voortgangsverslag in. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. De Commissie beoordeelt de door de lidstaten overeenkomstig artikel 14, lid 1,")
    thisalinea.textcontent.append("ingediende voortgangsverslagen en doet in voorkomend geval aanbevelingen aan de")
    thisalinea.textcontent.append("lidstaten om ervoor te zorgen dat de in deze verordening vastgestelde doelstellingen")
    thisalinea.textcontent.append("en verplichtingen worden verwezenlijkt. Uiterlijk zes maanden na die aanbevelingen")
    thisalinea.textcontent.append("van de Commissie dienen de lidstaten bij de Commissie een actualisering van hun")
    thisalinea.textcontent.append("voortgangsverslag in.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. De Commissie dient één jaar ..."
    thisalinea.nativeID = 306
    thisalinea.parentID = 303
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. De Commissie dient één jaar na de indiening van de nationale voortgangsverslagen door de lidstaten bij het Europees Parlement en de Raad een verslag in over haar beoordeling van de voortgangsverslagen overeenkomstig artikel 14, lid 1. Daarin worden de volgende aspecten beoordeeld: (a) de vooruitgang die de lidstaten hebben geboekt bij de verwezenlijking van de streefcijfers en doelstellingen; (b) de samenhang van de ontwikkeling op EU-niveau. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. De Commissie dient één jaar na de indiening van de nationale voortgangsverslagen")
    thisalinea.textcontent.append("door de lidstaten bij het Europees Parlement en de Raad een verslag in over haar")
    thisalinea.textcontent.append("beoordeling van de voortgangsverslagen overeenkomstig artikel 14, lid 1. Daarin")
    thisalinea.textcontent.append("worden de volgende aspecten beoordeeld:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) de vooruitgang die de lidstaten ..."
    thisalinea.nativeID = 307
    thisalinea.parentID = 306
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) de vooruitgang die de lidstaten hebben geboekt bij de verwezenlijking van de streefcijfers en doelstellingen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) de vooruitgang die de lidstaten hebben geboekt bij de verwezenlijking van de")
    thisalinea.textcontent.append("streefcijfers en doelstellingen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) de samenhang van de ontwikkeling ..."
    thisalinea.nativeID = 308
    thisalinea.parentID = 306
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) de samenhang van de ontwikkeling op EU-niveau. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) de samenhang van de ontwikkeling op EU-niveau.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. Op basis van de door ..."
    thisalinea.nativeID = 309
    thisalinea.parentID = 303
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. Op basis van de door de lidstaten overeenkomstig artikel 13, lid 1, en artikel 14, lid 1, ingediende nationale beleidskaders en nationale voortgangsverslagen, publiceert en actualiseert de Commissie regelmatig informatie over de door de lidstaten meegedeelde nationale streefcijfers en doelstellingen met betrekking tot: (a) het aantal openbaar toegankelijke laadpunten en -stations, uitgesplitst in laadpunten voor lichte voertuigen en laadpunten voor zware bedrijfsvoertuigen, en overeenkomstig de categorisering in bijlage III; (b) het aantal openbaar toegankelijke waterstoftankpunten; (c) de infrastructuur voor walstroomvoorziening in zee- en binnenhavens van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk; (d) de infrastructuur voor elektriciteitsvoorziening voor stilstaande luchtvaartuigen "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. Op basis van de door de lidstaten overeenkomstig artikel 13, lid 1, en artikel 14, lid")
    thisalinea.textcontent.append("1, ingediende nationale beleidskaders en nationale voortgangsverslagen, publiceert")
    thisalinea.textcontent.append("en actualiseert de Commissie regelmatig informatie over de door de lidstaten")
    thisalinea.textcontent.append("meegedeelde nationale streefcijfers en doelstellingen met betrekking tot:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) het aantal openbaar toegankelijke laadpunten ..."
    thisalinea.nativeID = 310
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) het aantal openbaar toegankelijke laadpunten en -stations, uitgesplitst in laadpunten voor lichte voertuigen en laadpunten voor zware bedrijfsvoertuigen, en overeenkomstig de categorisering in bijlage III; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) het aantal openbaar toegankelijke laadpunten en -stations, uitgesplitst in")
    thisalinea.textcontent.append("laadpunten voor lichte voertuigen en laadpunten voor zware bedrijfsvoertuigen,")
    thisalinea.textcontent.append("en overeenkomstig de categorisering in bijlage III;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) het aantal openbaar toegankelijke waterstoftankpunten; "
    thisalinea.nativeID = 311
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) het aantal openbaar toegankelijke waterstoftankpunten; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) het aantal openbaar toegankelijke waterstoftankpunten;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(c) de infrastructuur voor walstroomvoorziening in ..."
    thisalinea.nativeID = 312
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(c) de infrastructuur voor walstroomvoorziening in zee- en binnenhavens van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(c) de infrastructuur voor walstroomvoorziening in zee- en binnenhavens van het")
    thisalinea.textcontent.append("TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(d) de infrastructuur voor elektriciteitsvoorziening voor ..."
    thisalinea.nativeID = 313
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "(d) de infrastructuur voor elektriciteitsvoorziening voor stilstaande luchtvaartuigen op luchthavens van het TEN-T-kernnetwerk en het uitgebreide TEN-T- netwerk; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(d) de infrastructuur voor elektriciteitsvoorziening voor stilstaande luchtvaartuigen")
    thisalinea.textcontent.append("op luchthavens van het TEN-T-kernnetwerk en het uitgebreide TEN-T-")
    thisalinea.textcontent.append("netwerk;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(e) het aantal LNG-tankpunten in zee- ..."
    thisalinea.nativeID = 314
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "(e) het aantal LNG-tankpunten in zee- en binnenhavens van het TEN-T- kernnetwerk en het uitgebreide TEN-T-netwerk; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(e) het aantal LNG-tankpunten in zee- en binnenhavens van het TEN-T-")
    thisalinea.textcontent.append("kernnetwerk en het uitgebreide TEN-T-netwerk;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(f) het aantal openbaar toegankelijke LNG-tankpunten ..."
    thisalinea.nativeID = 315
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "(f) het aantal openbaar toegankelijke LNG-tankpunten voor motorvoertuigen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(f) het aantal openbaar toegankelijke LNG-tankpunten voor motorvoertuigen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(g) het aantal openbaar toegankelijke CNG-tankpunten ..."
    thisalinea.nativeID = 316
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "(g) het aantal openbaar toegankelijke CNG-tankpunten voor motorvoertuigen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(g) het aantal openbaar toegankelijke CNG-tankpunten voor motorvoertuigen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(h) de tank- en laadpunten voor ..."
    thisalinea.nativeID = 317
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "(h) de tank- en laadpunten voor andere alternatieve brandstoffen in zee- en binnenhavens van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(h) de tank- en laadpunten voor andere alternatieve brandstoffen in zee- en")
    thisalinea.textcontent.append("binnenhavens van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(i) de tank- en laadinfrastructuur voor ..."
    thisalinea.nativeID = 318
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "(i) de tank- en laadinfrastructuur voor andere alternatieve brandstoffen in luchthavens van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(i) de tank- en laadinfrastructuur voor andere alternatieve brandstoffen in")
    thisalinea.textcontent.append("luchthavens van het TEN-T-kernnetwerk en het uitgebreide TEN-T-netwerk;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(j) tank- en laadpunten voor treinen. "
    thisalinea.nativeID = 319
    thisalinea.parentID = 309
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 9
    thisalinea.summary = "(j) tank- en laadpunten voor treinen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(j) tank- en laadpunten voor treinen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 16"
    thisalinea.nativeID = 320
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 23
    thisalinea.summary = "Voortgangsbewaking doelstellingen kan worden getoetst. Indien de Commissie de corrigerende maatregelen toereikend acht, actualiseert de betrokken lidstaat zijn laatste voortgangsverslag als bedoeld in artikel 14 met de corrigerende maatregelen en stelt hij de Commissie daarvan in kennis. 1. Uiterlijk op 28 februari van het jaar na de inwerkingtreding van deze verordening en vervolgens jaarlijks uiterlijk op dezelfde datum brengen de lidstaten aan de Commissie verslag uit over het totale laadvermogen, het aantal openbaar toegankelijke laadpunten en het aantal geregistreerde plug-in hybride- en batterijvoertuigen die op 31 december van het voorgaande jaar op hun grondgebied in gebruik waren, overeenkomstig de voorschriften "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Voortgangsbewaking")
    thisalinea.textcontent.append("doelstellingen kan worden getoetst. Indien de Commissie de corrigerende")
    thisalinea.textcontent.append("maatregelen toereikend acht, actualiseert de betrokken lidstaat zijn laatste")
    thisalinea.textcontent.append("voortgangsverslag als bedoeld in artikel 14 met de corrigerende maatregelen en stelt")
    thisalinea.textcontent.append("hij de Commissie daarvan in kennis.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Uiterlijk op 28 februari van ..."
    thisalinea.nativeID = 321
    thisalinea.parentID = 320
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Uiterlijk op 28 februari van het jaar na de inwerkingtreding van deze verordening en vervolgens jaarlijks uiterlijk op dezelfde datum brengen de lidstaten aan de Commissie verslag uit over het totale laadvermogen, het aantal openbaar toegankelijke laadpunten en het aantal geregistreerde plug-in hybride- en batterijvoertuigen die op 31 december van het voorgaande jaar op hun grondgebied in gebruik waren, overeenkomstig de voorschriften van bijlage III. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Uiterlijk op 28 februari van het jaar na de inwerkingtreding van deze verordening en")
    thisalinea.textcontent.append("vervolgens jaarlijks uiterlijk op dezelfde datum brengen de lidstaten aan de")
    thisalinea.textcontent.append("Commissie verslag uit over het totale laadvermogen, het aantal openbaar")
    thisalinea.textcontent.append("toegankelijke laadpunten en het aantal geregistreerde plug-in hybride- en")
    thisalinea.textcontent.append("batterijvoertuigen die op 31 december van het voorgaande jaar op hun grondgebied")
    thisalinea.textcontent.append("in gebruik waren, overeenkomstig de voorschriften van bijlage III.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Wanneer uit het in lid ..."
    thisalinea.nativeID = 322
    thisalinea.parentID = 320
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Wanneer uit het in lid 1 van dit artikel bedoelde verslag of uit informatie waarover de Commissie beschikt, blijkt dat het risico bestaat dat een lidstaat zijn nationale streefcijfers als bedoeld in artikel 3, lid 1, niet haalt, kan de Commissie een bevinding in die zin formuleren en de betrokken lidstaat verzoeken corrigerende maatregelen te nemen om de nationale streefcijfers alsnog te halen. Binnen drie maanden na ontvangst van de bevindingen van de Commissie stelt de betrokken lidstaat de Commissie in kennis van de corrigerende maatregelen die hij voornemens is uit te voeren om de in artikel 3, lid "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Wanneer uit het in lid 1 van dit artikel bedoelde verslag of uit informatie waarover de")
    thisalinea.textcontent.append("Commissie beschikt, blijkt dat het risico bestaat dat een lidstaat zijn nationale")
    thisalinea.textcontent.append("streefcijfers als bedoeld in artikel 3, lid 1, niet haalt, kan de Commissie een")
    thisalinea.textcontent.append("bevinding in die zin formuleren en de betrokken lidstaat verzoeken corrigerende")
    thisalinea.textcontent.append("maatregelen te nemen om de nationale streefcijfers alsnog te halen. Binnen drie")
    thisalinea.textcontent.append("maanden na ontvangst van de bevindingen van de Commissie stelt de betrokken")
    thisalinea.textcontent.append("lidstaat de Commissie in kennis van de corrigerende maatregelen die hij voornemens")
    thisalinea.textcontent.append("is uit te voeren om de in artikel 3, lid 1, vastgestelde streefcijfers te halen. De")
    thisalinea.textcontent.append("corrigerende maatregelen omvatten aanvullende maatregelen die de lidstaat zal")
    thisalinea.textcontent.append("uitvoeren om de in artikel 3, lid 1, vastgestelde streefcijfers te halen, en een duidelijk")
    thisalinea.textcontent.append("tijdschema voor maatregelen waaraan de jaarlijkse voortgang bij het behalen van die")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 17"
    thisalinea.nativeID = 323
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 24
    thisalinea.summary = "Informatie voor gebruikers 1. Er moet relevante, coherente en duidelijke informatie beschikbaar worden gesteld met betrekking tot motorvoertuigen die kunnen rijden op specifieke brandstoffen die in de handel worden gebracht of die op laadpunten kunnen worden opgeladen. Die informatie moet worden meegedeeld in de motorvoertuighandleidingen, bij de tank- en laadpunten, op de motorvoertuigen en bij de verkopers van motorvoertuigen. Deze eis geldt voor alle motorvoertuigen en de bijbehorende handleidingen die na 18 november 2016 op de markt worden gebracht. 2. De identificatie van de compatibiliteit tussen voertuigen en infrastructuur alsmede de identificatie van de compatibiliteit tussen brandstoffen en voertuigen, als "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Informatie voor gebruikers")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Er moet relevante, coherente en ..."
    thisalinea.nativeID = 324
    thisalinea.parentID = 323
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Er moet relevante, coherente en duidelijke informatie beschikbaar worden gesteld met betrekking tot motorvoertuigen die kunnen rijden op specifieke brandstoffen die in de handel worden gebracht of die op laadpunten kunnen worden opgeladen. Die informatie moet worden meegedeeld in de motorvoertuighandleidingen, bij de tank- en laadpunten, op de motorvoertuigen en bij de verkopers van motorvoertuigen. Deze eis geldt voor alle motorvoertuigen en de bijbehorende handleidingen die na 18 november 2016 op de markt worden gebracht. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Er moet relevante, coherente en duidelijke informatie beschikbaar worden gesteld")
    thisalinea.textcontent.append("met betrekking tot motorvoertuigen die kunnen rijden op specifieke brandstoffen die")
    thisalinea.textcontent.append("in de handel worden gebracht of die op laadpunten kunnen worden opgeladen. Die")
    thisalinea.textcontent.append("informatie moet worden meegedeeld in de motorvoertuighandleidingen, bij de tank-")
    thisalinea.textcontent.append("en laadpunten, op de motorvoertuigen en bij de verkopers van motorvoertuigen. Deze")
    thisalinea.textcontent.append("eis geldt voor alle motorvoertuigen en de bijbehorende handleidingen die na")
    thisalinea.textcontent.append("18 november 2016 op de markt worden gebracht.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. De identificatie van de compatibiliteit ..."
    thisalinea.nativeID = 325
    thisalinea.parentID = 323
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. De identificatie van de compatibiliteit tussen voertuigen en infrastructuur alsmede de identificatie van de compatibiliteit tussen brandstoffen en voertuigen, als bedoeld in lid 1, moeten voldoen aan de in bijlage II, punten 9.1 en 9.2, bedoelde technische specificaties. Indien deze normen betrekking hebben op de grafische weergave, m.i.v. kleurcodes, moet die weergave eenvoudig en gemakkelijk te begrijpen zijn en op een duidelijk zichtbare manier worden aangebracht: (a) op de overeenkomstige pompen en hun vulpistolen bij alle tankpunten, vanaf de datum waarop de brandstoffen op de markt worden gebracht; of (b) in de onmiddellijke nabijheid van de brandstoftankkleppen van de "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. De identificatie van de compatibiliteit tussen voertuigen en infrastructuur alsmede de")
    thisalinea.textcontent.append("identificatie van de compatibiliteit tussen brandstoffen en voertuigen, als bedoeld in")
    thisalinea.textcontent.append("lid 1, moeten voldoen aan de in bijlage II, punten 9.1 en 9.2, bedoelde technische")
    thisalinea.textcontent.append("specificaties. Indien deze normen betrekking hebben op de grafische weergave,")
    thisalinea.textcontent.append("m.i.v. kleurcodes, moet die weergave eenvoudig en gemakkelijk te begrijpen zijn en")
    thisalinea.textcontent.append("op een duidelijk zichtbare manier worden aangebracht:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) op de overeenkomstige pompen en ..."
    thisalinea.nativeID = 326
    thisalinea.parentID = 325
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) op de overeenkomstige pompen en hun vulpistolen bij alle tankpunten, vanaf de datum waarop de brandstoffen op de markt worden gebracht; of "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) op de overeenkomstige pompen en hun vulpistolen bij alle tankpunten, vanaf")
    thisalinea.textcontent.append("de datum waarop de brandstoffen op de markt worden gebracht; of")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) in de onmiddellijke nabijheid van ..."
    thisalinea.nativeID = 327
    thisalinea.parentID = 325
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) in de onmiddellijke nabijheid van de brandstoftankkleppen van de motorvoertuigen die aanbevolen zijn voor en compatibel zijn met de desbetreffende brandstof, en in handleidingen van motorvoertuigen, als die motorvoertuigen na 18 november 2016 op de markt zijn gebracht. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) in de onmiddellijke nabijheid van de brandstoftankkleppen van de")
    thisalinea.textcontent.append("motorvoertuigen die aanbevolen zijn voor en compatibel zijn met de")
    thisalinea.textcontent.append("desbetreffende brandstof, en in handleidingen van motorvoertuigen, als die")
    thisalinea.textcontent.append("motorvoertuigen na 18 november 2016 op de markt zijn gebracht.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Wanneer de brandstofprijzen in een ..."
    thisalinea.nativeID = 328
    thisalinea.parentID = 323
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Wanneer de brandstofprijzen in een tankstation worden weergegeven, wordt in voorkomend geval een vergelijking tussen de relevante eenheidsprijzen getoond en wordt, met name voor elektriciteit en waterstof, ter informatie de in bijlage II, punt 9.3, bedoelde gemeenschappelijke methodologie voor prijsvergelijking per eenheid voor alternatieve brandstoffen meegedeeld. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Wanneer de brandstofprijzen in een tankstation worden weergegeven, wordt in")
    thisalinea.textcontent.append("voorkomend geval een vergelijking tussen de relevante eenheidsprijzen getoond en")
    thisalinea.textcontent.append("wordt, met name voor elektriciteit en waterstof, ter informatie de in bijlage II, punt")
    thisalinea.textcontent.append("9.3, bedoelde gemeenschappelijke methodologie voor prijsvergelijking per eenheid")
    thisalinea.textcontent.append("voor alternatieve brandstoffen meegedeeld.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. Als in de Europese normen ..."
    thisalinea.nativeID = 329
    thisalinea.parentID = 323
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. Als in de Europese normen tot vaststelling van technische specificaties van een brandstof geen etiketteringsvoorschriften voor de naleving van de betrokken normen zijn opgenomen, als er in de etiketteringsvoorschriften geen sprake is van een grafische weergave met kleurcodes, of als de etiketteringsvoorschriften niet geschikt zijn om de doelstellingen van deze verordening te verwezenlijken, kan de Commissie met het oog op de uniforme toepassing van de leden 1 en 2: (a) de ENO’s de opdracht geven specificaties voor compatibiliteitsetikettering te ontwikkelen; (b) uitvoeringshandelingen vaststellen tot bepaling van de grafische weergave, met inbegrip van kleurcodes, betreffende de compatibiliteit van brandstoffen die "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. Als in de Europese normen tot vaststelling van technische specificaties van een")
    thisalinea.textcontent.append("brandstof geen etiketteringsvoorschriften voor de naleving van de betrokken normen")
    thisalinea.textcontent.append("zijn opgenomen, als er in de etiketteringsvoorschriften geen sprake is van een")
    thisalinea.textcontent.append("grafische weergave met kleurcodes, of als de etiketteringsvoorschriften niet geschikt")
    thisalinea.textcontent.append("zijn om de doelstellingen van deze verordening te verwezenlijken, kan de Commissie")
    thisalinea.textcontent.append("met het oog op de uniforme toepassing van de leden 1 en 2:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) de ENO’s de opdracht geven ..."
    thisalinea.nativeID = 330
    thisalinea.parentID = 329
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) de ENO’s de opdracht geven specificaties voor compatibiliteitsetikettering te ontwikkelen; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) de ENO’s de opdracht geven specificaties voor compatibiliteitsetikettering te")
    thisalinea.textcontent.append("ontwikkelen;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) uitvoeringshandelingen vaststellen tot bepaling van ..."
    thisalinea.nativeID = 331
    thisalinea.parentID = 329
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) uitvoeringshandelingen vaststellen tot bepaling van de grafische weergave, met inbegrip van kleurcodes, betreffende de compatibiliteit van brandstoffen die op de EU-markt worden gebracht en die volgens de analyse van de Commissie minstens 1 % van het totale verkoopvolume in meer dan één lidstaat vertegenwoordigen. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) uitvoeringshandelingen vaststellen tot bepaling van de grafische weergave, met")
    thisalinea.textcontent.append("inbegrip van kleurcodes, betreffende de compatibiliteit van brandstoffen die op")
    thisalinea.textcontent.append("de EU-markt worden gebracht en die volgens de analyse van de Commissie")
    thisalinea.textcontent.append("minstens 1 % van het totale verkoopvolume in meer dan één lidstaat")
    thisalinea.textcontent.append("vertegenwoordigen.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5. Als de etiketteringsvoorschriften van de ..."
    thisalinea.nativeID = 332
    thisalinea.parentID = 323
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "5. Als de etiketteringsvoorschriften van de respectieve Europese normen worden geactualiseerd, als uitvoeringshandelingen betreffende etikettering worden vastgesteld of als nieuwe Europese normen voor alternatieve brandstoffen worden ontwikkeld, zijn de overeenkomstige etiketteringseisen 24 maanden na de datum van vaststelling of actualisering van toepassing op alle tank- en laadpunten en op alle motorvoertuigen die op het grondgebied van de lidstaten zijn ingeschreven "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("5. Als de etiketteringsvoorschriften van de respectieve Europese normen worden")
    thisalinea.textcontent.append("geactualiseerd, als uitvoeringshandelingen betreffende etikettering worden")
    thisalinea.textcontent.append("vastgesteld of als nieuwe Europese normen voor alternatieve brandstoffen worden")
    thisalinea.textcontent.append("ontwikkeld, zijn de overeenkomstige etiketteringseisen 24 maanden na de datum van")
    thisalinea.textcontent.append("vaststelling of actualisering van toepassing op alle tank- en laadpunten en op alle")
    thisalinea.textcontent.append("motorvoertuigen die op het grondgebied van de lidstaten zijn ingeschreven")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 18"
    thisalinea.nativeID = 333
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 25
    thisalinea.summary = "Gegevensverstrekking 1. De lidstaten wijzen een organisatie voor identificatieregistratie (IDRO) aan. Uiterlijk één jaar na de in artikel 24 bedoelde datum verleent de IDRO unieke identificatiecodes (ID's) voor de identificatie van ten minste de exploitanten van laadpunten en aanbieders van mobiliteitsdiensten. 2. Exploitanten van openbaar toegankelijke laad- en tankpunten of, overeenkomstig de tussen beide partijen getroffen regelingen, eigenaars van dergelijke punten zorgen ervoor dat statische en dynamische gegevens over de door hen geëxploiteerde infrastructuur voor alternatieve brandstoffen beschikbaar is en dat die gegevens kosteloos toegankelijk zijn via de nationale toegangspunten. De volgende types gegevens worden beschikbaar gesteld: (a) statische gegevens "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Gegevensverstrekking")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. De lidstaten wijzen een organisatie ..."
    thisalinea.nativeID = 334
    thisalinea.parentID = 333
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. De lidstaten wijzen een organisatie voor identificatieregistratie (IDRO) aan. Uiterlijk één jaar na de in artikel 24 bedoelde datum verleent de IDRO unieke identificatiecodes (ID's) voor de identificatie van ten minste de exploitanten van laadpunten en aanbieders van mobiliteitsdiensten. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. De lidstaten wijzen een organisatie voor identificatieregistratie (IDRO) aan. Uiterlijk")
    thisalinea.textcontent.append("één jaar na de in artikel 24 bedoelde datum verleent de IDRO unieke")
    thisalinea.textcontent.append("identificatiecodes (ID's) voor de identificatie van ten minste de exploitanten van")
    thisalinea.textcontent.append("laadpunten en aanbieders van mobiliteitsdiensten.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Exploitanten van openbaar toegankelijke laad- ..."
    thisalinea.nativeID = 335
    thisalinea.parentID = 333
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Exploitanten van openbaar toegankelijke laad- en tankpunten of, overeenkomstig de tussen beide partijen getroffen regelingen, eigenaars van dergelijke punten zorgen ervoor dat statische en dynamische gegevens over de door hen geëxploiteerde infrastructuur voor alternatieve brandstoffen beschikbaar is en dat die gegevens kosteloos toegankelijk zijn via de nationale toegangspunten. De volgende types gegevens worden beschikbaar gesteld: (a) statische gegevens over de door hen geëxploiteerde openbaar toegankelijke laad- en tankpunten: i) de geografische locatie van het laad- of tankpunt, ii) het aantal connectoren, iii) het aantal parkeerplaatsen voor personen met een handicap, iv) contactgegevens van de eigenaar en de exploitant van "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Exploitanten van openbaar toegankelijke laad- en tankpunten of, overeenkomstig de")
    thisalinea.textcontent.append("tussen beide partijen getroffen regelingen, eigenaars van dergelijke punten zorgen")
    thisalinea.textcontent.append("ervoor dat statische en dynamische gegevens over de door hen geëxploiteerde")
    thisalinea.textcontent.append("infrastructuur voor alternatieve brandstoffen beschikbaar is en dat die gegevens")
    thisalinea.textcontent.append("kosteloos toegankelijk zijn via de nationale toegangspunten. De volgende types")
    thisalinea.textcontent.append("gegevens worden beschikbaar gesteld:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) statische gegevens over de door ..."
    thisalinea.nativeID = 336
    thisalinea.parentID = 335
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) statische gegevens over de door hen geëxploiteerde openbaar toegankelijke laad- en tankpunten: i) de geografische locatie van het laad- of tankpunt, ii) het aantal connectoren, iii) het aantal parkeerplaatsen voor personen met een handicap, iv) contactgegevens van de eigenaar en de exploitant van het laad- en tankstation. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) statische gegevens over de door hen geëxploiteerde openbaar toegankelijke")
    thisalinea.textcontent.append("laad- en tankpunten:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "i) de geografische locatie van het ..."
    thisalinea.nativeID = 337
    thisalinea.parentID = 336
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i) de geografische locatie van het laad- of tankpunt, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i) de geografische locatie van het laad- of tankpunt,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "ii) het aantal connectoren, "
    thisalinea.nativeID = 338
    thisalinea.parentID = 336
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii) het aantal connectoren, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii) het aantal connectoren,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "iii) het aantal parkeerplaatsen voor personen ..."
    thisalinea.nativeID = 339
    thisalinea.parentID = 336
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "iii) het aantal parkeerplaatsen voor personen met een handicap, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("iii) het aantal parkeerplaatsen voor personen met een handicap,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "iv) contactgegevens van de eigenaar en ..."
    thisalinea.nativeID = 340
    thisalinea.parentID = 336
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "iv) contactgegevens van de eigenaar en de exploitant van het laad- en tankstation. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("iv) contactgegevens van de eigenaar en de exploitant van het laad- en")
    thisalinea.textcontent.append("tankstation.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) aanvullende statische gegevens over de ..."
    thisalinea.nativeID = 341
    thisalinea.parentID = 335
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) aanvullende statische gegevens over de door hen geëxploiteerde openbaar toegankelijke laad- en tankpunten: i) identificatiecodes (ID), ten minste van de exploitant van het laadpunt en van de aanbieders van mobiliteitsdiensten die op dat laadpunt diensten aanbieden, zoals bedoeld in lid 1, ii) type connector, iii) stroomtype (AC/DC), iv) laadvermogen (kW), "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) aanvullende statische gegevens over de door hen geëxploiteerde openbaar")
    thisalinea.textcontent.append("toegankelijke laad- en tankpunten:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "i) identificatiecodes (ID), ten minste van ..."
    thisalinea.nativeID = 342
    thisalinea.parentID = 341
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i) identificatiecodes (ID), ten minste van de exploitant van het laadpunt en van de aanbieders van mobiliteitsdiensten die op dat laadpunt diensten aanbieden, zoals bedoeld in lid 1, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i) identificatiecodes (ID), ten minste van de exploitant van het laadpunt en")
    thisalinea.textcontent.append("van de aanbieders van mobiliteitsdiensten die op dat laadpunt diensten")
    thisalinea.textcontent.append("aanbieden, zoals bedoeld in lid 1,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "ii) type connector, "
    thisalinea.nativeID = 343
    thisalinea.parentID = 341
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii) type connector, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii) type connector,")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "iii) stroomtype (AC/DC), "
    thisalinea.nativeID = 344
    thisalinea.parentID = 341
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "iii) stroomtype (AC/DC), "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("iii) stroomtype (AC/DC),")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "iv) laadvermogen (kW), "
    thisalinea.nativeID = 345
    thisalinea.parentID = 341
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "iv) laadvermogen (kW), "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("iv) laadvermogen (kW),")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(c) dynamische gegevens over de door ..."
    thisalinea.nativeID = 346
    thisalinea.parentID = 335
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(c) dynamische gegevens over de door hen geëxploiteerde openbaar toegankelijke laad- en tankpunten: i) operationele status (in of buiten werking), ii) beschikbaarheid (in gebruik/niet in gebruik), iii) ad-hocprijs. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(c) dynamische gegevens over de door hen geëxploiteerde openbaar toegankelijke")
    thisalinea.textcontent.append("laad- en tankpunten:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "i) operationele status (in of buiten ..."
    thisalinea.nativeID = 347
    thisalinea.parentID = 346
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i) operationele status (in of buiten werking), "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i) operationele status (in of buiten werking),")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "ii) beschikbaarheid (in gebruik/niet in gebruik), "
    thisalinea.nativeID = 348
    thisalinea.parentID = 346
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii) beschikbaarheid (in gebruik/niet in gebruik), "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii) beschikbaarheid (in gebruik/niet in gebruik),")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "iii) ad-hocprijs. "
    thisalinea.nativeID = 349
    thisalinea.parentID = 346
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "iii) ad-hocprijs. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("iii) ad-hocprijs.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. De lidstaten zorgen ervoor dat ..."
    thisalinea.nativeID = 350
    thisalinea.parentID = 333
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. De lidstaten zorgen ervoor dat gegevens overeenkomstig Richtlijn 2010/40/EU29 van het Europees Parlement en de Raad via hun nationale toegangspunt op open en niet- discriminerende basis toegankelijk zijn voor alle belanghebbenden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. De lidstaten zorgen ervoor dat gegevens overeenkomstig Richtlijn 2010/40/EU29 van")
    thisalinea.textcontent.append("het Europees Parlement en de Raad via hun nationale toegangspunt op open en niet-")
    thisalinea.textcontent.append("discriminerende basis toegankelijk zijn voor alle belanghebbenden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. De Commissie is bevoegd om ..."
    thisalinea.nativeID = 351
    thisalinea.parentID = 333
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. De Commissie is bevoegd om overeenkomstig artikel 17 gedelegeerde handelingen vast te stellen teneinde: (a) aanvullende types gegevens toe te voegen aan de in lid 2 gespecificeerde types gegevens; (b) de elementen te specificeren met betrekking tot het formaat, de frequentie en de kwaliteit waarin deze gegevens beschikbaar worden gesteld; (c) gedetailleerde procedures vast te stellen voor het verstrekken en uitwisselen van de krachtens lid 2 vereiste gegevens. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. De Commissie is bevoegd om overeenkomstig artikel 17 gedelegeerde handelingen")
    thisalinea.textcontent.append("vast te stellen teneinde:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) aanvullende types gegevens toe te ..."
    thisalinea.nativeID = 352
    thisalinea.parentID = 351
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) aanvullende types gegevens toe te voegen aan de in lid 2 gespecificeerde types gegevens; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) aanvullende types gegevens toe te voegen aan de in lid 2 gespecificeerde types")
    thisalinea.textcontent.append("gegevens;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) de elementen te specificeren met ..."
    thisalinea.nativeID = 353
    thisalinea.parentID = 351
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) de elementen te specificeren met betrekking tot het formaat, de frequentie en de kwaliteit waarin deze gegevens beschikbaar worden gesteld; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) de elementen te specificeren met betrekking tot het formaat, de frequentie en")
    thisalinea.textcontent.append("de kwaliteit waarin deze gegevens beschikbaar worden gesteld;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(c) gedetailleerde procedures vast te stellen ..."
    thisalinea.nativeID = 354
    thisalinea.parentID = 351
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "(c) gedetailleerde procedures vast te stellen voor het verstrekken en uitwisselen van de krachtens lid 2 vereiste gegevens. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(c) gedetailleerde procedures vast te stellen voor het verstrekken en uitwisselen")
    thisalinea.textcontent.append("van de krachtens lid 2 vereiste gegevens.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 19"
    thisalinea.nativeID = 355
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 26
    thisalinea.summary = "Gemeenschappelijke technische specificaties 1. Laadpunten met normaal vermogen voor elektrische voertuigen, met uitzondering van draadloze of inductieve eenheden, die met ingang van de in artikel 24 bedoelde datum worden geïnstalleerd of vernieuwd, moeten ten minste voldoen aan de technische specificaties van punt 1.1 van bijlage II. 2. Laadpunten met hoog vermogen voor elektrische voertuigen, met uitzondering van draadloze of inductieve eenheden, die met ingang van de in artikel 24 bedoelde datum worden geïnstalleerd of vernieuwd, moeten ten minste voldoen aan de technische specificaties van punt 1.2 van bijlage II. 3. Openbaar toegankelijke waterstoftankpunten die met ingang van de in artikel "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Gemeenschappelijke technische specificaties")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Laadpunten met normaal vermogen voor ..."
    thisalinea.nativeID = 356
    thisalinea.parentID = 355
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Laadpunten met normaal vermogen voor elektrische voertuigen, met uitzondering van draadloze of inductieve eenheden, die met ingang van de in artikel 24 bedoelde datum worden geïnstalleerd of vernieuwd, moeten ten minste voldoen aan de technische specificaties van punt 1.1 van bijlage II. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Laadpunten met normaal vermogen voor elektrische voertuigen, met uitzondering")
    thisalinea.textcontent.append("van draadloze of inductieve eenheden, die met ingang van de in artikel 24 bedoelde")
    thisalinea.textcontent.append("datum worden geïnstalleerd of vernieuwd, moeten ten minste voldoen aan de")
    thisalinea.textcontent.append("technische specificaties van punt 1.1 van bijlage II.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Laadpunten met hoog vermogen voor ..."
    thisalinea.nativeID = 357
    thisalinea.parentID = 355
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Laadpunten met hoog vermogen voor elektrische voertuigen, met uitzondering van draadloze of inductieve eenheden, die met ingang van de in artikel 24 bedoelde datum worden geïnstalleerd of vernieuwd, moeten ten minste voldoen aan de technische specificaties van punt 1.2 van bijlage II. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Laadpunten met hoog vermogen voor elektrische voertuigen, met uitzondering van")
    thisalinea.textcontent.append("draadloze of inductieve eenheden, die met ingang van de in artikel 24 bedoelde")
    thisalinea.textcontent.append("datum worden geïnstalleerd of vernieuwd, moeten ten minste voldoen aan de")
    thisalinea.textcontent.append("technische specificaties van punt 1.2 van bijlage II.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Openbaar toegankelijke waterstoftankpunten die met ..."
    thisalinea.nativeID = 358
    thisalinea.parentID = 355
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Openbaar toegankelijke waterstoftankpunten die met ingang van de in artikel 24 bedoelde datum worden geïnstalleerd of vernieuwd, moeten voldoen aan de technische specificaties van de punten 3.1, 3.2, 3.3 en 3.4 van bijlage II. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Openbaar toegankelijke waterstoftankpunten die met ingang van de in artikel 24")
    thisalinea.textcontent.append("bedoelde datum worden geïnstalleerd of vernieuwd, moeten voldoen aan de")
    thisalinea.textcontent.append("technische specificaties van de punten 3.1, 3.2, 3.3 en 3.4 van bijlage II.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. Walstroominstallaties voor de zeevaart die ..."
    thisalinea.nativeID = 359
    thisalinea.parentID = 355
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. Walstroominstallaties voor de zeevaart die met ingang van de in artikel 24 bedoelde datum worden geïnstalleerd of vernieuwd, moeten voldoen aan de technische specificaties van de punten 4.1 en 4.2 van bijlage II. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. Walstroominstallaties voor de zeevaart die met ingang van de in artikel 24 bedoelde")
    thisalinea.textcontent.append("datum worden geïnstalleerd of vernieuwd, moeten voldoen aan de technische")
    thisalinea.textcontent.append("specificaties van de punten 4.1 en 4.2 van bijlage II.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5. CNG-tankpunten voor motorvoertuigen die met ..."
    thisalinea.nativeID = 360
    thisalinea.parentID = 355
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "5. CNG-tankpunten voor motorvoertuigen die met ingang van de in artikel 24 bedoelde datum worden geïnstalleerd of vernieuwd, moeten voldoen aan de technische specificaties van punt 8 van bijlage II. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("5. CNG-tankpunten voor motorvoertuigen die met ingang van de in artikel 24 bedoelde")
    thisalinea.textcontent.append("datum worden geïnstalleerd of vernieuwd, moeten voldoen aan de technische")
    thisalinea.textcontent.append("specificaties van punt 8 van bijlage II.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "6. Overeenkomstig artikel 10 van Verordening ..."
    thisalinea.nativeID = 361
    thisalinea.parentID = 355
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "6. Overeenkomstig artikel 10 van Verordening (EU) nr. 1025/2012 kan de Commissie Europese normalisatieorganisaties verzoeken Europese normen op te stellen ter bepaling van technische specificaties betreffende de in bijlage II bij deze verordening vermelde gebieden waarvoor de Commissie geen gemeenschappelijke technische specificaties heeft vastgesteld. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("6. Overeenkomstig artikel 10 van Verordening (EU) nr. 1025/2012 kan de Commissie")
    thisalinea.textcontent.append("Europese normalisatieorganisaties verzoeken Europese normen op te stellen ter")
    thisalinea.textcontent.append("bepaling van technische specificaties betreffende de in bijlage II bij deze verordening")
    thisalinea.textcontent.append("vermelde gebieden waarvoor de Commissie geen gemeenschappelijke technische")
    thisalinea.textcontent.append("specificaties heeft vastgesteld.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "7. De Commissie is overeenkomstig artikel ..."
    thisalinea.nativeID = 362
    thisalinea.parentID = 355
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "7. De Commissie is overeenkomstig artikel 17 bevoegd om gedelegeerde handelingen vast te stellen teneinde: (a) dit artikel aan te vullen met gemeenschappelijke technische specificaties om volledige technische interoperabiliteit van de laad- en tankinfrastructuur mogelijk te maken op het gebied van fysieke aansluitingen en communicatie betreffende de in bijlage II genoemde gebieden; (b) bijlage II te wijzigen door de verwijzingen naar de normen in de technische specificaties in die bijlage bij te werken. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("7. De Commissie is overeenkomstig artikel 17 bevoegd om gedelegeerde handelingen")
    thisalinea.textcontent.append("vast te stellen teneinde:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(a) dit artikel aan te vullen ..."
    thisalinea.nativeID = 363
    thisalinea.parentID = 362
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "(a) dit artikel aan te vullen met gemeenschappelijke technische specificaties om volledige technische interoperabiliteit van de laad- en tankinfrastructuur mogelijk te maken op het gebied van fysieke aansluitingen en communicatie betreffende de in bijlage II genoemde gebieden; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(a) dit artikel aan te vullen met gemeenschappelijke technische specificaties")
    thisalinea.textcontent.append("om volledige technische interoperabiliteit van de laad- en")
    thisalinea.textcontent.append("tankinfrastructuur mogelijk te maken op het gebied van fysieke")
    thisalinea.textcontent.append("aansluitingen en communicatie betreffende de in bijlage II genoemde")
    thisalinea.textcontent.append("gebieden;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "(b) bijlage II te wijzigen door ..."
    thisalinea.nativeID = 364
    thisalinea.parentID = 362
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "(b) bijlage II te wijzigen door de verwijzingen naar de normen in de technische specificaties in die bijlage bij te werken. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("(b) bijlage II te wijzigen door de verwijzingen naar de normen in de")
    thisalinea.textcontent.append("technische specificaties in die bijlage bij te werken.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 20"
    thisalinea.nativeID = 365
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 27
    thisalinea.summary = "Uitoefening van de bevoegdheidsdelegatie 1. De bevoegdheid om gedelegeerde handelingen vast te stellen, wordt aan de Commissie toegekend onder de in dit artikel neergelegde voorwaarden. 2. De in de artikelen 18 en 19 bedoelde bevoegdheid om gedelegeerde handelingen vast te stellen, wordt aan de Commissie toegekend voor een termijn van vijf jaar met ingang van de in artikel 24 bedoelde datum. De Commissie stelt uiterlijk negen maanden voor het einde van de termijn van vijf jaar een verslag op over de bevoegdheidsdelegatie. De bevoegdheidsdelegatie wordt stilzwijgend met termijnen van dezelfde duur verlengd, tenzij het Europees Parlement of de Raad zich "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Uitoefening van de bevoegdheidsdelegatie")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. De bevoegdheid om gedelegeerde handelingen ..."
    thisalinea.nativeID = 366
    thisalinea.parentID = 365
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. De bevoegdheid om gedelegeerde handelingen vast te stellen, wordt aan de Commissie toegekend onder de in dit artikel neergelegde voorwaarden. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. De bevoegdheid om gedelegeerde handelingen vast te stellen, wordt aan de")
    thisalinea.textcontent.append("Commissie toegekend onder de in dit artikel neergelegde voorwaarden.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. De in de artikelen 18 ..."
    thisalinea.nativeID = 367
    thisalinea.parentID = 365
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. De in de artikelen 18 en 19 bedoelde bevoegdheid om gedelegeerde handelingen vast te stellen, wordt aan de Commissie toegekend voor een termijn van vijf jaar met ingang van de in artikel 24 bedoelde datum. De Commissie stelt uiterlijk negen maanden voor het einde van de termijn van vijf jaar een verslag op over de bevoegdheidsdelegatie. De bevoegdheidsdelegatie wordt stilzwijgend met termijnen van dezelfde duur verlengd, tenzij het Europees Parlement of de Raad zich uiterlijk drie maanden voor het einde van elke termijn tegen deze verlenging verzet. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. De in de artikelen 18 en 19 bedoelde bevoegdheid om gedelegeerde handelingen vast")
    thisalinea.textcontent.append("te stellen, wordt aan de Commissie toegekend voor een termijn van vijf jaar met")
    thisalinea.textcontent.append("ingang van de in artikel 24 bedoelde datum. De Commissie stelt uiterlijk negen")
    thisalinea.textcontent.append("maanden voor het einde van de termijn van vijf jaar een verslag op over de")
    thisalinea.textcontent.append("bevoegdheidsdelegatie. De bevoegdheidsdelegatie wordt stilzwijgend met termijnen")
    thisalinea.textcontent.append("van dezelfde duur verlengd, tenzij het Europees Parlement of de Raad zich uiterlijk")
    thisalinea.textcontent.append("drie maanden voor het einde van elke termijn tegen deze verlenging verzet.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Het Europees Parlement of de ..."
    thisalinea.nativeID = 368
    thisalinea.parentID = 365
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Het Europees Parlement of de Raad kan de in de artikelen 18 en 19 bedoelde bevoegdheidsdelegatie te allen tijde intrekken. Het besluit tot intrekking beëindigt de delegatie van de in dat besluit genoemde bevoegdheid. Het wordt van kracht op de dag na die van de bekendmaking ervan in het Publicatieblad van de Europese Unie of op een daarin genoemde latere datum. Het laat de geldigheid van de reeds van kracht zijnde gedelegeerde handelingen onverlet. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Het Europees Parlement of de Raad kan de in de artikelen 18 en 19 bedoelde")
    thisalinea.textcontent.append("bevoegdheidsdelegatie te allen tijde intrekken. Het besluit tot intrekking beëindigt de")
    thisalinea.textcontent.append("delegatie van de in dat besluit genoemde bevoegdheid. Het wordt van kracht op de")
    thisalinea.textcontent.append("dag na die van de bekendmaking ervan in het Publicatieblad van de Europese Unie of")
    thisalinea.textcontent.append("op een daarin genoemde latere datum. Het laat de geldigheid van de reeds van kracht")
    thisalinea.textcontent.append("zijnde gedelegeerde handelingen onverlet.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. Zodra de Commissie een gedelegeerde ..."
    thisalinea.nativeID = 369
    thisalinea.parentID = 365
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. Zodra de Commissie een gedelegeerde handeling heeft vastgesteld, doet zij daarvan gelijktijdig kennisgeving aan het Europees Parlement en de Raad. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. Zodra de Commissie een gedelegeerde handeling heeft vastgesteld, doet zij daarvan")
    thisalinea.textcontent.append("gelijktijdig kennisgeving aan het Europees Parlement en de Raad.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5. Een overeenkomstig de artikelen 18 ..."
    thisalinea.nativeID = 370
    thisalinea.parentID = 365
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "5. Een overeenkomstig de artikelen 18 en 19 vastgestelde gedelegeerde handeling treedt alleen in werking indien het Europees Parlement noch de Raad daartegen binnen een termijn van twee maanden na de kennisgeving van de handeling aan het Europees Parlement en de Raad bezwaar heeft gemaakt, of indien zowel het Europees Parlement als de Raad voor het verstrijken van die termijn de Commissie hebben meegedeeld dat zij daartegen geen bezwaar zullen maken. Die termijn wordt op initiatief van het Europees Parlement of de Raad met drie maanden verlengd. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("5. Een overeenkomstig de artikelen 18 en 19 vastgestelde gedelegeerde handeling treedt")
    thisalinea.textcontent.append("alleen in werking indien het Europees Parlement noch de Raad daartegen binnen een")
    thisalinea.textcontent.append("termijn van twee maanden na de kennisgeving van de handeling aan het Europees")
    thisalinea.textcontent.append("Parlement en de Raad bezwaar heeft gemaakt, of indien zowel het Europees")
    thisalinea.textcontent.append("Parlement als de Raad voor het verstrijken van die termijn de Commissie hebben")
    thisalinea.textcontent.append("meegedeeld dat zij daartegen geen bezwaar zullen maken. Die termijn wordt op")
    thisalinea.textcontent.append("initiatief van het Europees Parlement of de Raad met drie maanden verlengd.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 21"
    thisalinea.nativeID = 371
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 28
    thisalinea.summary = "Comitéprocedure besloten of door een eenvoudige meerderheid van de leden van het comité daarom wordt verzocht. 1. De Commissie wordt bijgestaan door een comité. Dat comité is een comité in de zin van Verordening (EU) nr. 182/2011. 2. Wanneer naar dit lid wordt verwezen, is artikel 5 van Verordening (EU) nr. 182/2011 van toepassing. Indien door het comité geen advies wordt uitgebracht, neemt de Commissie de ontwerpuitvoeringshandeling niet aan en is artikel 5, lid 4, derde alinea, van Verordening (EU) nr. 182/2011 van toepassing. 3. Wanneer het advies van het comité via de schriftelijke procedure moet worden verkregen, wordt die "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Comitéprocedure")
    thisalinea.textcontent.append("besloten of door een eenvoudige meerderheid van de leden van het comité daarom")
    thisalinea.textcontent.append("wordt verzocht.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. De Commissie wordt bijgestaan door ..."
    thisalinea.nativeID = 372
    thisalinea.parentID = 371
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. De Commissie wordt bijgestaan door een comité. Dat comité is een comité in de zin van Verordening (EU) nr. 182/2011. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. De Commissie wordt bijgestaan door een comité. Dat comité is een comité in de zin")
    thisalinea.textcontent.append("van Verordening (EU) nr. 182/2011.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Wanneer naar dit lid wordt ..."
    thisalinea.nativeID = 373
    thisalinea.parentID = 371
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Wanneer naar dit lid wordt verwezen, is artikel 5 van Verordening (EU) nr. 182/2011 van toepassing. Indien door het comité geen advies wordt uitgebracht, neemt de Commissie de ontwerpuitvoeringshandeling niet aan en is artikel 5, lid 4, derde alinea, van Verordening (EU) nr. 182/2011 van toepassing. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Wanneer naar dit lid wordt verwezen, is artikel 5 van Verordening (EU) nr. 182/2011")
    thisalinea.textcontent.append("van toepassing. Indien door het comité geen advies wordt uitgebracht, neemt de")
    thisalinea.textcontent.append("Commissie de ontwerpuitvoeringshandeling niet aan en is artikel 5, lid 4, derde")
    thisalinea.textcontent.append("alinea, van Verordening (EU) nr. 182/2011 van toepassing.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Wanneer het advies van het ..."
    thisalinea.nativeID = 374
    thisalinea.parentID = 371
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. Wanneer het advies van het comité via de schriftelijke procedure moet worden verkregen, wordt die procedure zonder gevolg beëindigd indien, binnen de termijn voor het uitbrengen van het advies, door de voorzitter van het comité daartoe wordt "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Wanneer het advies van het comité via de schriftelijke procedure moet worden")
    thisalinea.textcontent.append("verkregen, wordt die procedure zonder gevolg beëindigd indien, binnen de termijn")
    thisalinea.textcontent.append("voor het uitbrengen van het advies, door de voorzitter van het comité daartoe wordt")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 22"
    thisalinea.nativeID = 375
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 29
    thisalinea.summary = "Evaluatie Uiterlijk op 31 december 2026 evalueert de Commissie deze verordening en dient zij, in voorkomend geval, een voorstel in tot wijziging daarvan. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Evaluatie")
    thisalinea.textcontent.append("Uiterlijk op 31 december 2026 evalueert de Commissie deze verordening en dient zij, in")
    thisalinea.textcontent.append("voorkomend geval, een voorstel in tot wijziging daarvan.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 23 Intrekking"
    thisalinea.nativeID = 376
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 30
    thisalinea.summary = "1. Richtlijn 2014/94/EG wordt met ingang van de in artikel 24 bedoelde datum ingetrokken. 2. Verwijzingen naar de Richtlijn 2014/94/EG gelden als verwijzingen naar deze verordening en worden gelezen volgens de in bijlage IV opgenomen concordantietabel. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Richtlijn 2014/94/EG wordt met ingang ..."
    thisalinea.nativeID = 377
    thisalinea.parentID = 376
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Richtlijn 2014/94/EG wordt met ingang van de in artikel 24 bedoelde datum ingetrokken. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Richtlijn 2014/94/EG wordt met ingang van de in artikel 24 bedoelde datum")
    thisalinea.textcontent.append("ingetrokken.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Verwijzingen naar de Richtlijn 2014/94/EG ..."
    thisalinea.nativeID = 378
    thisalinea.parentID = 376
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Verwijzingen naar de Richtlijn 2014/94/EG gelden als verwijzingen naar deze verordening en worden gelezen volgens de in bijlage IV opgenomen concordantietabel. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Verwijzingen naar de Richtlijn 2014/94/EG gelden als verwijzingen naar deze")
    thisalinea.textcontent.append("verordening en worden gelezen volgens de in bijlage IV opgenomen")
    thisalinea.textcontent.append("concordantietabel.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Artikel 24"
    thisalinea.nativeID = 379
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 31
    thisalinea.summary = "Inwerkingtreding Deze verordening treedt in werking op de twintigste dag na die van de bekendmaking ervan in het Publicatieblad van de Europese Unie. Deze verordening is verbindend in al haar onderdelen en is rechtstreeks toepasselijk in elke lidstaat. Gedaan te Brussel, Voor het Europees Parlement Voor de Raad De voorzitter De voorzitter "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("Inwerkingtreding")
    thisalinea.textcontent.append("Deze verordening treedt in werking op de twintigste dag na die van de bekendmaking ervan in")
    thisalinea.textcontent.append("het Publicatieblad van de Europese Unie.")
    thisalinea.textcontent.append("Deze verordening is verbindend in al haar onderdelen en is rechtstreeks toepasselijk in elke")
    thisalinea.textcontent.append("lidstaat.")
    thisalinea.textcontent.append("Gedaan te Brussel,")
    thisalinea.textcontent.append("Voor het Europees Parlement Voor de Raad")
    thisalinea.textcontent.append("De voorzitter De voorzitter")
    alineas.append(thisalinea)

    return alineas
