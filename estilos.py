def obtener_estilo_visual():
    return """
    <style>
        /* Fondo negro absoluto para toda la página */
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
        }
        
        /* Asegurar que el área principal también sea negra */
        .stApp {
            background-color: #000000;
        }

        /* Título con estilo neón */
        h1 {
            color: #00ffcc !important;
            text-shadow: 0 0 10px #00ffcc;
        }

        /* Chat con bordes definidos */
        [data-testid="stChatInput"] {
            background-color: #1a1a1a;
        }
        
        /* Ajuste de burbujas de chat */
        [data-testid="stChatMessage"] {
            background-color: #1a1a1a !important;
            border: 1px solid #333;
        }
    </style>
    """
