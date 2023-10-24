from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

filename = "./cellar_dbb134db-e575-11eb-a1a5-01aa75ed71a1.0005.01_DOC_1.pdf"
#filename = "./st09111.en22.pdf"
maxlevel = 100

def parse(filename, maxlevel):
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    parser.set_document(doc)
    #doc.set_parser(parser)

    outlines = doc.get_outlines()
    typemarker = True
    for (level, title, dest, a, se) in outlines:
        if (typemarker==True):
            typemarker = False
            print("type(level) = " + str(type(level)))
            print("type(title) = " + str(type(title)))
            print("type(dest) = " + str(type(dest)))
            print("type(a) = " + str(type(a)))
            print("type(se) = " + str(type(se)))
        
        if level <= maxlevel:
            print(str(level) + " | " + str(title) + " | " + str(dest[2]))


if __name__ == '__main__':
    parse(filename,maxlevel)
