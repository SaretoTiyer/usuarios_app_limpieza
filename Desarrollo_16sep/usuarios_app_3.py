import pandas as pd 
import random as r 


nombres = ["Sofía", "Alejandro", "Valentina", "Sebastián", "Isabella", "Mateo", "Camila", 
            "Daniel", "Mariana", "Nicolás", "Gabriela", "Diego", "Victoria", "Samuel", 
            "Luciana", "Santiago", "Valeria", "Joaquín", "Emilia", "Felipe", "Antonia", 
            "Benjamín", "Florencia", "Ignacio", "Martina", "Lucas", "Josefa", "Agustín", "Catalina"]


paises = ["Colombia", "Mexico", "Argentina", "Peru", "Chile", "Brasil"]

suscripciones = ["Free", "Premium"]

estados = ["Activo", "Inactivo"]

data = []

for i in range(1,201):
    nombre = r.choice(nombres)
    edad = r.randint(18,60)
    pais = r.choice(paises)
    tiempo = r.randint(5, 200)
    estado = r.choice(estados)
    suscripcion = r.choice(suscripciones)
    clicks = r.randint(10,300)
    compras = r.randint(0,5)

    data.append([i,nombre,edad,pais,tiempo,estado,suscripcion,clicks,compras])

df = pd.DataFrame(data, columns=["usuario_id","nombre","edad","pais","tiempo_sesion_min",
                                    "estado","suscripcion","clicks","compras"])

df.to_excel("usuarios_app_clase3.xlsx", index=False)
df.to_csv("usuarios_app_clase3.csv", index=False, encoding="Utf-8")

