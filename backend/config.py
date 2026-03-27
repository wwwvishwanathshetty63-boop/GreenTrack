"""Application configuration classes."""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback-jwt-secret-key')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False  # Set True in production (HTTPS)
    JWT_COOKIE_CSRF_PROTECT = False  # We use our own CSRF
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_COOKIE_SAMESITE = 'Lax'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # We handle CSRF via custom tokens for API
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5000').split(',')


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
