from flask import abort, jsonify, make_response


def abort_response(data, code):
    abort(make_response(jsonify(data), code))


def abort_unauthorized(sms='UNAUTHORIZED', **kwargs):
    abort_response({
        "message": sms,
        **kwargs
    }, 401)


def abort_not_found(sms='NOT FOUND', **kwargs):
    abort_response({
        "message": sms,
        **kwargs
    }, 404)


def abort_bad_request(sms='BAD REQUEST', **kwargs):
    abort_response({
        "message": sms,
        **kwargs
    }, 400)


def abort_validation(sms='VALIDATION ERROR', **kwargs):
    abort_response({
        "message": sms,
        **kwargs
    }, 422)
