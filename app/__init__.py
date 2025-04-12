from flask import Flask

from .extensions import db,mail,migrate,scheduler
from .routes import main_bp
from app.email import send_email

from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")
    
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    scheduler.init_app(app)

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    scheduler.add_job(func=send_email, trigger='interval', days=7, id='weekly_email', name='Enviar resumo semanal', replace_existing=True)
    scheduler.start()

    return app