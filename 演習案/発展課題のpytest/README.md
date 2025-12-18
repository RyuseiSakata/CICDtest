# タイマーアプリ演習用 pytest セット（模範解答 + ひな形）

## 目的
- 仕様書どおりに **pytest を作る/直す**体験をする
- CI（GitHub Actions）でテストが落ちたら原因を特定して直す体験をする

## 前提（想定API）
- Flask `app` は `timer_app.app` に存在
- API:
  - GET  /health
  - GET  /timer
  - POST /timer/start
  - POST /timer/stop
  - POST /timer/lap
  - POST /timer/reset
  - GET  /clock?tz=...

## 使い方
- 模範解答: `tests_model_solution/` を `tests/` にコピーして `pytest`
- ひな形: `tests_template/` を `tests/` にコピーして、コメントアウト部を完成させる

## 実行例
```bash
PYTHONPATH=src pytest -q
```
