from grobid_client_python.grobid_client.grobid_client import GrobidClient

#make sure to have grobid running before executing this script
client = GrobidClient(config_path="../grobid_client_python/config.json")
client.process("processFulltextDocument",  "../Corpus_pdf/", output="../Grobid_processed_pdf/", tei_coordinates=True, force=True)
