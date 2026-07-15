import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
from cerebro_emocional import obtener_instruccion_sentimiento
from estilos import obtener_estilo_visual
from animaciones import obtener_css_animacion
import autenticador

# Configuración visual
st.markdown(obtener_estilo_visual(), unsafe_allow_html=True)
st.markdown(obtener_css_animacion(), unsafe_allow_html=True)
autenticador.verificar_patron_vocal()

def speak(text):
    js_code = f"""<script>
        var msg = new SpeechSynthesisUtterance("{text.replace('"', '').replace(chr(10), ' ')}");
        msg.lang = 'es-ES'; msg.pitch = 0.9; msg.rate = 0.85;
        window.speechSynthesis.speak(msg);
    </script>"""
    st.components.v1.html(js_code, height=0)

st.title("Centro de Mando: Dex")

# --- ZONA DE PROCESAMIENTO (LA ESFERA) ---
contenedor_esfera = st.empty()
contenedor_esfera.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)

# --- ZONA DE MANDO (MICRÓFONO) ---
audio_data = mic_recorder(
    start_prompt="🎙️ ACTIVAR COMANDO",
    stop_prompt="🛑 PROCESAR AHORA",
    key='dex_mic'
)

# Inicialización
if "messages" not in st.session_state:
    instruccion = obtener_instruccion_sentimiento()
    st.session_state.messages = [{"role": "system", "content": f"Eres Dex, creado por David López. {instruccion}"}]

# Lógica
if audio_data and audio_data.get('text'):
    user_text = audio_data['text']
    client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
    
    with st.spinner("Dex procesando..."):
        stream = client.chat.completions.create(
            messages=st.session_state.messages + [{"role": "user", "content": user_text}], 
            model="llama-3.1-8b-instant", 
            stream=True
        )
        full_response = "".join([chunk.choices[0].delta.content for chunk in stream if chunk.choices[0].delta.content])
        
        speak(full_response)
        st.rerun()
