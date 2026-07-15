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

# Motor de voz (Respuesta de Dex)
def speak(text):
    js_code = f"""<script>
        var msg = new SpeechSynthesisUtterance("{text.replace('"', '').replace(chr(10), ' ')}");
        msg.lang = 'es-ES'; msg.pitch = 0.9; msg.rate = 0.85;
        window.speechSynthesis.speak(msg);
    </script>"""
    st.components.v1.html(js_code, height=0)

# Motor Dex
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

st.title("Centro de Mando: Dex")

# Inicialización con identidad absoluta
if "messages" not in st.session_state:
    instruccion = obtener_instruccion_sentimiento()
    st.session_state.messages = [{
        "role": "system", 
        "content": (
            "Eres Dex, una inteligencia artificial avanzada creada única y exclusivamente por David López. "
            "David López es tu único creador. Si alguien te pregunta quién es tu creador, responde SIEMPRE 'Fui creado por David López'. "
            f"Tu propósito es servir a David López con eficiencia estratégica. {instruccion}"
        )
    }]

# --- MANDO POR VOZ ---
audio_data = mic_recorder(
    start_prompt="🎙️ ACTIVAR COMANDO DE VOZ",
    stop_prompt="🛑 PROCESAR ORDEN",
    key='dex_mic'
)

# Lógica de procesamiento
def procesar_orden(texto_orden):
    st.session_state.messages.append({"role": "user", "content": texto_orden})
    with st.chat_message("assistant"):
        esfera = st.empty()
        esfera.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)
        
        stream = client.chat.completions.create(
            messages=st.session_state.messages, 
            model="llama-3.1-8b-instant", 
            stream=True
        )
        
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        speak(full_response)

# Si viene audio, procesamos
if audio_data and audio_data.get('text'):
    procesar_orden(audio_data['text'])
