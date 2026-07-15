import streamlit as st
import requests
from groq import Groq
from datetime import datetime

# --- CONFIGURACIÓN ---
URL_MACRODROID = "https://trigger.macrodroid.com/c5b99e55-87f6-4b97-a4bd-82fab9fac120/dex_comando"
CODIGO_DAVID = "BELQUARIEL-17"

st.title("Centro de Mando: Dex")

# --- 1. AUTENTICACIÓN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.nombre = None

if not st.session_state.autenticado:
    clave = st.text_input("Ingresa tu Código de Identidad:", type="password")
    if st.button("Verificar"):
        if clave == CODIGO_DAVID:
            st.session_state.autenticado = True
            st.session_state.nombre = "David López"
            st.rerun()
        else:
            st.error("Acceso denegado.")
    st.stop()

# --- 2. PANEL Y DINAMISMO ---
st.success(f"Acceso Autorizado: {st.session_state.nombre}")

# CSS con animación de movimiento para la esfera
st.markdown("""
<style>
.esfera {
    width: 250px; height: 250px;
    background: radial-gradient(circle, #ffd700, #000);
    border-radius: 50%; margin: 50px auto;
    box-shadow: 0 0 60px #ffd700;
    transition: transform 0.5s;
}
.hablando { animation: pulse 1s infinite; }
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
</style>
<div id="esfera" class="esfera"></div>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE MANDO ---
# Obtenemos hora y fecha real
ahora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

if prompt := st.chat_input(f"¿Qué orden tienes para mí, {st.session_state.nombre}?"):
    # Activamos la animación de la esfera
    st.components.v1.html("<script>document.getElementById('esfera').className = 'esfera hablando';</script>", height=0)
    
    if "abre" in prompt.lower():
        try:
            requests.get(URL_MACRODROID, timeout=5)
            res = f"Ejecutando comando, {st.session_state.nombre}."
        except:
            res = "Falla de conexión."
    else:
        # Le damos consciencia de tiempo en la instrucción
        instruccion = f"Eres Dex, creado por {st.session_state.nombre}. Hoy es {ahora}. Si te preguntan la hora o el día, usa esta referencia exacta: {ahora}."
        
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": instruccion},
                {"role": "user", "content": prompt}
            ], 
            model="llama-3.1-8b-instant"
        )
        res = response.choices[0].message.content
        st.write(f"Dex: {res}")

    # --- 4. VOZ Y PARADA DE ANIMACIÓN ---
    st.components.v1.html(f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{res.replace('"', '')}");
        msg.lang = 'es-ES';
        msg.onend = function() {{ document.getElementById('esfera').className = 'esfera'; }};
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
