import streamlit as st
import requests
from groq import Groq

# --- CONFIGURACIÓN ---
URL_MACRODROID = "https://trigger.macrodroid.com/c5b99e55-87f6-4b97-a4bd-82fab9fac120/dex_comando"
CODIGO_DAVID = "BELQUARIEL-17"

st.title("Centro de Mando: Dex")

# --- 1. AUTENTICACIÓN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    clave = st.text_input("Ingresa tu Código de Identidad:", type="password")
    if st.button("Verificar"):
        if clave == CODIGO_DAVID:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Acceso denegado. Código incorrecto.")
    st.stop()

# --- 2. ACCESO CONCEDIDO (DAVID LÓPEZ) ---
st.success("Acceso Autorizado: David López")
st.markdown("""
<style>
.esfera {
    width: 250px; height: 250px;
    background: radial-gradient(circle, #ffd700, #000);
    border-radius: 50%; margin: 50px auto;
    box-shadow: 0 0 60px #ffd700;
}
</style>
<div class="esfera"></div>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE MANDO ---
if prompt := st.chat_input("Dime tu orden, David..."):
    # Comando de apertura
    if "abre" in prompt.lower() or "abrir" in prompt.lower():
        st.write(f"Orden recibida: {prompt}")
        try:
            requests.get(URL_MACRODROID, timeout=5)
            res = "Comando ejecutado, David López."
        except:
            res = "Error de conexión con el móvil."
    else:
        # IA Estratégica
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
        response = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.1-8b-instant")
        res = response.choices[0].message.content
        st.write(f"Dex: {res}")

    # --- 4. VOZ FORZADA ---
    st.components.v1.html(f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{res.replace('"', '')}");
        msg.lang = 'es-ES';
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
