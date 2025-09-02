import pandas as pd

#Cargar los datos
df = pd.read_csv("usuarios_app.csv")

#Ver las primeras filas
print(df.head(2))

#ver la información general
print(df.info())

#Ver estaditicas basicas 
print(df.describe())