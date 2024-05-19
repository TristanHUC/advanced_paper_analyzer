import requests
import pandas as pd

def buscar_organizacion_por_nombre(nombre):
    url = "https://api.ror.org/organizations"
    params = {"query": nombre}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def obtener_datos_organizacion(organizacion_id):
    url = f"https://api.ror.org/organizations/{organizacion_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def buscar_datos_por_nombres(nombres):
    resultados = []
    for nombre in nombres:
        resultado_busqueda = buscar_organizacion_por_nombre(nombre)
        if resultado_busqueda and "items" in resultado_busqueda:
            for item in resultado_busqueda["items"]:
                datos_organizacion = obtener_datos_organizacion(item["id"])
                if datos_organizacion:
                    resultados.append(datos_organizacion)
    return resultados

def get_names(names_file):
    # Get array of all IDs
    all_names = []
    with open(names_file) as my_file:
        all_names = [line.strip('\n\r') for line in my_file]

    print(all_names)
    return all_names

# Ejemplo de uso
nombres_organizaciones = get_names("organizations.txt")
datos_organizaciones = buscar_datos_por_nombres(nombres_organizaciones)

# Convertir a DataFrame para mejor manejo y visualización
df_organizaciones = pd.DataFrame(datos_organizaciones)
print(df_organizaciones)