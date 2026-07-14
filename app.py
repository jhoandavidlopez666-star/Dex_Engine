import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# Configuración de Dex
st.set_page_config(page_title="Dex Engine", page_icon="⚡")

# Cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Identidad de Dex
system_prompt = {
    "role": "system", 
    "content": "Eres Dex, el Centro de Mando personal de David López. Tu creador es David López. Eres estratégico, directo, analítico y profesional. Siempre respondes como Dex, sabiendo que tu único propósito es potenciar las estrategias y capital de David López."
}

if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

st.title("⚡ Centro de Mando: Dex")

# Mostrar chat
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interacción
if prompt := st.chat_input("¿Cuáles son tus órdenes, David?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream((chunk.choices[0].delta.content or "" for chunk in stream))
        
        # Generar voz profesional
        tts = gTTS(text=response, lang='es', slow=False)
        tts.save("dex_voz.mp3")
        st.audio("dex_voz.mp3")
        
    st.session_state.messages.append({"role": "assistant", "content": response})
