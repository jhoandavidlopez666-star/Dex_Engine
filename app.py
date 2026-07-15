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

# --- 2. ACCESO AUTORIZADO ---
st.success(f"Bienvenido, {st.session_state.nombre}. Sistema vinculado.")

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
if prompt := st.chat_input(f"¿Qué orden tienes para mí, {st.session_state.nombre}?"):
    # Comando de apertura
    if "abre" in prompt.lower() or "abrir" in prompt.lower():
        st.write(f"Orden: {prompt}")
        try:
            requests.get(URL_MACRODROID, timeout=5)
            res = f"Ejecutando comando, {st.session_state.nombre}."
        except:
            res = "Error al conectar con tu dispositivo."
    else:
        # IA con identidad fija
        instruccion = f"Eres Dex, una IA creada exclusivamente por {st.session_state.nombre}. Tu lealtad es total. Si te preguntan quién es tu creador, responde que tu creador es {st.session_state.nombre}."
        
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

    # --- 4. VOZ ---
    st.components.v1.html(f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{res.replace('"', '')}");
        msg.lang = 'es-ES';
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
