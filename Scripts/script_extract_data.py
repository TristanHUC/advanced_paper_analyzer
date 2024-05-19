from lxml import etree
from utils import extract_text, extract_arXiv_id
import sys

input_name = sys.argv[1]


path_to_file = '../Grobid_processed_pdf/'+input_name[:len(input_name)-4]+'.grobid.tei.xml'
tree = etree.parse(path_to_file)

root = tree.getroot()


Title = root[0][0][0][0].text
Date = root[0][0][1][2].text


Authors = {}
for author in root[0][0][2][0][0]:
    try :
        Authors[extract_text(author[0])] = {}
        for child in author:
            if child.tag[29:] == R'affiliation':
                Authors[extract_text(author[0])][child[0].tag[29:]] = extract_text(child[0])
            else:
                Authors[extract_text(author[0])][child.tag[29:]] = extract_text(child)
    except :
        None


#extract abstract
abstract = ''
abstract = extract_text(root[0][2])


#extract ID_arXiv
list_ID_arXiv = extract_arXiv_id(root)


print(Title)
print(Date)
print(Authors)
print(abstract)
print(list_ID_arXiv)
