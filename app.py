import streamlit as st
import requests
from groq import Groq

# 1. Configuración de URL (La que sale en tu foto)
URL_MACRODROID = "https://trigger.macrodroid.com/c5b99e55-87f6-4b97-a4bd-82fab9fac120/dex_comando"

# 2. Configuración de IA
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

st.title("Centro de Mando: Dex")

# 3. Diseño de la Esfera (Grande y reactiva)
st.markdown("""
<style>
.esfera {
    width: 250px; height: 250px;
    background: radial-gradient(circle, #ffd700, #000);
    border-radius: 50%; margin: 50px auto;
    box-shadow: 0 0 60px #ffd700;
    transition: transform 0.3s;
}
.hablando { animation: palpitar 1s infinite; }
@keyframes palpitar { 0% { transform: scale(1); } 50% { transform: scale(1.2); } 100% { transform: scale(1); } }
</style>
<div id="esfera" class="esfera"></div>
""", unsafe_allow_html=True)

# 4. Lógica de Mando
if prompt := st.chat_input("Dime tu orden..."):
    # Si es comando de abrir app
    if "abre" in prompt.lower() or "abrir" in prompt.lower():
        st.write(f"David: {prompt}")
        try:
            requests.get(URL_MACRODROID, timeout=5)
            respuesta = "Ejecutando comando en tu dispositivo."
        except Exception as e:
            respuesta = "Error al contactar con el dispositivo."
    else:
        # Consulta normal
        response = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.1-8b-instant")
        respuesta = response.choices[0].message.content
        st.write(f"Dex: {respuesta}")

    # 5. Voz y Animación (Habla siempre)
    st.components.v1.html(f"""
    <script>
        var sphere = window.parent.document.getElementById('esfera');
        sphere.className = 'esfera hablando';
        var msg = new SpeechSynthesisUtterance("{respuesta.replace('"', '').replace(chr(10), ' ')}");
        msg.lang = 'es-ES';
        msg.onend = function() {{ sphere.className = 'esfera'; }};
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
