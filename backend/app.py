"""Flask application factory."""
import os
import logging
from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_talisman import Talisman

from backend.config import config_map
from backend.models import db

jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per hour"])


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend'),
        static_url_path=''
    )
    config_obj = config_map.get(config_name, config_map['development'])
    app.config.from_object(config_obj)
    config_obj.init_app(app)

    # ── Extensions ──────────────────────────────────────────────
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    CORS(app, origins=app.config.get('CORS_ORIGINS', ['http://localhost:5000']),
         supports_credentials=True)

    # Talisman – harden security headers and CSP
    csp = {
        'default-src': ["'self'"],
        'script-src': ["'self'", "https://cdn.jsdelivr.net"],  # Removed 'unsafe-inline'

        'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net"],
        'font-src': ["'self'", "https://fonts.gstatic.com"],
        'img-src': ["'self'", "data:", "https:"],
        'connect-src': ["'self'"],
    }
    Talisman(
        app,
        content_security_policy=csp,
        force_https=not app.debug,
        strict_transport_security=True,
        session_cookie_http_only=True,
        frame_options='DENY'
    )


    # ── Blueprints ──────────────────────────────────────────────
    from backend.routes.auth import auth_bp
    from backend.routes.data import data_bp
    from backend.routes.leaderboard import leaderboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(data_bp, url_prefix='/api')
    app.register_blueprint(leaderboard_bp, url_prefix='/api')

    # ── Serve frontend pages ────────────────────────────────────
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory(app.static_folder, filename)

    # ── Error handlers ──────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return {'error': 'Rate limit exceeded. Please try again later.'}, 429

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f'Internal server error: {e}')
        return {'error': 'An internal error occurred'}, 500

    # ── JWT error handlers ──────────────────────────────────────
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired', 'code': 'token_expired'}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token', 'code': 'invalid_token'}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization required', 'code': 'authorization_required'}, 401

    # ── Create tables ───────────────────────────────────────────
    with app.app_context():
        if os.getenv('VERCEL'):
            instance_path = '/tmp/instance'
        else:
            instance_path = os.path.join(os.path.dirname(__file__), '..', 'instance')
        
        os.makedirs(instance_path, exist_ok=True)
        db.create_all()

    # ── Logging ─────────────────────────────────────────────────
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(debug=True, port=5000)
