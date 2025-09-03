import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar CSV
df = pd.read_csv("usuarios_app_limpieza.csv")

# Limpieza de datos
df = df.drop_duplicates(subset=['nombre','edad','país','estado'])
df = df.dropna(subset=['edad'])

#Filtrar los datos que el usuario este activo
df = df[df["estado"] == "activo"]

#Asegurar que edad y tiempo de Sesión sean numericos
df["edad"] = pd.to_numeric(df["edad"])
df["tiempo sesión"] = pd.to_numeric(df["tiempo sesión"])

#Grafico de dispersión
sns.scatterplot(x="edad", y="país", data=df, hue="país", palette="pastel")

plt.title("Edad vs Países")
plt.xlabel("Edad")
plt.ylabel("País")

plt.show()

