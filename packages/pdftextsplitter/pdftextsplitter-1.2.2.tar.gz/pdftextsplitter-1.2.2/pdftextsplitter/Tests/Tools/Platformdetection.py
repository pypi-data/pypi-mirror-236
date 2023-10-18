# import commands:
import platform
from enum import Enum

# Platform enumeration definition:
class MySystem(Enum):
    UNKNOWN = 0
    LINUX = 1
    WINDOWS = 2
    AZURE = 3
    
# function definition to detect the system:
def detectsystem() -> MySystem:
    """
    This function automatically detects the system using the platform-library.
    
    # Parameters: None
    # Returns (enum): MySystem: the result of the detection is given as output in the form of an enumeration, so it is unambiguous.
    """
    
    # ----------------------------------------------
    
    # Collect the platform-string:
    thesystem = platform.system()
    thesystem = thesystem.lower()
    
    # compare to enumerations:
    Answer = MySystem.UNKNOWN
    if "linux" in thesystem: Answer = MySystem.LINUX
    if "windows" in thesystem: Answer = MySystem.WINDOWS
    if "azure" in thesystem: Answer = MySystem.AZURE
    
    # Return answer:
    return Answer
    
