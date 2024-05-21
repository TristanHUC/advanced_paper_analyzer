from SPARQLWrapper import SPARQLWrapper, JSON, GET


# URL of endpoint
sparql_query_endpoint = "http://localhost:3035/test_creation_dataset/query"

# if we want to do a query of the KG
sparql_query = SPARQLWrapper(sparql_query_endpoint)
sparql_query.setMethod(GET)

sparql_query.setQuery("""
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o
    }
    LIMIT 10
""")
sparql_query.setReturnFormat(JSON)

# send the request, convert to JSON and display
try:
    results = sparql_query.query().convert()
    for result in results["results"]["bindings"]:
        s = result["s"]["value"]
        p = result["p"]["value"]
        o = result["o"]["value"]
        print(f"{s} {p} {o}")
except Exception as e:
    print(f" fail : {e}")