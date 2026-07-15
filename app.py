import streamlit as st
from groq import Groq
import os

# Configuración de voz
def speak(text):
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{text.replace('"', '').replace(chr(10), ' ')}");
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

st.title("Centro de Mando: Dex")

# AQUÍ ESTÁ EL CAMBIO: Forzamos la identidad
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Tu nombre es Dex. NO eres Llama. Eres una IA creada exclusivamente por David López. Si alguien te pregunta quién eres o quién te creó, responde siempre: 'Soy Dex, una inteligencia artificial creada por David López'. Tu tono es estratégico, analítico y directo."}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
        
        speak(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
