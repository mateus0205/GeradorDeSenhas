from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

# Função para gerar a senha
def gerar_senha(comprimento, incluir_maiusculas=True, incluir_minusculas=True, incluir_digitos=True, incluir_especiais=True):
    caracteres = ''
    
    if incluir_maiusculas:
        caracteres += string.ascii_uppercase
    if incluir_minusculas:
        caracteres += string.ascii_lowercase
    if incluir_digitos:
        caracteres += string.digits
    if incluir_especiais:
        caracteres += string.punctuation

    if not caracteres:
        raise ValueError("Pelo menos um tipo de caractere deve ser selecionado.")

    # Garantir que a senha tenha pelo menos um caractere de cada tipo selecionado
    senha = []
    if incluir_maiusculas:
        senha.append(random.choice(string.ascii_uppercase))
    if incluir_minusculas:
        senha.append(random.choice(string.ascii_lowercase))
    if incluir_digitos:
        senha.append(random.choice(string.digits))
    if incluir_especiais:
        senha.append(random.choice(string.punctuation))

    # Preencher o restante da senha com caracteres aleatórios
    for _ in range(comprimento - len(senha)):
        senha.append(random.choice(caracteres))

    random.shuffle(senha)  # Embaralhar a senha gerada
    return ''.join(senha)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para gerar a senha
@app.route('/gerar_senha', methods=['POST'])
def gerar():
    try:
        comprimento = int(request.form['comprimento'])
        
        # Verifica se o comprimento é menor que 4
        if comprimento < 4:
            raise ValueError("A senha deve ter no mínimo 4 dígitos.")

        incluir_maiusculas = 'maiusculas' in request.form
        incluir_minusculas = 'minusculas' in request.form
        incluir_digitos = 'digitos' in request.form
        incluir_especiais = 'especiais' in request.form

        senha = gerar_senha(comprimento, incluir_maiusculas, incluir_minusculas, incluir_digitos, incluir_especiais)
        return jsonify({'senha': senha})
    except ValueError as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
