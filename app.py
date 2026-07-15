import streamlit as st
import requests
from groq import Groq

# URL CONFIGURADA Y VERIFICADA
URL_MACRODROID = "https://trigger.macrodroid.com/c5b99e55-87f6-4b97-a4bd-82fab9fac120/dex_comando"

# --- DISEÑO DEL CENTRO DE MANDO (Dorado y Negro) ---
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

# --- LÓGICA DE MANDO ---
if prompt := st.chat_input("Dime tu orden..."):
    # 1. Detectar comando de apertura
    if "abre" in prompt.lower() or "abrir" in prompt.lower():
        st.write(f"Orden recibida: {prompt}")
        try:
            # Enviamos la petición GET a la URL de tu disparador
            respuesta = requests.get(URL_MACRODROID, timeout=5)
            if respuesta.status_code == 200:
                res = "Orden ejecutada, abriendo aplicación."
            else:
                res = f"El dispositivo respondió con error {respuesta.status_code}. Verifica la Macro."
        except Exception as e:
            res = f"Error de conexión con el móvil: {e}"
    else:
        # 2. Consulta IA normal
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
        response = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.1-8b-instant")
        res = response.choices[0].message.content
        st.write(f"Dex: {res}")

    # 3. VOZ Y ANIMACIÓN (Habla y palpita)
    st.components.v1.html(f"""
    <script>
        var sphere = window.parent.document.getElementById('esfera');
        sphere.className = 'esfera hablando';
        var msg = new SpeechSynthesisUtterance("{res.replace('"', '')}");
        msg.lang = 'es-ES';
        msg.onend = function() {{ sphere.className = 'esfera'; }};
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
