from ._common import client

# ----------------------------
# 仕様: /health は {"status":"ok"} を返す
# ----------------------------
def test_health_should_return_ok():
    # Flaskのテストクライアントを生成する（サーバ起動不要）。
    c = client()

    # GET /health を呼び出す（死活監視・CIの最小確認に使う）
    res = c.get("/health")

    # HTTP 200 は「正常」を意味する
    assert res.status_code == 200

    # 返却JSONが仕様通りかを確認する
    assert res.get_json() == {"status": "ok"}


# TODO: 画面（GET /）が 200 を返すテストを追加してみよう
# def test_index_should_load_html():
#     ...
