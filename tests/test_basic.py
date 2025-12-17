from timer_app.app import app


def test_health_should_return_ok():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_timer_should_return_shape():
    client = app.test_client()
    res = client.get("/timer")
    assert res.status_code == 200
    body = res.get_json()
    assert "state" in body
    assert "elapsed_ms" in body
    assert "laps" in body


def test_clock_should_return_time_shape():
    client = app.test_client()
    res = client.get("/clock?tz=UTC")
    assert res.status_code == 200
    body = res.get_json()
    assert body["tz"] == "UTC"
    assert "iso" in body
    assert "epoch_ms" in body
