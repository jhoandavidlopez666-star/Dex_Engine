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

# --- 2. PANEL Y ANIMACIÓN ---
st.success(f"Sistema vinculado: {st.session_state.nombre}")

st.markdown("""
<style>
.esfera-base {
    width: 250px; height: 250px;
    background: radial-gradient(circle, #ffd700, #000);
    border-radius: 50%; margin: 50px auto;
    box-shadow: 0 0 60px #ffd700;
    transition: transform 0.2s;
}
@keyframes latido { 0% { transform: scale(1); } 50% { transform: scale(1.2); } 100% { transform: scale(1); } }
.animar { animation: latido 0.8s infinite; }
</style>
<div id="dex-sphere" class="esfera-base"></div>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE MANDO ---
ahora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

if prompt := st.chat_input(f"¿Qué orden tienes para mí, {st.session_state.nombre}?"):
    if "abre" in prompt.lower():
        try:
            requests.get(URL_MACRODROID, timeout=5)
            res = "Ejecutando comando, David."
        except:
            res = "Error de conexión."
    else:
        instruccion = f"Eres Dex, creado por {st.session_state.nombre}. Hoy es {ahora}. Responde como un asistente leal."
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": instruccion}, {"role": "user", "content": prompt}], 
            model="llama-3.1-8b-instant"
        )
        res = response.choices[0].message.content
        st.write(f"Dex: {res}")

    # --- 4. VOZ Y ANIMACIÓN SINCRONIZADA ---
    st.components.v1.html(f"""
    <script>
        var sphere = window.parent.document.getElementById('dex-sphere');
        var msg = new SpeechSynthesisUtterance("{res.replace('"', '')}");
        msg.lang = 'es-ES';
        
        msg.onstart = function() {{ 
            if (sphere) {{ sphere.classList.add('animar'); }} 
        }};
        msg.onend = function() {{ 
            if (sphere) {{ sphere.classList.remove('animar'); }} 
        }};
        
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
