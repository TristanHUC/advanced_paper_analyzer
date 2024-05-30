from SPARQLWrapper import SPARQLWrapper, JSON
import os
from pathlib import Path
from Scripts.enriched_kg.utils_request import make_request_with_retry

# Función para obtener datos de ROR
def get_ror_data(organization_name):
    ror_api_url = f"https://api.ror.org/organizations?query={organization_name}"
    response = make_request_with_retry(ror_api_url)
    data = response.json()

    if data['number_of_results'] > 0:
        org_data = data['items'][0]
        ror_id = org_data['id']
        alias = org_data.get('aliases', [])
        types = org_data.get('types', [])
        sector = org_data.get('sector', '')
        relationships = [{'name': rel['label'], 'type': rel['type']} for rel in org_data.get('relationships', [])]

        return {
            'ROR ID': ror_id,
            'Alias': alias,
            'Types': types,
            'Sector': sector,
            'Relationships': relationships
        }
    else:
        return None

# Función para obtener datos de Wikidata
def get_wikidata_data(organization_name):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = f"""
    SELECT ?org ?orgLabel ?description ?publication ?publicationLabel ?project ?projectLabel WHERE {{
      ?org ?label "{organization_name}"@en.
      OPTIONAL {{ ?org wdt:P31 wd:Q43229. }}  # Tipo de organización (ej. Universidad)
      OPTIONAL {{ ?org wdt:P856 ?website. }}  # Sitio web
      OPTIONAL {{ ?org wdt:P1448 ?official_name. }}  # Nombre oficial
      OPTIONAL {{ ?org schema:description ?description. FILTER (lang(?description) = "en") }}
      OPTIONAL {{ ?publication wdt:P50 ?org. }}  # Publicaciones
      OPTIONAL {{ ?project wdt:P710 ?org. }}  # Proyectos

      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    description = None
    publications = set()
    projects = set()

    for result in results["results"]["bindings"]:
        if 'description' in result:
            description = result['description']['value']
        if 'publicationLabel' in result:
            publications.add(result['publicationLabel']['value'])
        if 'projectLabel' in result:
            projects.add(result['projectLabel']['value'])

    return {
        'Description': description,
        'Publications': list(publications),
        'Projects': list(projects)
    }

def get_names(names_file):
    # Get array of all IDs
    all_names = []
    with open(names_file) as my_file:
        all_names = [line.strip('\n\r') for line in my_file]

    #print(all_names)
    return all_names


def get_organization_data(title):
    organizations = get_names(os.path.join("Scripts","results", title, "organizations.txt"))

    # Recopilación de datos
    for org in organizations:
        ror_data = get_ror_data(org)
        wikidata_data = get_wikidata_data(org)

        Path(os.path.join("Scripts","results", "organizations")).mkdir(parents=True, exist_ok=True)

        path = os.path.join("Scripts","results", "organizations", org)
        with open(path,"w+") as file:
            if ror_data:
                for key, value in ror_data.items():
                    file.write(f"{key}: {value}\n")

            if wikidata_data:
                for key, value in wikidata_data.items():
                    file.write(f"{key}: {value}\n")