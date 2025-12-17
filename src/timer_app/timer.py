import time
import os
from flask import Flask, jsonify, render_template
import subprocess

try:
    # pytest経由では pythonpath=src で timer_app.* として解決
    from timer_app.lap import register_lap_routes
    from timer_app.world_clock import register_clock_routes
except (
    ModuleNotFoundError
):  # 手動実行時は src/timer_app ディレクトリ内なので lap を直接 import
    from lap import register_lap_routes
    from world_clock import register_clock_routes


# コミットハッシュを取得
def get_git_commit():
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except Exception:
        return "unknown"


app = Flask(__name__, template_folder="templates")


# =========================
# デプロイ情報表示
# =========================
def deploy_metadata():
    return {
        "commit": get_git_commit(),
    }


# =========================
# 内部状態（シンプル実装）
# =========================
state = "stopped"  # "running" or "stopped"
start_time = None  # time.monotonic() を保存
elapsed_ms = 0  # 停止時点までの累積時間
laps = []  # ラップ一覧


def get_state():
    return state


def get_laps():
    return laps


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
    meta = deploy_metadata()
    return render_template(
        "index.html",
        commit=meta["commit"],
    )


# =========================
# API
# =========================
@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/timer")
def get_timer():
    return (
        jsonify({"state": state, "elapsed_ms": current_elapsed_ms(), "laps": laps}),
        200,
    )


@app.post("/timer/start")
def start_timer():
    global state, start_time
    if state == "running":
        return jsonify({"error": "ALREADY_RUNNING"}), 409

    state = "running"
    start_time = time.monotonic()
    return jsonify({"state": state, "elapsed_ms": 0}), 200


@app.post("/timer/stop")
def stop_timer():
    global state, elapsed_ms, start_time
    if state == "stopped":
        return jsonify({"error": "ALREADY_STOPPED"}), 409

    # running → stopped
    elapsed_ms = current_elapsed_ms()
    start_time = None
    state = "stopped"

    return jsonify({"state": state, "elapsed_ms": elapsed_ms}), 200


register_lap_routes(
    app=app,
    current_elapsed_ms=current_elapsed_ms,
    get_state=get_state,
    get_laps=get_laps,
)


@app.post("/timer/reset")
def reset_timer():
    global state, start_time, elapsed_ms, laps
    if state == "running":
        return jsonify({"error": "CANNOT_RESET_WHILE_RUNNING"}), 409

    state = "stopped"
    start_time = None
    elapsed_ms = 0
    laps = []

    return jsonify({"state": state, "elapsed_ms": 0, "laps": []}), 200


# =========================
# Clock API（世界時計）
# =========================
register_clock_routes(app=app)


# =========================
# ローカル実行用
# =========================
def main():
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
