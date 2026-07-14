import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# Configuración de Dex
st.set_page_config(page_title="Dex Engine", page_icon="⚡")

# Cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Identidad
system_prompt = {"role": "system", "content": "Eres Dex, el Centro de Mando de David López."}

if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

st.title("⚡ Centro de Mando: Dex")

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿Cuáles son tus órdenes?"):
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
        
        # Voz
        tts = gTTS(text=response, lang='es', slow=False)
        tts.save("dex_voz.mp3")
        st.audio("dex_voz.mp3")
        
    st.session_state.messages.append({"role": "assistant", "content": response})
