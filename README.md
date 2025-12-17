# cicd-work2

ストップウォッチWebアプリ

```
cicd-timer-flask-render-ready/
├─ src/
│  └─ timer_app/
│     ├─ __init__.py
│     ├─ timer.py        ← アプリ本体（タイマーAPI）
│     └─ templates/
│        └─ index.html
│
├─ tests/
│  ├─ test_basic.py      ← 最低限のテスト（最初に通す）
│  ├─ test_timer.py      ←（自分で作成）タイマー仕様テスト
│  └─ test_lap.py        ←（自分で作成）ラップ仕様テスト
│
├─ .github/
│  └─ workflows/
│     ├─ ci.yml          ← CI（pytestを自動実行）
│     └─ deploy.yml      ← CD（CI成功時のみデプロイ）
│
├─ requirements.txt
├─ pyproject.toml
└─ README.md
```
