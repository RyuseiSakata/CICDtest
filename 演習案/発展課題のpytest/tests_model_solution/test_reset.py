from ._common import client, sleep_ms

def test_reset_should_clear_elapsed_and_laps_when_stopped():
    c = client()
    c.post("/timer/start")
    sleep_ms(20)
    c.post("/timer/lap")
    c.post("/timer/stop")

    res = c.post("/timer/reset")
    assert res.status_code == 200
    body = res.get_json()
    assert body["state"] == "stopped"
    assert body["elapsed_ms"] == 0
    assert body["laps"] == []

    t = c.get("/timer").get_json()
    assert t["elapsed_ms"] == 0
    assert t["laps"] == []

def test_reset_while_running_should_409():
    c = client()
    c.post("/timer/start")
    res = c.post("/timer/reset")
    assert res.status_code == 409
    assert res.get_json() == {"error": "CANNOT_RESET_WHILE_RUNNING"}
