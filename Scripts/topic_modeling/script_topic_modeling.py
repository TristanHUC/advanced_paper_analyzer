from Scripts.utils import extract_text, text_to_ListSentences, remove_stopwords
import os
from lxml import etree
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


def topic_classification(title,path_directory):
    i = 0

    #list of sentences from all abstracts (for topic modeling)
    listSentence_all_abstracts = []

    topics = {}

    all_abstracts = ''
    for filename in os.listdir(path_directory):
        i += 1
        path_to_file = 'Grobid_processed_pdf/' + filename
        tree = etree.parse(path_to_file)

        root = tree.getroot()
        #extract abstract
        abstract = extract_text(root[0][2])

        # pre-process the abstract for topic modeling
        pre_processed_abstract = remove_stopwords(abstract)
        listSentence_abstract = text_to_ListSentences(pre_processed_abstract)

        listSentence_all_abstracts += listSentence_abstract

        #save the list of sentence of our abstract
        if title == root[0][0][0][0].text:
            listSentence_of_interest = listSentence_abstract



    #topic modeling
    count_vectorizer = CountVectorizer()
    tokenized_abstracts = count_vectorizer.fit_transform(listSentence_all_abstracts)
    lda = LatentDirichletAllocation(n_components=i, random_state=0)
    lda.fit(tokenized_abstracts)
    feature_names = count_vectorizer.get_feature_names_out()

    #topic classification
    tokenized_abstract = count_vectorizer.transform(listSentence_of_interest)
    topic_distribution = lda.transform(tokenized_abstract)

    for topic_idx, topic_prob in enumerate(topic_distribution[0]):
        topic_name = " ".join([feature_names[i] for i in lda.components_[topic_idx].argsort()[:-6:-1]])
        topics[topic_name] = round(topic_prob*100)/100

    return topics