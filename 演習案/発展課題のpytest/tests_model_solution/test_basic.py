from ._common import client

def test_health_should_return_ok():
    c = client()
    res = c.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}

def test_index_should_load_html():
    c = client()
    res = c.get("/")
    assert res.status_code == 200
