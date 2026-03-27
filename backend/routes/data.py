"""Data routes – add carbon entry, retrieve user data."""
import logging
from datetime import date, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from backend.models import db
from backend.models.carbon_entry import CarbonEntry
from backend.models.carbon_result import CarbonResult
from backend.services import calculate_daily_emission, calculate_green_score
from backend.services.suggestions import generate_suggestions
from backend.utils import validate_carbon_entry
from backend.app import limiter

data_bp = Blueprint('data', __name__)
logger = logging.getLogger(__name__)


@data_bp.route('/add-entry', methods=['POST'])
@jwt_required()
@limiter.limit("30 per minute")
def add_entry():
    """Add a new carbon footprint entry."""
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    # Validate input
    is_valid, error_msg, cleaned = validate_carbon_entry(data)
    if not is_valid:
        return jsonify({'error': error_msg}), 400

    try:
        # Create entry
        entry = CarbonEntry(
            user_id=user_id,
            travel_mode=cleaned['travel_mode'],
            distance=cleaned['distance'],
            electricity_usage=cleaned['electricity_usage'],
            food_habit=cleaned['food_habit'],
            entry_date=date.today(),
        )
        db.session.add(entry)

        # Calculate emissions
        emissions = calculate_daily_emission(
            cleaned['travel_mode'],
            cleaned['distance'],
            cleaned['electricity_usage'],
            cleaned['food_habit'],
        )

        # Store result
        result = CarbonResult(
            user_id=user_id,
            travel_emission=emissions['travel_emission'],
            electricity_emission=emissions['electricity_emission'],
            food_emission=emissions['food_emission'],
            total_emission=emissions['total_emission'],
            result_date=date.today(),
        )
        db.session.add(result)
        db.session.commit()

        logger.info(f'Entry added for user {user_id}: {emissions["total_emission"]} kg CO₂')
        return jsonify({
            'message': 'Entry added successfully',
            'entry': entry.to_dict(),
            'emissions': emissions,
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f'Add entry error: {e}')
        return jsonify({'error': 'Failed to add entry. Please try again.'}), 500


@data_bp.route('/user-data', methods=['GET'])
@jwt_required()
def get_user_data():
    """Retrieve aggregated user data for the dashboard."""
    user_id = int(get_jwt_identity())
    today = date.today()

    try:
        # ── Weekly data (last 7 days) ────────────────────────────
        week_start = today - timedelta(days=6)
        weekly_results = CarbonResult.query.filter(
            CarbonResult.user_id == user_id,
            CarbonResult.result_date >= week_start,
            CarbonResult.result_date <= today,
        ).all()

        weekly_total = sum(r.total_emission for r in weekly_results)

        # Daily breakdown for charts
        daily_data = {}
        for i in range(7):
            d = week_start + timedelta(days=i)
            day_label = d.strftime('%a')
            day_results = [r for r in weekly_results if r.result_date == d]
            daily_data[day_label] = round(sum(r.total_emission for r in day_results), 2)

        # ── Category breakdown ───────────────────────────────────
        cat_travel = round(sum(r.travel_emission for r in weekly_results), 2)
        cat_electricity = round(sum(r.electricity_emission for r in weekly_results), 2)
        cat_food = round(sum(r.food_emission for r in weekly_results), 2)

        # ── Monthly total ────────────────────────────────────────
        month_start = today.replace(day=1)
        monthly_total_query = db.session.query(
            func.coalesce(func.sum(CarbonResult.total_emission), 0)
        ).filter(
            CarbonResult.user_id == user_id,
            CarbonResult.result_date >= month_start,
        ).scalar()
        monthly_total = round(float(monthly_total_query), 2)

        # ── Green score ──────────────────────────────────────────
        green_score = calculate_green_score(weekly_total)

        # ── Recent entries ───────────────────────────────────────
        recent_entries = CarbonEntry.query.filter_by(user_id=user_id) \
            .order_by(CarbonEntry.entry_date.desc()).limit(10).all()
        entries_list = [e.to_dict() for e in recent_entries]

        # ── Suggestions ──────────────────────────────────────────
        suggestions = generate_suggestions(entries_list, weekly_total)

        return jsonify({
            'weekly_total': round(weekly_total, 2),
            'monthly_total': monthly_total,
            'green_score': green_score,
            'daily_data': daily_data,
            'category_breakdown': {
                'travel': cat_travel,
                'electricity': cat_electricity,
                'food': cat_food,
            },
            'recent_entries': entries_list,
            'suggestions': suggestions,
        }), 200

    except Exception as e:
        logger.error(f'User data error: {e}')
        return jsonify({'error': 'Failed to load data'}), 500
