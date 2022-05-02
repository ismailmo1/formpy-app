from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_mgr = LoginManager()
csrf = CSRFProtect()
login_mgr.login_view = "login"


def create_app(config_filepath):
    app = Flask(__name__)

    app.config.from_pyfile(config_filepath)

    from app.blueprints import auth, crud, home, processing
    from app.db import mongo

    mongo.init_app(app)
    csrf.init_app(app)
    login_mgr.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(crud.bp)
    app.register_blueprint(processing.bp)
    app.register_blueprint(home.bp)

    return app
