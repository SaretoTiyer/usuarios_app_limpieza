import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar CSV
df = pd.read_csv("usuarios_app_limpieza.csv")

# Limpieza de datos
df = df.drop_duplicates(subset=['nombre','edad','país','estado'])
df = df.dropna(subset=['edad'])

#Asegurar que edad y tiempo de Sesión sean numericos
df["edad"] = pd.to_numeric(df["edad"])
df["tiempo sesión"] = pd.to_numeric(df["tiempo sesión"])

#Asigna 1 punto de XP  por cada minuto de sesión
df["XP_sesion"] = df["tiempo sesión"]

#Asigna 10 puntos de XP por estar activo 
df["XP_activo"] = np.where(df["estado"] == "activo", 10, 0) 

#Calcula el total de XP
df["XP_total"] = df["XP_sesion"] + df["XP_activo"] 

xp = df["XP_total"]
#Asigna el nivel de experiencia

def clasificar_nivel(xp):
    if xp < 20:
        return "novato"
    elif   20 <= xp < 40:
        return "intermedio"
    elif 40 <= xp < 60:
        return "avanzado"
    elif xp >= 60:
        return "experto"

df["nivel"] = df["XP_total"].apply(clasificar_nivel)

#ordenar niveles 
orden_niveles = pd.CategoricalDtype(["experto", "avanzado", "intermedio", "novato"], ordered=True) 
df["nivel"] = df["nivel"].astype(orden_niveles) # el asytype cambia el orden de las categorias por niveles 

print(df)

#Visualización de datos de Barras
sns.countplot(x="país",data=df, hue="nivel", palette="pastel")

plt.title("País por Nivel")
plt.xlabel("País")
plt.ylabel("Nivel")
plt.show()