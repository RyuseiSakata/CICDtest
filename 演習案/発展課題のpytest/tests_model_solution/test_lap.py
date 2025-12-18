from ._common import client, sleep_ms

def test_lap_should_return_incremental_differences():
    c = client()
    c.post("/timer/start")

    sleep_ms(25)
    r1 = c.post("/timer/lap")
    assert r1.status_code == 201
    lap1 = r1.get_json()
    assert lap1["lap_index"] == 1
    assert lap1["lap_elapsed_ms"] >= 10
    assert lap1["total_elapsed_ms"] >= lap1["lap_elapsed_ms"]

    sleep_ms(25)
    r2 = c.post("/timer/lap")
    assert r2.status_code == 201
    lap2 = r2.get_json()
    assert lap2["lap_index"] == 2

    assert lap2["total_elapsed_ms"] > lap1["total_elapsed_ms"]

    diff = lap2["total_elapsed_ms"] - lap1["total_elapsed_ms"]
    assert abs(lap2["lap_elapsed_ms"] - diff) <= 5
