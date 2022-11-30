venv:
    source venv/bin/activate

send-report: venv
    python src/report.py
