import csv
import sys
from pathlib import Path

import requests

API_URL = "http://localhost:8000/api/analyze"
CSV_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "test_messages.csv"


def load_test_cases(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters="\t,")
        except csv.Error:
            dialect = csv.excel_tab  # fall back to tab
        reader = csv.DictReader(f, dialect=dialect)
        return list(reader)


def run_tests() -> None:
    if not CSV_PATH.exists():
        print(f"❌ Test file not found at {CSV_PATH}")
        sys.exit(1)

    cases = load_test_cases(CSV_PATH)
    passed, failed = 0, 0
    failures: list[dict] = []

    for row in cases:
        try:
            resp = requests.post(API_URL, json={"message": row["message"]}, timeout=10)
        except requests.exceptions.ConnectionError:
            print("❌ Could not reach the API — is uvicorn running on port 8000?")
            sys.exit(1)

        if resp.status_code != 200:
            failed += 1
            failures.append({
                "id": row["id"], "category": row["category"],
                "reason": f"HTTP {resp.status_code}", "message": row["message"],
            })
            continue

        data = resp.json()
        expected_signals = set(row["expected_signals"].split(";")) - {"NONE"}
        actual_signals = {s["type"] for s in data["signals"]}

        risk_match = data["risk_level"] == row["expected_risk"]
        signals_match = expected_signals == actual_signals

        if risk_match and signals_match:
            passed += 1
        else:
            failed += 1
            failures.append({
                "id": row["id"],
                "category": row["category"],
                "message": row["message"][:60] + ("..." if len(row["message"]) > 60 else ""),
                "expected_risk": row["expected_risk"],
                "actual_risk": data["risk_level"],
                "expected_signals": sorted(expected_signals),
                "actual_signals": sorted(actual_signals),
            })

    total = passed + failed
    print(f"\n{'='*60}")
    print(f"RESULTS: {passed}/{total} passed ({passed/total*100:.1f}%)")
    print(f"{'='*60}\n")

    if failures:
        print(f"{len(failures)} FAILURES:\n")
        for f in failures:
            print(f"  #{f['id']} [{f['category']}]")
            print(f"    message : {f.get('message', '')}")
            if "reason" in f:
                print(f"    reason  : {f['reason']}")
            else:
                print(f"    risk    : expected={f['expected_risk']}  actual={f['actual_risk']}")
                print(f"    signals : expected={f['expected_signals']}")
                print(f"              actual  ={f['actual_signals']}")
            print()


if __name__ == "__main__":
    run_tests()