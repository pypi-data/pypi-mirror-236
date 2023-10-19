import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from Source code:
sys.path.insert(1, '../../')
from Source.ContainsCountry import ContainsCountry

# Definition of unit tests:
def TestCountry_a() -> bool:
    """
    # Unit test for text the script using the ContainsCountry.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define some test string:
    teststr = "this is some nice tekst without any country name"

    # Execute the test:
    Answer = False
    if (ContainsCountry(teststr) == False): Answer = True
    return Answer


def TestCountry_b() -> bool:
    """
    # Unit test for text the script using the ContainsCountry.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define some test string:
    teststr = "this is some nice tekst with the African country name Mauritania"

    # Execute the test:
    if ContainsCountry(teststr): return True
    return False


def TestCountry_c() -> bool:
    """
    # Unit test for text the script using the ContainsCountry.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define some test string:
    teststr = "A European country Netherlands was not yet called"

    # Execute the test:
    if ContainsCountry(teststr): return True
    return False


def TestCountry_d() -> bool:
    """
    # Unit test for text the script using the ContainsCountry.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define some test string:
    teststr = "Kazakhstan and dkdjhdjd"

    # Execute the test:
    if ContainsCountry(teststr): return True
    return False


def TestCountry_e() -> bool:
    """
    # Unit test for text the script using the ContainsCountry.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define some test string:
    teststr = "does UNiTed STaTES also get detected in capitals and small letters at the same time?"

    # Execute the test:
    if ContainsCountry(teststr): return True
    return False


def TestCountry_f() -> bool:
    """
    # Unit test for text the script using the ContainsCountry.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define some test string:
    teststr = "dhdh and KIRIBATI"

    # Execute the test:
    if ContainsCountry(teststr): return True
    return False


def TestCountry_g() -> bool:
    """
    # Unit test for text the script using the ContainsCountry.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define some test string:
    teststr = "peru in small letters"

    # Execute the test:
    if ContainsCountry(teststr): return True
    return False


# Definition of collection:
def TestCountries() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    if not TestCountry_a():
        Answer = False
        print('Empty test (a) failed for detecting a country-string')

    if not TestCountry_d():
        Answer = False
        print('African test (b) failed for detecting a country-string')

    if not TestCountry_c():
        Answer = False
        print('European test (c) failed for detecting a country-string')

    if not TestCountry_d():
        Answer = False
        print('Asian test (d) failed for detecting a country-string')

    if not TestCountry_e():
        Answer = False
        print('N-America test (e) failed for detecting a country-string')

    if not TestCountry_f():
        Answer = False
        print('Oceania test (f) failed for detecting a country-string')

    if not TestCountry_g():
        Answer = False
        print('S-America test (g) failed for detecting a country-string')

    return Answer

if __name__ == '__main__':
    if TestCountries():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
