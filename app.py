from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
conversa = []  # Armazena as mensagens da conversa

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mensagem = request.form.get('mensagem')
        if mensagem:
            conversa.append(f"Você: {mensagem}")
            resposta = f"Bot: Eu recebi sua mensagem: '{mensagem}'"
            conversa.append(resposta)
        return redirect(url_for('index'))
    return render_template('chat.html', conversa=conversa)

if __name__ == '__main__':
    app.run(debug=True)
