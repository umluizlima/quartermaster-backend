from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """Handle error response."""
    payload = {
        'error': HTTP_STATUS_CODES.get(status_code,
                                       'Unknown error')
    }
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """Return a JSON message with code 400."""
    return error_response(400, message)


def unauthorized(message):
    """Return a JSON message with code 403."""
    return error_response(403, message)


def not_found(message):
    """Return JSON message with code 404."""
    return error_response(404, message)
