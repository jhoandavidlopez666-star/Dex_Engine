import streamlit as st
from groq import Groq
import autenticador

# 1. Seguridad
autenticador.verificar_patron_vocal()

# 2. Configuración del Cliente
# Asegúrate de que tu secreto GROQ_API_KEY esté configurado en Streamlit
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("Error: La API KEY no está configurada en los secretos de la aplicación.")
else:
    client = Groq(api_key=api_key)

    st.title("Centro de Mando: Dex (Diagnóstico)")

    # 3. Entrada de prueba
    if prompt := st.chat_input("Escribe una orden de prueba:"):
        st.write(f"David envió: {prompt}")
        
        try:
            # Llamada directa al modelo
            with st.spinner("Conectando con el núcleo..."):
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Eres Dex, creado por David López."},
                        {"role": "user", "content": prompt}
                    ], 
                    model="llama-3.1-8b-instant"
                )
                
                respuesta_dex = response.choices[0].message.content
                st.success(f"Dex responde: {respuesta_dex}")
                
        except Exception as e:
            st.error(f"Error detectado en la conexión: {e}")
