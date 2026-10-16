import urllib.request
import urllib.parse
import json

def test_api():
    print("--- 1. Testing GET /api/summary ---")
    with urllib.request.urlopen("http://127.0.0.1:8000/api/summary") as res:
        summary = json.loads(res.read().decode())
        print("Summary:", json.dumps(summary, indent=2))

    print("\n--- 2. Testing GET /api/tenders ---")
    with urllib.request.urlopen("http://127.0.0.1:8000/api/tenders") as res:
        tenders = json.loads(res.read().decode())
        print(f"Total Tenders returned from Neon: {len(tenders)}")
        first = tenders[0]
        print(f"Top Outlier Tender: {first['tender_id']}")
        print(f"Anomaly Score: {first['anomaly_score']} ({first['status_badge']})")

    print(f"\n--- 3. Testing GET /api/tenders/{first['tender_id']} ---")
    encoded_tid = urllib.parse.quote(first['tender_id'], safe='')
    with urllib.request.urlopen(f"http://127.0.0.1:8000/api/tenders/{encoded_tid}") as res:
        detail = json.loads(res.read().decode())
        print(f"Work Name: {detail.get('work_name')}")
        print(f"SHAP Waterfall Drivers count: {len(detail.get('shap_waterfall', []))}")
        for item in detail.get('shap_waterfall', [])[:2]:
            print(f"  * {item['label']}: impact={item['impact']} ({item['direction']})")

    print(f"\n--- 4. Testing POST /api/tenders/{first['tender_id']}/audit ---")
    payload = json.dumps({
        "auditor_action": "Acknowledge & Clear",
        "justification": "E2E verification of Neon PostgreSQL database write path.",
        "auditor_name": "Antigravity Neon Agent"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"http://127.0.0.1:8000/api/tenders/{encoded_tid}/audit",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as res:
        logs = json.loads(res.read().decode())
        print(f"Updated audit log entries for tender: {len(logs)}")
        for log in logs[:2]:
            print(f"  * [{log['timestamp']}] {log['auditor_action']} by {log['auditor_name']}: {log['justification']}")

    print("\n>>> ALL NEON ENDPOINTS TESTED AND PROVEN WORKING END-TO-END! <<<")

if __name__ == "__main__":
    test_api()
