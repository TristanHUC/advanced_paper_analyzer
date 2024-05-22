from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD
import os
import json

NAMESPACE = Namespace("http://example.org/#")
SCH = Namespace("http://schema.org/")


def create_rdf(path = None) -> Graph:

    if not path:
        filename = "rdfschema.ttl"
    else :
        filename = path+"rdfschema.ttl"

    g = Graph()

    g.bind("ex", NAMESPACE)
    g.bind("sch", SCH)

    g.parse("Scripts//create_rdf//rdfschema.ttl",format="turtle")
    return g
           
# Función para añadir una persona al grafo
def add_person(graph, person_id, name=None, orcid=None, nationality=None, affiliation=None):
    person_uri = URIRef(f"http://example.org/#Person{person_id}")
    graph.add((person_uri, RDF.type, SCH.Person))
    if name:
        graph.add((person_uri, SCH.name, Literal(name, datatype=XSD.string)))
    if orcid:
        graph.add((person_uri, SCH.orcid, Literal(orcid, datatype=XSD.string)))
    if nationality:
        graph.add((person_uri, SCH.nationality, Literal(nationality, datatype=XSD.string)))
    if affiliation:
        graph.add((person_uri, SCH.affiliation, URIRef(affiliation)))
    return person_uri

# Función para añadir una organizacion al grafo
def add_organization(graph, org_id, name,description=None, identifier=None, legal_name=None, website=None, org_type=None):
    org_uri = URIRef(f"http://example.org/#Organization{org_id}")
    graph.add((org_uri, RDF.type, SCH.Organization))
    graph.add((org_uri, SCH.name, Literal(name, datatype=XSD.string)))
    if description:
        graph.add((org_uri, NAMESPACE.descriprtion, Literal(description, datatype=XSD.string)))
    if identifier:
        graph.add((org_uri, SCH.identifier, Literal(identifier, datatype=XSD.string)))
    if legal_name:
        graph.add((org_uri, SCH.legalName, Literal(legal_name, datatype=XSD.string)))
    if website:
        graph.add((org_uri, SCH.sameAs, Literal(website, datatype=XSD.string)))
    if org_type:
        graph.add((org_uri, NAMESPACE.hasOrganizationType, Literal(org_type, datatype=XSD.string)))
    return org_uri

# Función para crear un artículo académico en el grafo
def create_scholarly_article(graph, article_id, title, identifier, doi, funder_uri=None, author_uri=None):
    article_uri = URIRef(f"http://example.org/#Article{article_id}")
    graph.add((article_uri, RDF.type, SCH.ScholarlyArticle))
    graph.add((article_uri, SCH.about, Literal(title, datatype=XSD.string)))
    graph.add((article_uri, SCH.identifier, Literal(identifier, datatype=XSD.string)))
    graph.add((article_uri, SCH.sameAs, Literal(doi, datatype=XSD.string)))
    if funder_uri:
        graph.add((article_uri, SCH.funder, funder_uri))
    if author_uri:
        graph.add((article_uri, SCH.author, author_uri))
    return article_uri

def add_funder_to_article(graph,article_uri,funder_uri):
    graph.add((article_uri, SCH.funder, funder_uri))

def add_author_to_article(graph,article_uri,author_uri):
    graph.add((article_uri, SCH.author, author_uri))


def create_topic(graph, topic_id, name, identifier = None):
    topic_uri = URIRef(f"http://example.org/#Topic{topic_id}")
    graph.add((topic_uri, RDF.type, NAMESPACE.Topic))
    graph.add((topic_uri, NAMESPACE.name, Literal(name, datatype=XSD.string)))
    if identifier:
        graph.add((topic_uri, NAMESPACE.identifier, Literal(identifier, datatype=XSD.string)))
    return topic_uri

