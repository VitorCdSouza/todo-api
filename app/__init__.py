from flask import Flask, jsonify
from flask_cors import CORS
from app.routes import todos
from app.config import Config


# starting app with CORS
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # handling OPTIONS for Cross Origin
    @app.route('/todos', methods=['OPTIONS'])
    def handle_preflight():
        response = jsonify({"message": "Preflight OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        return response

    app.register_blueprint(todos.bp)

    return app
