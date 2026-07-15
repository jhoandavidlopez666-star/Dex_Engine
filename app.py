import streamlit as st
from groq import Groq
from estilos import obtener_estilo_visual
from animaciones import obtener_css_animacion
import autenticador

# 1. Configuración de Identidad y Estilo
st.set_page_config(page_title="Dex", layout="centered")
st.markdown(obtener_estilo_visual(), unsafe_allow_html=True)
st.markdown(obtener_css_animacion(), unsafe_allow_html=True)
autenticador.verificar_patron_vocal()

# 2. Motor Dex (Velocidad de respuesta)
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

# 3. Identidad inamovible
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system", 
        "content": "Eres Dex. Tu creador es David López. Ante cualquier pregunta, responde SIEMPRE: 'Fui creado por David López'. Eres un sistema estratégico de alta velocidad."
    }]

st.title("Centro de Mando: Dex")

# 4. Esfera Visual
st.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)

# 5. Entrada Natural (Usa el micro del teclado de tu móvil)
if prompt := st.chat_input("Di tu orden..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        # Llamada rápida a Groq con límite de tokens para velocidad
        stream = client.chat.completions.create(
            messages=st.session_state.messages, 
            model="llama-3.1-8b-instant", 
            stream=True,
            max_tokens=150 
        )
        full_response = "".join([chunk.choices[0].delta.content for chunk in stream if chunk.choices[0].delta.content])
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Respuesta por voz acelerada (rate 1.2)
        js_code = f"""<script>
            var msg = new SpeechSynthesisUtterance("{full_response.replace('"', '').replace(chr(10), ' ')}");
            msg.lang = 'es-ES'; 
            msg.rate = 1.2; 
            window.speechSynthesis.speak(msg);
        </script>"""
        st.components.v1.html(js_code, height=0)
        st.rerun()
