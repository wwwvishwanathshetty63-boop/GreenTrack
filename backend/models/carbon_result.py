"""Carbon result model for calculated emissions."""
from datetime import datetime, timezone, date
from backend.models import db


class CarbonResult(db.Model):
    __tablename__ = 'carbon_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    travel_emission = db.Column(db.Float, nullable=False, default=0.0)
    electricity_emission = db.Column(db.Float, nullable=False, default=0.0)
    food_emission = db.Column(db.Float, nullable=False, default=0.0)
    total_emission = db.Column(db.Float, nullable=False, default=0.0)
    result_date = db.Column(db.Date, nullable=False, default=lambda: date.today())
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'travel_emission': round(self.travel_emission, 2),
            'electricity_emission': round(self.electricity_emission, 2),
            'food_emission': round(self.food_emission, 2),
            'total_emission': round(self.total_emission, 2),
            'result_date': self.result_date.isoformat() if self.result_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
