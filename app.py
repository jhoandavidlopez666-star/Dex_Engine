import streamlit as st
from groq import Groq
import os

# 1. Configuración de memoria
def cargar_memoria():
    memoria = ""
    for arch in ['identidad.txt', 'estrategia.txt', 'protocolo_humano.txt']:
        if os.path.exists(arch):
            with open(arch, 'r', encoding='utf-8') as f:
                memoria += f.read() + "\n"
    return memoria

# 2. Cliente y validación de seguridad
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("Error: Configura GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

client = Groq(api_key=api_key)

st.title("Centro de Mando: Dex")

# 3. Inicialización segura de historial
if "messages" not in st.session_state:
    contexto = cargar_memoria()
    st.session_state.messages = [
        {"role": "system", "content": f"Eres Dex. Contexto: {contexto}. Sé estratégico, analítico y directo."}
    ]

# 4. Mostrar historial existente
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. Lógica de chat con manejo de errores
if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Creamos un mensaje sin el historial previo si es necesario para evitar errores
            response_stream = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.1-8b-instant",
                stream=True,
            )
            
            full_response = ""
            placeholder = st.empty()
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # Si falla, limpiamos el historial para que el usuario pueda empezar de nuevo
            st.error("Error técnico detectado. Limpiando sesión...")
            st.session_state.messages = [] 
            st.rerun()
