from flask import make_response


def _build_cors_preflight_response():
    '''Add headers to preflight response'''

    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    '''Add headers to actual response'''

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
