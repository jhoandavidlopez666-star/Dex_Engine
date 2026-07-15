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
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 3. Inicialización
if "messages" not in st.session_state:
    contexto = cargar_memoria()
    st.session_state.messages = [
        {"role": "system", "content": f"Eres Dex. Contexto: {contexto}. Sé estratégico, analítico y directo."}
    ]

st.title("Centro de Mando: Dex")

# 4. Chat y visualización
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
            messages=st.session_state.messages,
            model="llama-3.1-8b-instant",
            stream=True,
        )
        
        full_response = ""
        placeholder = st.empty()
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
