import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import random

# 👉 Token de Clash Royale
load_dotenv()
API_TOKEN = os.getenv("CLASH_ROYALE_TOKEN")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Configuración del dashboard
st.set_page_config(page_title="Estadísticas Clash Royale", layout="wide")
st.title("🏆 Dashboard de Estudiantes Clash Royale")
st.markdown("Compara el rendimiento de tus estudiantes en tiempo real usando la API oficial de Clash Royale.")

# Función para obtener datos generales de un jugador
def get_player_data(tag):
    tag = tag.replace("#", "").upper()
    url = f"https://api.clashroyale.com/v1/players/%23{tag}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return {
            "Tag": tag,
            "Nombre": data.get("name"),
            "Nivel Rey": data.get("expLevel"),
            "Trofeos": data.get("trophies"),
            "Máx Trofeos": data.get("bestTrophies"),
            "Victorias": data.get("wins"),
            "Derrotas": data.get("losses"),
            "Batallas 1v1": data.get("battleCount"),
            "Cartas Desbloqueadas": data.get("cardsUnlocked"),
            "Clan": data.get("clan", {}).get("name", "Sin clan")
        }
    else:
        return {"Tag": tag, "Error": f"No se pudo obtener datos ({response.status_code})"}

# Función para obtener historial de batallas con imágenes de cartas
def get_battle_log(tag):
    tag = tag.replace("#", "").upper()
    url = f"https://api.clashroyale.com/v1/players/%23{tag}/battlelog"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        battles = response.json()
        logs = []
        for battle in battles[:5]:
            if "team" in battle and "opponent" in battle:
                raw_time = battle.get("battleTime", "N/A")
                if raw_time != "N/A":
                    fecha = datetime.strptime(raw_time, "%Y%m%dT%H%M%S.%fZ")
                    fecha = fecha.replace(tzinfo=ZoneInfo("UTC"))
                    fecha_colombia = fecha.astimezone(ZoneInfo("America/Bogota"))
                    fecha_legible = fecha_colombia.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    fecha_legible = "N/A"

                mazo_html = ""
                for card in battle["team"][0]["cards"]:
                    img_url = card.get("iconUrls", {}).get("medium", "")
                    if img_url:
                        mazo_html += f'<img src="{img_url}" width="40" style="margin:2px;border-radius:8px;">'

                logs.append({
                    "Fecha": fecha_legible,
                    "Modo": battle.get("gameMode", {}).get("name", "Desconocido"),
                    "Resultado": "Victoria" if battle["team"][0].get("crowns", 0) > battle["opponent"][0].get("crowns", 0) else "Derrota",
                    "Mazo": mazo_html
                })
        df = pd.DataFrame(logs)
        return df
    else:
        return pd.DataFrame([{"Error": f"No se pudo obtener el historial ({response.status_code})"}])

# Entrada de tags de estudiantes
st.sidebar.header("🎓 Ingresar player tags")
tags_input = st.sidebar.text_area("Escribe los tags separados por coma", "#Y022GRCJQ,#R09228V,#V222YCG8G")

# Estado del torneo
if "ronda" not in st.session_state:
    st.session_state.ronda = 1
if "llaves" not in st.session_state:
    st.session_state.llaves = []
if "ganadores" not in st.session_state:
    st.session_state.ganadores = []

# Generar llaves aleatorias con pase automático si hay número impar
def generar_llaves(tags):
    random.shuffle(tags)
    llaves = []
    i = 0
    while i < len(tags) - 1:
        llaves.append((tags[i], tags[i+1]))
        i += 2
    if len(tags) % 2 == 1:
        llaves.append((tags[-1], "BYE"))  # El último jugador pasa automáticamente
    return llaves

# Mostrar llaves y registrar ganadores
def mostrar_llaves(llaves):
    st.subheader(f"🎯 Ronda {st.session_state.ronda} del Torneo")
    ganadores = []
    for i, (p1, p2) in enumerate(llaves):
        col1, col2, col3 = st.columns([3, 3, 2])
        col1.markdown(f"**Jugador 1:** {p1}")
        col2.markdown(f"**Jugador 2:** {p2}")
        if p2 == "BYE":
            col3.markdown("✅ Pase automático")
            ganadores.append(p1)
        else:
            ganador = col3.selectbox(f"Ganador del duelo {i+1}", [p1, p2], key=f"duelo_{i}_r{st.session_state.ronda}")
            ganadores.append(ganador)
    return ganadores

# Procesar tags ingresados
if tags_input:
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
    st.subheader("📊 Estadísticas generales")
    data = [get_player_data(tag) for tag in tags]
    df = pd.DataFrame(data)
    st.dataframe(df)

    st.subheader("📈 Comparación de trofeos")
    st.bar_chart(df.set_index("Nombre")["Trofeos"])

    st.subheader("📈 Comparación de nivel de rey")
    st.bar_chart(df.set_index("Nombre")["Nivel Rey"])

    st.subheader("📈 Comparación de victorias")
    st.bar_chart(df.set_index("Nombre")["Victorias"])

    st.subheader("🏅 Ranking por trofeos")
    ranking = df.sort_values(by="Trofeos", ascending=False).reset_index(drop=True)
    st.table(ranking[["Nombre", "Trofeos", "Nivel Rey", "Victorias"]])

    st.subheader("📜 Historial de batallas recientes")
    for tag in tags:
        info = get_player_data(tag)
        nombre = info.get("Nombre", "Desconocido")
        st.markdown(f"### 🔍 {nombre} ({tag})")
        log_df = get_battle_log(tag)
        if "Error" in log_df.columns:
            st.dataframe(log_df)
        else:
            for _, row in log_df.iterrows():
                st.markdown(
                    f"**{row['Fecha']}** | {row['Modo']} | **{row['Resultado']}**<br>{row['Mazo']}",
                    unsafe_allow_html=True
                )

    # Fase de torneo
    st.subheader("🏆 Fase de Torneo Eliminatorio")
    if st.button("🎮 Iniciar torneo"):
        st.session_state.ronda = 1
        st.session_state.llaves = generar_llaves(tags)
        st.session_state.ganadores = []

    if st.session_state.llaves:
        ganadores_ronda = mostrar_llaves(st.session_state.llaves)
        if st.button("✅ Confirmar resultados de la ronda"):
            st.session_state.ganadores = ganadores_ronda
            if len(ganadores_ronda) == 1:
                st.success(f"🏅 ¡Campeón del torneo: {ganadores_ronda[0]}!")
                st.session_state.llaves = []
            else:
                st.session_state.ronda += 1
                st.session_state.llaves = generar_llaves(ganadores_ronda)

    # Preguntas educativas
    st.subheader("🧠 Reflexión")
    st.markdown("""
    - ¿Qué decisiones podrías tomar basándote en estos datos?
    - ¿Qué cartas aparecen en tus derrotas?
    - ¿Cómo podrías mejorar tu mazo?
    - ¿Qué aprendiste sobre el análisis de datos que podrías aplicar en otras áreas?
    """)
else:
    st.info("👈 Ingresa los player tags en la barra lateral para comenzar.")