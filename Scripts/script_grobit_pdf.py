from grobid_client_python.grobid_client.grobid_client import GrobidClient

#make sure to have grobid running before executing this script
def process_pdf():
    try :
        client = GrobidClient(config_path="grobid_client_python/config.json")
        client.process("processFulltextDocument",  "Corpus_pdf/", output="Grobid_processed_pdf/", tei_coordinates=True, force=True)
        return ['data processed sucessfully']
    except  Exception as e:
        return [f'fail : {e}']
