"""Application configuration classes."""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False  # Set True in production (HTTPS)
    JWT_COOKIE_CSRF_PROTECT = True  # CSRF protection enabled
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_COOKIE_SAMESITE = 'Lax'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # We handle CSRF via JWT CSRF tokens
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5000').split(',')

    @staticmethod
    def init_app(app):
        if not app.config.get('SECRET_KEY') or not app.config.get('JWT_SECRET_KEY'):
            if not app.debug:
                raise RuntimeError("SECRET_KEY and JWT_SECRET_KEY must be set in production")



class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(basedir, "instance", "greentrack.db")}'
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    JWT_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
