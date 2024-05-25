import tkinter as tk
from Scripts.KG_server_queries.script_KG_query import query
from Scripts.KG_server_queries.script_KG_insertion_data import insert
from Scripts.script_grobit_pdf import process_pdf
from Scripts.script_extract_data import extract_data_all_pdf
from Scripts.enriched_kg.script_enrich_data import process_enriched_kg

def request(raw_text, Insert = False, Query = False):
    if Query and not Insert:
        return query(query = raw_text)
    elif Insert and not Query:
        return insert()

def submit_query():
    raw_text = input.get(1.0, tk.END)
    results = request(raw_text, Query = True)
    output.delete(1.0, tk.END)
    for result in results:
        output.insert(tk.END, '\n')
        output.insert(tk.END, result)

def submit_insert():
    raw_text = input.get(1.0, tk.END)
    results = request(raw_text, Insert = True)
    output.delete(1.0, tk.END)
    for result in results:
        output.insert(tk.END, result)

def submit_process():
    output.delete(1.0, tk.END)
    output.insert(tk.END,process_pdf())

def submit_extract():
    output.delete(1.0, tk.END)
    output.insert(tk.END,extract_data_all_pdf())

def submit_enrich():
    output.delete(1.0, tk.END)
    output.insert(tk.END,process_enriched_kg())

window = tk.Tk()

window.title("Interface")
window.geometry("1300x750")

bouton_process = tk.Button(window, text="PROCESS PDF WITH GROBID (1)", command=submit_process, height=1, width=24)
bouton_process.pack()

bouton_extract = tk.Button(window, text="EXTRACT DATA (2)", command=submit_extract, height=1, width=24)
bouton_extract.pack()

bouton_enrich = tk.Button(window, text="Enrich DATA (3)", command=submit_enrich, height=1, width=24)
bouton_enrich.pack()

bouton_insert = tk.Button(window, text="INSERT DATA FROM RDF (4)", command=submit_insert, height=1, width=24)
bouton_insert.pack()

label = tk.Label(window, text="Enter your SPARQL query :")
label.pack()

input = tk.Text(window, height=13, width=70)
input.pack()

bouton_query = tk.Button(window, text="SUBMIT QUERY (5)", command=submit_query, height=1, width=24)
bouton_query.pack()

output = tk.Text(window, height=18, width=160)
output.pack()

window.mainloop()