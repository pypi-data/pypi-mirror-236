from PyPDF2 import PdfReader
import datetime

pdf = PdfReader("./cellar.pdf")
info = pdf.metadata

thevars = list(dir(info))
for onevar in thevars:
    if not ("__" in onevar):
        if not ("_raw" in onevar):
            print(onevar)

mydatestr = info.creation_date.strftime("%d-%B-%Y")
mydatestr = mydatestr.replace("-"," ")

print("author = " + str(info.author) + "\n\n")
print("creation_date = " + mydatestr + "\n\n")
print("creator = " + str(info.creator) + "\n\n")
print("modification_date = " + str(info.modification_date) + "\n\n")
print("producer = " + str(info.producer) + "\n\n")
print("subject = " + str(info.subject) + "\n\n")
print("title = " + str(info.title) + "\n\n")
