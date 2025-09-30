import pandas as pd 
import matplotlib.pyplot as plit
import seaborn as sns


df = pd.read_csv("usuarios_segmentación_clase3.csv")

plit.figure(figsize=(12,8))
#Grafico de barras
plit.subplot(2,2,1)
sns.countplot(data=df, x="segmento_clicks", hue="suscripcion", palette="Set2")
plit.title("Usuarios por Segmento de clicks")
#Grafico de cajas
plit.subplot(2,2,2)
sns.boxplot(data=df,x="suscripcion", y="compras", palette="muted")
plit.title("Distribució de compras segun la suscripción")
#Grafico de barras
plit.subplot(2,2,3)
sns.countplot(data=df, x="pais", hue="estado",palette="Set1")
plit.title("Usuarios por País")
#Grafico de mapa de calor
plit.subplot(2,2,4)
sns.heatmap(df.select_dtypes(include=["int64","float64"]).corr(), annot=True, cmap="coolwarm")
plit.title("Correlación")


plit.tight_layout()
plit.show()