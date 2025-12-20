from ._common import client, sleep_ms

# ----------------------------
# 仕様: start→stop で elapsed_ms が増える
# ----------------------------
def test_start_then_stop_should_increase_elapsed():
    c = client()

    # 1) start（停止→稼働）
    res = c.post("/timer/start")
    assert res.status_code == 200
    assert res.get_json()["state"] == "running"

    # 2) 少し待つ（実時間に依存するので短く）
    sleep_ms(30)

    # 3) stop（稼働→停止）
    res = c.post("/timer/stop")
    assert res.status_code == 200
    body = res.get_json()

    # 4) 停止状態になっていること
    assert body["state"] == "stopped"

    # 5) 経過時間が“0より増えている”こと（厳密値は比較しない）
    assert body["elapsed_ms"] >= 10


# TODO: startを2回押したら409になる（ALREADY_RUNNING）を追加してみよう
# def test_start_twice_should_409():
#     ...
