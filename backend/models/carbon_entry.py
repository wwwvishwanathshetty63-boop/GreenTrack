"""Carbon entry model for user activity logging."""
from datetime import datetime, timezone, date
from backend.models import db


class CarbonEntry(db.Model):
    __tablename__ = 'carbon_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    travel_mode = db.Column(db.String(20), nullable=False)  # car, bus, bike, walking
    distance = db.Column(db.Float, nullable=False, default=0.0)
    electricity_usage = db.Column(db.Float, nullable=False, default=0.0)
    food_habit = db.Column(db.String(20), nullable=False)  # veg, non-veg, vegan
    entry_date = db.Column(db.Date, nullable=False, default=lambda: date.today())
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'travel_mode': self.travel_mode,
            'distance': self.distance,
            'electricity_usage': self.electricity_usage,
            'food_habit': self.food_habit,
            'entry_date': self.entry_date.isoformat() if self.entry_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
