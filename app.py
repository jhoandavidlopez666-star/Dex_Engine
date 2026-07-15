with st.chat_message("assistant"):
        # Esto simplifica el mensaje para que Groq no falle
        stream = client.chat.completions.create(
            messages=[{"role": "system", "content": "Actúa como Dex."}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] != "system"],
            model="llama3-8b-8192",
            stream=True,
        )
        response = st.write_stream(stream)
