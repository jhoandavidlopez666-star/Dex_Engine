import streamlit as st
from groq import Groq
import os

# Configuración de voz "suave" y profesional
def speak(text):
    # Ajustes: rate 0.85 (más lento), pitch 0.9 (más profundo/cálido)
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{text.replace('"', '').replace(chr(10), ' ')}");
        var voices = window.speechSynthesis.getVoices();
        // Intentamos buscar una voz femenina en español si existe
        var femaleVoice = voices.find(v => v.lang.includes('es') && v.name.toLowerCase().includes('female'));
        if (femaleVoice) msg.voice = femaleVoice;
        
        msg.lang = 'es-ES';
        msg.pitch = 0.9; 
        msg.rate = 0.85; 
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# Configuración de Dex
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Centro de Mando: Dex")

if prompt := st.chat_input("Escribe tu orden..."):
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
        
        # Inyectamos la voz suave
        speak(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
