'''
Extracts data of referenced papers
Requires list of papers IDs (arXiv or DOI)
'''

import xml.etree.ElementTree as ET
import os
from pathlib import Path
from enriched_kg.utils_request import make_request_with_retry


TITLE = ""

def get_referenced_papers(title):

    global TITLE
    TITLE = title
    # global final_results_path

    # final_results_path = "enriched_results"

    # final_results_path = os.path.join(results_path_name,f"{title}")

    arxiv_ids = get_ids(os.path.join("results", TITLE,'arxiv.txt'))
    # doi_ids = get_ids('doi.txt')

    # get_dois(doi_ids)

    doi_list = []

    for arxiv_id in arxiv_ids:
        doi = get_doi_from_arxiv(arxiv_id)
        if doi:
            doi_list.append(doi)


    # get_dois(doi_list)

    get_arxivs(arxiv_ids)



def get_ids(ids_file):
    # Get array of all IDs
    all_ids = []
    with open(ids_file) as my_file:
        all_ids = [line.strip('\n\r') for line in my_file]

    #print(all_ids)
    return all_ids

def get_doi_from_arxiv(arxiv_id):
    url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
    response = make_request_with_retry(url)
    root = ET.fromstring(response.content)
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
            if 'title' in link.attrib and link.attrib['title'] == 'doi':
                return link.attrib['href'].split('/')[-1]
    return None

# def get_dois(doi_list):

    # # Construir la parte VALUES de la consulta SPARQL dinámicamente
    # values_part = ' '.join(f'"{doi}"' for doi in doi_list)

    # query = f"""
    # SELECT ?item ?itemLabel ?doi ?author ?authorLabel WHERE {{
    # VALUES ?doi {{ {values_part} }}
    # ?item wdt:P356 ?doi.
    # OPTIONAL {{ ?item wdt:P50 ?author. }}
    # SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    # }}
    # """

    # url = 'https://query.wikidata.org/sparql'
    # response = make_request_with_retry(url, params={'query': query, 'format': 'json'})
    # data = response.json()

    # with open(os.path.join(final_results_path, "papers_dois"), "+w") as file:
    #     for item in data['results']['bindings']:
    #         doi = item['doi']['value']
    #         title = item['itemLabel']['value']
    #         authors = []
    #         if 'author' in item:
    #             authors = [item['authorLabel']['value'] for author in item['author']]
    #         file.write(f"DOI: {doi}, Title: {title}, Authors: {', '.join(authors)}")

def get_arxivs(arxiv_list):
    global TITLE
    values_part = ' '.join(f'"{doi}"' for doi in arxiv_list)
    query = f"""
    SELECT ?item ?itemLabel ?arxivId ?author ?authorLabel WHERE {{
    VALUES ?arxivId {{ {values_part} }}  # Reemplaza con tus IDs
    ?item wdt:P818 ?arxivId.
    OPTIONAL {{ ?item wdt:P50 ?author. }}
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """

    url = 'https://query.wikidata.org/sparql'
    response = make_request_with_retry(url, params={'query': query, 'format': 'json'})

    data = response.json()
    i = 1
    for item in data['results']['bindings']:
        Path(os.path.join("results", TITLE, "papers",f"paper_{i}")).mkdir(parents=True, exist_ok=True)
        if 'authorLabel' in item:
            with open(os.path.join("results", TITLE, "papers",f"paper_{i}", "authors.txt"), "+w") as file:
                file.write(str(item['authorLabel']['value']))
        with open(os.path.join("results", TITLE, "papers",f"paper_{i}", "title.txt"), "+w") as file:
            file.write(str(item['itemLabel']['value']))
        i += 1
