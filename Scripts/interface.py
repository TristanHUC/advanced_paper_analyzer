import tkinter as tk
from KG_server_queries.script_KG_query import query
from KG_server_queries.script_KG_insertion_data import insert
from script_grobit_pdf import process_pdf
from script_extract_data import extract_data_all_pdf

def request(requete, Insert = False, Query = False):
    if Query and not Insert:
        return query(query = requete)
    elif Insert and not Query:
        return insert()

def submit_query():
    requete = input.get()
    results = request(requete, Query = True)
    output.delete(1.0, tk.END)
    output.insert(tk.END, '?Entity  |  ?Attribut  |  ?Value  ')
    output.insert(tk.END, '\n')
    for result in results:
        output.insert(tk.END, '\n')
        output.insert(tk.END, result)

def submit_insert():
    requete = input.get()
    results = request(requete, Insert = True)
    output.delete(1.0, tk.END)
    for result in results:
        output.insert(tk.END, result)

def submit_process():
    output.delete(1.0, tk.END)
    output.insert(tk.END,process_pdf())

def submit_extract():
    output.delete(1.0, tk.END)
    output.insert(tk.END,extract_data_all_pdf())

window = tk.Tk()

window.title("Interface")
window.geometry("1300x700")

label = tk.Label(window, text="Enter your SPARQL query :")
label.pack()

input = tk.Entry(window, width=200)
input.pack()

bouton_query = tk.Button(window, text="SUBMIT QUERY (4)", command=submit_query, height=2, width=24)
bouton_query.pack()

output = tk.Text(window, height=30, width=150)
output.pack()

bouton_insert = tk.Button(window, text="INSERT DATA FROM RDF (3)", command=submit_insert, height=2, width=24)
bouton_insert.pack()

bouton_process = tk.Button(window, text="PROCESS PDF WITH GROBID (1)", command=submit_process, height=2, width=24)
bouton_process.pack()

bouton_extract = tk.Button(window, text="EXTRACT DATA (2)", command=submit_extract, height=2, width=24)
bouton_extract.pack()

window.mainloop()