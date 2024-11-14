from flask import Blueprint, request, jsonify
from app.db_config import db_pousadas, Pousada
from tinydb import Query

pousada_bp = Blueprint('pousada', __name__)

@pousada_bp.route('/cadastrar_pousada', methods=['POST'])
def cadastrar_pousada():
    nome = request.form.get('nome')
    pousada_id = request.form.get('id_pousada')
    valor = request.form.get('valor')

    if nome and pousada_id and valor:
        db_pousadas.insert({
            'nome': nome,
            'id': pousada_id,
            'valor': valor,
            'status': 'livre'
        })
        return jsonify({'message': 'Pousada cadastrada com sucesso!'}), 200
    return jsonify({'message': 'Falha ao cadastrar pousada! Campos vazios.'}), 400

@pousada_bp.route('/listar_pousadas', methods=['GET'])
def listar_pousadas():
    pousadas = db_pousadas.search(Pousada.id.exists())
    return jsonify(pousadas), 200

@pousada_bp.route('/editar_pousada', methods=['POST'])
def editar_pousada():
    pousada_id = request.form.get('id_pousada')
    nome = request.form.get('nome')
    valor = request.form.get('valor')
    status = request.form.get('status')

    if pousada_id:
        db_pousadas.update({
            'nome': nome,
            'valor': valor,
            'status': status
        }, Pousada.id == pousada_id)
        return jsonify({'message': 'Pousada atualizada com sucesso!'}), 200
    return jsonify({'message': 'Pousada não encontrada!'}), 404

@pousada_bp.route('/remover_pousada', methods=['POST'])
def remover_pousada():
    pousada_id = request.form.get('id_pousada')

    if pousada_id:
        db_pousadas.remove(Pousada.id == pousada_id)
        return jsonify({'message': 'Pousada removida com sucesso!'}), 200
    return jsonify({'message': 'Falha ao remover pousada! Campos vazios.'}), 400
