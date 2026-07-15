def obtener_css_animacion():
    return """
    <style>
        /* Animación de pulso para el Centro de Mando */
        .pulso {
            width: 10px;
            height: 10px;
            background: #00ffcc;
            border-radius: 50%;
            box-shadow: 0 0 10px #00ffcc;
            animation: pulse-animation 2s infinite;
            display: inline-block;
            margin-right: 10px;
        }
        @keyframes pulse-animation {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 204, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
        }
    </style>
    """
