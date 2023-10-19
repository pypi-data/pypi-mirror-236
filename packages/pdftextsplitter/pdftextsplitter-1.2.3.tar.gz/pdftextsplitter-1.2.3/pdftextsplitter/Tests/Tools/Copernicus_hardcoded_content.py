import sys
sys.path.insert(1, '../../')

from TextPart.textalinea import textalinea
from TextPart.masterrule import texttype
from TextPart.enum_type import enum_type

def hardcodedalineas_Copernicus() -> list[textalinea]:
    """
    This code holds the content of the textalineas-array in the textsplitter-class
    for the document Copernicus
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
    thisalinea.texttitle = "Copernicus"
    thisalinea.nativeID = 0
    thisalinea.parentID = -1
    thisalinea.alineatype = texttype.TITLE
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Les conclusions du Conseil sur « Copernicus à horizon 2035 » ont été préparées en vue du Conseil Compétitivité prévu le 10 juin 2022. La Présidence a proposé ce projet de conclusions du Conseil pour préparer les principaux axes de réflexion sur l’avenir du programme Copernicus à horizon 2035 et donner une direction politique aux futurs développements du programme en se reposant sur le Pacte Vert, la transition numérique et la sécurité afin de contribuer à une Europe plus résiliente. 2. Ces conclusions soulignent l’importance des évolutions technologiques et scientifiques à prendre en compte, y compris le numérique, ainsi "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "I. INTRODUCTION"
    thisalinea.nativeID = 1
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Les conclusions du Conseil sur « Copernicus à horizon 2035 » ont été préparées en vue du Conseil Compétitivité prévu le 10 juin 2022. La Présidence a proposé ce projet de conclusions du Conseil pour préparer les principaux axes de réflexion sur l’avenir du programme Copernicus à horizon 2035 et donner une direction politique aux futurs développements du programme en se reposant sur le Pacte Vert, la transition numérique et la sécurité afin de contribuer à une Europe plus résiliente. 2. Ces conclusions soulignent l’importance des évolutions technologiques et scientifiques à prendre en compte, y compris le numérique, ainsi "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. Les conclusions du Conseil sur ..."
    thisalinea.nativeID = 2
    thisalinea.parentID = 1
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. Les conclusions du Conseil sur « Copernicus à horizon 2035 » ont été préparées en vue du Conseil Compétitivité prévu le 10 juin 2022. La Présidence a proposé ce projet de conclusions du Conseil pour préparer les principaux axes de réflexion sur l’avenir du programme Copernicus à horizon 2035 et donner une direction politique aux futurs développements du programme en se reposant sur le Pacte Vert, la transition numérique et la sécurité afin de contribuer à une Europe plus résiliente. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. Les conclusions du Conseil sur « Copernicus à horizon 2035 » ont été préparées en vue du")
    thisalinea.textcontent.append("Conseil Compétitivité prévu le 10 juin 2022. La Présidence a proposé ce projet de conclusions")
    thisalinea.textcontent.append("du Conseil pour préparer les principaux axes de réflexion sur l’avenir du programme")
    thisalinea.textcontent.append("Copernicus à horizon 2035 et donner une direction politique aux futurs développements du")
    thisalinea.textcontent.append("programme en se reposant sur le Pacte Vert, la transition numérique et la sécurité afin de")
    thisalinea.textcontent.append("contribuer à une Europe plus résiliente.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. Ces conclusions soulignent l’importance des ..."
    thisalinea.nativeID = 3
    thisalinea.parentID = 1
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. Ces conclusions soulignent l’importance des évolutions technologiques et scientifiques à prendre en compte, y compris le numérique, ainsi que les besoins des utilisateurs et la complémentarité avec les services commerciaux ainsi que la contribution du programme aux enjeux de sécurité de l'Union. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. Ces conclusions soulignent l’importance des évolutions technologiques et scientifiques à")
    thisalinea.textcontent.append("prendre en compte, y compris le numérique, ainsi que les besoins des utilisateurs et la")
    thisalinea.textcontent.append("complémentarité avec les services commerciaux ainsi que la contribution du programme aux")
    thisalinea.textcontent.append("enjeux de sécurité de l'Union.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "II. ETAT DES LIEUX"
    thisalinea.nativeID = 4
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "3. Le groupe Espace a examiné le projet de conclusions lors de six réunions depuis le 18 janvier 2022. 4. Le texte présenté en Annexe de cette Note est identique au texte circulé après le groupe Espace (doc. 7745/21 +REV3) et qui n’a pas soulevé d’objections de la part des délégations. Il représente un compromis acceptable qui ouvre la voie à une approbation par le Conseil. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. Le groupe Espace a examiné ..."
    thisalinea.nativeID = 5
    thisalinea.parentID = 4
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "3. Le groupe Espace a examiné le projet de conclusions lors de six réunions depuis le 18 janvier 2022. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. Le groupe Espace a examiné le projet de conclusions lors de six réunions depuis le 18 janvier")
    thisalinea.textcontent.append("2022.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. Le texte présenté en Annexe ..."
    thisalinea.nativeID = 6
    thisalinea.parentID = 4
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "4. Le texte présenté en Annexe de cette Note est identique au texte circulé après le groupe Espace (doc. 7745/21 +REV3) et qui n’a pas soulevé d’objections de la part des délégations. Il représente un compromis acceptable qui ouvre la voie à une approbation par le Conseil. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. Le texte présenté en Annexe de cette Note est identique au texte circulé après le groupe")
    thisalinea.textcontent.append("Espace (doc. 7745/21 +REV3) et qui n’a pas soulevé d’objections de la part des délégations.")
    thisalinea.textcontent.append("Il représente un compromis acceptable qui ouvre la voie à une approbation par le Conseil.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "III. CONCLUSION"
    thisalinea.nativeID = 7
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "5. Le Comité des Représentants Permanents est invité à confirmer le texte de compromis proposé en Annexe de cette Note et à envoyer pour approbation le projet de conclusions au Conseil (Compétitivité) à sa réunion du 10 juin 2022. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5. Le Comité des Représentants Permanents ..."
    thisalinea.nativeID = 8
    thisalinea.parentID = 7
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "5. Le Comité des Représentants Permanents est invité à confirmer le texte de compromis proposé en Annexe de cette Note et à envoyer pour approbation le projet de conclusions au Conseil (Compétitivité) à sa réunion du 10 juin 2022. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("5. Le Comité des Représentants Permanents est invité à confirmer le texte de compromis")
    thisalinea.textcontent.append("proposé en Annexe de cette Note et à envoyer pour approbation le projet de conclusions au")
    thisalinea.textcontent.append("Conseil (Compétitivité) à sa réunion du 10 juin 2022.")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "Draft Council conclusions on Copernicus by 2035 ANNEX"
    thisalinea.nativeID = 9
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "THE COUNCIL OF THE EUROPEAN UNION RECALLING A. the Council conclusions on ‘Space solutions for a sustainable Arctic’ of 29 November 20191, recognising Europe’s remarkable capabilities in Earth observation and their importance for monitoring and combatting the effects of climate change in the Arctic environment; noting, however, some remaining gaps in the monitoring capacities and services; B. the Council conclusions on ‘Space for a sustainable Europe’ of 4 June 20202, underlining that Earth science and European space data, services and technologies may contribute to the European Green Deal, and calling on the European Commission and Member States to facilitate and "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("THE COUNCIL OF THE EUROPEAN UNION")
    thisalinea.textcontent.append("RECALLING")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "A. the Council conclusions on ‘Space ..."
    thisalinea.nativeID = 10
    thisalinea.parentID = 9
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.BIGLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "A. the Council conclusions on ‘Space solutions for a sustainable Arctic’ of 29 November 20191, recognising Europe’s remarkable capabilities in Earth observation and their importance for monitoring and combatting the effects of climate change in the Arctic environment; noting, however, some remaining gaps in the monitoring capacities and services; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("A. the Council conclusions on ‘Space solutions for a sustainable Arctic’ of 29 November 20191,")
    thisalinea.textcontent.append("recognising Europe’s remarkable capabilities in Earth observation and their importance for")
    thisalinea.textcontent.append("monitoring and combatting the effects of climate change in the Arctic environment; noting,")
    thisalinea.textcontent.append("however, some remaining gaps in the monitoring capacities and services;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "B. the Council conclusions on ‘Space ..."
    thisalinea.nativeID = 11
    thisalinea.parentID = 9
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.BIGLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "B. the Council conclusions on ‘Space for a sustainable Europe’ of 4 June 20202, underlining that Earth science and European space data, services and technologies may contribute to the European Green Deal, and calling on the European Commission and Member States to facilitate and promote the usage of data and services; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("B. the Council conclusions on ‘Space for a sustainable Europe’ of 4 June 20202, underlining that")
    thisalinea.textcontent.append("Earth science and European space data, services and technologies may contribute to the")
    thisalinea.textcontent.append("European Green Deal, and calling on the European Commission and Member States to")
    thisalinea.textcontent.append("facilitate and promote the usage of data and services;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "C. the Council conclusions on ‘Space ..."
    thisalinea.nativeID = 12
    thisalinea.parentID = 9
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.BIGLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "C. the Council conclusions on ‘Space for people in European coastal areas’ of 28 May 20213, stressing that Copernicus services and applications provide an invaluable contribution to the green transition and to decision-making and planning tools for the ultimate benefit of citizens; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("C. the Council conclusions on ‘Space for people in European coastal areas’ of 28 May 20213,")
    thisalinea.textcontent.append("stressing that Copernicus services and applications provide an invaluable contribution to the")
    thisalinea.textcontent.append("green transition and to decision-making and planning tools for the ultimate benefit of citizens;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "D. The Council conclusions on ‘New ..."
    thisalinea.nativeID = 13
    thisalinea.parentID = 9
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.BIGLETTER
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "D. The Council conclusions on ‘New Space for People’ of 28 May 20214 calling on the Commission and EU Space Programme Agency (EUSPA) to foster, through an action plan, the uptake of space services by stimulating the adoption of space solutions across a wide range of EU policies and to increase the competitiveness of the EU downstream space industry; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("D. The Council conclusions on ‘New Space for People’ of 28 May 20214 calling on the")
    thisalinea.textcontent.append("Commission and EU Space Programme Agency (EUSPA) to foster, through an action plan,")
    thisalinea.textcontent.append("the uptake of space services by stimulating the adoption of space solutions across a wide")
    thisalinea.textcontent.append("range of EU policies and to increase the competitiveness of the EU downstream space")
    thisalinea.textcontent.append("industry;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "E. the Council conclusions on ‘Forging ..."
    thisalinea.nativeID = 14
    thisalinea.parentID = 9
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.BIGLETTER
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "E. the Council conclusions on ‘Forging a climate-resilient Europe – the new EU Strategy on Adaptation to Climate Change’ of 10 June 20215, stressing in particular the importance of further developing the Copernicus services for assessing climate change impacts; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("E. the Council conclusions on ‘Forging a climate-resilient Europe – the new EU Strategy on")
    thisalinea.textcontent.append("Adaptation to Climate Change’ of 10 June 20215, stressing in particular the importance of")
    thisalinea.textcontent.append("further developing the Copernicus services for assessing climate change impacts;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "I. Introduction: State of play and trends"
    thisalinea.nativeID = 15
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "1. RECALLS that Copernicus is a civil, user-driven operational system, built to respond to major societal challenges and based on solid scientific expertise, that generates free and open access data and information; UNDERLINES that, with Copernicus, the Union is a worldwide leader with the ability to observe, to monitor the Earth and predict changes, in particular by using modelling, and to serve scientific, institutional and commercial users and that Copernicus is already delivering manifold tangible results for Europe, for example in climate services, environmental land, ocean and atmospheric monitoring, for disaster management and civil security; 2. UNDERLINES that, in order "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "1. RECALLS that Copernicus is a ..."
    thisalinea.nativeID = 16
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "1. RECALLS that Copernicus is a civil, user-driven operational system, built to respond to major societal challenges and based on solid scientific expertise, that generates free and open access data and information; UNDERLINES that, with Copernicus, the Union is a worldwide leader with the ability to observe, to monitor the Earth and predict changes, in particular by using modelling, and to serve scientific, institutional and commercial users and that Copernicus is already delivering manifold tangible results for Europe, for example in climate services, environmental land, ocean and atmospheric monitoring, for disaster management and civil security; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("1. RECALLS that Copernicus is a civil, user-driven operational system, built to respond to")
    thisalinea.textcontent.append("major societal challenges and based on solid scientific expertise, that generates free and open")
    thisalinea.textcontent.append("access data and information; UNDERLINES that, with Copernicus, the Union is a worldwide")
    thisalinea.textcontent.append("leader with the ability to observe, to monitor the Earth and predict changes, in particular by")
    thisalinea.textcontent.append("using modelling, and to serve scientific, institutional and commercial users and that")
    thisalinea.textcontent.append("Copernicus is already delivering manifold tangible results for Europe, for example in climate")
    thisalinea.textcontent.append("services, environmental land, ocean and atmospheric monitoring, for disaster management")
    thisalinea.textcontent.append("and civil security;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "2. UNDERLINES that, in order to ..."
    thisalinea.nativeID = 17
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "2. UNDERLINES that, in order to keep Europe at the forefront, the continuity and continuous improvement of the Copernicus Services and of the in-situ and space observation capabilities and data should not only be guaranteed, but also improved upon and extended to new types of observation capabilities and to new services based on updated scientific and institutional user requirements and benefitting from the latest technological and scientific knowledge; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("2. UNDERLINES that, in order to keep Europe at the forefront, the continuity and continuous")
    thisalinea.textcontent.append("improvement of the Copernicus Services and of the in-situ and space observation capabilities")
    thisalinea.textcontent.append("and data should not only be guaranteed, but also improved upon and extended to new types of")
    thisalinea.textcontent.append("observation capabilities and to new services based on updated scientific and institutional user")
    thisalinea.textcontent.append("requirements and benefitting from the latest technological and scientific knowledge;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "3. RECALLS that the vision of ..."
    thisalinea.nativeID = 18
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "3. RECALLS that the vision of Copernicus by 2035 must take into account the main trends in terms of its core users and should closely follow the political priorities of the Union and its Member States, environmental challenges and technological advances while striving to increase its ability to address societal challenges under three pillars: the Green Deal, in particular the climate challenge, the digital transition, and civil security, together contributing to a more resilient Europe; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("3. RECALLS that the vision of Copernicus by 2035 must take into account the main trends in")
    thisalinea.textcontent.append("terms of its core users and should closely follow the political priorities of the Union and its")
    thisalinea.textcontent.append("Member States, environmental challenges and technological advances while striving to")
    thisalinea.textcontent.append("increase its ability to address societal challenges under three pillars: the Green Deal, in")
    thisalinea.textcontent.append("particular the climate challenge, the digital transition, and civil security, together contributing")
    thisalinea.textcontent.append("to a more resilient Europe;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "4. UNDERLINES that Copernicus’s success relies ..."
    thisalinea.nativeID = 19
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "4. UNDERLINES that Copernicus’s success relies on the expertise of the Commission, the Member States, and core partners, i.e. all the organisations that bring their high-level know- how to Copernicus: the European Space Agency, the European Organisation for the Exploitation of Meteorological Satellites, the EU Space Programme Agency, the European Centre for Medium-Range Weather Forecasts, Mercator Ocean International, the European Environmental Agency, the EU Satellite Centre, the European Maritime Safety Agency, and Frontex, as well as European industry and research organisations; ACKNOWLEDGES that the governance of Copernicus has played and will continue to have a key role in the success "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("4. UNDERLINES that Copernicus’s success relies on the expertise of the Commission, the")
    thisalinea.textcontent.append("Member States, and core partners, i.e. all the organisations that bring their high-level know-")
    thisalinea.textcontent.append("how to Copernicus: the European Space Agency, the European Organisation for the")
    thisalinea.textcontent.append("Exploitation of Meteorological Satellites, the EU Space Programme Agency, the European")
    thisalinea.textcontent.append("Centre for Medium-Range Weather Forecasts, Mercator Ocean International, the European")
    thisalinea.textcontent.append("Environmental Agency, the EU Satellite Centre, the European Maritime Safety Agency, and")
    thisalinea.textcontent.append("Frontex, as well as European industry and research organisations; ACKNOWLEDGES that")
    thisalinea.textcontent.append("the governance of Copernicus has played and will continue to have a key role in the success")
    thisalinea.textcontent.append("of the programme; RECALLS that the Copernicus User Forum is the expert body on user")
    thisalinea.textcontent.append("needs and on user uptake; and UNDERLINES the importance of the User Forum’s role along")
    thisalinea.textcontent.append("the entire value chain;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "5. CALLS FOR the evolution of ..."
    thisalinea.nativeID = 20
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "5. CALLS FOR the evolution of Copernicus Services and data by 2035 in order to meet the Green Deal climate and environmental goals, i.e. the transformation towards sustainable development, including climate change mitigation and adaptation, in particular through enhanced CO2 monitoring; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("5. CALLS FOR the evolution of Copernicus Services and data by 2035 in order to meet the")
    thisalinea.textcontent.append("Green Deal climate and environmental goals, i.e. the transformation towards sustainable")
    thisalinea.textcontent.append("development, including climate change mitigation and adaptation, in particular through")
    thisalinea.textcontent.append("enhanced CO2 monitoring;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "6. RECALLS that Copernicus provides scientifically ..."
    thisalinea.nativeID = 21
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "6. RECALLS that Copernicus provides scientifically relevant tools and indicators for assessing the current state of the climate, causes and trends, but also for long-term projections of climate change scenarios, thus providing valuable support to policy and decision-makers as well as economic actors and citizens; and HIGHLIGHTS the key role of Copernicus in ensuring the availability of critical data, in monitoring and measuring progress in achieving some of the goals of the Paris Agreement, including support to the estimation of global stocktake, and in decisions made at subsequent Conferences of the Parties; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("6. RECALLS that Copernicus provides scientifically relevant tools and indicators for assessing")
    thisalinea.textcontent.append("the current state of the climate, causes and trends, but also for long-term projections of")
    thisalinea.textcontent.append("climate change scenarios, thus providing valuable support to policy and decision-makers as")
    thisalinea.textcontent.append("well as economic actors and citizens; and HIGHLIGHTS the key role of Copernicus in")
    thisalinea.textcontent.append("ensuring the availability of critical data, in monitoring and measuring progress in achieving")
    thisalinea.textcontent.append("some of the goals of the Paris Agreement, including support to the estimation of global")
    thisalinea.textcontent.append("stocktake, and in decisions made at subsequent Conferences of the Parties;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "7. UNDERLINES the key role Copernicus ..."
    thisalinea.nativeID = 22
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "7. UNDERLINES the key role Copernicus must play in supporting public decisions and actions, particularly in areas such as biodiversity and ecosystems, health as part of a ‘one health’ approach, support to clean energy, the fight against pollution, decarbonisation of economy and society, urban sustainability, transport and smart mobility, food and water resources, cryosphere, sustainable ocean management, coastal areas, maritime surveillance, forestry, sustainable agriculture, natural resources, cultural heritage, desertification, risk management and disaster management such as hydro- or geohazards; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("7. UNDERLINES the key role Copernicus must play in supporting public decisions and actions,")
    thisalinea.textcontent.append("particularly in areas such as biodiversity and ecosystems, health as part of a ‘one health’")
    thisalinea.textcontent.append("approach, support to clean energy, the fight against pollution, decarbonisation of economy")
    thisalinea.textcontent.append("and society, urban sustainability, transport and smart mobility, food and water resources,")
    thisalinea.textcontent.append("cryosphere, sustainable ocean management, coastal areas, maritime surveillance, forestry,")
    thisalinea.textcontent.append("sustainable agriculture, natural resources, cultural heritage, desertification, risk management")
    thisalinea.textcontent.append("and disaster management such as hydro- or geohazards;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "8. UNDERLINES the importance of taking ..."
    thisalinea.nativeID = 23
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "8. UNDERLINES the importance of taking into account the following new trends in order to maximise their benefits for the Copernicus programme: i. On technologies: – Additional Earth observations through new measurements and instruments; – Additional Earth observations through new architectures and new business models, especially public or commercial constellations and New Space opportunities; ii. On science: – The impact of the evolution of computing science on numerical models of the Earth system in all its components, including the approach to coupled modelling systems and ensembles; iii. On digital: – The digital transformation, including high performance computing, big data analytics, "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("8. UNDERLINES the importance of taking into account the following new trends in order to")
    thisalinea.textcontent.append("maximise their benefits for the Copernicus programme:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "i. On technologies: "
    thisalinea.nativeID = 24
    thisalinea.parentID = 23
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i. On technologies: – Additional Earth observations through new measurements and instruments; – Additional Earth observations through new architectures and new business models, especially public or commercial constellations and New Space opportunities; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i. On technologies:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– Additional Earth observations through new ..."
    thisalinea.nativeID = 25
    thisalinea.parentID = 24
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "– Additional Earth observations through new measurements and instruments; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Additional Earth observations through new measurements and instruments;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– Additional Earth observations through new ..."
    thisalinea.nativeID = 26
    thisalinea.parentID = 24
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "– Additional Earth observations through new architectures and new business models, especially public or commercial constellations and New Space opportunities; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– Additional Earth observations through new architectures and new business")
    thisalinea.textcontent.append("models, especially public or commercial constellations and New Space")
    thisalinea.textcontent.append("opportunities;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "ii. On science: "
    thisalinea.nativeID = 27
    thisalinea.parentID = 23
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii. On science: – The impact of the evolution of computing science on numerical models of the Earth system in all its components, including the approach to coupled modelling systems and ensembles; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii. On science:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– The impact of the evolution ..."
    thisalinea.nativeID = 28
    thisalinea.parentID = 27
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "– The impact of the evolution of computing science on numerical models of the Earth system in all its components, including the approach to coupled modelling systems and ensembles; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– The impact of the evolution of computing science on numerical models of the")
    thisalinea.textcontent.append("Earth system in all its components, including the approach to coupled modelling")
    thisalinea.textcontent.append("systems and ensembles;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "iii. On digital: "
    thisalinea.nativeID = 29
    thisalinea.parentID = 23
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "iii. On digital: – The digital transformation, including high performance computing, big data analytics, artificial intelligence, data fusion and visualisation, data long-term preservation, right up to the concept of digital twinning; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("iii. On digital:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "– The digital transformation, including high ..."
    thisalinea.nativeID = 30
    thisalinea.parentID = 29
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SIGNMARK
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "– The digital transformation, including high performance computing, big data analytics, artificial intelligence, data fusion and visualisation, data long-term preservation, right up to the concept of digital twinning; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("– The digital transformation, including high performance computing, big data")
    thisalinea.textcontent.append("analytics, artificial intelligence, data fusion and visualisation, data long-term")
    thisalinea.textcontent.append("preservation, right up to the concept of digital twinning;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "9. RECALLS the expectation of Member ..."
    thisalinea.nativeID = 31
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "9. RECALLS the expectation of Member States that EU emergency management and security service capabilities in support of a more resilient Europe be developed; and HIGHLIGHTS the need to strengthen the security Service portfolio with developments such as more early warning and risk assessment capabilities for the monitoring and analysis of potential population displacement due to climate change impacts; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("9. RECALLS the expectation of Member States that EU emergency management and security")
    thisalinea.textcontent.append("service capabilities in support of a more resilient Europe be developed; and HIGHLIGHTS")
    thisalinea.textcontent.append("the need to strengthen the security Service portfolio with developments such as more early")
    thisalinea.textcontent.append("warning and risk assessment capabilities for the monitoring and analysis of potential")
    thisalinea.textcontent.append("population displacement due to climate change impacts;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "10. RECALLS the long-standing need for ..."
    thisalinea.nativeID = 32
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 9
    thisalinea.summary = "10. RECALLS the long-standing need for more reactivity and more precision in data acquisition and distribution, including through higher flexibility and timeliness in the programming of satellites over the requested area; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("10. RECALLS the long-standing need for more reactivity and more precision in data acquisition")
    thisalinea.textcontent.append("and distribution, including through higher flexibility and timeliness in the programming of")
    thisalinea.textcontent.append("satellites over the requested area;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "11. RECALLS that Copernicus user uptake ..."
    thisalinea.nativeID = 33
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 10
    thisalinea.summary = "11. RECALLS that Copernicus user uptake is a priority and that the services, data and information must be user-friendly, relevant to societal, economic and environmental needs and useful first for public authorities, but also for scientific, economic actors and citizens; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("11. RECALLS that Copernicus user uptake is a priority and that the services, data and")
    thisalinea.textcontent.append("information must be user-friendly, relevant to societal, economic and environmental needs")
    thisalinea.textcontent.append("and useful first for public authorities, but also for scientific, economic actors and citizens;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "12. UNDERLINES that easy and flexible ..."
    thisalinea.nativeID = 34
    thisalinea.parentID = 15
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 11
    thisalinea.summary = "12. UNDERLINES that easy and flexible access to and use of data, including all data necessary for Copernicus Services, must be facilitated and that Copernicus can contribute to the end-to- end development of a European value chain, including fostering the downstream sector, by implementing and promoting user-friendly and, as far as possible and where appropriate, energy efficient European data and information access platforms; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("12. UNDERLINES that easy and flexible access to and use of data, including all data necessary")
    thisalinea.textcontent.append("for Copernicus Services, must be facilitated and that Copernicus can contribute to the end-to-")
    thisalinea.textcontent.append("end development of a European value chain, including fostering the downstream sector, by")
    thisalinea.textcontent.append("implementing and promoting user-friendly and, as far as possible and where appropriate,")
    thisalinea.textcontent.append("energy efficient European data and information access platforms;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 1
    thisalinea.texttitle = "II. Recommendations"
    thisalinea.nativeID = 35
    thisalinea.parentID = 0
    thisalinea.alineatype = texttype.HEADLINES
    thisalinea.enumtype = enum_type.UNKNOWN
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "13. CONFIRMS Copernicus as a civil, operational, user-focused EU-led programme in support of the Green Deal, the digital transition and civil security, together contributing to a more resilient Europe; RECOMMENDS keeping the priority of climate change, supporting mitigation and adaptation policies; and RECOMMENDS that the free, full and open data policy in respect of Copernicus is to be maintained; 14. CALLS FOR the long-term enhanced continuity of current space and in situ observations and Services; 15. URGES the implementation of priorities for Copernicus that have not yet been implemented, including the Sentinels Next Generation and the six Copernicus Expansion missions "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "13. CONFIRMS Copernicus as a civil, ..."
    thisalinea.nativeID = 36
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "13. CONFIRMS Copernicus as a civil, operational, user-focused EU-led programme in support of the Green Deal, the digital transition and civil security, together contributing to a more resilient Europe; RECOMMENDS keeping the priority of climate change, supporting mitigation and adaptation policies; and RECOMMENDS that the free, full and open data policy in respect of Copernicus is to be maintained; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("13. CONFIRMS Copernicus as a civil, operational, user-focused EU-led programme in support of")
    thisalinea.textcontent.append("the Green Deal, the digital transition and civil security, together contributing to a more")
    thisalinea.textcontent.append("resilient Europe; RECOMMENDS keeping the priority of climate change, supporting")
    thisalinea.textcontent.append("mitigation and adaptation policies; and RECOMMENDS that the free, full and open data")
    thisalinea.textcontent.append("policy in respect of Copernicus is to be maintained;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "14. CALLS FOR the long-term enhanced ..."
    thisalinea.nativeID = 37
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "14. CALLS FOR the long-term enhanced continuity of current space and in situ observations and Services; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("14. CALLS FOR the long-term enhanced continuity of current space and in situ observations and")
    thisalinea.textcontent.append("Services;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "15. URGES the implementation of priorities ..."
    thisalinea.nativeID = 38
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "15. URGES the implementation of priorities for Copernicus that have not yet been implemented, including the Sentinels Next Generation and the six Copernicus Expansion missions and the dedicated support to policy areas such as Arctic, coastal areas, cultural heritage, environmental compliance, taking into account the security of the space and ground segment and the integrity of the data; HIGHLIGHTS the need to address new services such as agriculture, food and water security; and RECOMMENDS preparing the long term evolution of the Sentinel family, based on updated user requirements; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("15. URGES the implementation of priorities for Copernicus that have not yet been implemented,")
    thisalinea.textcontent.append("including the Sentinels Next Generation and the six Copernicus Expansion missions and the")
    thisalinea.textcontent.append("dedicated support to policy areas such as Arctic, coastal areas, cultural heritage,")
    thisalinea.textcontent.append("environmental compliance, taking into account the security of the space and ground segment")
    thisalinea.textcontent.append("and the integrity of the data; HIGHLIGHTS the need to address new services such as")
    thisalinea.textcontent.append("agriculture, food and water security; and RECOMMENDS preparing the long term evolution")
    thisalinea.textcontent.append("of the Sentinel family, based on updated user requirements;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "16. RECOMMENDS that responses to main ..."
    thisalinea.nativeID = 39
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "16. RECOMMENDS that responses to main user requirements should be clearly focused on the provision of usable and uncorrupted information, and should be defined by the Commission in a transparent and structured dialogue in coordination with the Copernicus User Forum; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("16. RECOMMENDS that responses to main user requirements should be clearly focused on the")
    thisalinea.textcontent.append("provision of usable and uncorrupted information, and should be defined by the Commission in")
    thisalinea.textcontent.append("a transparent and structured dialogue in coordination with the Copernicus User Forum;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "17. CALLS FOR allocating adequate funds ..."
    thisalinea.nativeID = 40
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "17. CALLS FOR allocating adequate funds to research and development and operations of Copernicus Services to ensure the preparation of new services and new projects which take advantage of future data, and their better integration, including with other sources, in order to maintain the state-of-the-art capacity and the international competitiveness of Copernicus; and HIGHLIGHTS that increased attention must be paid to the sustainability of the Earth observation infrastructure along the value chain and to monitoring its environmental footprint; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("17. CALLS FOR allocating adequate funds to research and development and operations of")
    thisalinea.textcontent.append("Copernicus Services to ensure the preparation of new services and new projects which take")
    thisalinea.textcontent.append("advantage of future data, and their better integration, including with other sources, in order to")
    thisalinea.textcontent.append("maintain the state-of-the-art capacity and the international competitiveness of Copernicus; and")
    thisalinea.textcontent.append("HIGHLIGHTS that increased attention must be paid to the sustainability of the Earth")
    thisalinea.textcontent.append("observation infrastructure along the value chain and to monitoring its environmental footprint;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "18. HIGHLIGHTS that the interface with ..."
    thisalinea.nativeID = 41
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "18. HIGHLIGHTS that the interface with the Digital Europe programme should be followed carefully, including the Destination Earth initiative; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("18. HIGHLIGHTS that the interface with the Digital Europe programme should be followed")
    thisalinea.textcontent.append("carefully, including the Destination Earth initiative;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "19. RECOMMENDS strengthening the hybrid Copernicus ..."
    thisalinea.nativeID = 42
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 6
    thisalinea.summary = "19. RECOMMENDS strengthening the hybrid Copernicus space segment driven by core user requirements and taking into account the advice and recommendations of the Copernicus User Forum; RECOMMENDS defining which capabilities and services should be reinforced in the ‘Sentinel architecture’ in order to guarantee autonomy and resilience; and CALLS ON the Commission to assess how far the Sentinel missions, as the backbone of the Copernicus infrastructure, could be complemented with additional European public and/or commercial capacities, paying particular attention to New Space solutions; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("19. RECOMMENDS strengthening the hybrid Copernicus space segment driven by core user")
    thisalinea.textcontent.append("requirements and taking into account the advice and recommendations of the Copernicus User")
    thisalinea.textcontent.append("Forum; RECOMMENDS defining which capabilities and services should be reinforced in the")
    thisalinea.textcontent.append("‘Sentinel architecture’ in order to guarantee autonomy and resilience; and CALLS ON the")
    thisalinea.textcontent.append("Commission to assess how far the Sentinel missions, as the backbone of the Copernicus")
    thisalinea.textcontent.append("infrastructure, could be complemented with additional European public and/or commercial")
    thisalinea.textcontent.append("capacities, paying particular attention to New Space solutions;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "20. RECOMMENDS, as a way forward, ..."
    thisalinea.nativeID = 43
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 7
    thisalinea.summary = "20. RECOMMENDS, as a way forward, to assess how the hybrid Copernicus space segment could benefit from additional capabilities, innovations and efficiency gains in Earth observation, including flexible and dynamic tasking, more frequent revisits, as well as higher resolution images, to support near real-time Copernicus Services in order to meet constantly changing demands, while taking into account the risks to EU security interests; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("20. RECOMMENDS, as a way forward, to assess how the hybrid Copernicus space segment")
    thisalinea.textcontent.append("could benefit from additional capabilities, innovations and efficiency gains in Earth")
    thisalinea.textcontent.append("observation, including flexible and dynamic tasking, more frequent revisits, as well as higher")
    thisalinea.textcontent.append("resolution images, to support near real-time Copernicus Services in order to meet constantly")
    thisalinea.textcontent.append("changing demands, while taking into account the risks to EU security interests;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "21. HIGHLIGHTS the need to ensure ..."
    thisalinea.nativeID = 44
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 8
    thisalinea.summary = "21. HIGHLIGHTS the need to ensure the calibration and validation of satellite data and information products, using reliable high quality in situ data, with documented quality, access to analysis ready data, the fusion of data from all sources and different resolutions, as well as the rapid availability of high-quality data in order to maximise their use; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("21. HIGHLIGHTS the need to ensure the calibration and validation of satellite data and")
    thisalinea.textcontent.append("information products, using reliable high quality in situ data, with documented quality, access")
    thisalinea.textcontent.append("to analysis ready data, the fusion of data from all sources and different resolutions, as well as")
    thisalinea.textcontent.append("the rapid availability of high-quality data in order to maximise their use;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "22. SUPPORTS the ambition of offering ..."
    thisalinea.nativeID = 45
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 9
    thisalinea.summary = "22. SUPPORTS the ambition of offering advanced public data and products to foster downstream commercial activities; and CALLS ON the Commission to ensure that Copernicus can play an important role for EU industry by offering contracts for obtaining data of a minimum standard on the basis of user needs, data quality and scientific relevance; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("22. SUPPORTS the ambition of offering advanced public data and products to foster downstream")
    thisalinea.textcontent.append("commercial activities; and CALLS ON the Commission to ensure that Copernicus can play an")
    thisalinea.textcontent.append("important role for EU industry by offering contracts for obtaining data of a minimum standard")
    thisalinea.textcontent.append("on the basis of user needs, data quality and scientific relevance;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "23. RECOMMENDS stepping up the efforts ..."
    thisalinea.nativeID = 46
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 10
    thisalinea.summary = "23. RECOMMENDS stepping up the efforts on the implementation of policies to foster the use of Copernicus data in public services, at European and national levels, in non-space sectors, and remove barriers to policies and regulations that hinder their use where necessary; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("23. RECOMMENDS stepping up the efforts on the implementation of policies to foster the use of")
    thisalinea.textcontent.append("Copernicus data in public services, at European and national levels, in non-space sectors, and")
    thisalinea.textcontent.append("remove barriers to policies and regulations that hinder their use where necessary;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "24. CONSIDERS that international cooperation on ..."
    thisalinea.nativeID = 47
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 11
    thisalinea.summary = "24. CONSIDERS that international cooperation on Earth observations is essential to effectively achieve international common policy objectives; and UNDERLINES the need for reciprocity in agreements and administrative arrangements negotiated with international partners and the need to reach a balance between EU autonomy and cooperation, including through more effective interfaces with international Earth observation groups and institutions; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("24. CONSIDERS that international cooperation on Earth observations is essential to effectively")
    thisalinea.textcontent.append("achieve international common policy objectives; and UNDERLINES the need for reciprocity")
    thisalinea.textcontent.append("in agreements and administrative arrangements negotiated with international partners and the")
    thisalinea.textcontent.append("need to reach a balance between EU autonomy and cooperation, including through more")
    thisalinea.textcontent.append("effective interfaces with international Earth observation groups and institutions;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 2
    thisalinea.texttitle = "25. On the user uptake: "
    thisalinea.nativeID = 48
    thisalinea.parentID = 35
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.DIGIT
    thisalinea.horizontal_ordering = 12
    thisalinea.summary = "25. On the user uptake: a. RECOMMENDS the active participation and the informed opinion of the Copernicus User Forum, based in particular on feedback from users and Member States, for the development of the Services, including space data and products, as well as for the acquisition of new data, the use of additional information and for the user uptake of Copernicus; b. UNDERLINES the importance of implementing at least one Copernicus data and information access platform associated with computing resources to support economic ecosystems and research; and of networking national data platforms in order to ensure a sustainable and independent "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("25. On the user uptake:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "a. RECOMMENDS the active participation and ..."
    thisalinea.nativeID = 49
    thisalinea.parentID = 48
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "a. RECOMMENDS the active participation and the informed opinion of the Copernicus User Forum, based in particular on feedback from users and Member States, for the development of the Services, including space data and products, as well as for the acquisition of new data, the use of additional information and for the user uptake of Copernicus; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("a. RECOMMENDS the active participation and the informed opinion of the Copernicus")
    thisalinea.textcontent.append("User Forum, based in particular on feedback from users and Member States, for the")
    thisalinea.textcontent.append("development of the Services, including space data and products, as well as for the")
    thisalinea.textcontent.append("acquisition of new data, the use of additional information and for the user uptake of")
    thisalinea.textcontent.append("Copernicus;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "b. UNDERLINES the importance of implementing ..."
    thisalinea.nativeID = 50
    thisalinea.parentID = 48
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "b. UNDERLINES the importance of implementing at least one Copernicus data and information access platform associated with computing resources to support economic ecosystems and research; and of networking national data platforms in order to ensure a sustainable and independent European access to data and information products; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("b. UNDERLINES the importance of implementing at least one Copernicus data and")
    thisalinea.textcontent.append("information access platform associated with computing resources to support economic")
    thisalinea.textcontent.append("ecosystems and research; and of networking national data platforms in order to ensure a")
    thisalinea.textcontent.append("sustainable and independent European access to data and information products;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 3
    thisalinea.texttitle = "c. RECOMMENDS to the Commission, together ..."
    thisalinea.nativeID = 51
    thisalinea.parentID = 48
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLLETTER
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "c. RECOMMENDS to the Commission, together with Copernicus entrusted entities, including EUSPA, and the involvement of Member States, to define a coherent user uptake strategy and the associated action plan by mid-2023 in order to support EU and national policies and while targeting socio-economic value creation enabled by the EU space programme, in particular: i. the development of solutions to make the Copernicus data and products easier to use for evidence-based decisions, especially for decision-makers and institutions in charge of public policies; ii. the need to develop cross-cutting and multi-disciplinary services required for user uptake development including by non-space actors; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("c. RECOMMENDS to the Commission, together with Copernicus entrusted entities,")
    thisalinea.textcontent.append("including EUSPA, and the involvement of Member States, to define a coherent user")
    thisalinea.textcontent.append("uptake strategy and the associated action plan by mid-2023 in order to support EU and")
    thisalinea.textcontent.append("national policies and while targeting socio-economic value creation enabled by the EU")
    thisalinea.textcontent.append("space programme, in particular:")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "i. the development of solutions to ..."
    thisalinea.nativeID = 52
    thisalinea.parentID = 51
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 0
    thisalinea.summary = "i. the development of solutions to make the Copernicus data and products easier to use for evidence-based decisions, especially for decision-makers and institutions in charge of public policies; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("i. the development of solutions to make the Copernicus data and products easier to")
    thisalinea.textcontent.append("use for evidence-based decisions, especially for decision-makers and institutions")
    thisalinea.textcontent.append("in charge of public policies;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "ii. the need to develop cross-cutting ..."
    thisalinea.nativeID = 53
    thisalinea.parentID = 51
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 1
    thisalinea.summary = "ii. the need to develop cross-cutting and multi-disciplinary services required for user uptake development including by non-space actors; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("ii. the need to develop cross-cutting and multi-disciplinary services required for user")
    thisalinea.textcontent.append("uptake development including by non-space actors;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "iii. the cross-fertilisation between various components ..."
    thisalinea.nativeID = 54
    thisalinea.parentID = 51
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 2
    thisalinea.summary = "iii. the cross-fertilisation between various components of the EU space programme such as Galileo and Copernicus; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("iii. the cross-fertilisation between various components of the EU space programme")
    thisalinea.textcontent.append("such as Galileo and Copernicus;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "iv. the support to national user ..."
    thisalinea.nativeID = 55
    thisalinea.parentID = 51
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 3
    thisalinea.summary = "iv. the support to national user forums, Copernicus relays and the Copernicus Academy and other nationally-driven initiatives making good use of existing EU instruments, in order to expand user uptake actions across Member States with the support of the entrusted entities, taking advantage of the Copernicus User Forum’s recommendations; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("iv. the support to national user forums, Copernicus relays and the Copernicus")
    thisalinea.textcontent.append("Academy and other nationally-driven initiatives making good use of existing EU")
    thisalinea.textcontent.append("instruments, in order to expand user uptake actions across Member States with the")
    thisalinea.textcontent.append("support of the entrusted entities, taking advantage of the Copernicus User Forum’s")
    thisalinea.textcontent.append("recommendations;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "v. the opportunity to acquire the ..."
    thisalinea.nativeID = 56
    thisalinea.parentID = 51
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 4
    thisalinea.summary = "v. the opportunity to acquire the skills to develop user uptake and contribute to reducing the space and digital divide across Europe, in particular through capacity-building in all Member States and training of national professionals, entrepreneurs and academics; "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("v. the opportunity to acquire the skills to develop user uptake and contribute to")
    thisalinea.textcontent.append("reducing the space and digital divide across Europe, in particular through")
    thisalinea.textcontent.append("capacity-building in all Member States and training of national professionals,")
    thisalinea.textcontent.append("entrepreneurs and academics;")
    alineas.append(thisalinea)

    thisalinea = textalinea()
    thisalinea.textlevel = 4
    thisalinea.texttitle = "vi. the development of targeted measures ..."
    thisalinea.nativeID = 57
    thisalinea.parentID = 51
    thisalinea.alineatype = texttype.ENUMERATION
    thisalinea.enumtype = enum_type.SMALLROMAN
    thisalinea.horizontal_ordering = 5
    thisalinea.summary = "vi. the development of targeted measures to enhance capacity across Member States with an emerging space industry, support the New Space ecosystem and the downstream sector. "
    thisalinea.sum_CanbeEmpty = False
    thisalinea.textcontent.clear()
    thisalinea.textcontent.append("vi. the development of targeted measures to enhance capacity across Member States")
    thisalinea.textcontent.append("with an emerging space industry, support the New Space ecosystem and the")
    thisalinea.textcontent.append("downstream sector.")
    alineas.append(thisalinea)

    return alineas
