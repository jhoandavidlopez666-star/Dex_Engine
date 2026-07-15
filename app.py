import streamlit as st
import requests
from groq import Groq

# 1. Configuración de API
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
URL_MACRODROID = "https://trigger.macrodroid.com/c5b99e55-87f6-4b97-a4bd-82fab9fac120/dex_comando"

st.title("Centro de Mando: Dex")

# 2. Entrada de usuario
if prompt := st.chat_input("Dime tu orden..."):
    # Detectar orden de abrir app
    if "abre" in prompt.lower() or "abrir" in prompt.lower():
        st.write(f"David: {prompt}")
        try:
            # Enviar señal al teléfono
            respuesta = requests.get(URL_MACRODROID, timeout=5)
            if respuesta.status_code == 200:
                st.success("Orden enviada al dispositivo.")
            else:
                st.error(f"Respuesta del servidor: {respuesta.status_code}")
        except Exception as e:
            st.error(f"Error de conexión: {e}")
    
    else:
        # Consulta normal a IA
        st.write(f"David: {prompt}")
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}], 
            model="llama-3.1-8b-instant"
        )
        respuesta_ia = response.choices[0].message.content
        st.write(f"Dex: {respuesta_ia}")
