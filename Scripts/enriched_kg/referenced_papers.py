'''
Extracts data of referenced papers
Requires list of papers IDs (arXiv or DOI)
'''

import requests
import xml.etree.ElementTree as ET


def main():
    arxiv_ids = get_ids('arxiv.txt')
    doi_ids = get_ids('doi.txt')

    get_dois(doi_ids)

    doi_list = []

    for arxiv_id in arxiv_ids:
        doi = get_doi_from_arxiv(arxiv_id)
        if doi:
            doi_list.append(doi)

    print(doi_list)
    
    get_dois(doi_list)

    get_arxivs(arxiv_ids)



def get_ids(ids_file):
    # Get array of all IDs
    all_ids = []
    with open(ids_file) as my_file:
        all_ids = [line.strip('\n\r') for line in my_file]

    print(all_ids)
    return all_ids

def get_doi_from_arxiv(arxiv_id):
    url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
    response = requests.get(url)
    root = ET.fromstring(response.content)
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
            if 'title' in link.attrib and link.attrib['title'] == 'doi':
                return link.attrib['href'].split('/')[-1]
    return None

def get_dois(doi_list):

    # Construir la parte VALUES de la consulta SPARQL dinámicamente
    values_part = ' '.join(f'"{doi}"' for doi in doi_list)

    query = f"""
    SELECT ?item ?itemLabel ?doi ?author ?authorLabel WHERE {{
    VALUES ?doi {{ {values_part} }}
    ?item wdt:P356 ?doi.
    OPTIONAL {{ ?item wdt:P50 ?author. }}
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """

    url = 'https://query.wikidata.org/sparql'
    response = requests.get(url, params={'query': query, 'format': 'json'})
    data = response.json()

    for item in data['results']['bindings']:
        doi = item['doi']['value']
        title = item['itemLabel']['value']
        authors = []
        if 'author' in item:
            authors = [item['authorLabel']['value'] for author in item['author']]
        print(f"DOI: {doi}, Title: {title}, Authors: {', '.join(authors)}")

def get_arxivs(arxiv_list):
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
    response = requests.get(url, params={'query': query, 'format': 'json'})
    data = response.json()

    for item in data['results']['bindings']:
        print(item)


if __name__ == "__main__":
    main()