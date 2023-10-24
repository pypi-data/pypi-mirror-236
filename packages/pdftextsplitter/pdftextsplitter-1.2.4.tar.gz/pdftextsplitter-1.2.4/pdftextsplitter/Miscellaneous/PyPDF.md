PyPDF2's extractText is really simple, it just looks for "draw letter sequence XYZ" commands and writes all the letters it finds in the order the draw instructions appear in the PDF, and apparently adds a new line after each instruction.

It seems your PDF file was created by the layout program with one instruction to write "Normal" then another to write "ly" (probably because of different kerning), etc.

tl;dr: PyPDF2 is not sophisticated enough to extract text reliably. The docs for extractText say:

    Locate all text drawing commands, in the order they are provided in the content stream, and extract the text. This works well for some PDF files, but poorly for others, depending on the generator used. This will be refined in the future. Do not rely on the order of text coming out of this function, as it will change if this function is made more sophisticated.
