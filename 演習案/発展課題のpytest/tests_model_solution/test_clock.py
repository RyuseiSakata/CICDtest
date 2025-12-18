from ._common import client

ALLOWED = ["UTC", "Asia/Tokyo", "America/New_York", "Europe/London"]

def test_clock_default_should_return_utc():
    c = client()
    res = c.get("/clock")
    assert res.status_code == 200
    body = res.get_json()
    assert body["tz"] == "UTC"
    assert "iso" in body
    assert "epoch_ms" in body

def test_clock_allowed_timezones_should_return_shape():
    c = client()
    for tz in ALLOWED:
        res = c.get(f"/clock?tz={tz}")
        assert res.status_code == 200
        body = res.get_json()
        assert body["tz"] == tz
        assert "iso" in body
        assert "epoch_ms" in body

def test_clock_invalid_timezone_should_400():
    c = client()
    res = c.get("/clock?tz=Invalid/Zone")
    assert res.status_code == 400
    assert res.get_json() == {"error": "INVALID_TIMEZONE"}
