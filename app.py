import streamlit as st
from groq import Groq
import os

# Función para cargar la memoria personalizada
def cargar_memoria():
    memoria = ""
    archivos = ['identidad.txt', 'estrategia.txt', 'protocolo_humano.txt']
    for nombre_archivo in archivos:
        if os.path.exists(nombre_archivo):
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                memoria += f.read() + "\n"
    return memoria

# Configuración del cliente
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Inicializar memoria si no existe
if "messages" not in st.session_state:
    contexto = cargar_memoria()
    st.session_state.messages = [
        {"role": "system", "content": f"Tu base de conocimiento es: {contexto}. Actúa siempre bajo esta estructura de pensamiento."}
    ]

# Resto de tu código (la interfaz de chat sigue igual)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model="llama3-8b-8192",
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
