from datetime import datetime as dt
from flask import (
    jsonify, request
)
from app.models import (
    db, Reservation, User, Thirdparty
)
from app.api.errors import (
    bad_request, internal_server, not_found
)
from app.api import api
from app.api.controllers.auth import token_required


@api.route('/reservations', methods=['POST'])
@token_required
def create_reservation():
    data = request.get_json() or {}

    error = Reservation.check_data(data=data, new=True)
    if 'user_id' in data and data['user_id'] is not None and \
            User.query.get(data['user_id']) is None:
        error = 'usuário não existe'
    if 'thirdparty_id' in data and data['thirdparty_id'] is not None and \
            Thirdparty.query.get(data['thirdparty_id']) is None:
        error = 'terceiro não existe'
    if Reservation.query.filter(
                Reservation.date_start >= data['date_start']
            ).filter(
                Reservation.date_start <= data['date_end']
            ).all() or Reservation.query.filter(
                Reservation.date_end >= data['date_start']
            ).filter(
                Reservation.date_end <= data['date_end']
            ).all():
        error = 'já existe um evento nesse período'

    if error:
        return bad_request(error)

    reservation = Reservation()
    reservation.from_dict(data)

    try:
        db.session.add(reservation)
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(reservation.to_dict()), 201


@api.route('/reservations', methods=['GET'])
def get_open_reservations():
    return jsonify(
        [reservation.to_dict() for reservation
            in Reservation.query.filter(Reservation.date_end >= dt.utcnow())]
    )


@api.route('/reservations/all', methods=['GET'])
def get_all_reservations():
    return jsonify(
        [reservation.to_dict() for reservation in Reservation.query.all()]
    )


@api.route('/reservations/<int:id>', methods=['GET'])
@token_required
def get_reservation(id: int):
    reservation = Reservation.query.filter_by(id=id).first()
    if reservation is None:
        return not_found('reserva não encontrada')
    return jsonify(reservation.to_dict())


@api.route('/reservations/<int:id>', methods=['PUT'])
@token_required
def update_reservation(id: int):
    reservation = Reservation.query.filter_by(id=id).first()
    if reservation is None:
        return not_found('reserva não encontrada')

    data = request.get_json() or {}

    error = Reservation.check_data(data=data)
    if 'user_id' in data and data['user_id'] is not None and \
            User.query.get(data['user_id']) is None:
        error = 'usuário não existe'
    if 'thirdparty_id' in data and data['thirdparty_id'] is not None and \
            Thirdparty.query.get(data['thirdparty_id']) is None:
        error = 'terceiro não existe'
    if Reservation.query.filter(
                Reservation.date_start >= data['date_start']
            ).filter(
                Reservation.date_start <= data['date_end']
            ).all() or Reservation.query.filter(
                Reservation.date_end >= data['date_start']
            ).filter(
                Reservation.date_end <= data['date_end']
            ).all():
        error = 'já existe um evento nesse período'

    if error:
        return bad_request(error)

    reservation.from_dict(data)
    try:
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(reservation.to_dict())


@api.route('/reservations/<int:id>', methods=['DELETE'])
@token_required
def delete_reservation(id: int):
    reservation = Reservation.query.filter_by(id=id).first()
    if reservation is None:
        return not_found('reserva não encontrada')

    try:
        db.session.delete(reservation)
        db.session.commit()
    except Exception:
        return internal_server()

    return '', 204
