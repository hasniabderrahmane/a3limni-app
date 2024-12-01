from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from a3limni.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from a3limni.main.routes import main
    from a3limni.auth.routes import auth
    from a3limni.students.routes import students

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(students)

    with app.app_context():
        db.create_all()

    return app
