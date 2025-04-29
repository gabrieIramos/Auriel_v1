from flask import Flask, render_template, request, redirect, url_for
from sourcedados import DadosAcoes  # Importa a classe DadosAcoes do arquivo sourcedados.py

app = Flask(__name__)
conversa = []  # Armazena as mensagens da conversa

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mensagem = request.form.get('mensagem')
        if mensagem:
            conversa.append(f"Você: {mensagem}")
            resposta = DadosAcoes.obter_dados_acoes('AAPL', '2018-01-01', '2023-01-01')  # Chama a função para obter dados de ações
            
            conversa.append(resposta)
        return redirect(url_for('index'))
    return render_template('chat.html', conversa=conversa)

if __name__ == '__main__':
    app.run(debug=True)
