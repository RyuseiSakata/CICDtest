from ._common import client, sleep_ms

# ----------------------------
# 仕様: lap は 201 を返し、lap_index / lap_elapsed_ms / total_elapsed_ms を含む
# （この例では“形”の確認を中心にする）
# ----------------------------
def test_lap_should_return_shape():
    c = client()

    # 1) running にしてから lap を取る
    c.post("/timer/start")
    sleep_ms(20)

    # 2) lap を実行
    res = c.post("/timer/lap")

    # 3) 作成系なので 201（Created）を期待
    assert res.status_code == 201
    body = res.get_json()

    # 4) 返るJSONの形を確認（値は厳密比較しない）
    assert body["lap_index"] == 1
    assert "lap_elapsed_ms" in body
    assert "total_elapsed_ms" in body


# TODO: 2周目以降は lap_elapsed_ms が差分（前回 total との差）になるテストを書いてみよう
# def test_lap_should_be_incremental_difference():
#     ...
