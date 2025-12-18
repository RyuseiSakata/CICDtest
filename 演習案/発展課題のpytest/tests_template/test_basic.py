from ._common import client

def test_health_should_return_ok():
    # ねらい: CIで“生きているか”を最初に保証する
    c = client()
    res = c.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}

def test_index_should_load_html():
    # ねらい: 画面が返る（= ルーティング/テンプレの壊れを検出）
    c = client()
    res = c.get("/")
    assert res.status_code == 200
