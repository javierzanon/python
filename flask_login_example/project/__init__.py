from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Secret*tesT'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'api_user_management.login'
    login_manager.init_app(app)

    from .data_models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .api_user_management import api_user_management as user_management_blueprint
    app.register_blueprint(user_management_blueprint)

    from .api_platform import api_platform as platform_blueprint
    app.register_blueprint(platform_blueprint)

    return app
