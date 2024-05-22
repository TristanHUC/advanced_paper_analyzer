import tkinter as tk
from Scripts.KG_server_queries.script_KG_query import query
from Scripts.KG_server_queries.script_KG_insertion_data import insert

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

window = tk.Tk()

window.title("Interface")
window.geometry("1300x700")

label = tk.Label(window, text="Enter your SPARQL query :")
label.pack()

input = tk.Entry(window, width=200)
input.pack()

bouton_query = tk.Button(window, text="SUBMIT QUERY", command=submit_query, height=2, width=20)
bouton_query.pack()

output = tk.Text(window, height=30, width=150)
output.pack()

bouton_insert = tk.Button(window, text="INSERT DATA FROM RDF", command=submit_insert, height=2, width=20)
bouton_insert.pack()

window.mainloop()
