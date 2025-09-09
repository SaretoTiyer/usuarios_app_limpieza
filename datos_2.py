import pandas as pd

df = pd.read_csv("usuarios_app_limpieza.csv")

#Ver las primeras filas
print(df.head(2))

#ver la información general
print(df.info())

#Ver estaditicas basicas 
print(df.describe())

#limpieza de datos
df = df.drop_duplicates(subset=['nombre','edad','país','estado'])

#Rellenar valores nulos en "edad" con el promedio 
df["edad"] = df["edad"].fillna(df["edad"].mean())

#Eliminar filas con valores nulos
df = df.dropna()

#filtrar los datos que el usuario este activo
usuarios_activos = df[df["estado"] == "activo"]

print(usuarios_activos)

