"""Smart suggestions engine that generates personalized eco tips."""

from backend.services import TRAVEL_FACTORS, FOOD_FACTORS, ELECTRICITY_FACTOR


def generate_suggestions(entries, weekly_total):
    """Generate personalized eco suggestions based on user data patterns.

    Args:
        entries: List of recent CarbonEntry dicts.
        weekly_total: Total weekly emission in kg CO₂.

    Returns:
        List of suggestion strings.
    """
    suggestions = []

    if not entries:
        suggestions.append("🌱 Start logging your daily activities to get personalized eco tips!")
        return suggestions

    # Analyse patterns
    travel_modes = [e.get('travel_mode', '') for e in entries]
    food_habits = [e.get('food_habit', '') for e in entries]
    avg_distance = sum(e.get('distance', 0) for e in entries) / len(entries)
    avg_electricity = sum(e.get('electricity_usage', 0) for e in entries) / len(entries)

    # ── Travel suggestions ───────────────────────────────────
    car_count = travel_modes.count('car')
    if car_count > len(entries) * 0.5:
        suggestions.append(
            "🚌 You drive a lot! Switching to public transport even 2 days a week "
            f"could save ~{round(avg_distance * (TRAVEL_FACTORS['car'] - TRAVEL_FACTORS['bus']) * 2, 1)} kg CO₂/week."
        )
    if car_count > 0 and 'bike' not in travel_modes:
        suggestions.append(
            "🚲 Try cycling for short-distance trips. It's zero-emission and great exercise!"
        )
    if 'walking' not in travel_modes:
        suggestions.append(
            "🚶 Walking short distances is the greenest option—and it's free!"
        )

    # ── Electricity suggestions ──────────────────────────────
    if avg_electricity > 5:
        suggestions.append(
            "💡 Your electricity usage is high. Try switching off lights and "
            "unplugging devices when not in use."
        )
    if avg_electricity > 10:
        suggestions.append(
            "⚡ Consider using energy-efficient LED bulbs and power strips "
            "to cut your electricity footprint."
        )
    if avg_electricity > 3:
        suggestions.append(
            "🌙 Reduce screen brightness and enable power-saving modes on your devices."
        )

    # ── Food suggestions ─────────────────────────────────────
    nonveg_count = food_habits.count('non-veg')
    if nonveg_count > len(entries) * 0.5:
        savings = round((FOOD_FACTORS['non-veg'] - FOOD_FACTORS['veg']) * nonveg_count, 1)
        suggestions.append(
            f"🥗 Switching to vegetarian meals a few days a week could save ~{savings} kg CO₂."
        )
    if 'vegan' not in food_habits and nonveg_count > 0:
        suggestions.append(
            "🌿 Try a vegan meal once a week. Plant-based diets have the lowest carbon footprint."
        )

    # ── General suggestions ──────────────────────────────────
    if weekly_total > 40:
        suggestions.append(
            "📊 Your weekly footprint is above average. Small changes in transport "
            "and diet can make a big difference!"
        )
    elif weekly_total < 15:
        suggestions.append(
            "🌟 Amazing! Your carbon footprint is very low. Keep up the great work!"
        )
    else:
        suggestions.append(
            "👍 You're on the right track! Focus on reducing your highest-emission category."
        )

    # Always include a motivational one
    suggestions.append(
        "🌍 Remember: every small step counts toward a greener planet!"
    )

    return suggestions[:6]  # Return top 6 suggestions
