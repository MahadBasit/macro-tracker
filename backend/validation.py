def validate_meal(payload):
    required = ["name", "protein", "carbs", "fat", "calories"]
    for field in required:
        if field not in payload:
            return f"Missing field: {field}"

    if not isinstance(payload["name"], str) or not payload["name"].strip():
        return "name must be a non-empty string"

    for field in ["protein", "carbs", "fat", "calories"]:
        try:
            value = float(payload[field])
        except (TypeError, ValueError):
            return f"{field} must be a number"
        if value < 0:
            return f"{field} must be >= 0"

    return None


def validate_goals(payload):
    required = ["protein", "carbs", "fat", "calories"]
    for field in required:
        if field not in payload:
            return f"Missing field: {field}"

    for field in required:
        try:
            value = float(payload[field])
        except (TypeError, ValueError):
            return f"{field} must be a number"
        if value < 0:
            return f"{field} must be >= 0"

    return None
