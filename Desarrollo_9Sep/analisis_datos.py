import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1) Cargar la base de datos
df = pd.read_csv(r"C:\Users\reyes\OneDrive\Documentos\WorkSpace\pruebasPy\2025-SENA\III Trismestre\Desarrollo_9Sep\usuarios_app_limpio9sep.csv", encoding="utf-8")

# 2) KPI Rápidos : Total de usuarios. 
total_usuarios = len(df)
print("Total de usuarios:", total_usuarios)

# 3) KPI Rápidos : Promedio, mediana  y cantidad de sesiones por pais y estado
stats = (
    df.groupby(["pais", "estado"])["tiempo_sesion_min"] #Agrupamos los datos por país y estado, y seleccionamos la columna de tiempo de sesión
    .agg(["mean","median","count"]) #Calculamos la media, la mediana y la cantidad de sesiones
    .rename(columns = {"mean":"promedio", "median":"mediana","count":"cantidad"}) #Renombramos las columnas
    .reset_index()
)
print("\nEstadísticas por país y estado:")
print(stats)

# 4) coorrelación entre edad y numero de clicks
# la correlación mide que tan relacionados estan dos valores numericos.
Correlación = df["edad"].corr(df["clicks"])
print("\nCorrelación entre edad y numero de clicks:", Correlación)
# A medida que la edad los clicks disminuyen.

# 5) Visualzación 1: Usuarios por gráfico de barras. 
plt.figure(figsize=(8,6))
usuarios_por_pais = df.groupby("pais")["usuario_id"].count().reset_index()
sns.barplot(data=usuarios_por_pais,x="pais", y="usuario_id", hue="pais", palette="viridis")
plt.title("Usuarios por país")
plt.xlabel("País")
plt.ylabel("Cantidad de usuarios")
plt.show()

# 6) Visualización 2: País por edad
plt.figure(figsize=(10,5))
sns.boxplot(data=df, x="pais", y="edad", palette="pastel")
plt.title("Distribución de edades por país")
plt.xlabel("País")
plt.ylabel("Edad")
plt.show()

# 7) Visualización 3: Mapa de calor de correlaciones
plt.figure(figsize=(8,6))
sns.heatmap(df.select_dtypes(include=["number"]).corr(), annot=True, cmap="coolwarm")
plt.title("Heatmap de correlaciones")
plt.tight_layout()
plt.show()