def set_prob_value(graph,prob_id,article_uri,topic_uri,value):
    prob_uri = URIRef(f"http://example.org/#Probability{prob_id}")
    graph.add(prob_uri,NAMESPACE.probabilityValue,value)
    graph.add(prob_uri,NAMESPACE.hasTopic,topic_uri)
    graph.add(prob_uri,NAMESPACE.hasArticle,article_uri)

# Función para crear un proyecto en el grafo
def create_project(graph, project_id, name, identifier=None, date_created=None):
    project_uri = URIRef(f"http://example.org/#Project{project_id}")
    graph.add((project_uri, RDF.type, SCH.Project))
    graph.add((project_uri, SCH.name, Literal(name, datatype=XSD.string)))
    if identifier:
        graph.add((project_uri, SCH.identifier, Literal(identifier, datatype=XSD.string)))
    if date_created:
        graph.add((project_uri, SCH.dateCreated, Literal(date_created, datatype=XSD.date)))
    return project_uri

# Función para crear una similitud en el grafo
def create_similarity(graph, similarity_id, value, first_article_uri, second_article_uri):
    similarity_uri = URIRef(f"http://example.org/#Similarity{similarity_id}")
    graph.add((similarity_uri, RDF.type, NAMESPACE.Similarity))
    graph.add((similarity_uri, NAMESPACE.value, Literal(value, datatype=XSD.float)))
    graph.add((similarity_uri, NAMESPACE.firstArticle, first_article_uri))
    graph.add((similarity_uri, NAMESPACE.secondArticle, second_article_uri))
    return similarity_uri

# Función para crear una probabilidad en el grafo
def create_probability(graph, probability_id, value, article_uri, topic_uri):
    probability_uri = URIRef(f"http://example.org/#Probability{probability_id}")
    graph.add((probability_uri, RDF.type, NAMESPACE.Probability))
    graph.add((probability_uri, NAMESPACE.probabilityValue, Literal(value, datatype=XSD.float)))
    graph.add((probability_uri, NAMESPACE.hasArticle, article_uri))
    graph.add((probability_uri, NAMESPACE.hasTopic, topic_uri))

# Función para asociar un empleado a un proyecto en el grafo
def add_employee_to_project(graph, project_uri, person_uri):
    graph.add((project_uri, SCH.employee, person_uri))

# Función para asociar una referecia de a a b
def add_reference(graph, article_uri1, article_uri2):
    graph.add((article_uri1, NAMESPACE.reference, article_uri2))

def affiliate_person_to_organization(graph, person_uri, organization_uri):
    graph.add((person_uri, SCH.affiliation, organization_uri))

def org_partent_of(graph, org_uri1,org_uri2):
    graph.add((org_uri1, NAMESPACE.hasChild, org_uri2))

def org_relatedTo(graph, org_uri1,org_uri2):
    graph.add((org_uri1, NAMESPACE.isRelated, org_uri2))

def org_project(graph,org_uri,project_uri):
    graph.add((org_uri, NAMESPACE.hasProject, project_uri))

