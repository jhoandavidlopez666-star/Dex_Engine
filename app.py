import streamlit as st
from groq import Groq
import os

# Configuración forzada de API Key
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("No se encontró la API Key en los secretos de Streamlit. Ve a Settings -> Secrets y agrégala.")
    st.stop()

client = Groq(api_key=api_key)

# Inicialización de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Centro de Mando: Dex")

# Mostrar chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interacción
if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama3-8b-8192",
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error de conexión con Groq: {e}")
