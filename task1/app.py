from auth.error_handlers import error_blueprint
from auth.views import auth_blueprint, users_blueprint
from extensions import db, jwt, migrate
from flask import Blueprint, Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
    api_v1.register_blueprint(auth_blueprint)
    api_v1.register_blueprint(users_blueprint)

    app.register_blueprint(api_v1)
    app.register_blueprint(error_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
    )
