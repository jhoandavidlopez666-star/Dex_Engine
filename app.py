import streamlit as st
from groq import Groq
from cerebro_emocional import obtener_instruccion_sentimiento
from estilos import obtener_estilo_visual
from animaciones import obtener_css_animacion

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

client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

st.title("Centro de Mando: Dex")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": f"Eres Dex. {obtener_instruccion_sentimiento()}"}]

# Mostrar historial limpio
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="consola-dex">{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "user":
        st.write(f"**Tú:** {message['content']}")

if prompt := st.chat_input("Escribe tu orden..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.write(f"**Tú:** {prompt}")

    with st.chat_message("assistant"):
        # Mostramos la esfera
        esfera = st.empty()
        esfera.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)
        
        # Respuesta inmediata con streaming
        stream = client.chat.completions.create(messages=st.session_state.messages, model="llama-3.1-8b-instant", stream=True)
        
        full_response = ""
        texto_placeholder = st.empty()
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                # Renderizamos con estilo consola directo, sin etiquetas de código
                texto_placeholder.markdown(f'<div class="consola-dex">{full_response}▌</div>', unsafe_allow_html=True)
        
        texto_placeholder.markdown(f'<div class="consola-dex">{full_response}</div>', unsafe_allow_html=True)
        speak(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