def get_organization_list(g,location):
    global relation_list
    global relation_from_list
    global organization_list
    global organization_list_uri
    global project_list
    global project_list_uri
    for subdir, dirs, files in os.walk(location):
        for filename in files:
            file_dir = os.path.join(location,filename)
            # Comprobar si el archivo 'organizations' existe
            if os.path.isfile(file_dir):
                # Leer el contenido del archivo
                with open(file_dir, 'r',encoding="utf-8") as file:
                    ror_id = file.readline().removeprefix("ROR ID: ").removesuffix("\n")
                    file.readline()
                    org_type = file.readline().removesuffix("\n")
                    list_part = org_type.split("['")[1].split("']")[0]
                    org_type = list_part.split(",")[0].strip().strip("'")
                    file.readline()
                    relation_list.append(file.readline())

                    description = file.readline().removeprefix("Description: ").removesuffix("\n")
                    file.readline()
                    projline = file.readline().removesuffix("\n")
                    list_part = projline.split("Projects: ")[1]
                    list_part = list_part.strip("[]")
                    projects = list_part.split(",")
                    projects = [proj.strip().strip("'") for proj in projects]

                    claned_name = filename.removeprefix(" ")
                    organization_list.append(claned_name)
                    org_uri = add_organization(g,len(organization_list),claned_name,description,ror_id,org_type=org_type)
                    organization_list_uri.append(org_uri)

                    
                    relation_from_list.append(org_uri)
                    
                    for project in projects:
                        if not project == "":
                            project_uri = ""
                            if not project_list.count(project) > 0:
                                project_list.append(project)
                                project_uri = create_project(g,len(project_list),project)
                                project_list_uri.append(project_uri)
                            else:
                                project_uri = project_list_uri[project_list.index(project)]
                            org_project(g,org_uri,project_uri)

                    # while line:
                    #     if not organization_list.count(line) >0:
                    #         organization_list.append(line.removesuffix(" \n").removesuffix("\n")).removesuffix(" ").removeprefix(" ")
                    #     line = file.readline()

def get_paper_name(path):
    c_path = os.path.join(path,"title.txt")
    with open(c_path, 'r',encoding="utf-8") as file:
        name = file.readline().removesuffix("\n")
        return name

def create_all_papers(g,location):
    global prob_it
    global paper_list
    global paper_list_uri
    global person_list
    global person_list_uri
    global organization_list
    global organization_list_uri
    global topic_list
    global topic_list_uri
    for subdir, dirs, files in os.walk(location):
        for dir_name in dirs:
            subdir_path = os.path.join(subdir, dir_name)
            if dir_name == "organizations":
                get_organization_list(g,subdir_path) 
            elif dir_name == "papers":
                pass
            else:
                authors_file_path = os.path.join(subdir_path, 'authors.txt')
                organizations_file_path = os.path.join(subdir_path, 'organizations.txt')
                topics_file_path = os.path.join(subdir_path, 'topics.txt')
                paper_name = get_paper_name(subdir_path)
                if not paper_list.count(paper_name) >0:
                    paper_list.append(paper_name)
                    paper_uri = create_scholarly_article(g,len(paper_list)-1,paper_name,len(paper_list)-1,len(paper_list)-1)
                    paper_list_uri.append(paper_uri)
                if os.path.isfile(authors_file_path):
                    with open(authors_file_path, 'r',encoding="utf-8") as file:
                        line = file.readline()
                        while line:
                            person_uri =""
                            person_name = line.removesuffix(" \n").removesuffix("\n")
                            if not person_list.count(person_name) >0:
                                person_list.append(person_name)
                                person_uri = add_person(g,len(person_list),person_name)
                                person_list_uri.append(person_uri)
                            else:
                                person_uri = person_list_uri[person_list.index(person_name)]
                            add_author_to_article(g,paper_uri,person_uri)
                            line = file.readline()
                if os.path.isfile(organizations_file_path):
                    with open(organizations_file_path, 'r',encoding="utf-8") as file:
                        line = file.readline()
                        while line:
                            org_uri =""
                            org_name = line.removesuffix(" \n").removesuffix("\n").removesuffix(" ").removeprefix(" ")
                            if not organization_list.count(org_name) >0:
                                organization_list.append(org_name)
                                org_uri = add_organization(g,len(organization_list),org_name)
                                organization_list_uri.append(org_uri)
                            else:
                                org_uri = organization_list_uri[organization_list.index(org_name)]
                            add_funder_to_article(g,paper_uri,org_uri)
                            line = file.readline()
                if os.path.isfile(topics_file_path):
                    with open(topics_file_path, 'r',encoding="utf-8") as file:
                        line = file.readline().removesuffix("\n")
                        while line:                            
                            cleaned_str = line.strip("()")
                            parts = cleaned_str.rsplit(", ", 1)
                            titulo = parts[0].strip("'")
                            porcentaje = float(parts[1])
                            topic_uri =""
                            titulo = titulo.removesuffix(" ").removeprefix(" ")
                            if not topic_list.count(titulo) >0:
                                topic_list.append(titulo)
                                topic_uri = create_topic(g,len(topic_list),titulo)
                                topic_list_uri.append(topic_uri)
                            else:
                                topic_uri = topic_list_uri[topic_list.index(titulo)]
                            prob_it +=1
                            create_probability(g,prob_it,porcentaje,paper_uri,topic_uri)

                            line = file.readline().removesuffix("\n")

