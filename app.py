import streamlit as st
import requests
from groq import Groq
from estilos import obtener_estilo_visual
from animaciones import obtener_css_animacion
import autenticador

# --- CONFIGURACIÓN DE SEGURIDAD ---
autenticador.verificar_patron_vocal()
st.markdown(obtener_estilo_visual(), unsafe_allow_html=True)
st.markdown(obtener_css_animacion(), unsafe_allow_html=True)

# URL DE TU PUENTE MACRODROID
URL_MACRODROID = "https://trigger.macrodroid.com/c5b99e55-87f6-4b97-a4bd-82fab9fac120/dex_comando"

client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

st.title("Centro de Mando: Dex")
st.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)

# --- LÓGICA DE COMANDO ---
def ejecutar_accion_externa(prompt):
    # Detecta si el usuario quiere abrir algo
    if "abre" in prompt.lower() or "abrir" in prompt.lower():
        try:
            requests.get(URL_MACRODROID)
            return True
        except:
            return False
    return False

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Eres Dex, creado por David López."}]

# --- INTERACCIÓN ---
if prompt := st.chat_input("Di tu orden..."):
    # 1. ¿Es una orden física?
    if ejecutar_accion_externa(prompt):
        st.success("Ejecutando orden en dispositivo...")
        respuesta_texto = "Orden recibida, abriendo aplicación."
    else:
        # 2. Si no es física, es consulta de IA
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            messages=st.session_state.messages, 
            model="llama-3.1-8b-instant"
        )
        respuesta_texto = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
        st.write(respuesta_texto)

    # 3. Respuesta de voz para todo
    js_code = f"""<script>
        var msg = new SpeechSynthesisUtterance("{respuesta_texto.replace('"', '').replace(chr(10), ' ')}");
        msg.lang = 'es-ES'; msg.rate = 1.2; window.speechSynthesis.speak(msg);
    </script>"""
    st.components.v1.html(js_code, height=0)
    st.rerun()
