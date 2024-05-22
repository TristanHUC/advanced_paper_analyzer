import os
from referenced_papers import get_referenced_papers
from organization_data import get_organization_data

path_directory = "results"

for filename in os.listdir(path_directory):
    get_referenced_papers(filename)
    get_organization_data(filename)