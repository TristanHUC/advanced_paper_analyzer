import data_toRDF as dtrdf

# Datos de las 10 personas
person_data = [
    (1, "Alice Smith", "0000-0002-1825-0097"),
    (2, "Bob Johnson", "0000-0003-1825-0098", "Canada"),
    (3, "Carol Williams", "0000-0004-1825-0099", "United Kingdom"),
    # (4, "David Brown", "0000-0005-1825-0100", "Australia"),
    # (5, "Eve Davis", "0000-0006-1825-0101", "New Zealand"),
    # (6, "Frank Miller", "0000-0007-1825-0102", "Germany"),
    # (7, "Grace Wilson", "0000-0008-1825-0103", "France"),
    # (8, "Hank Moore", "0000-0009-1825-0104", "Italy"),
    # (9, "Ivy Taylor", "0000-0010-1825-0105", "Spain"),
    # (10, "Jack Anderson", "0000-0011-1825-0106", "Netherlands")
]

organization_data = [
    (1, "Example Corp", "ORG-001", "Example Corporation", "http://www.example.com", "Corporation"),
    (2, "Sample LLC", "ORG-002", "Sample Limited Liability Company", "http://www.samplellc.com", "Limited Liability Company"),
    (3, "Test Foundation", "ORG-003", "Test Foundation Inc.", "http://www.testfoundation.org", "Foundation"),
    (4, "Trial Institute", "ORG-004", "Trial Research Institute", "http://www.trialinstitute.edu", "Research Institute"),
    (5, "Demo Association", "ORG-005", "Demo Association Group", "http://www.demoassociation.org", "Association")
]

g = dtrdf.create_rdf(None)


# Añadir las personas al grafo
for person in person_data:
    dtrdf.add_person(g, *person)

# Añadir las organizaciones al grafo
for org in organization_data:
    dtrdf.add_organization(g, *org)

person_uri1 = dtrdf.URIRef("http://example.org/#Person1")  # Ejemplo de URI de una persona
person_uri3 = dtrdf.URIRef("http://example.org/#Person3")  # Ejemplo de URI de una persona
organization_uri1 = dtrdf.URIRef("http://example.org/#Organization1")  # Ejemplo de URI de una organización
organization_uri2 = dtrdf.URIRef("http://example.org/#Organization2")  # Ejemplo de URI de una organización


funder_uri = dtrdf.URIRef("http://example.org/#Organization5")  # Ejemplo de URI de una organización (funder)
author_uri = dtrdf.URIRef("http://example.org/#Person2")  # Ejemplo de URI de una persona (autor)

article_uri1 = dtrdf.create_scholarly_article(g, 1, "Título del Artículo 1", "ART-001", "10.1234/example.doi1", "2023-05-21", funder_uri, author_uri)
article_uri2 = dtrdf.create_scholarly_article(g, 2, "Título del Artículo 2", "ART-002", "10.5678/example.doi2", "2023-06-15", organization_uri1, person_uri1)
article_uri3 = dtrdf.create_scholarly_article(g, 3, "Título del Artículo 3", "ART-003", "10.9012/example.doi3", "2023-07-30", organization_uri2, person_uri3)

topic_uri1 = dtrdf.create_topic(g, 1, "Semantic Web", "TOPIC-001")
topic_uri2 = dtrdf.create_topic(g, 2, "Open Science", "TOPIC-002")
topic_uri3 = dtrdf.create_topic(g, 3, "Artificial Intellingece", "TOPIC-003")
topic_uri4 = dtrdf.create_topic(g, 4, "Data Mining", "TOPIC-004")

project_uri1 =dtrdf.create_project(g, 1, "Project Alpha", "PROJ-001", "2023-01-01")
project_uri2 =dtrdf.create_project(g, 2, "Project Beta", "PROJ-002", "2023-02-15")
project_uri3 =dtrdf.create_project(g, 3, "Project Gamma", "PROJ-003", "2023-03-30")

dtrdf.add_employee_to_project(g, project_uri1, person_uri1)
dtrdf.add_employee_to_project(g, project_uri2, person_uri1)
dtrdf.add_employee_to_project(g, project_uri3, person_uri3)

dtrdf.create_similarity(g, 1, 0.85, article_uri1, article_uri2)
dtrdf.create_similarity(g, 2, 0.10, article_uri2, article_uri3)

dtrdf.create_probability(g, 1, 0.95, article_uri1, topic_uri4)

dtrdf.affiliate_person_to_organization(g, person_uri1, organization_uri1)
dtrdf.affiliate_person_to_organization(g, person_uri3, organization_uri2)

dtrdf.add_reference(g,article_uri1,article_uri3)

g.serialize(destination="output.ttl", format="turtle")