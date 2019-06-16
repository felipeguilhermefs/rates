from flask import Flask, jsonify

from .api_exception import InvalidQueryParam

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.errorhandler(InvalidQueryParam)
    def handle_invalid_query_param(error):
        response = jsonify({'message': error.message})
        response.status_code = 400
        return response

    return app
