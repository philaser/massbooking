from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """ initialize the app factory """

    app = Flask(__name__)
    app.config.from_object('config.Config')

    """ initialize the plugins"""
    db.init_app(app)

    with app.app_context():
        from app.general.general import general_bp
        from app.admin.admin import admin_bp

        app.register_blueprint(general_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')

        return app


