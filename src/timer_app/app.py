"""互換用エントリポイント。実装は timer.py に集約済み。"""

try:
    # `python -m timer_app.app` や pytest 経由
    from timer_app.timer import app, main
except ModuleNotFoundError:  # `python app.py` を src/timer_app で実行
    from timer import app, main


if __name__ == "__main__":
    main()
