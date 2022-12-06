venv:
    source venv/bin/activate

send-report: venv
    python src/report.py

send-wrapped: venv
    python src/wrapped.py
