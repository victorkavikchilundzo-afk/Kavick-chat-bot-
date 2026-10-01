from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

CHAVE = os.environ.get("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

HTML = """
<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Kavick Chat Bot</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    min-height: 100vh;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.container {
    width: 100%;
    max-width: 650px;
    background: rgba(255,255,255,0.10);
    backdrop-filter: blur(12px);
    border-radius: 25px;
    padding: 30px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.35);
}

.logo {
    width: 150px;
    height: 150px;
    object-fit: contain;
    display: block;
    margin: 0 auto 15px;
}
    width: 70px;
    height: 70px;
    background: white;
    color: #1e3a8a;
    border-radius: 50%;
    margin: 0 auto 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: bold;
}

h1 {
    text-align: center;
    margin: 5px 0;
    font-size: 30px;
}

.subtitle {
    text-align: center;
    opacity: 0.8;
    margin-bottom: 25px;
}

textarea {
    width: 100%;
    min-height: 130px;
    border: none;
    border-radius: 15px;
    padding: 15px;
    font-size: 16px;
    resize: vertical;
    outline: none;
}

button {
    width: 100%;
    margin-top: 15px;
    padding: 15px;
    border: none;
    border-radius: 15px;
    background: white;
    color: #1e3a8a;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    transform: scale(1.02);
}

.answer {
    margin-top: 25px;
    background: rgba(0,0,0,0.25);
    padding: 20px;
    border-radius: 15px;
    line-height: 1.6;
    white-space: pre-wrap;
}

.footer {
    text-align: center;
    margin-top: 20px;
    font-size: 13px;
    opacity: 0.65;
}
</style>
</head>

<body>

<div class="container">

<img src="https://raw.githubusercontent.com/victorkavikchilundzo-afk/Kavick-chat-bot-/main/file_00000000fc9c824684030973344a89d3.png" class="logo">

<h1>KAVICK CHAT BOT</h1>

<div class="subtitle">
Assistente Inteligente com IA Generativa
</div>

<form method="POST">

<textarea
name="pergunta"
placeholder="Digite a sua pergunta..."
required></textarea>

<button type="submit">
🤖 Perguntar à IA
</button>

</form>

{% if resposta %}

<div class="answer">
<strong>🤖 Kavick Chat Bot:</strong>

<br><br>

{{ resposta }}

</div>

{% endif %}

<div class="footer">
Projeto escolar • IA Generativa • Python • Robótica
</div>

</div>

</body>
</html>
"""

def perguntar_ia(pergunta):
    def perguntar_ia(pergunta):
    pergunta_lower = pergunta.lower()

    if "victor kavick" in pergunta_lower:
        return "Sim, conheço Victor Kavick. Victor Kavick é uma pessoa bastante inteligente e focada."

    if not CHAVE:
        return "A chave da IA ainda não foi configurada."

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + CHAVE
    }

    dados = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Seu nome é Kavick Chat Bot. "
                    "Você é um assistente inteligente criado "
                    "para um projeto escolar sobre IA generativa, "
                    "Python e robótica. "
                    "Responda em português de forma simples, "
                    "clara e educativa. "
                    "Não invente estatísticas."
                )
            },
            {
                "role": "user",
                "content": pergunta
            }
        ]
    }

    try:
        resposta = requests.post(
            URL,
            headers=headers,
            json=dados,
            timeout=60
        )

        if resposta.status_code == 200:
            resultado = resposta.json()
            return resultado["choices"][0]["message"]["content"]

        return "Erro da IA: " + str(resposta.status_code)

    except Exception as erro:
        return "Erro de conexão: " + str(erro)


@app.route("/", methods=["GET", "POST"])
def inicio():

    resposta = ""

    if request.method == "POST":

        pergunta = request.form.get("pergunta", "")

        if pergunta:
            resposta = perguntar_ia(pergunta)

    return render_template_string(
        HTML,
        resposta=resposta
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
