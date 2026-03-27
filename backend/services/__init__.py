"""Carbon footprint calculation service with realistic emission factors."""

# Emission factors (kg CO₂)
TRAVEL_FACTORS = {
    'car': 0.21,       # kg CO₂ per km
    'bus': 0.05,       # kg CO₂ per km
    'bike': 0.10,      # kg CO₂ per km
    'walking': 0.00,   # zero emissions
}

ELECTRICITY_FACTOR = 0.82  # kg CO₂ per unit

FOOD_FACTORS = {
    'veg': 1.5,        # kg CO₂ per day
    'non-veg': 3.0,    # kg CO₂ per day
    'vegan': 1.2,      # kg CO₂ per day
}


def calculate_daily_emission(travel_mode, distance, electricity_usage, food_habit):
    """Calculate the daily carbon footprint breakdown.

    Args:
        travel_mode: One of 'car', 'bus', 'bike', 'walking'.
        distance: Distance traveled in km.
        electricity_usage: Electricity consumed in units (daily share).
        food_habit: One of 'veg', 'non-veg', 'vegan'.

    Returns:
        dict with travel_emission, electricity_emission, food_emission, total_emission.
    """
    travel_emission = TRAVEL_FACTORS.get(travel_mode, 0) * max(distance, 0)
    electricity_emission = ELECTRICITY_FACTOR * max(electricity_usage, 0)
    food_emission = FOOD_FACTORS.get(food_habit, 1.5)

    total_emission = travel_emission + electricity_emission + food_emission

    return {
        'travel_emission': round(travel_emission, 2),
        'electricity_emission': round(electricity_emission, 2),
        'food_emission': round(food_emission, 2),
        'total_emission': round(total_emission, 2),
    }


def calculate_green_score(weekly_total):
    """Calculate a green score from 0–100.

    Lower emissions → higher score.
    Baseline: ~50 kg CO₂/week is average for a student.
    """
    if weekly_total <= 0:
        return 100
    baseline = 50.0
    score = max(0, min(100, int(100 * (1 - weekly_total / baseline))))
    return score
