import pandas as pd
import numpy as np
import re

df = pd.read_csv("usuarios_app_clase2.csv", encoding="utf-8")

# 2. Normalizar nombre de columnas
df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_",regex = False) ) #elimina espacios y cambia espacios por guiones

#3. Unificar países
map_pais = {"mexico": "México", 
            "méxico":"México",
            "Mexico":"México",} 

df['pais'] = df['pais'].astype(str).str.strip().replace(map_pais)

def to_number(x):
    if pd.isna(x)  or str(x).strip() == "": #si la celda esta vacia
        return np.nan #retorna un valor faltante
    
    s = str(x).strip().lower() 
    palabras = {"quince": 15}
    if s in palabras:
        return float(palabras[s]) #retorna el numero
    
    m = re.search(r"(\d+)", s) #busca un numero en la celda
    return float(m.group(1)) if m else np.nan #si no encuentra un numero retorna un valor faltante