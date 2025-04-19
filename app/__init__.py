import os
import click
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)

    if os.path.exists('.devcontainer/.env'):
        load_dotenv('.devcontainer/.env')

    app.config.from_object(config_class)
    secret_key = os.environ.get('SECRET_KEY')
    app.config['SECRET_KEY'] = secret_key

    # Heroku's DATABASE_URL format isn't supported by SQLAlchemy
    # https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre 
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    security_password_salt = os.environ.get('SECURITY_PASSWORD_SALT')
    app.config['SECURITY_PASSWORD_SALT'] = security_password_salt

    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.phases import phases_bp
    from app.routes.settings import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(phases_bp)
    app.register_blueprint(settings_bp)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

        # Auto-seed database on first run if environment variable is set
        if os.environ.get('FLASK_AUTO_SEED', 'False').lower() == 'true':
            from app.seed import seed_default_data
            seed_default_data()

    @app.cli.command("seed-db")
    @click.option('--force', is_flag=True, help='Force seeding even if data exists')
    def seed_db_command(force):
        """Seed database with default data."""
        from app.seed import seed_default_data
        with app.app_context():
            seed_default_data(force=force)
        print("Database seeded!")

    return app