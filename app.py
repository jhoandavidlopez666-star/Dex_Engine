import streamlit as st
from groq import Groq

# Título de la aplicación
st.title("Dex Engine: Centro de Mando")

# 1. Caja para la API Key (esto es seguro, se oculta mientras escribes)
api_key = st.text_input("Ingresa tu API Key de Groq", type="password")

# Solo ejecutamos el resto si se ha introducido una API Key
if api_key:
    try:
        client = Groq(api_key=api_key)
        
        # 2. Caja para el input del usuario
        user_input = st.text_input("¿Qué tarea quieres que ejecute Dex?")
        
        # 3. La lógica solo corre cuando escribes una tarea y presionas Enter
        if user_input:
            with st.spinner('Ejecutando...'):
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": user_input}],
                    model="llama3-8b-8192",
                )
                # Mostramos la respuesta
                st.subheader("Respuesta de Dex:")
                st.write(chat_completion.choices[0].message.content)
    except Exception as e:
        st.error(f"Error: {e}. Revisa que tu API Key sea correcta.")
else:
    st.info("Por favor, ingresa tu API Key para empezar.")
