"""テスト共通ユーティリティ

- Flask test_client を使う（実ネットワークは使わない）
- 時間を扱うテストは“厳密な値比較”を避け、増減や下限/上限で確認する
"""

import time
from timer_app.app import app

def client():
    return app.test_client()

def sleep_ms(ms: int):
    time.sleep(ms / 1000.0)
