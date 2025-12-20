from ._common import client

# ----------------------------
# 仕様: /clock?tz=UTC は 200 を返し、tz/iso/epoch_ms を含む
# ----------------------------
def test_clock_should_return_utc_shape():
    c = client()

    # tz=UTC で現在時刻を取得
    res = c.get("/clock?tz=UTC")
    assert res.status_code == 200

    body = res.get_json()

    # 指定したタイムゾーンがそのまま返る
    assert body["tz"] == "UTC"

    # 現在時刻は毎回変わるので “キーの存在” を中心に検証する
    assert "iso" in body
    assert "epoch_ms" in body


# TODO: 不正TZは400（INVALID_TIMEZONE）になるテストを追加してみよう
# def test_clock_invalid_timezone_should_400():
#     ...
