import streamlit as st
from groq import Groq
from cerebro_emocional import obtener_instruccion_sentimiento
from estilos import obtener_estilo_visual
from animaciones import obtener_css_animacion

# Configuración visual
st.markdown(obtener_estilo_visual(), unsafe_allow_html=True)
st.markdown(obtener_css_animacion(), unsafe_allow_html=True)

# Motor de voz
def speak(text):
    js_code = f"""<script>
        var msg = new SpeechSynthesisUtterance("{text.replace('"', '').replace(chr(10), ' ')}");
        msg.lang = 'es-ES'; msg.pitch = 0.9; msg.rate = 0.85;
        window.speechSynthesis.speak(msg);
    </script>"""
    st.components.v1.html(js_code, height=0)

# Motor Dex
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.title("Centro de Mando: Dex")

# Interacción minimalista
if prompt := st.chat_input("Escribe tu orden..."):
    with st.chat_message("assistant"):
        # La esfera central toma el mando
        esfera = st.empty()
        esfera.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)
        
        # Procesamiento silencioso
        stream = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}], 
            model="llama-3.1-8b-instant", 
            stream=True
        )
        
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        
        # Dex habla sin dejar rastro de texto en la pantalla
        speak(full_response)
        
        # La esfera permanece activa
