from Scripts.utils import extract_text, text_to_ListSentences, cosine, remove_stopwords
from sentence_transformers import SentenceTransformer
import os
from lxml import etree


def pdf_similarity(title,path_directory):

    # list of lists of sentences from abstracts (to compare them with the abstract of interest)
    list_listSentenceEmbedded_all_abstracts = []

    filenames = []
    similarities = {}

    for filename in os.listdir(path_directory):
        path_to_file = '../Grobid_processed_pdf/' + filename
        tree = etree.parse(path_to_file)

        root = tree.getroot()
        #extract abstract
        abstract = extract_text(root[0][2])
        pre_processed_abstract = remove_stopwords(abstract)
        listSentence_abstract = text_to_ListSentences(pre_processed_abstract)
        sbert_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        sentence_embeddings = sbert_model.encode(listSentence_abstract)
        sentences_embeddings_average = sentence_embeddings.mean(axis=0) #mean ? o np.mean ?


        #list of sentence of our abstract
        if title == root[0][0][0][0].text:
            listSentenceEmbedded_of_interest = sentences_embeddings_average
        else :
            filenames.append(filename[: len(filename) - 15])
            list_listSentenceEmbedded_all_abstracts.append(sentences_embeddings_average)

    for filename, embedded_Abstract in zip(filenames,list_listSentenceEmbedded_all_abstracts):
        similarities[filename] = cosine(embedded_Abstract, listSentenceEmbedded_of_interest)

    return similarities
