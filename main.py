from flask import Flask, session, redirect, url_for, render_template, request, jsonify
from flask_cors import CORS
from app.db_config import db_funcionarios, Funcionario, db_reservas, db_clientes, db_pousadas
from werkzeug.security import generate_password_hash, check_password_hash
from app.cliente import cliente_bp
from app.pousada import pousada_bp
from app.reserva import reserva_bp
from tinydb import Query

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Ativar CORS para todas as rotas
CORS(app)

# Registra os Blueprints
app.register_blueprint(cliente_bp)
app.register_blueprint(pousada_bp)
app.register_blueprint(reserva_bp)

# Rota de login
@app.route('/')
def login():
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

# Rota para processar o login
@app.route('/login', methods=['POST'])
def login_post():
    cpf_cnpj = request.form.get('cpf_cnpj')
    senha = request.form.get('senha')
    
    funcionario = db_funcionarios.search(Funcionario.cpf_cnpj == cpf_cnpj)
    if funcionario and check_password_hash(funcionario[0]['senha'], senha):
        session['user'] = funcionario[0]['cpf_cnpj']
        return redirect(url_for('index'))
    else:
        return jsonify({'message': 'Falha no login! Verifique suas credenciais.'})

# Rota para o menu principal (index.html)
@app.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])

# Rota para a página de gerenciamento de clientes
@app.route('/clientes')
def clientes():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('clientes.html')

# Rota para a página de gerenciamento de pousadas
@app.route('/pousadas')
def pousadas():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('pousadas.html')

# Rota para a página de reserva de pousada
@app.route('/reservas')
def reservas():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('reservas.html')

# Rota para o chat
@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

# Rota para listar todas as reservas
@app.route('/listar_reservas', methods=['GET'])
def listar_reservas():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    Reserva = Query()
    reservas = db_reservas.search(Reserva.pousada_id.exists())
    return jsonify(reservas), 200

# Rota para fornecer dados de contexto para o chatbot
@app.route('/context_data', methods=['GET'])
def get_context_data():
    reservas = db_reservas.all()
    clientes = db_clientes.all()
    pousadas = db_pousadas.all()

    context = {
        "reservas": reservas,
        "clientes": clientes,
        "pousadas": pousadas
    }
    return jsonify(context)

# Rota para receber a mensagem do chatbot e responder
@app.route('/ia', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    user_message = data.get("text", "")
    
    # Processamento básico de resposta (exemplo simplificado)
    response_text = f"Resposta para: {user_message}"
    
    # Retorna a resposta como JSON
    return jsonify({"response": response_text})

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
