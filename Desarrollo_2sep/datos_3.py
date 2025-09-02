import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar CSV
df = pd.read_csv("usuarios_app_limpieza.csv")

# Limpieza de datos
df = df.drop_duplicates(subset=['nombre','edad','país','estado'])
df = df.dropna(subset=['edad'])

print(df)

plt.figure(figsize=(8,6)) #la figura tendrá 8 pulgadas de ancho y 6 pulgadas de alto.
sns.boxplot(x="país", y="edad", data=df, palette="pastel")

plt.title("Distribución de edades por país")
plt.xlabel("País")
plt.ylabel("Edad")
plt.show()
