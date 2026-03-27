"""Authentication routes – register, login, logout."""
import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, set_access_cookies, unset_jwt_cookies,
    jwt_required, get_jwt_identity
)
from backend.models import db
from backend.models.user import User
from backend.utils import (
    sanitize_string, validate_email, validate_password, validate_username
)
from backend.app import limiter

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("10 per minute")
def register():
    """Register a new user."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    # Validate username
    username = sanitize_string(data.get('username', ''))
    valid, msg = validate_username(username)
    if not valid:
        return jsonify({'error': msg}), 400

    # Validate email
    email = sanitize_string(data.get('email', '').lower())
    if not validate_email(email):
        return jsonify({'error': 'Invalid email address'}), 400

    # Validate password
    password = data.get('password', '')
    valid, msg = validate_password(password)
    if not valid:
        return jsonify({'error': msg}), 400

    # Check duplicates
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Create user
    try:
        user = User(username=username, email=email, role='student')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        logger.info(f'New user registered: {username}')
        return jsonify({'message': 'Registration successful', 'user': user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f'Registration error: {e}')
        return jsonify({'error': 'Registration failed. Please try again.'}), 500


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("20 per minute")
def login():
    """Authenticate user and issue JWT cookie."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    raw_username = data.get('username', '').strip()
    password = data.get('password', '')

    if not raw_username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Query by raw username
    user = User.query.filter_by(username=raw_username).first()
    if not user:
        # Fallback: try case-insensitive search
        user = User.query.filter(User.username.ilike(raw_username)).first()

    logger.info(f'Login attempt for: "{raw_username}", user found: {user is not None}')

    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    if not user.check_password(password):
        logger.warning(f'Password mismatch for user: {raw_username}')
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=str(user.id))
    response = jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    })
    set_access_cookies(response, access_token)
    logger.info(f'User logged in: {raw_username}')
    return response, 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required(optional=True)
def logout():
    """Clear JWT cookies."""
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response, 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Return current authenticated user."""
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200
