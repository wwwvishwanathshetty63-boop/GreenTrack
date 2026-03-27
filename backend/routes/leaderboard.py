"""Leaderboard routes – rank users by lowest carbon footprint."""
import logging
from datetime import date, timedelta
from flask import Blueprint, jsonify
from sqlalchemy import func

from backend.models import db
from backend.models.user import User
from backend.models.carbon_result import CarbonResult
from backend.app import limiter

leaderboard_bp = Blueprint('leaderboard', __name__)
logger = logging.getLogger(__name__)


@leaderboard_bp.route('/leaderboard', methods=['GET'])
@limiter.limit("30 per minute")
def get_leaderboard():
    """Return top 10 users ranked by lowest weekly carbon footprint."""
    today = date.today()
    week_start = today - timedelta(days=6)

    try:
        # Aggregate weekly emissions per user
        results = db.session.query(
            User.id,
            User.username,
            func.coalesce(func.sum(CarbonResult.total_emission), 0).label('weekly_total')
        ).join(
            CarbonResult, User.id == CarbonResult.user_id
        ).filter(
            CarbonResult.result_date >= week_start,
            CarbonResult.result_date <= today,
        ).group_by(User.id, User.username) \
         .order_by(func.sum(CarbonResult.total_emission).asc()) \
         .limit(10).all()

        leaderboard = []
        for rank, row in enumerate(results, start=1):
            leaderboard.append({
                'rank': rank,
                'username': row.username,
                'weekly_total': round(float(row.weekly_total), 2),
            })

        return jsonify({'leaderboard': leaderboard}), 200

    except Exception as e:
        logger.error(f'Leaderboard error: {e}')
        return jsonify({'error': 'Failed to load leaderboard'}), 500
