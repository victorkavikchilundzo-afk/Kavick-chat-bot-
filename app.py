from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

CHAVE = os.environ.get("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Kavick Chat Bot</title>
</head>
<body>

<h1>KAVICK CHAT BOT</h1>
<p>Assistente Inteligente com IA Generativa</p>

<form method="POST">
    <textarea name="pergunta"
    placeholder="Digite a sua pergunta..."
    rows="5"
    style="width:90%;"></textarea>

    <br><br>
    <button type="submit">Perguntar</button>
</form>

{% if resposta %}
<h2>Resposta:</h2>
<div style="white-space: pre-wrap;">{{ resposta }}</div>
{% endif %}

</body>
</html>
"""

def perguntar_ia(pergunta):

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
