import os
from Scripts.enriched_kg.referenced_papers import get_referenced_papers
from Scripts.enriched_kg.organization_data import get_organization_data

def process_grobid():
    path_directory = os.path.join("Scripts", "results")

    for filename in os.listdir(path_directory):
        if filename != 'similarities.txt':
            get_referenced_papers(filename)
            get_organization_data(filename)