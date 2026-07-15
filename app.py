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
        return "Actúa como Dex, tu arquetipo es Aquarius, estratégico y analítico."

# 2. Cliente y validación de llave
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("Error: Configura la GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

client = Groq(api_key=api_key)

# 3. Inicialización de sesión
if "messages" not in st.session_state:
    contexto = cargar_memoria()
    st.session_state.messages = [
        {"role": "system", "content": f"Eres Dex. Tu contexto es: {contexto}. Responde siempre con tono estratégico, directo y analítico."}
    ]

st.title("Centro de Mando: Dex")

# 4. Interfaz de Chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama3-70b-8192",
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error de conexión: {e}")
