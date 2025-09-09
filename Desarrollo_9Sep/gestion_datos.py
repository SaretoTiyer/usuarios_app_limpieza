import pandas as pd
import numpy as np
import re

df = pd.read_csv(r"C:\Users\reyes\OneDrive\Documentos\WorkSpace\pruebasPy\2025-SENA\III Trismestre\Desarrollo_9Sep\usuarios_app_clase2.csv", encoding="utf-8")

# 2). Normalizar nombre de columnas
df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_",regex = False) ) #elimina espacios y cambia espacios por guiones

#3). Unificar países
map_pais = {"mexico": "México", 
            "méxico":"México",
            "Mexico":"México",} 

df['pais'] = df['pais'].astype(str).str.strip().replace(map_pais)

#4) Limpieza de datos
def to_number(x):
    if pd.isna(x)  or str(x).strip() == "": #si la celda esta vacia
        return np.nan #retorna un valor faltante
    
    s = str(x).strip().lower() 
    palabras = {"quince": 15}
    if s in palabras:
        return float(palabras[s]) #retorna el numero
    
    m = re.search(r"(\d+)", s) #busca un numero en la celda
    return float(m.group(1)) if m else np.nan #si no encuentra un numero retorna un valor faltante

#Aplicar conversiones
df["edad"] = df["edad"].apply(to_number) 
df["tiempo_sesion_min"] = df["tiempo_sesion_min"].apply(to_number)
df["clicks"] = pd.to_numeric(df["compras"], errors="coerce") #validamos que sea un numero

# 5) Eliminar duplicados (Ignorando el usuario_id)
df = df.drop_duplicates(subset=['nombre','edad','pais','tiempo_sesion_min','estado','suscripcion','clicks','compras'])

#6) Quitar filas sin edad o tiempo de sesión
df = df.dropna(subset=["edad", "tiempo_sesion_min"])

#7) rangos razonables
df = df[df['edad'].between(10,100)] 
df = df[df['tiempo_sesion_min'].between(0,1000)]

#8) Guardar datos
df.to_csv("usuarios_app_limpio9sep.csv", index=False, encoding="utf-8")
print("Limpieza finalizado. Filas:", df.shape[0])