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
        headers = []
        for var in results["results"]["bindings"][0]:
            headers.append(var)
        output.append(" | ".join(headers))
        output.append("\n")
        for result in results["results"]["bindings"]:
            row = []
            for var in result:
                value = result[var]["value"] if "value" in result[var] else "N/A"
                row.append(value)
            output.append(" | ".join(row))
    except Exception as e:
        print(e)
        output.append(f" fail : {e}")

    return output