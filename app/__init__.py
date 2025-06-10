from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_migrate import Migrate
from config import Config

# Create ONE global db instance here
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()

# Flask-Login config
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    csrf.init_app(app)            # Enable CSRF protection globally
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Import models here so SQLAlchemy can register them before migrations
    from app.models import User, Task, Note  # <-- added Note here

    # Define the user_loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import main as main_bp
    from app.auth import auth as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # CSRF error handler: render a nice template with the error message
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('csrf_error.html', reason=e.description), 400

    return app
