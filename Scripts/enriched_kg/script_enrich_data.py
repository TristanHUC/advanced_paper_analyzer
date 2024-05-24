from enriched_kg.process_grobid_data import process_grobid
from enriched_kg.authors import process_authors

def process_enriched_kg():
    try :
        process_grobid()
        #process_authors()  to have the other papers of the author ; not yet implemented
        return ["Data Enriched"]
    except Exception as e:
        return [f"Fail to enrich data : {e}"]