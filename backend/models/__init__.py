"""SQLAlchemy database instance and model imports."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models so they are registered with SQLAlchemy
from backend.models.user import User  # noqa: F401, E402
from backend.models.carbon_entry import CarbonEntry  # noqa: F401, E402
from backend.models.carbon_result import CarbonResult  # noqa: F401, E402
