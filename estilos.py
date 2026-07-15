def obtener_estilo_visual():
    return """
    <style>
        /* Fondo oscuro tipo Centro de Mando */
        .stApp { background-color: #0a0a0a; color: #00ffcc; }
        
        /* Animación de carga tipo Jarvis */
        .chat-container { border: 1px solid #00ffcc; padding: 20px; border-radius: 10px; }
        
        /* Efecto de pulso cuando habla */
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        .hablando { animation: pulse 1.5s infinite; }
    </style>
    """
