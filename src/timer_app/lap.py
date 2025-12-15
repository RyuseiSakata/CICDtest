from flask import jsonify


def register_lap_routes(app, current_elapsed_ms, get_state, get_laps):
    """Register lap endpoint separately from main app module."""

    @app.post("/timer/lap")
    def lap_timer():
        if get_state() != "running":
            return jsonify({"error": "NOT_RUNNING"}), 409

        laps = get_laps()
        total = current_elapsed_ms()
        if len(laps) == 0:
            lap_elapsed = total
        else:
            lap_elapsed = total - laps[-1]["total_elapsed_ms"]

        lap = {
            "lap_index": len(laps) + 1,
            "lap_elapsed_ms": lap_elapsed,
            "total_elapsed_ms": total,
        }
        laps.append(lap)

        return jsonify(lap), 201

    return lap_timer
