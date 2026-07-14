import streamlit as st
from groq import Groq

st.title("Dex Engine: Centro de Mando")
api_key = st.text_input("Ingresa tu API Key de Groq", type="password")

if api_key:
    client = Groq(api_key=api_key)
    user_input = st.text_input("¿Qué tarea quieres que ejecute Dex?")
    if user_input:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model="llama3-8b-8192",
        )
        st.write(chat_completion.choices[0].message.content)
