"""テスト共通ユーティリティ

- Flask test_client を使う（実ネットワークは使わない）
- 時間を扱うテストは“厳密な値比較”を避け、増減・下限/上限で確認する
"""

import time
from timer_app.app import app

def client():
    # Flaskのテストクライアントを生成する（サーバ起動不要）。
    # 実際にHTTPポートを立てずにAPIを呼べる。
    return app.test_client()

def sleep_ms(ms: int):
    time.sleep(ms / 1000.0)
