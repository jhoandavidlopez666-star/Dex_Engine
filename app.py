# Interacción
if prompt := st.chat_input("¿Cuáles son tus órdenes, David?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream((chunk.choices[0].delta.content or "" for chunk in stream))
    st.session_state.messages.append({"role": "assistant", "content": response})
