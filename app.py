import streamlit as st
import requests
from groq import Groq

# 1. Configuración
URL_MACRODROID = "https://trigger.macrodroid.com/c5b99e55-87f6-4b97-a4bd-82fab9fac120/dex_comando"
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

st.title("Centro de Mando: Dex")

# Esfera fija (CSS directo para que no falle)
st.markdown("""
<style>
.esfera { width: 100px; height: 100px; background: radial-gradient(circle, #00f, #000); border-radius: 50%; margin: 20px auto; }
</style>
<div class="esfera"></div>
""", unsafe_allow_html=True)

# 2. Lógica de Mando
if prompt := st.chat_input("Dime tu orden..."):
    st.write(f"Orden: {prompt}")
    
    # ¿Es apertura?
    if "abre" in prompt.lower() or "abrir" in prompt.lower():
        try:
            requests.get(URL_MACRODROID, timeout=5)
            respuesta = "Ejecutando apertura."
        except:
            respuesta = "Error de conexión con el móvil."
    else:
        # IA normal
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}], 
            model="llama-3.1-8b-instant"
        )
        respuesta = response.choices[0].message.content
        st.write(f"Dex: {respuesta}")

    # 3. Voz forzada
    st.components.v1.html(f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{respuesta.replace('"', '')}");
        msg.lang = 'es-ES';
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
