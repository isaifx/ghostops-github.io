import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Database URI - SQLite file located in the project directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
