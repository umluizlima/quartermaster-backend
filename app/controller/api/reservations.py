"""Reservations API.

This module maps the API endpoints for the Reservation data model, implementing
the POST, GET, PUT and DELETE http methods for its CRUD operations,
respectively.

Endpoints
    GET - /reservations - return the collection of all reservations.
    GET - /reservations/<id> - return a reservation with given id number.
    POST - /reservations - register a new reservation.
    PUT - /reservations/<id> - modify a reservation with given id number.
    DELETE - /reservations/<id> - remove a reservation with id number.

"""
from flask import (
    jsonify, request)

from app.model import db, Reservation
from app.controller.api.errors import bad_request, not_found
from app.controller.api import bp


# Create
@bp.route('/reservations', methods=['POST'])
def create_reservation():
    """Create new reservation."""
    data = request.get_json() or {}

    error = Reservation.check_data(data=data, new=True)
    if error:
        return bad_request(error)

    # Create new instance and commit to database.
    reservation = Reservation()
    reservation.from_dict(data)
    db.session.add(reservation)
    db.session.commit()
    return jsonify(reservation.to_dict()), 201


# Read
@bp.route('/reservations', methods=['GET'])
def get_reservations():
    """Return list of reservations."""
    return jsonify(
        [reservation.to_dict() for reservation in Reservation.query.all()])


# Read
@bp.route('/reservations/<int:id>', methods=['GET'])
def get_reservation(id: int):
    """Return reservation with given id."""
    reservation = Reservation.query.filter_by(id=id).first()
    if reservation is None:
        return not_found('reservation not found')
    return jsonify(reservation.to_dict())


@bp.route('/reservations/<int:id>', methods=['PUT'])
def update_reservation(id: int):
    """Update given reservation, if exists."""
    reservation = Reservation.query.filter_by(id=id).first()
    if reservation is None:
        return not_found('reservation not found')

    data = request.get_json() or {}

    error = Reservation.check_data(data=data)
    if error:
        return bad_request(error)

    # Check for unique key compliance
    # if 'name' in data and data['name'] != reservation.name and \
    #         Reservation.query.filter_by(name=data['name']).first() is not None:
    #     return bad_request('please use a different name')

    reservation.from_dict(data)
    db.session.commit()
    return jsonify(reservation.to_dict())


# Delete
@bp.route('/reservations/<int:id>', methods=['DELETE'])
def delete_reservation(id: int):
    """Delete given reservation, if exists."""
    reservation = Reservation.query.filter_by(id=id).first()
    if reservation is None:
        return not_found('reservation not found')

    db.session.delete(reservation)
    db.session.commit()
    return '', 204
