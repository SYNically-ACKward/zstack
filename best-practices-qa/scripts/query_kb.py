#!/usr/bin/env python3
"""
Query the Zscaler Best Practices Knowledge Base hosted on HuggingFace Spaces.
Uses the Gradio REST API to search ChromaDB vector embeddings.

Usage:
    python3 query_kb.py "What is the best practice for ZPA connector placement?"
    python3 query_kb.py --json "ZIA SSL inspection recommendations"
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

SPACE_URL = "https://pganti-zscaler-best-practices-qa.hf.space"
TIMEOUT = 120  # seconds — generous for cold starts


def query_run_predict(question: str) -> str:
    """Try the synchronous /run/predict endpoint first."""
    url = f"{SPACE_URL}/run/predict"
    payload = json.dumps({"data": [question]}).encode()
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=TIMEOUT)
    result = json.loads(resp.read().decode())
    data = result.get("data", [])
    return data[0] if data else ""


def query_call_predict(question: str) -> str:
    """Fallback: use the async /call/predict → event stream pattern."""
    # Step 1: initiate
    url = f"{SPACE_URL}/call/predict"
    payload = json.dumps({"data": [question]}).encode()
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=TIMEOUT)
    event_id = json.loads(resp.read().decode()).get("event_id")
    if not event_id:
        raise RuntimeError("No event_id returned from /call/predict")

    # Step 2: poll for result
    result_url = f"{SPACE_URL}/call/predict/{event_id}"
    for _ in range(30):
        time.sleep(2)
        try:
            resp = urllib.request.urlopen(result_url, timeout=TIMEOUT)
            body = resp.read().decode()
            # SSE format: lines like "event: complete\ndata: [...]"
            for line in body.strip().split("\n"):
                if line.startswith("data:"):
                    data = json.loads(line[5:].strip())
                    if isinstance(data, list) and data:
                        return data[0]
                    return str(data)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue  # not ready yet
            raise
    raise TimeoutError("Timed out waiting for KB response")


def query(question: str) -> str:
    """Query the KB, trying /run/predict first then falling back to /call/predict."""
    try:
        return query_run_predict(question)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return query_call_predict(question)


def main():
    parser = argparse.ArgumentParser(
        description="Query Zscaler Best Practices Knowledge Base"
    )
    parser.add_argument("question", help="Natural language question to ask the KB")
    parser.add_argument(
        "--json", action="store_true", help="Output raw JSON instead of plain text"
    )
    args = parser.parse_args()

    try:
        answer = query(args.question)
        if args.json:
            print(json.dumps({"question": args.question, "answer": answer}, indent=2))
        else:
            print(answer)
    except Exception as e:
        print(f"Error querying KB: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
