from flask import Flask
from calc.models import db
from calc.controllers.main import main


def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/
    Arguments:
        object_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig
        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    # initialize SQLAlchemy
    db.init_app(app)

    # register our blueprints
    app.register_blueprint(main)

    return app
