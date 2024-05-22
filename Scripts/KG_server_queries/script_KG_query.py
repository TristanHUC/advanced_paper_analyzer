from SPARQLWrapper import SPARQLWrapper, JSON, GET

def query(URL = "http://localhost:3035/KG_dataset/query", query = None):

    # URL of endpoint
    sparql_query_endpoint = URL

    # if we want to do a query of the KG
    sparql_query = SPARQLWrapper(sparql_query_endpoint)
    sparql_query.setMethod(GET)

    sparql_query.setQuery(query)
    sparql_query.setReturnFormat(JSON)

    # send the request, convert to JSON and display
    output = []
    try:
        results = sparql_query.query().convert()
        for result in results["results"]["bindings"]:
            Entity = result["Entity"]["value"] if "Entity" in result else "N/A"
            Attribut = result["Attribut"]["value"] if "Attribut" in result else "N/A"
            Value = result["Value"]["value"] if "Value" in result else "N/A"
            output.append(f"{Entity} | {Attribut} | {Value}")
    except Exception as e:
        print(e)
        output.append(f" fail : {e}")

    return output