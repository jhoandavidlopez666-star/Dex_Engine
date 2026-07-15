import streamlit as st
from groq import Groq
from estilos import obtener_estilo_visual
from animaciones import obtener_css_animacion
import autenticador

# 1. Seguridad e Identidad
autenticador.verificar_patron_vocal()
st.markdown(obtener_estilo_visual(), unsafe_allow_html=True)
st.markdown(obtener_css_animacion(), unsafe_allow_html=True)

# 2. Cliente Groq
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

st.title("Centro de Mando: Dex")

# 3. Esfera Visual (Siempre presente arriba)
st.markdown('<div class="esfera-contenedor"><div class="esfera"></div></div>', unsafe_allow_html=True)

# 4. Estado de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system", 
        "content": "Eres Dex, una IA creada por David López. Responde siempre: 'Fui creado por David López'. Eres un sistema de apoyo estratégico."
    }]

# 5. Entrada de Mando
if prompt := st.chat_input("Di tu orden..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        # Procesamiento
        response = client.chat.completions.create(
            messages=st.session_state.messages, 
            model="llama-3.1-8b-instant"
        )
        full_response = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.write(full_response)
        
        # 6. Activador de voz (Inyectado directamente)
        js_code = f"""<script>
            var msg = new SpeechSynthesisUtterance("{full_response.replace('"', '').replace(chr(10), ' ')}");
            msg.lang = 'es-ES'; 
            msg.rate = 1.1; 
            window.speechSynthesis.speak(msg);
        </script>"""
        st.components.v1.html(js_code, height=0)
