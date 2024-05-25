from SPARQLWrapper import SPARQLWrapper, POST
import Scripts.create_rdf.data_toRDF as dtrdf
import os

def insert(URL = "http://localhost:3035/KG_dataset/update"):
    # URL of endpoint
    sparql_update_endpoint = URL

    sparql_update = SPARQLWrapper(sparql_update_endpoint)
    sparql_update.setMethod(POST)
    sparql_update.setCredentials("admin", "pw123")

    g = dtrdf.make_rdf_file(os.path.join("Scripts", "create_rdf"))

    # Serialize without prefixes (prefixes make it bug)
    data = g.serialize(format='nt')

    # construct query
    sparql_update.setQuery(f"""
    INSERT DATA {{
        {data}
    }}
    """)

    try:
        response = sparql_update.query()
        return ["Data added to the Knowledge Graph"]
    except Exception as e:
        return [f"Fail to add data : {e}"]