def create_org_relations(g):
    global relation_list
    global relation_from_list
    global organization_list
    global organization_list_uri
    for index, relations in enumerate(relation_list):
        # Extraer la parte de la cadena que contiene la lista
        list_part = relations.split("Relationships: ")[1]

        # Convertir las comillas simples a comillas dobles para hacerla una cadena JSON válida
        list_part_json = list_part.replace("'", '"')

        # Convertir la cadena JSON en una lista de diccionarios
        relationships = json.loads(list_part_json)

        for relationship in relationships:
            name = relationship['name']
            type_ = relationship['type']
            to_uri = None
            if organization_list.count(name)> 0:
                to_uri = organization_list_uri[organization_list.index(name)]
            else:
                organization_list.append(name)
                to_uri = add_organization(g,len(organization_list),name)
                organization_list_uri.append(to_uri)
            from_uri = relation_from_list[index]
            if type_ == 'Parent':
                org_partent_of(g,from_uri,to_uri)
            elif type_ == 'Child':
                org_partent_of(g,to_uri,from_uri)
            elif type_ == 'Related':
                org_relatedTo(g,from_uri,to_uri)
            else:
                pass

def create_similarities(g,location):
    global sim_it
    global similarity_list
    global similarity_list_uri
    global paper_list
    global paper_list_uri
    path = os.path.join(location,"similarities.txt")
    if os.path.isfile(path):
        with open(path, 'r',encoding="utf-8") as file:
            line = file.readline().removesuffix("\n")
            while line:
                cleaned_str = line.strip("()")
                parts = cleaned_str.rsplit(", ", 1)
                strings_part = parts[0].strip("()")
                s1, s2 = strings_part.split(", ")
                s1 = s1.strip("'")
                s2 = s2.strip("'")
                sim = float(parts[1])
                line = file.readline().removesuffix("\n")
                
                art_uri1 = ""
                art_uri2 = ""
                if not paper_list.count(s1) > 0:
                    paper_list.append(s1)
                    art_uri1 = create_scholarly_article(g,len(paper_list)-1,s1,len(paper_list)-1,len(paper_list)-1)
                    paper_list_uri.append(art_uri1)
                else:
                    art_uri1 = paper_list_uri[paper_list.index(s1)]

                if not paper_list.count(s2) > 0:
                    paper_list.append(s2)
                    art_uri2 = create_scholarly_article(g,len(paper_list)-1,s2,len(paper_list)-1,len(paper_list)-1)
                    paper_list_uri.append(art_uri2)
                else:
                    art_uri2 = paper_list_uri[paper_list.index(s2)]

                sim_it+=1
                sim_uri = create_similarity(g,sim_it,sim,art_uri1,art_uri2)


data_location = os.path.join("Scripts","results")

person_list = []
person_list_uri = []

organization_list = []
organization_list_uri = []

paper_list = []
paper_list_uri = []

relation_list = []
relation_from_list = []

project_list = []
project_list_uri = []

topic_list = []
topic_list_uri = []

similarity_list = []
similarity_list_uri = []

prob_it =0
sim_it =0

def make_rdf_file():
    global data_location
    g =create_rdf()
    create_all_papers(g,data_location)
    create_org_relations(g)
    create_similarities(g,data_location)
    g.serialize(destination=os.path.join("Scripts","output.ttl"), format="turtle")
    return g
