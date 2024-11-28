from flask import Flask, Blueprint, request, jsonify, render_template
from tinydb import TinyDB, Query


app = Flask(__name__)


reserva_bp = Blueprint('reserva', __name__)


db_pousadas = TinyDB('pousada.json')
db_reservas = TinyDB('reservas.json')
Pousada = Query()
Reserva = Query()


@reserva_bp.route('/cadastrar_pousada', methods=['POST'])
def cadastrar_pousada():
    data = request.get_json()
    id_pousada, nome, valor = data.get('id_pousada'), data.get('nome'), data.get('valor')

    if id_pousada and nome and valor:
        if db_pousadas.contains(Pousada.id == id_pousada):
            return jsonify({'message': 'ID já cadastrado!'}), 400
        db_pousadas.insert({'id': id_pousada, 'nome': nome, 'valor': valor})
        return jsonify({'message': 'Pousada cadastrada com sucesso!'}), 200
    return jsonify({'message': 'Campos vazios não são permitidos!'}), 400


@reserva_bp.route('/listar_pousadas', methods=['GET'])
def listar_pousadas():
    return jsonify(db_pousadas.all()), 200


@reserva_bp.route('/buscar_pousada_preco', methods=['GET'])
def buscar_pousada_preco():
    pousada_id = request.args.get('pousada_id')
    pousada = db_pousadas.get(Pousada.id == pousada_id)
    
    if pousada:
        return jsonify(success=True, nome=pousada['nome'], valor=pousada['valor'])
    else:
        return jsonify(success=False, message='Pousada não encontrada'), 404


@reserva_bp.route('/reservar_pousada', methods=['POST'])
def reservar_pousada():
    data = request.get_json()
    nomeCompleto = data.get('nomeCompleto')
    cpf = data.get('cpf')
    pousadaId = data.get('pousadaId')
    diaCheckin = data.get('diaCheckin')
    diaCheckout = data.get('diaCheckout')
    quantidade = data.get('quantidade')
    valor = data.get('valor')
    metodoPagamento = data.get('metodoPagamento')

    if nomeCompleto and cpf and pousadaId and diaCheckin and diaCheckout and quantidade and valor and metodoPagamento:
        db_reservas.insert(data)
        return jsonify({'success': True, 'message': 'Reserva incluída com sucesso!'}), 200
    return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios!'}), 400


@reserva_bp.route('/listar_reservas', methods=['GET'])
def listar_reservas():
    return jsonify(db_reservas.all()), 200


@reserva_bp.route('/editar_reserva', methods=['POST'])
def editar_reserva():
    data = request.get_json()
    print(data) 
    cpf = data.get('cpf')
    pousadaId = data.get('pousadaId')
    nomeCompleto = data.get('nomeCompleto')
    diaCheckin = data.get('diaCheckin')
    diaCheckout = data.get('diaCheckout')
    quantidade = data.get('quantidade')
    valor = data.get('valor')
    metodoPagamento = data.get('metodoPagamento')

    if cpf and pousadaId and nomeCompleto and diaCheckin and diaCheckout and quantidade and valor and metodoPagamento:
        db_reservas.update({'pousadaId': pousadaId, 'nomeCompleto': nomeCompleto, 'diaCheckin': diaCheckin, 'diaCheckout': diaCheckout, 'quantidade': quantidade, 'valor': valor, 'metodoPagamento': metodoPagamento}, Reserva.cpf == cpf)
        return jsonify({'success': True, 'message': 'Reserva editada com sucesso!'}), 200
    return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios!'}), 400


@reserva_bp.route('/remover_reserva', methods=['POST'])
def remover_reserva():
    data = request.get_json()
    pousada_id = data.get('pousada_id')

    if db_reservas.remove(Reserva.pousadaId == pousada_id):
        return jsonify({'success': True, 'message': 'Reserva removida com sucesso!'}), 200
    return jsonify({'success': False, 'message': 'Reserva não encontrada!'}), 404

@reserva_bp.route('/dashboard', methods=['GET'])
def dashboard():
    pousadas = db_pousadas.all()
    reservas = db_reservas.all()

    total_pousadas = len(pousadas)
    total_reservas = len(reservas)

    
    total_hospedes = sum(int(reserva['quantidade']) for reserva in reservas if isinstance(reserva['quantidade'], int) or reserva['quantidade'].isdigit())
    media_hospedes_por_reserva = total_hospedes / total_reservas if total_reservas > 0 else 0
    valor_total_arrecadado = sum(float(reserva['valor']) for reserva in reservas if isinstance(reserva['valor'], (int, float)) or reserva['valor'].replace('.', '', 1).isdigit())

    
    pousada_reserva_contagem = {}
    for reserva in reservas:
        pousada_id = reserva['pousadaId']
        if pousada_id in pousada_reserva_contagem:
            pousada_reserva_contagem[pousada_id] += 1
        else:
            pousada_reserva_contagem[pousada_id] = 1
    pousada_mais_popular = max(pousada_reserva_contagem, key=pousada_reserva_contagem.get) if pousada_reserva_contagem else None
    nome_pousada_mais_popular = next((p['nome'] for p in pousadas if p['id'] == pousada_mais_popular), "N/A")

    return render_template('dashboard.html', 
                           total_pousadas=total_pousadas,
                           total_reservas=total_reservas,
                           total_hospedes=total_hospedes,
                           media_hospedes_por_reserva=media_hospedes_por_reserva,
                           valor_total_arrecadado=valor_total_arrecadado,
                           nome_pousada_mais_popular=nome_pousada_mais_popular)


app.register_blueprint(reserva_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)










