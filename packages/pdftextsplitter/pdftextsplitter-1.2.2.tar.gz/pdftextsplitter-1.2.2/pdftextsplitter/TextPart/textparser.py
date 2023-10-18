# Python functionality:
import math

# Textpart imports:
from .masterrule import texttype

def alineas_to_html_textsplitter(self, mode = "standalone"):
    """
    Converts the content of textsplitter.textalineas to a html-readable string so that
    a nice visualization can be obtained of the summarizing-results.
    
    # Parameters: str: mode. If this is set to standalone, it will build a separate
    html-page that can be opened on its own. Otherwise, it will only build the part needed by Django.
    # Return: None (stored inside the class)
    """

    # ----------------------------------------------------------------------------------

    # Before we begin: if there are no alineas, we cannot do anything:
    if (len(self.textalineas)==0): 
        self.html_visualization = "<html></html>"
    else:

        # Clear before we start:
        self.html_visualization = ""

        # Next, we begin by extracting all cascade levels:
        allcascades = []
        for alinea in self.textalineas:
            allcascades.append(alinea.textlevel)
    
        # Define max and min:
        mincascadelevel = 0
        maxcascadelevel = max(allcascades)
    
        # Define other variables we need:
        Header_level = 0
        children_array = []
    
        # Now: we need to loop over textalineas multiple times, because we
        # need to start visualizing the lower levels before we can do the
        # upper ones:
        for thiscascade in range(mincascadelevel,maxcascadelevel+1):
        
            # Define current cascade level. we want to loop from high to low:
            current_cascade = maxcascadelevel - thiscascade
            Header_level = current_cascade + 1
        
            # Then, loop over all alineas:
            for currentalinea in self.textalineas:
            
                # Then, only deal with the alineas that conform to
                # the selected cascade level:
                if (current_cascade==currentalinea.textlevel):
                    
                    # Begin by identify all direct children of this textalinea:
                    children_array.clear()
                    for child_alinea in self.textalineas:
                        
                        # test that we do not take the same one:
                        if not (child_alinea.nativeID==currentalinea.nativeID):
                            
                            # Then, test for the parent:
                            if (child_alinea.parentID==currentalinea.nativeID):
                                
                                # Then, this alinea is a child of currentalinea.
                                # But we only shwo it, if the summary is nonempty:
                                if not (child_alinea.summary==""):
                                    children_array.append(child_alinea)
                    
                    # Next, we must sort this array based on increasing nativeID; as not all children may share
                    # the same cascadelevel.
                    children_array = sorted(children_array, key=lambda x: x.nativeID, reverse=False)
                    
                    # Create html classnames for separate styling:
                    alinea_name = "texttype_unknown"
                    if (currentalinea.alineatype==texttype.UNKNOWN): alinea_name = "texttype_unknown"
                    elif (currentalinea.alineatype==texttype.TITLE): alinea_name = "texttype_title"
                    elif (currentalinea.alineatype==texttype.HEADLINES): alinea_name = "texttype_headlines"
                    elif (currentalinea.alineatype==texttype.FOOTER): alinea_name = "texttype_footer"
                    elif (currentalinea.alineatype==texttype.BODY): alinea_name = "texttype_body"
                    elif (currentalinea.alineatype==texttype.ENUMERATION): alinea_name = "texttype_enumeration"
                        
                    hierarchy_type = "unknown"
                    if (currentalinea.alineatype==texttype.HEADLINES)and(currentalinea.typelevel==0): hierarchy_type = "chapter"
                    elif (currentalinea.alineatype==texttype.HEADLINES)and(currentalinea.typelevel==1): hierarchy_type = "section"
                    elif (currentalinea.alineatype==texttype.HEADLINES)and(currentalinea.typelevel==2): hierarchy_type = "subsection"
                    elif (currentalinea.alineatype==texttype.HEADLINES)and(currentalinea.typelevel==3): hierarchy_type = "subsubsection"
                    elif (currentalinea.alineatype==texttype.ENUMERATION): hierarchy_type = "bullet" + str(currentalinea.typelevel+1)
                    elif (currentalinea.alineatype==texttype.TITLE): hierarchy_type = "title"
                    
                    # Then, compose the html-visualization:
                    if (currentalinea.summary==""):
                        
                        # Begin with the generation of a header that can NOT be opened & closed:
                        currentalinea.html_visualization = '<h'+str(Header_level)+' class="fold-link ' + str(alinea_name) + '-link ' + str(hierarchy_type) + '-link Empty_element-link">'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<table class="headertable" width = "100%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<tbody>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<tr valign="top">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "4%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + str(currentalinea.nr_pages) + '\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        
                        # If there is no structure, it is pointless to show all zero's:
                        if (currentalinea.nr_decendants==0):
                            currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "15%">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '<i>\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + 'Geen interne structuur.\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</i>\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                            
                        else:
                            currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "5%">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + str(currentalinea.nr_decendants) + '\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "5%">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + str(currentalinea.nr_children) + '\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "5%">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + str(currentalinea.nr_depths) + '\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        
                        # Continue with the header & title:
                        currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "1%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "80%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + currentalinea.texttitle
                        currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</tr>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</tbody>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</table>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</h'+str(Header_level)+'>\n'
                    
                        # Diff-class that cannot be folded:
                        currentalinea.html_visualization = currentalinea.html_visualization + '<div class="' + str(alinea_name) + ' ' + str(hierarchy_type) + ' Empty_element">\n'
                        
                    else: 
                        
                        # Calculate statistics:
                        summary_length = len(currentalinea.summary.split())
                        Reductiefactor = 0.0
                        textlength = 0
                
                        if (summary_length>0):
                            Reductiefactor = math.ceil(currentalinea.total_wordcount/summary_length)
                
                        for textline in currentalinea.textcontent:
                            textlength = textlength + len(textline.split())
                        
                        for child_alinea in children_array:
                            textlength = textlength + len(child_alinea.summary.split())
                        
                        # Begin with the generation of a header that can be opened & closed:
                        currentalinea.html_visualization = '<h'+str(Header_level)+' class="fold-link Structure_element-link ' + str(alinea_name) + '-link ' + str(hierarchy_type) + '-link">'
                        
                        # Begin with displaying meta-data in the header:
                        currentalinea.html_visualization = currentalinea.html_visualization + '<table class="headertable" width = "100%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<tbody>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<tr valign="top">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "4%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + str(currentalinea.nr_pages) + '\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        
                        # If there is no structure, it is pointless to show all zero's:
                        if (currentalinea.nr_decendants==0):
                            currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "15%">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '<i>\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + 'Geen interne structuur.\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</i>\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                            
                        else:
                            currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "5%">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + str(currentalinea.nr_decendants) + '\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "5%">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + str(currentalinea.nr_children) + '\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "5%">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + str(currentalinea.nr_depths) + '\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        
                        # Continue with the header & title:
                        currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "1%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "80%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + currentalinea.texttitle
                        currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</tr>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</tbody>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</table>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</h'+str(Header_level)+'>\n'
                    
                        # Diff-class folded (for the entire alinea-item):
                        if (current_cascade==0):
                            currentalinea.html_visualization = currentalinea.html_visualization + '<div class="unfolded Structure_element ' + str(alinea_name) + ' ' + str(hierarchy_type) + '">\n'
                        else:
                            currentalinea.html_visualization = currentalinea.html_visualization + '<div class="folded Structure_element ' + str(alinea_name) + ' ' + str(hierarchy_type) + '">\n'
                    
                        # Add a summary & original content as a table:
                        currentalinea.html_visualization = currentalinea.html_visualization + '<table class="summarytable" width = "100%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<tbody>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<tr valign="top">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "20%">\n'
                        
                        # Add meta-data on the top-level:
                        if (currentalinea.textlevel==0):
                            currentalinea.html_visualization = currentalinea.html_visualization + '<h'+str(Header_level+1)+' class="fold-link doc_metadata-link ' + str(alinea_name) + '-link ' + str(hierarchy_type) + '-link">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + 'Document meta-data: <br />\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '(wat er beschikbaar is) <br />\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '</h'+str(Header_level+1)+'>\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '<div class="unfolded doc_metadata ' + str(alinea_name) + ' ' + str(hierarchy_type) + '">\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + self.doc_metadata_fullstring
                            currentalinea.html_visualization = currentalinea.html_visualization + '</div>\n'
                        
                        currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "40%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<h'+str(Header_level+1)+' class="fold-link Summary-link ' + str(alinea_name) + '-link ' + str(hierarchy_type) + '-link">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + 'Samenvatting over ' + str(currentalinea.total_wordcount) + ' woorden: <br />\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + str(Reductiefactor) + 'x reductie; ' +  str(summary_length) + ' woorden; ca. ' + str(math.ceil(summary_length/230.0)) + ' min.\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</h'+str(Header_level+1)+'>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<div class="unfolded Summary ' + str(alinea_name) + ' ' + str(hierarchy_type) + '">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + currentalinea.summary + '\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</div>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<td width = "40%">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<h'+str(Header_level+1)+' class="fold-link Source-link ' + str(alinea_name) + '-link ' + str(hierarchy_type) + '-link">\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + 'Onderliggende Tekst: <br />\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + str(textlength) + ' woorden; ca. ' + str(math.ceil(textlength/230.0)) + ' min.\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</h'+str(Header_level+1)+'>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<div class="folded Source ' + str(alinea_name) + ' ' + str(hierarchy_type) + '">\n'
                    
                        # Next, add the content (including child-summaries):
                        for textline in currentalinea.textcontent:
                            currentalinea.html_visualization = currentalinea.html_visualization + textline + '\n'
                    
                        # Add a line-break:
                        currentalinea.html_visualization = currentalinea.html_visualization + '<br />\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '<br />\n'
                    
                        # Add children-summaries:
                        for child_alinea in children_array:
                            currentalinea.html_visualization = currentalinea.html_visualization + child_alinea.summary + '\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '<br />\n'
                            currentalinea.html_visualization = currentalinea.html_visualization + '<br />\n'
                        
                        # Close the html-items:
                        currentalinea.html_visualization = currentalinea.html_visualization + '</div>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</td>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</tr>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</tbody>\n'
                        currentalinea.html_visualization = currentalinea.html_visualization + '</table>\n'
                        
                        # NOTE: Under the else: we start & end with table for the part that is different when summary is empty or not.
                    
                    # Then, we must add all html-visualizations of the children to this visualization:
                    for child_alinea in children_array:
                        currentalinea.html_visualization = currentalinea.html_visualization + child_alinea.html_visualization
                        # NOTE: as we loop through the alineas in reversed order, this will be good enough.
                    
                    # Next, we close the div over the entire textalinea-object:
                    currentalinea.html_visualization = currentalinea.html_visualization + '<hr class="'+str(hierarchy_type)+'-horline">\n'
                    currentalinea.html_visualization = currentalinea.html_visualization + '</div>\n'
        
        # Next, we take the mother-alinea of the entire document & build the html-code around it:
        if (mode=="standalone"):
            self.html_visualization = '<!DOCTYPE html>\n'
            self.html_visualization = self.html_visualization + '<html lang="en">\n'
            self.html_visualization = self.html_visualization + '<head>\n'
            self.html_visualization = self.html_visualization + '<meta charset="utf-8">\n'
            self.html_visualization = self.html_visualization + '<link rel="stylesheet" href=https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">\n'
            self.html_visualization = self.html_visualization + '<link rel="stylesheet" type="text/css" href="../../TextPart/huisstijl.css">\n'
            self.html_visualization = self.html_visualization + '<link rel="stylesheet" type="text/css" href="../../TextPart/Styling.css">\n'
            self.html_visualization = self.html_visualization + '<title> ' + str(self.documentname) + ' </title>\n'

        self.html_visualization = self.html_visualization + '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>\n'

        if (mode=="standalone"):
            self.html_visualization = self.html_visualization + '<script>\n'
            self.html_visualization = self.html_visualization + 'window.onload = function() {\n'
            self.html_visualization = self.html_visualization + '// Vind het eerste img element in body\n'
            self.html_visualization = self.html_visualization + 'var img = document.body.querySelector("img:first-child");\n'
            self.html_visualization = self.html_visualization + '// Vind het element dat direct volgt op de afbeelding\n'
            self.html_visualization = self.html_visualization + 'var nextElement = img.nextElementSibling;\n'
            self.html_visualization = self.html_visualization + 'if (img && nextElement) {\n'
            self.html_visualization = self.html_visualization + '    // Bereken de hoogte van de afbeelding\n'
            self.html_visualization = self.html_visualization + '    var imgHeight = img.offsetHeight;\n'
            self.html_visualization = self.html_visualization + '    // Pas de bovenmarge van het volgende element aan\n'
            self.html_visualization = self.html_visualization + '    nextElement.style.marginTop = imgHeight + "px";\n'
            self.html_visualization = self.html_visualization + '}\n'
            self.html_visualization = self.html_visualization + '};\n'
            self.html_visualization = self.html_visualization + 'window.onresize = function() {\n'
            self.html_visualization = self.html_visualization + '// Vind het eerste img element in body\n'
            self.html_visualization = self.html_visualization + 'var img = document.body.querySelector("img:first-child");\n'
            self.html_visualization = self.html_visualization + '// Vind het element dat direct volgt op de afbeelding\n'
            self.html_visualization = self.html_visualization + 'var nextElement = img.nextElementSibling;\n'
            self.html_visualization = self.html_visualization + 'if (img && nextElement) {\n'
            self.html_visualization = self.html_visualization + '    // Bereken de nieuwe hoogte van de afbeelding\n'
            self.html_visualization = self.html_visualization + '    var imgHeight = img.offsetHeight;\n'
            self.html_visualization = self.html_visualization + '    // Pas de bovenmarge van het volgende element aan\n'
            self.html_visualization = self.html_visualization + '    nextElement.style.marginTop = imgHeight + "px";\n'
            self.html_visualization = self.html_visualization + '}\n'
            self.html_visualization = self.html_visualization + '};\n'
            self.html_visualization = self.html_visualization + '</script>\n'
            self.html_visualization = self.html_visualization + '</head>\n'
            self.html_visualization = self.html_visualization + '<img src="../../TextPart/Logo.png" alt="Hipster" width=800 />\n'
            self.html_visualization = self.html_visualization + '<body>\n'

        self.html_visualization = self.html_visualization + '<h2 class="Structure_element-link texttype_headlines-link chapter-link">'
        self.html_visualization = self.html_visualization + '<table class="bannertable-' + str(mode) + '" width = "100%">\n'
        self.html_visualization = self.html_visualization + '<tbody>\n'
        self.html_visualization = self.html_visualization + '<tr valign="top">\n'
        self.html_visualization = self.html_visualization + '<td width = "4%">\n'
        self.html_visualization = self.html_visualization + 'Pag.\n'
        self.html_visualization = self.html_visualization + '</td>\n'
        self.html_visualization = self.html_visualization + '<td width = "5%">\n'
        self.html_visualization = self.html_visualization + 'Struct.\n'
        self.html_visualization = self.html_visualization + '</td>\n'
        self.html_visualization = self.html_visualization + '<td width = "5%">\n'
        self.html_visualization = self.html_visualization + 'Links.\n'
        self.html_visualization = self.html_visualization + '</td>\n'
        self.html_visualization = self.html_visualization + '<td width = "5%">\n'
        self.html_visualization = self.html_visualization + 'Diepte.\n'
        self.html_visualization = self.html_visualization + '</td>\n'
        self.html_visualization = self.html_visualization + '<td width = "1%">\n'
        self.html_visualization = self.html_visualization + '\n'
        self.html_visualization = self.html_visualization + '</td>\n'
        self.html_visualization = self.html_visualization + '<td width = "80%">\n'
        self.html_visualization = self.html_visualization + 'Titel:\n'
        self.html_visualization = self.html_visualization + '</td>\n'
        self.html_visualization = self.html_visualization + '</tr>\n'
        self.html_visualization = self.html_visualization + '</tbody>\n'
        self.html_visualization = self.html_visualization + '</table>\n'
        self.html_visualization = self.html_visualization + '</h2>'
        self.html_visualization = self.html_visualization + '<hr class="Title-horline">\n'
        self.html_visualization = self.html_visualization + self.textalineas[0].html_visualization
        self.html_visualization = self.html_visualization + '<script>\n'
        self.html_visualization = self.html_visualization + '$(document).ready(function() {\n'
        self.html_visualization = self.html_visualization + '// Hide all of the folded sections\n'
        self.html_visualization = self.html_visualization + '$(".folded").hide();\n'
        self.html_visualization = self.html_visualization + '// Add click handlers to the folded links\n'
        self.html_visualization = self.html_visualization + '$(".fold-link").click(function() {\n'
        self.html_visualization = self.html_visualization + '// Find the next sibling div and toggle its visibility\n'
        self.html_visualization = self.html_visualization + '$(this).next("div").toggle();\n'
        self.html_visualization = self.html_visualization + '});\n'
        self.html_visualization = self.html_visualization + '});\n'
        self.html_visualization = self.html_visualization + '</script>\n'

        if (mode=="standalone"):
            self.html_visualization = self.html_visualization + '</body>\n'
            self.html_visualization = self.html_visualization + '</html>\n'
        
    # Write the output to a file:
    if (mode=="standalone"):
        html_file = open(self.outputpath + self.documentname + "_html_visualization.html", 'w', encoding="utf-8")
        html_file.write(self.html_visualization)
        html_file.close()
    
    # Done.
