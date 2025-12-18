from ._common import client, sleep_ms

def test_start_then_stop_should_increase_elapsed():
    c = client()

    res = c.post("/timer/start")
    assert res.status_code == 200
    assert res.get_json()["state"] == "running"

    sleep_ms(30)

    res = c.post("/timer/stop")
    assert res.status_code == 200
    body = res.get_json()
    assert body["state"] == "stopped"
    assert body["elapsed_ms"] >= 10

def test_start_twice_should_409():
    c = client()
    assert c.post("/timer/start").status_code == 200
    res = c.post("/timer/start")
    assert res.status_code == 409
    assert res.get_json() == {"error": "ALREADY_RUNNING"}

def test_stop_when_stopped_should_409():
    c = client()
    res = c.post("/timer/stop")
    assert res.status_code == 409
    assert res.get_json() == {"error": "ALREADY_STOPPED"}

def test_lap_when_not_running_should_409():
    c = client()
    res = c.post("/timer/lap")
    assert res.status_code == 409
    assert res.get_json() == {"error": "NOT_RUNNING"}
