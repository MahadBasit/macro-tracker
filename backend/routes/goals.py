from flask import Blueprint, request, g, jsonify
from auth import require_auth
from validation import validate_goals
from supabase_client import supabase

goals_bp = Blueprint("goals", __name__)


@goals_bp.route("/api/goals", methods=["POST"])
@require_auth
def set_goals():
    payload = request.get_json(silent=True) or {}
    error = validate_goals(payload)
    if error:
        return jsonify({"error": error}), 400

    data = {
        "user_id": g.user_id,
        "protein": float(payload["protein"]),
        "carbs": float(payload["carbs"]),
        "fat": float(payload["fat"]),
        "calories": float(payload["calories"]),
    }

    result = (
        supabase.table("daily_goals")
        .upsert(data, on_conflict="user_id")
        .execute()
    )
    if not result.data:
        return jsonify({"error": "Failed to save goals"}), 500

    return jsonify({"data": result.data[0]}), 200


@goals_bp.route("/api/goals", methods=["GET"])
@require_auth
def get_goals():
    result = (
        supabase.table("daily_goals")
        .select("protein, carbs, fat, calories")
        .eq("user_id", g.user_id)
        .execute()
    )

    goals = result.data[0] if result.data else None
    return jsonify({"data": goals}), 200
