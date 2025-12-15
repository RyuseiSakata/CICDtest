import time
import os
from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder="templates")

# =========================
# 内部状態（シンプル実装）
# =========================
state = "stopped"          # "running" or "stopped"
start_time = None          # time.monotonic() を保存
elapsed_ms = 0             # 停止時点までの累積時間
laps = []                  # ラップ一覧

# =========================
# 補助関数
# =========================
def current_elapsed_ms():
    """現在の経過時間（ms）を返す"""
    global elapsed_ms, start_time, state
    if state == "running" and start_time is not None:
        return elapsed_ms + int((time.monotonic() - start_time) * 1000)
    return elapsed_ms

# =========================
# 画面（タイマーアプリ）
# =========================
@app.get("/")
def index():
    return render_template("index.html")

# =========================
# API
# =========================
@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/timer")
def get_timer():
    return jsonify({
        "state": state,
        "elapsed_ms": current_elapsed_ms(),
        "laps": laps
    }), 200

@app.post("/timer/start")
def start_timer():
    global state, start_time
    if state == "running":
        return jsonify({"error": "ALREADY_RUNNING"}), 409

    state = "running"
    start_time = time.monotonic()
    return jsonify({
        "state": state,
        "elapsed_ms": 0
    }), 200

@app.post("/timer/stop")
def stop_timer():
    global state, elapsed_ms, start_time
    if state == "stopped":
        return jsonify({"error": "ALREADY_STOPPED"}), 409

    # running → stopped
    elapsed_ms = current_elapsed_ms()
    start_time = None
    state = "stopped"

    return jsonify({
        "state": state,
        "elapsed_ms": elapsed_ms
    }), 200

@app.post("/timer/lap")
def lap_timer():
    global laps
    if state != "running":
        return jsonify({"error": "NOT_RUNNING"}), 409

    total = current_elapsed_ms()
    if len(laps) == 0:
        lap_elapsed = total
    else:
        lap_elapsed = total - laps[-1]["total_elapsed_ms"]

    lap = {
        "lap_index": len(laps) + 1,
        "lap_elapsed_ms": lap_elapsed,
        "total_elapsed_ms": total
    }
    laps.append(lap)

    return jsonify(lap), 201

@app.post("/timer/reset")
def reset_timer():
    global state, start_time, elapsed_ms, laps
    if state == "running":
        return jsonify({"error": "CANNOT_RESET_WHILE_RUNNING"}), 409

    state = "stopped"
    start_time = None
    elapsed_ms = 0
    laps = []

    return jsonify({
        "state": state,
        "elapsed_ms": 0,
        "laps": []
    }), 200

# =========================
# ローカル実行用
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
