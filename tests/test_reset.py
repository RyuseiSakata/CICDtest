from ._common import client, sleep_ms

# ----------------------------
# 仕様: stopped状態で reset すると elapsed_ms=0 かつ laps=[] になる
# ----------------------------
def test_reset_should_clear_elapsed_and_laps_when_stopped():
    c = client()

    # 1) start → 少し進める → lap → stop で、状態を“汚す”
    c.post("/timer/start")
    sleep_ms(20)
    c.post("/timer/lap")
    c.post("/timer/stop")

    # 2) reset 実行
    res = c.post("/timer/reset")
    assert res.status_code == 200
    body = res.get_json()

    # 3) 仕様の期待値を確認
    assert body["state"] == "stopped"
    assert body["elapsed_ms"] == 0
    assert body["laps"] == []


# TODO: running中にresetしたら409（CANNOT_RESET_WHILE_RUNNING）を追加してみよう
# def test_reset_while_running_should_409():
#     ...
