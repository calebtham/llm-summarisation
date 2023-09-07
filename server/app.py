import os
from flask import Flask, jsonify, request, make_response
from ml.summarise import summarise

app = Flask(__name__)


@app.route('/summarise', methods=['POST', 'OPTIONS'])
def summarise_api():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()

    text = request.get_json()['text']
    summary = summarise(text)

    response = jsonify({'summary': summary})
    return _corsify_actual_response(response)


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    app.run(port=8000, debug=True)
