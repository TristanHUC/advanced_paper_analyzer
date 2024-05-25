from lxml import etree
from utils import extract_text, extract_arXiv_id
from topic_modeling.script_topic_modeling import topic_classification
from similarity.script_similarity import pdf_similarity
import sys
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer


def extract_data_all_pdf():
    sbert_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    try :
        grobid_processed_pdf = os.listdir(os.path.join("..", "Grobid_processed_pdf"))

        results_path_name = "results"

        i = 1

        for input_name in grobid_processed_pdf:

            path_to_file = os.path.join("..", "Grobid_processed_pdf", input_name[:len(input_name)])
            # path_to_file = '../Grobid_processed_pdf/'+input_name[:len(input_name)]+'.grobid.tei.xml'
            tree = etree.parse(path_to_file)

            root = tree.getroot()

            Title = root[0][0][0][0].text

            try :
                Date = root[0][0][1][2].text
            except:
                Date = None

            Authors = {}
            Organizations = {}
            for author in root[0][0][2][0][0]:
                try :
                    if author[0].tag[29:] == R'affiliation':
                        Organizations[extract_text(author[0])] = {}
                    else:
                        Authors[extract_text(author[0])] = {}
                    # Organizations[extract_text(author[0])] = {}
                    # for child in author:
                    #     print(str(child.tag[29:]))
                        # if child.tag[29:] == R'affiliation':
                        #     Organizations[extract_text(author[0])][child[0].tag[29:]] = extract_text(child[0][0])
                        # else:
                        #     Authors[extract_text(author[0])][child.tag[29:]] = extract_text(child)
                except :
                    None

            #extract ID_arXiv
            list_ID_arXiv = extract_arXiv_id(root)

            #topics modeling and classification
            topics = topic_classification(Title,"../Grobid_processed_pdf")

            # RESULTS
            Path(os.path.join(results_path_name,f"paper_{i}")).mkdir(parents=True, exist_ok=True)

            title_path = os.path.join(os.path.join(results_path_name,f"paper_{i}"), "title.txt")
            with open(title_path, "w+") as title_file:
                title_file.write(Title + "\n")
            arxiv_path = os.path.join(os.path.join(results_path_name,f"paper_{i}"), "arxiv.txt")
            with open(arxiv_path, "w+") as arxiv_file:
                for arxiv in list_ID_arXiv:
                    arxiv_file.write(arxiv + "\n")

            authors_path = os.path.join(os.path.join(results_path_name,f"paper_{i}"), "authors.txt")
            with open(authors_path, "w+") as authors_file:
                for author in Authors:
                    authors_file.write(author + "\n")

            organizations_path = os.path.join(os.path.join(results_path_name,f"paper_{i}"), "organizations.txt")
            with open(organizations_path, "w+") as organizations_file:
                for organization in Organizations:
                    organizations_file.write(organization + "\n")

            topics_path = os.path.join(os.path.join(results_path_name,f"paper_{i}"), "topics.txt")
            with open(topics_path, "w+") as topics_file:
                topic_list = topics.items()
                for topic in topic_list:
                    topics_file.write(str(topic) + "\n")


            #print(Title)
            #print(Date)
            #print(topics)

            i += 1
            # print(similarities)

        #compute the similarity between all papers and all the others
        from itertools import combinations

        # Usar itertools.combinations para generar todos los pares posibles
        diferencias = [(pdf_similarity(a,b,sbert_model)) for a, b in combinations(grobid_processed_pdf, 2)]

        # Mostrar los resultados
        #for par, diferencia in diferencias:
            #print(f"Similarity entre {par[0]} y {par[1]}: {diferencia}")

        similarities_path = os.path.join("results", "similarities.txt")
        with open(similarities_path, "w+") as similarities_file:
            similarity_list = diferencias
            for similarity in similarity_list:
                similarities_file.write(str(similarity) + "\n")
        return ['data extracted successfully']
    except Exception as e:
        return [f'fail : {e}']
