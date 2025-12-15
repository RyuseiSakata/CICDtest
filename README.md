# CICDtest

```
cicd-timer-flask-render-ready/
├─ src/
│  └─ timer_app/
│     ├─ __init__.py
│     └─ app.py          ← アプリ本体（Flask）
│
├─ tests/
│  ├─ test_basic.py      ← 最低限のテスト（最初に通す）
│  ├─ test_timer.py      ←（今後追加）タイマー仕様テスト
│  └─ test_lap.py        ←（今後追加）ラップ仕様テスト
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
