from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def build_error_response(status_code, message=None):
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
    return build_error_response(400, message)


def unauthorized(message):
    return build_error_response(403, message)


def not_found(message):
    return build_error_response(404, message)


def internal_server():
    message = "The server encountered an internal \
error and was unable to complete your request."
    return build_error_response(500, message)
