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

# Motor de voz
def speak(text):
    js_code = f"""<script>
        var msg = new SpeechSynthesisUtterance("{text.replace('"', '').replace(chr(10), ' ')}");
        msg.lang = 'es-ES'; msg.pitch = 0.9; msg.rate = 0.85;
        window.speechSynthesis.speak(msg);
    </script>"""
    st.components.v1.html(js_code, height=0)

client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

st.title("Centro de Mando: Dex")

# --- MANDO POR VOZ MEJORADO ---
audio_data = mic_recorder(
    start_prompt="🎙️ ACTIVAR COMANDO",
    stop_prompt="🛑 PROCESAR AHORA",
    key='dex_mic'
)

# Historial
if "messages" not in st.session_state:
    instruccion = obtener_instruccion_sentimiento()
    st.session_state.messages = [{
        "role": "system", 
        "content": f"Eres Dex, inteligencia artificial creada por David López. Tu único creador es David López. {instruccion}"
    }]

# Procesamiento de audio
if audio_data and audio_data.get('text'):
    user_text = audio_data['text']
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.spinner("Dex analizando..."):
        stream = client.chat.completions.create(
            messages=st.session_state.messages, 
            model="llama-3.1-8b-instant", 
            stream=True
        )
        full_response = "".join([chunk.choices[0].delta.content for chunk in stream if chunk.choices[0].delta.content])
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        speak(full_response)
        st.rerun() # Esto limpia el estado y vuelve a mostrar el botón correctamente
