import streamlit as st
from groq import Groq
import os

# 1. Configuración de memoria
def cargar_memoria():
    try:
        memoria = ""
        for arch in ['identidad.txt', 'estrategia.txt', 'protocolo_humano.txt']:
            if os.path.exists(arch):
                with open(arch, 'r', encoding='utf-8') as f:
                    memoria += f.read() + "\n"
        return memoria
    except:
        return "Actúa como Dex."

# 2. Cliente
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Inicialización
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": cargar_memoria()}]

st.title("Centro de Mando: Dex")

# 4. Chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Llamada simplificada
        chat_completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama3-8b-8192",
            stream=True,
        )
        response = st.write_stream(chat_completion)
    st.session_state.messages.append({"role": "assistant", "content": response})
