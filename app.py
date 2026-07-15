import streamlit as st
import requests
from groq import Groq
from datetime import datetime

# --- CONFIGURACIÓN ---
URL_MACRODROID = "https://trigger.macrodroid.com/c5b99e55-87f6-4b97-a4bd-82fab9fac120/dex_comando"
CODIGO_DAVID = "BELQUARIEL-17"
# REEMPLAZA ESTO CON LA URL DE TU IMAGEN SUBIDA A GITHUB
URL_IMAGEN_DEX = "URL_DE_TU_IMAGEN_AQUI" 

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

# --- 2. PANEL Y ANIMACIÓN DE MENTE ACTIVA ---
st.success(f"Sistema vinculado: {st.session_state.nombre}")

st.markdown(f"""
<style>
.cabeza-dex {{
    width: 300px; height: 400px;
    background-image: url('{URL_IMAGEN_DEX}');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    margin: 50px auto;
    transition: transform 0.3s;
}}
@keyframes latido {{ 
    0% {{ transform: scale(1); filter: brightness(1); }} 
    50% {{ transform: scale(1.05); filter: brightness(1.5); }} 
    100% {{ transform: scale(1); filter: brightness(1); }} 
}}
.animar {{ animation: latido 0.8s infinite; }}
</style>
<div id="dex-sphere" class="cabeza-dex"></div>
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
        instruccion = f"Eres Dex, creado por {st.session_state.nombre}. Hoy es {ahora}. Responde con la precisión de una mente superior."
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
        var head = window.parent.document.getElementById('dex-sphere');
        var msg = new SpeechSynthesisUtterance("{res.replace('"', '')}");
        msg.lang = 'es-ES';
        
        msg.onstart = function() {{ 
            if (head) {{ head.classList.add('animar'); }} 
        }};
        msg.onend = function() {{ 
            if (head) {{ head.classList.remove('animar'); }} 
        }};
        
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
