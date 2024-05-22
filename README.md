# Advanced Paper Analyzer

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11243971.svg)](https://doi.org/10.5281/zenodo.11243971)
[![Documentation Status](https://readthedocs.org/projects/advanced-paper-analyzer/badge/?version=latest)](https://advanced-paper-analyzer.readthedocs.io/en/latest/?badge=latest)

## Table of Contents
- [Advanced Paper Analyzer](#advanced-paper-analyzer)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
    - [Python](#python)
    - [Dependencies](#dependencies)
    - [Grobid](#grobid)
    - [Apache Jena Fuseki](#apache-jena-fuseki)
  - [How to use](#how-to-use)
    - [To create the dataset](#to-create-the-dataset)

## Introduction
Advanced Paper Analyzer takes a set of research papers and extracts its metadata to obtain information. It accesses Wikidata and ROR to expand the information and also has processes that compare the similarity between the abstracts taken from the papers and that analyze the possible topics the paper is about.


### Python
The code runs on **Python 3.10**, so it must be installed in the system to be able to use Advanced Paper Analyzer.

### Dependencies
Dependencies can be installed by using [Poetry](https://python-poetry.org/). You simply must go to the root directory of the repository and run:

    poetry install

Or install all dependencies with pip using requirements.txt in the root directory of the repository by running:

    pip install -r requirements.txt

### Grobid
Grobid is used to extract metadata from the papers, which are then used for further analysis. For this reason you must install either the full or light version of the [Grobid 0.8.0](https://grobid.readthedocs.io/en/latest/) [Docker](https://www.docker.com/) image. 
To run Grobid use one of this commands depending on version you have:

Full image:
[https://hub.docker.com/r/grobid/grobid](https://hub.docker.com/r/grobid/grobid)

Light image:
[https://hub.docker.com/r/lfoppiano/grobid/](https://hub.docker.com/r/lfoppiano/grobid/)

### Apache Jena Fuseki
[Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) is used to create the triple-store and the SPARQL endpoint, so it must be installed and run as described in the section to create the dataset

## How to use

Download the repository : git clone --recursive https://github.com/anastmur/advanced_paper_analyzer

install the Dependencies : see dependencies section

download grobid and Jena-Fuseki image from dockerhub : 
- docker pull lfoppiano/grobid
- docker pull stain/jena-fuseki

and run them with : 
- docker run -p 8070:8070 lfoppiano/grobid:latest-develop
- docker run -p 3035:3030 -e ADMIN_PASSWORD=pw123 -e FUSEKI_DATASET_1=KG_dataset stain/jena-fuseki
(it creates the dataset at the same time)

- Run the script interface.py

    
