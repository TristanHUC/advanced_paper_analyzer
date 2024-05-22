from utils import extract_text, text_to_ListSentences, cosine, remove_stopwords
from lxml import etree


def pdf_similarity(title,file, sbert_model):
    # list of lists of sentences from abstracts (to compare them with the abstract of interest)
    list_listSentenceEmbedded_all_abstracts = []

    array = [title, file]

    for filename in array:
        print('start similarities :', title, filename)
        path_to_file = '../Grobid_processed_pdf/' + filename
        tree = etree.parse(path_to_file)

        root = tree.getroot()
        #extract abstract
        abstract = extract_text(root[0][2])
        pre_processed_abstract = remove_stopwords(abstract)
        listSentence_abstract = text_to_ListSentences(pre_processed_abstract)
        sentence_embeddings = sbert_model.encode(listSentence_abstract)
        sentences_embeddings_average = sentence_embeddings.mean(axis=0)


        #list of sentence of our abstract
        if title == filename:
            listSentenceEmbedded_of_interest = sentences_embeddings_average
        else :
            list_listSentenceEmbedded_all_abstracts.append(sentences_embeddings_average)

    for embedded_Abstract in list_listSentenceEmbedded_all_abstracts:
        similarities = cosine(embedded_Abstract, listSentenceEmbedded_of_interest)

    return similarities
