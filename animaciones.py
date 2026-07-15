def obtener_css_animacion():
    return """
    <style>
        /* Pulso imponente y brillante */
        .pulso {
            width: 25px; 
            height: 25px;
            background: #00ffcc;
            border-radius: 50%;
            box-shadow: 0 0 20px #00ffcc, 0 0 40px #00ffcc; /* Halo brillante */
            animation: pulse-animation 2s infinite;
            display: inline-block;
            margin-right: 15px;
            margin-top: 10px;
        }
        @keyframes pulse-animation {
            0% { transform: scale(1); box-shadow: 0 0 10px #00ffcc; }
            50% { transform: scale(1.5); box-shadow: 0 0 30px #00ffcc; }
            100% { transform: scale(1); box-shadow: 0 0 10px #00ffcc; }
        }
    </style>
    """
