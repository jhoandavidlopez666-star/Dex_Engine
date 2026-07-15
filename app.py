import streamlit as st
from groq import Groq
from cerebro_emocional import obtener_instruccion_sentimiento
from estilos import obtener_estilo_visual
from animaciones import obtener_css_animacion

# Inyectamos estilos y animaciones
st.markdown(obtener_estilo_visual(), unsafe_allow_html=True)
st.markdown(obtener_css_animacion(), unsafe_allow_html=True)

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

# Motor Dex
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.title("Centro de Mando: Dex")

# Inicialización
if "messages" not in st.session_state:
    instruccion = obtener_instruccion_sentimiento()
    st.session_state.messages = [{"role": "system", "content": f"Eres Dex. {instruccion}"}]

# Mostrar historial
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Lógica del chat
if prompt := st.chat_input("Escribe tu orden..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Contenedor estable para el círculo y estado
        status_container = st.empty()
        status_container.markdown('<div class="pulso"></div> **Dex procesando información...**', unsafe_allow_html=True)
        
        stream = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama-3.1-8b-instant",
            stream=True,
        )
        
        full_response = ""
        response_placeholder = st.empty()
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                # Mantenemos el texto fluyendo abajo
                response_placeholder.markdown(full_response + "▌")
        
        # Al terminar, quitamos el círculo y mostramos el texto final
        status_container.empty()
        response_placeholder.markdown(full_response)
        
        # Activamos la voz
        speak(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
