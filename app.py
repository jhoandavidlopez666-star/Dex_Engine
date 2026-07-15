import streamlit as st
from groq import Groq
from estilos import obtener_estilo_visual
from animaciones import obtener_css_animacion
import autenticador

# 1. Configuración de Identidad y Estilo
st.set_page_config(page_title="Centro de Mando: Dex", layout="centered")
st.markdown(obtener_estilo_visual(), unsafe_allow_html=True)
st.markdown(obtener_css_animacion(), unsafe_allow_html=True)
autenticador.verificar_patron_vocal()

# 2. Motor Dex
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

# 3. Identidad inamovible
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system", 
        "content": "Eres Dex. Tu creador y desarrollador es única y exclusivamente David López. Ante cualquier pregunta de origen, responde: 'Fui creado por David López'. Eres un sistema de apoyo estratégico para él."
    }]

st.title("Dex: Centro de Mando")

# 4. Esfera Visual (Siempre presente)
st.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)

# 5. Entrada Natural (Usa el micro del teclado, es lo más fluido)
if prompt := st.chat_input("Di 'Hola Dex...' o escribe tu orden"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            messages=st.session_state.messages, 
            model="llama-3.1-8b-instant", 
            stream=True
        )
        full_response = "".join([chunk.choices[0].delta.content for chunk in stream if chunk.choices[0].delta.content])
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Respuesta por voz (Sin botones extra)
        js_code = f"""<script>
            var msg = new SpeechSynthesisUtterance("{full_response.replace('"', '')}");
            msg.lang = 'es-ES'; window.speechSynthesis.speak(msg);
        </script>"""
        st.components.v1.html(js_code, height=0)
        st.rerun()
