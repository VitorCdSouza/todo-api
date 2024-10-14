from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.routes import todos, users
from app.config import Config
from app.utils import limiter


# starting app with CORS
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    JWTManager(app)
    CORS(app, supports_credentials=True)

    limiter.init_app(app)

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
    app.register_blueprint(users.bp)

    return app
