from flask import Blueprint, request, jsonify
from app.db_config import db_reservas, db_pousadas, Reserva, Pousada
from tinydb import Query

reserva_bp = Blueprint('reserva', __name__)

@reserva_bp.route('/reservar_pousada', methods=['POST'])
def reservar_pousada():
    cpf_cnpj = request.form.get('cpf_cnpj')
    pousada_id = request.form.get('pousada_id')
    data_fim = request.form.get('data_fim')

    if cpf_cnpj and pousada_id:
        reservas = db_reservas.search(Reserva.pousada_id == pousada_id)
        if reservas:
            return jsonify({'message': 'Pousada já reservada!'}), 400

        db_reservas.insert({'cpf_cnpj': cpf_cnpj, 'pousada_id': pousada_id, 'data_fim': data_fim})
        db_pousadas.update({'status': 'reservada'}, Pousada.id == pousada_id)
        return jsonify({'message': 'Reserva feita com sucesso!'}), 200
    return jsonify({'message': 'Falha ao reservar pousada! Campos vazios.'}), 400

@reserva_bp.route('/listar_reservas', methods=['GET'])
def listar_reservas():
    reservas = db_reservas.search(Reserva.pousada_id.exists())
    return jsonify(reservas), 200

@reserva_bp.route('/editar_reserva', methods=['POST'])
def editar_reserva():
    cpf_cnpj = request.form.get('cpf_cnpj')
    pousada_id = request.form.get('pousada_id')
    data_fim = request.form.get('data_fim')

    if cpf_cnpj and pousada_id:
        result = db_reservas.update(
            {'data_fim': data_fim},
            (Reserva.cpf_cnpj == cpf_cnpj) & (Reserva.pousada_id == pousada_id)
        )

        if result:
            return jsonify({'message': 'Reserva atualizada com sucesso!'}), 200
        else:
            return jsonify({'message': 'Reserva não encontrada!'}), 404

    return jsonify({'message': 'Falha ao atualizar reserva! Campos vazios.'}), 400

@reserva_bp.route('/remover_reserva', methods=['POST'])
def remover_reserva():
    cpf_cnpj = request.form.get('cpf_cnpj')
    pousada_id = request.form.get('pousada_id')

    if cpf_cnpj and pousada_id:
        db_reservas.remove((Reserva.cpf_cnpj == cpf_cnpj) & (Reserva.pousada_id == pousada_id))
        db_pousadas.update({'status': 'livre'}, Pousada.id == pousada_id)
        return jsonify({'message': 'Reserva removida com sucesso!'}), 200
    return jsonify({'message': 'Falha ao remover reserva! Campos vazios.'}), 400
