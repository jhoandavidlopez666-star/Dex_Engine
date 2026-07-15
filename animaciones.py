def obtener_css_animacion():
    return """
    <style>
        .esfera-contenedor {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60vh;
            width: 100%;
        }
        .esfera {
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, #00ffcc, #004433);
            border-radius: 50%;
            box-shadow: 0 0 50px #00ffcc, 0 0 100px #004433;
            animation: pulse-esfera 2s infinite ease-in-out;
        }
        @keyframes pulse-esfera {
            0% { transform: scale(1); box-shadow: 0 0 50px #00ffcc; }
            50% { transform: scale(1.2); box-shadow: 0 0 100px #00ffcc; }
            100% { transform: scale(1); box-shadow: 0 0 50px #00ffcc; }
        }
    </style>
    """
