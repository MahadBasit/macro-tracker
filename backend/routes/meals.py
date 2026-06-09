from flask import Blueprint, request, g, jsonify
from datetime import datetime, timezone
from auth import require_auth
from validation import validate_meal
from supabase_client import supabase

meals_bp = Blueprint("meals", __name__)


@meals_bp.route("/api/meals", methods=["POST"])
@require_auth
def log_meal():
    payload = request.get_json(silent=True) or {}
    error = validate_meal(payload)
    if error:
        return jsonify({"error": error}), 400

    data = {
        "user_id": g.user_id,
        "name": payload["name"].strip(),
        "protein": float(payload["protein"]),
        "carbs": float(payload["carbs"]),
        "fat": float(payload["fat"]),
        "calories": float(payload["calories"]),
    }

    result = supabase.table("meals").insert(data).execute()
    if not result.data:
        return jsonify({"error": "Failed to log meal"}), 500

    return jsonify({"data": result.data[0]}), 201


@meals_bp.route("/api/meals/today", methods=["GET"])
@require_auth
def get_today_meals():
    now = datetime.now(timezone.utc)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    day_end = now.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()

    result = (
        supabase.table("meals")
        .select("id, name, protein, carbs, fat, calories, logged_at")
        .eq("user_id", g.user_id)
        .gte("logged_at", day_start)
        .lte("logged_at", day_end)
        .order("logged_at")
        .execute()
    )

    return jsonify({"data": result.data}), 200
