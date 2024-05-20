import requests

# def query_wikidata(query):
#     sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
#     sparql.setQuery(query)
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#     return results

def query_wikidata(query):
    url = "https://query.wikidata.org/sparql"
    headers = {
        "Accept": "application/sparql-results+json"
    }
    response = requests.get(url, headers=headers, params={'query': query})
    response.raise_for_status()
    return response.json()


# f"""
#     SELECT ?person ?personLabel ?publication ?publicationLabel WHERE {{
#       ?person wdt:P31 wd:Q5;
#               rdfs:label ?name.
#       FILTER(CONTAINS(LCASE(?name), )).

#     ?publication wdt:P50 ?person;  # ?publication has author ?person
#                 rdfs:label ?publicationName.
#     FILTER(CONTAINS(LCASE(?publicationName), )).
      
#       SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
#     }}
#     """

def search_by_name_and_title(name, title):
    query = f"""
    SELECT ?person ?personLabel ?publication ?publicationLabel WHERE {{
    ?person wdt:P31 wd:Q5;  # ?person is an instance of human
            rdfs:label ?name.
    FILTER(CONTAINS(LCASE(?name), "{name.lower()}")).

    ?publication wdt:P50 ?person;  # ?publication has author ?person
                rdfs:label ?publicationName.
    FILTER(CONTAINS(LCASE(?publicationName), "asking before action: gather information in embodied decision making with language models")).
    
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """
    return query_wikidata(query)


def search_by_name_and_doi(name, doi):
    query = f"""
    SELECT ?person ?personLabel ?publication ?publicationLabel WHERE {{
      ?person wdt:P31 wd:Q5;
              rdfs:label ?name.
      FILTER(CONTAINS(LCASE(?name), "{name.lower()}")).

      ?publication wdt:P50 ?person;
                  wdt:P356 ?doi.
      FILTER(STR(?doi) = "{doi}").
      
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """
    return query_wikidata(query)

def get_names(names_file):
    # Get array of all IDs
    all_names = []
    with open(names_file) as my_file:
        all_names = [line.strip('\n\r') for line in my_file]

    print(all_names)
    separated_names = [line.split(">") for line in all_names]
    print(separated_names)
    return separated_names

def main():

    for line in get_names("authors.txt"):
        title = line[0]
        name = line[1]
        results_arxiv = search_by_name_and_title(name, title)
        print("Results:")
        for result in results_arxiv["results"]["bindings"]:
            print(result)

    # # Search by DOI
    # doi = "10.1234/example.doi"
    # results_doi = search_by_name_and_doi(name, doi)
    # print("\nResults for DOI:")
    # for result in results_doi["results"]["bindings"]:
    #     print(result)


if __name__ == "__main__":
    main()