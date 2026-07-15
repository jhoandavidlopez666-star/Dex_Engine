import streamlit as st
import textwrap
from gtts import gTTS
import os
import datetime

# --- CONFIGURACIÓN ---
IMAGEN_BASE64 = "data:image/jpeg;base64,AQUÍ_VA_TU_CODIGO_LARGO=="

def hablar(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save("saludo.mp3")
    st.audio("saludo.mp3", format="audio/mp3", autoplay=True)

st.set_page_config(page_title="Centro de Mando: Dex", layout="centered")

# --- ESTADO DE SESIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #FFD700;'>Centro de Mando: Dex</h1>", unsafe_allow_html=True)

if not st.session_state.autenticado:
    codigo = st.text_input("Ingresa tu Código:", type="password")
    if st.button("Verificar"):
        if codigo == "BELQUARIEL-17":
            st.session_state.autenticado = True
            st.rerun()
else:
    # CEREBRO OPERATIVO
    fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
    st.info(f"**Dex:** Sistema operativo en línea. Fecha: {fecha_actual}. Reconociendo a mi creador, David Lopez.")
    
    # VISUALIZACIÓN
    st.markdown(textwrap.dedent(f"""
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <img src="{IMAGEN_BASE64}" style="width: 300px; border-radius: 15px; border: 2px solid #FFD700;">
    </div>
    """), unsafe_allow_html=True)
    
    # MÓDULO DE ACCIÓN
    st.write("---")
    if st.button("Analizar Mercado Ahora"):
        reporte = f"Arquitecto, el mercado hoy {fecha_actual} muestra alta volatilidad. Protocolos de trading para Bitcoin y Solana listos."
        st.success(reporte)
        hablar(reporte)
    
    # CHAT DE COMANDOS
    for msg in st.session_state.mensajes:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Escribe tu comando operativo:"):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        respuesta_dex = f"Comando '{prompt}' registrado. El sistema sigue tus órdenes, Arquitecto."
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta_dex})
        with st.chat_message("assistant"):
            st.markdown(respuesta_dex)
            hablar(respuesta_dex)

    if st.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()
