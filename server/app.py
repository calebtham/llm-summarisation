from flask import Flask, jsonify, request
from util.cors import _build_cors_preflight_response, _corsify_actual_response
from service.summarise import summarise


app = Flask(__name__)


@app.route('/summarise', methods=['POST', 'OPTIONS'])
def summarise_api():
    '''Services a POST request to summarise a given text'''

    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()

    text = request.get_json()['text']
    summary = summarise(text)
    response = jsonify({'summary': summary})

    return _corsify_actual_response(response)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
