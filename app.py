import streamlit as st
import requests
from groq import Groq
import autenticador

# --- CONFIGURACIÓN ---
URL_MACRODROID = "https://trigger.macrodroid.com/c5b99e55-87f6-4b97-a4bd-82fab9fac120/dex_comando"
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

st.title("Centro de Mando: Dex")
st.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Eres Dex, la IA estratégica creada por David López."}]

# --- INTERACCIÓN ---
if prompt := st.chat_input("Dime tu orden..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 1. ¿Es una orden de ejecutar app?
    if "abre" in prompt.lower() or "abrir" in prompt.lower():
        respuesta_final = "Ejecutando orden en tu dispositivo."
        try:
            # Enviamos el disparo a MacroDroid
            requests.get(URL_MACRODROID, timeout=5)
        except:
            respuesta_final = "Error crítico de conexión con el dispositivo."
    else:
        # 2. Es consulta de IA
        response = client.chat.completions.create(
            messages=st.session_state.messages, 
            model="llama-3.1-8b-instant"
        )
        respuesta_final = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
        st.write(respuesta_final)

    # 3. VOZ FORZADA (El sistema SIEMPRE hablará)
    js_code = f"""<script>
        var msg = new SpeechSynthesisUtterance("{respuesta_final.replace('"', '').replace(chr(10), ' ')}");
        msg.lang = 'es-ES'; 
        msg.rate = 1.1; 
        window.speechSynthesis.speak(msg);
    </script>"""
    st.components.v1.html(js_code, height=0)
    st.rerun()
