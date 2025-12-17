from datetime import datetime
from zoneinfo import ZoneInfo
from flask import jsonify, request

# =========================
# Clock（世界時計）設定
# =========================
ALLOWED_TZ = {
    "UTC": "UTC",
    "Asia/Tokyo": "Asia/Tokyo",
    "America/New_York": "America/New_York",
    "Europe/London": "Europe/London",
}


# =========================
# Clock API（世界時計）
# =========================
def register_clock_routes(app):
    @app.get("/clock")
    def get_clock():
        tz = request.args.get("tz", "UTC")
        if tz not in ALLOWED_TZ:
            return jsonify({"error": "INVALID_TIMEZONE"}), 400

        now = datetime.now(ZoneInfo(ALLOWED_TZ[tz]))
        return (
            jsonify(
                {
                    "tz": tz,
                    "iso": now.isoformat(),
                    "epoch_ms": int(now.timestamp() * 1000),
                }
            ),
            200,
        )

    return get_clock
