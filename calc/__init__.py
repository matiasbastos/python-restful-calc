from flask import Flask, jsonify
from calc.models import db
from calc.controllers.main import main


def create_app(object_name, env="prod"):
    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env
    
    # define custom errors
    @app.errorhandler(400)
    def custom_error_400(error):
        response = jsonify({'message': error.description})
        response.status_code = 400
        return response

    @app.errorhandler(500)
    def custom_error_500(error):
        response = jsonify({'message': error.description})
        response.status_code = 500
        return response

    # initialize SQLAlchemy
    db.init_app(app)

    # register our blueprints
    app.register_blueprint(main)

    return app

