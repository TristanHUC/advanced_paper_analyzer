from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD

NAMESPACE = Namespace("http://example.org/#")
SCH = Namespace("http://schema.org/")


def create_rdf() -> Graph:
    g = Graph()

    g.bind("ex", NAMESPACE)
    g.bind("sch", SCH)

    g.parse("rdfschema.ttl",format="turtle")
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
def add_organization(graph, org_id, name, identifier, legal_name, website=None, org_type=None):
    org_uri = URIRef(f"http://example.org/#Organization{org_id}")
    graph.add((org_uri, RDF.type, SCH.Organization))
    graph.add((org_uri, SCH.name, Literal(name, datatype=XSD.string)))
    graph.add((org_uri, SCH.identifier, Literal(identifier, datatype=XSD.string)))
    graph.add((org_uri, SCH.legalName, Literal(legal_name, datatype=XSD.string)))
    if website:
        graph.add((org_uri, SCH.sameAs, Literal(website, datatype=XSD.string)))
    if org_type:
        graph.add((org_uri, NAMESPACE.hasOrganizationType, Literal(org_type, datatype=XSD.string)))
    return org_uri

# Función para crear un artículo académico en el grafo
def create_scholarly_article(graph, article_id, title, identifier, doi, date_created, funder_uri, author_uri):
    article_uri = URIRef(f"http://example.org/#Article{article_id}")
    graph.add((article_uri, RDF.type, SCH.ScholarlyArticle))
    graph.add((article_uri, SCH.about, Literal(title, datatype=XSD.string)))
    graph.add((article_uri, SCH.identifier, Literal(identifier, datatype=XSD.string)))
    graph.add((article_uri, SCH.sameAs, Literal(doi, datatype=XSD.string)))
    graph.add((article_uri, SCH.dateCreated, Literal(date_created, datatype=XSD.date)))
    graph.add((article_uri, SCH.funder, funder_uri))
    graph.add((article_uri, SCH.author, author_uri))
    return article_uri

def create_topic(graph, topic_id, name, identifier):
    topic_uri = URIRef(f"http://example.org/#Topic{topic_id}")
    graph.add((topic_uri, RDF.type, NAMESPACE.Topic))
    graph.add((topic_uri, NAMESPACE.name, Literal(name, datatype=XSD.string)))
    graph.add((topic_uri, NAMESPACE.identifier, Literal(identifier, datatype=XSD.string)))
    return topic_uri

# Función para crear un proyecto en el grafo
def create_project(graph, project_id, name, identifier, date_created):
    project_uri = URIRef(f"http://example.org/#Project{project_id}")
    graph.add((project_uri, RDF.type, SCH.Project))
    graph.add((project_uri, SCH.name, Literal(name, datatype=XSD.string)))
    graph.add((project_uri, SCH.identifier, Literal(identifier, datatype=XSD.string)))
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


