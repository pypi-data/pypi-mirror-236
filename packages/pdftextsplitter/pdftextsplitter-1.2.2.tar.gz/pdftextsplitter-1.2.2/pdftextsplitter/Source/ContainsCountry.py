# Function definition:
def ContainsCountry(textline: str) -> bool:
    '''
    This function checks whether a line of text contains a
    country name or not. The list of countries is hard-coded
    in this function per world area.
    
    Parameters:
    textline (str): the string of text to search for country names.
    
    Return:
    TestWorld (bool): Wheter it contains a country name or not.
    
    
    '''
    # ----------------------------------------------------------
    # Definition of countries:
    
    # African countries:
    Africa = []
    Africa.append("Algeria")
    Africa.append("Angola")
    Africa.append("Benin")
    Africa.append("Botswana")
    Africa.append("Burkina Faso")
    Africa.append("Burundi")
    Africa.append("Cameroon")
    Africa.append("Cape Verde")
    Africa.append("Central African Republic")
    Africa.append("Republic of Chad")
    Africa.append("Comoros")
    Africa.append("Democratic Republic of the Congo")
    Africa.append("Djibouti")
    Africa.append("Egypt")
    Africa.append("Equatorial Guinea")
    Africa.append("Eritrea")
    Africa.append("Eswatini")
    Africa.append("Ethiopia")
    Africa.append("Gabon")
    Africa.append("Gambia")
    Africa.append("Ghana")
    Africa.append("Guinea")
    Africa.append("Guinea-Bissau")
    Africa.append("Ivory Coast")
    Africa.append("Kenya")
    Africa.append("Lesotho")
    Africa.append("Liberia")
    Africa.append("Libya")
    Africa.append("Madagascar")
    Africa.append("Malawi")
    Africa.append("Mali")
    Africa.append("Mauritania")
    Africa.append("Mauritius")
    Africa.append("Morocco")
    Africa.append("Mozambique")
    Africa.append("Namibia")
    Africa.append("Niger")
    Africa.append("Nigeria")
    Africa.append("Republic of the Congo")
    Africa.append("Rwanda")
    Africa.append("Sao Tome and Principe")
    Africa.append("Senegal")
    Africa.append("Seychelles")
    Africa.append("Sierra Leone")
    Africa.append("Somalia")
    Africa.append("South Africa")
    Africa.append("South Sudan")
    Africa.append("Sudan")
    Africa.append("Tanzania")
    Africa.append("Togolese Republic")
    Africa.append("Tunisia")
    Africa.append("Uganda")
    Africa.append("Zambia")
    Africa.append("Zimbabwe")

    # Asian Countries:
    Asia = []
    Asia.append("Afghanistan")
    Asia.append("Bahrain")
    Asia.append("Bangladesh")
    Asia.append("Bhutan")
    Asia.append("Brunei")
    Asia.append("Cambodia")
    Asia.append("China")
    Asia.append("Hong Kong")
    Asia.append("India")
    Asia.append("Indonesia")
    Asia.append("Iran")
    Asia.append("Iraq")
    Asia.append("Israel")
    Asia.append("Japan")
    Asia.append("Jordan")
    Asia.append("Kazakhstan")
    Asia.append("Kuwait")
    Asia.append("Kyrgyzstan")
    Asia.append("Laos")
    Asia.append("Lebanon")
    Asia.append("Macau")
    Asia.append("Malaysia")
    Asia.append("Maldives")
    Asia.append("Mongolia")
    Asia.append("Myanmar")
    Asia.append("Nepal")
    Asia.append("North Korea")
    Asia.append("Oman")
    Asia.append("Pakistan")
    Asia.append("Palestine")
    Asia.append("Philippines")
    Asia.append("Qatar")
    Asia.append("Saudi Arabia")
    Asia.append("Singapore")
    Asia.append("South Korea")
    Asia.append("Sri Lanka")
    Asia.append("Syria")
    Asia.append("Taiwan")
    Asia.append("Tajikistan")
    Asia.append("Thailand")
    Asia.append("Timor-Leste")
    Asia.append("Turkmenistan")
    Asia.append("United Arab Emirates")
    Asia.append("Uzbekistan")
    Asia.append("Vietnam")
    Asia.append("Yemen")

    # Europian Countries:
    Europe = []
    Europe.append("Albania")
    Europe.append("Andorra")
    Europe.append("Armenia")
    Europe.append("Austria")
    Europe.append("Azerbaijan")
    Europe.append("Belarus")
    Europe.append("Belgium")
    Europe.append("Bosnia and Herzegovina")
    Europe.append("Bulgaria")
    Europe.append("Croatia")
    Europe.append("Cyprus")
    Europe.append("Czech Republic")
    Europe.append("Denmark")
    Europe.append("Estonia")
    Europe.append("Faroe Islands")
    Europe.append("Finland")
    Europe.append("France")
    Europe.append("Georgia")
    Europe.append("Germany")
    Europe.append("Greece")
    Europe.append("Holy See")
    Europe.append("Hungary")
    Europe.append("Iceland")
    Europe.append("Ireland")
    Europe.append("Italy")
    Europe.append("Latvia")
    Europe.append("Liechtenstein")
    Europe.append("Lithuania")
    Europe.append("Luxembourg")
    Europe.append("Malta")
    Europe.append("Moldova")
    Europe.append("Monaco")
    Europe.append("Montenegro")
    Europe.append("Netherlands")
    Europe.append("North Macedonia")
    Europe.append("Norway")
    Europe.append("Poland")
    Europe.append("Portugal")
    Europe.append("Romania")
    Europe.append("Russia")
    Europe.append("San Marino")
    Europe.append("Serbia")
    Europe.append("Slovakia")
    Europe.append("Slovenia")
    Europe.append("Spain")
    Europe.append("Sweden")
    Europe.append("Switzerland")
    Europe.append("Turkey")
    Europe.append("Ukraine")
    Europe.append("United Kingdom")
    Europe.append("Vatican City")

    # Countries in North America:
    North_America = []
    North_America.append("Antigua and Barbuda")
    North_America.append("Bahamas")
    North_America.append("Barbados")
    North_America.append("Belize")
    North_America.append("Bermuda")
    North_America.append("Canada")
    North_America.append("Costa Rica")
    North_America.append("Cuba")
    North_America.append("Dominica")
    North_America.append("Dominican Republic")
    North_America.append("El Salvador")
    North_America.append("Grenada")
    North_America.append("Guatemala")
    North_America.append("Haiti")
    North_America.append("Honduras")
    North_America.append("Jamaica")
    North_America.append("Mexico")
    North_America.append("Nicaragua")
    North_America.append("Panama")
    North_America.append("St. Kitts and Nevis")
    North_America.append("St. Lucia")
    North_America.append("St. Vincent and the Grenadines")
    North_America.append("Trinidad and Tobago")
    North_America.append("United States")

    # Countries in Oceanie:
    Oceanie = []
    Oceanie.append("American Samoa")
    Oceanie.append("Australia")
    Oceanie.append("Cook Islands")
    Oceanie.append("Fiji")
    Oceanie.append("French Polynesia")
    Oceanie.append("Guam")
    Oceanie.append("Kiribati")
    Oceanie.append("Marshall Islands")
    Oceanie.append("Micronesia")
    Oceanie.append("Nauru")
    Oceanie.append("New Caledonia")
    Oceanie.append("New Zealand")
    Oceanie.append("Niue")
    Oceanie.append("Northern Mariana Islands")
    Oceanie.append("Palau")
    Oceanie.append("Papua New Guinea")
    Oceanie.append("Samoa")
    Oceanie.append("Solomon Islands")
    Oceanie.append("Tokelau")
    Oceanie.append("Tonga")
    Oceanie.append("Tuvalu")
    Oceanie.append("Vanuatu")
    Oceanie.append("Wallis and Futuna")

    # Countries in South America:
    South_America = []
    South_America.append("Argentina")
    South_America.append("Bolivia")
    South_America.append("Brazil")
    South_America.append("Chile")
    South_America.append("Colombia")
    South_America.append("Ecuador")
    South_America.append("Guyana")
    South_America.append("Paraguay")
    South_America.append("Peru")
    South_America.append("Suriname")
    South_America.append("Uruguay")
    South_America.append("Venezuela")
    
    # ----------------------------------------------------------
    # Check the countries:
    
    TestAfrica = False
    for country in Africa:
        if (country.lower() in textline.lower()):
            TestAfrica = True
    
    TestAsia = False
    for country in Asia:
        if (country.lower() in textline.lower()):
            TestAsia = True

    TestEurope = False
    for country in Europe:
        if (country.lower() in textline.lower()):
            TestEurope = True

    TestNorth_America = False
    for country in North_America:
        if (country.lower() in textline.lower()):
            TestNorth_America = True
            
    TestOceanie = False
    for country in Oceanie:
        if (country.lower() in textline.lower()):
            TestOceanie = True
            
    TestSouth_America = False
    for country in South_America:
        if (country.lower() in textline.lower()):
            TestSouth_America = True
   
    TestWorld = (TestAfrica)or(TestAsia)or(TestEurope)or(TestNorth_America)or(TestOceanie)or(TestSouth_America)
    return TestWorld
   
   
