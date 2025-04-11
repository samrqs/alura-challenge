from flask import Flask
from flask_migrate import Migrate
from .extensions import db
from .routes import main_bp

migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")
    
    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Feedback, Classification

    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)
    
    return app
