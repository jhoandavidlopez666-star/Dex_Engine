import streamlit as st
from groq import Groq
import os

# Función para cargar memoria
def cargar_memoria():
    memoria = ""
    for archivo in ['identidad.txt', 'estrategia.txt', 'protocolo_humano.txt']:
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                memoria += f.read() + "\n"
    return memoria

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# INICIALIZACIÓN ÚNICA: Esto evita el error de "Bad Request"
if "messages" not in st.session_state:
    contexto = cargar_memoria()
    st.session_state.messages = [
        {"role": "system", "content": f"Tu base de conocimiento es: {contexto}. Actúa siempre bajo esta estructura de pensamiento."}
    ]
