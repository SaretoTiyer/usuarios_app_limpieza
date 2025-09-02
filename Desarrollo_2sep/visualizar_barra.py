import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("usuarios_app.csv")

#obtener la cantidad de usuarios por país
conteos = df["país"].value_counts()
#crear paleta de colores
colors = sns.color_palette("pastel" , len(conteos))

#graficar
ax = conteos.plot(kind="bar", color=colors)
#Titulos y etiquetas
plt.title("Usuarios por país")
plt.xlabel("País")
plt.ylabel("Cantidad de usuarios")
plt.show()

