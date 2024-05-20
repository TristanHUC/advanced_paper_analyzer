from lxml import etree
from utils import extract_text, extract_arXiv_id
from topic_modeling.script_topic_modeling import topic_classification
from similarity.Script_similarity import pdf_similarity
import sys

input_name = sys.argv[1]


path_to_file = '../Grobid_processed_pdf/'+input_name[:len(input_name)-4]+'.grobid.tei.xml'
tree = etree.parse(path_to_file)

root = tree.getroot()

Title = root[0][0][0][0].text

try :
    Date = root[0][0][1][2].text
except:
    Date = None

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

#extract ID_arXiv
list_ID_arXiv = extract_arXiv_id(root)

#topics modeling and classification
topics = topic_classification(Title,"../Grobid_processed_pdf")

#compute the similarity between this paper and all the others
similarities = pdf_similarity(Title,"../Grobid_processed_pdf")


print(Title)
print(Date)
print(Authors)
print(list_ID_arXiv)
print(topics)
print(similarities)
