from lxml import etree
def extract_text(element):
    text = ''
    if element.text:
        text += element.text.strip() + ' '
    for child in element:
        text += extract_text(child)
        if child.tail:
            text += child.tail.strip() + ' '
    return text


def look_for_links(element):
    list = []
    if element.tag.endswith('ptr'):
        if element.attrib.get('target','default')[0:4] == 'http':
            list.append(element.attrib['target'])
    for child in element:

        link = look_for_links(child)
        for l in link:
            list.append(l)
    return list


def count_figure(file_path):
    tree = etree.parse(file_path)

    root = tree.getroot()
    nb_figure = 0

    text = extract_text(root)
    word = ""
    next_word = ""

    # Iterate on the whole text to find the word 'figure' or 'fig' and capture the maximum number behind
    for i, char in enumerate(text):

        # current word
        if (not char.isspace() and char not in '.;,_\n()\""'):
            word += char
        else:
            # find the number of space to pass
            s = 1
            for space in text[i + 1:]:
                if space.isspace():
                    s += 1
                else:
                    break

            # if the word is good, look for the next word behind
            if word.lower() in ('fig', 'figure'):
                for char2 in text[i + s:]:

                    # check if the word behind is ended and if not check if it's a digit
                    if (not char2.isspace() and char2 not in '.;,\n()\""'):
                        if char2.isdigit():
                            next_word += char2
                        else:
                            break
                    else:
                        # when next word is over, compare it to the current nb of figure known
                        if int(next_word) > nb_figure:
                            nb_figure = int(next_word)
                            break
                        else:
                            break
            word = ""
            next_word = ""

    # trying to do it with figures only but some specific cases cause problems
    # nb_figure = 0
    # for sections in root[2][0]:
    #    if sections.tag.endswith('figure'):
    #        #print(sections[0].text)
    #        if sections[0].text[0:3] == 'Fig':
    #            nb_figure+=1

    return nb_figure


def extract_arXiv_id(root):
    list_ID_arXiv = []
    #root[2][1] is the 'back' element of the XML tree
    for div in root[2][1]:
        if div.get('type') == "references":
            for ListBibli in div:
                if ListBibli.tag[29:] == R'listBibl':
                    for bibli in ListBibli:
                        for child in bibli:
                            if child.tag[29:] == R'monogr' or child.tag[29:] == R'analytic':
                                for element in child:
                                    if element.tag[29:] == R'idno':
                                        if element.text[:5].lower() == R'arxiv' and (len(element.text) == 16 or len(element.text) == 15):
                                            list_ID_arXiv.append(element.text[6:])
                                        elif len(element.text) == 10:
                                            list_ID_arXiv.append(element.text)
    return list_ID_arXiv