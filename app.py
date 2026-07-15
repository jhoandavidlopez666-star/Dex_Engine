import streamlit as st
from groq import Groq
from cerebro_emocional import obtener_instruccion_sentimiento
from estilos import obtener_estilo_visual
from animaciones import obtener_css_animacion

# Inyectar estilos y animaciones
st.markdown(obtener_estilo_visual(), unsafe_allow_html=True)
st.markdown(obtener_css_animacion(), unsafe_allow_html=True)

# Motor de voz
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

# Configuración
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.title("Centro de Mando: Dex")

if "messages" not in st.session_state:
    instruccion = obtener_instruccion_sentimiento()
    st.session_state.messages = [{"role": "system", "content": f"Eres Dex. {instruccion}"}]

# Mostrar historial con estilo de consola
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(f"```text\n{message['content']}\n```")

# Lógica del Chat
if prompt := st.chat_input("Escribe tu orden..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"```text\n{prompt}\n```")

    with st.chat_message("assistant"):
        # Mostramos la esfera central
        esfera_placeholder = st.empty()
        esfera_placeholder.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)
        
        # Procesamiento
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
                # Mostramos el texto como si fuera una terminal escribiendo
                response_placeholder.markdown(f"```text\n{full_response}▌\n```")
        
        # Al terminar, fijamos el bloque de consola
        response_placeholder.markdown(f"```text\n{full_response}\n```")
        
        speak(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
