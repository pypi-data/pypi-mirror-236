# Definition of function to hard-code the full textalinea-array in the class:
def printcode_textsplitter(self):
    """
    This function will create a textfile with python-code with hardcoded
    information on all the textalineas. This can be used to easily generate
    regression tests when you know a certain output is correct.
    
    # Parameters: none (taken from the class)
    # Return: none (the generated script)
    """
    
    # Begin by generating the file and the basic code:
    f = open(self.outputpath + self.documentname + "_hardcoded_content.py",'w')
    
    # Next, generate the start of the code:
    if f.writable():
        f.write('import sys\n')
        f.write('sys.path.insert(1, "../../")\n')
        f.write('\n')
        f.write('from TextPart.textalinea import textalinea\n')
        f.write('from TextPart.masterrule import texttype\n')
        f.write('from TextPart.enum_type import enum_type\n')
        f.write('\n')
        f.write('def hardcodedalineas_' + str(self.documentname) + '() -> list[textalinea]:\n')
        f.write('    """\n')
        f.write('    This code holds the content of the textalineas-array in the textsplitter-class\n')
        f.write('    for the document ' + str(self.documentname) + '\n')
        f.write('    It is generated with the printcode()-functions of textsplitter & textalinea\n')
        f.write('    and it is supposed to be used only after a complete document analysis\n')
        f.write('    the outcome of this analysis (this script) can then be efficiently used\n')
        f.write('    for running regression-tests in the future.\n')
        f.write('\n')
        f.write('    # Parameters: None (everything is hardcoded)\n')
        f.write('    # Return: list[textalinea] the hardcoded textalineas-array.\n')
        f.write('    """\n')
        f.write('\n')
        f.write('    alineas = []\n')
        f.write('\n')
        
        # Then, loop over the array:
        for alinea in self.textalineas:
            alinea.printcode(f)
            
        # Next, close the file:
        f.write('    return alineas\n')
        f.close()
