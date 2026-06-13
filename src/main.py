#!/usr/bin/env python3
"""Prometheus Alert Explainer — enrich Prometheus alerts with AI explanations."""

import argparse
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

from alert_handler import parse_alertmanager_payload
from llm import explain_alert, check_ollama


def main():
    parser = argparse.ArgumentParser(description="Enrich Prometheus alerts with AI explanations")
    parser.add_argument("file", nargs="?", help="Alertmanager JSON payload")
    parser.add_argument("--webhook", action="store_true", help="Start webhook server")
    parser.add_argument("--port", type=int, default=9100, help="Webhook port")
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()

    if args.webhook:
        _start_server(args)
        return

    if not args.file:
        parser.error("Must specify file or use --webhook")

    content = sys.stdin.read() if args.file == "-" else open(args.file).read()
    alerts = parse_alertmanager_payload(json.loads(content))

    if not alerts:
        print("No alerts found.")
        return

    print(f"Alerts: {len(alerts)}\n")

    for alert in alerts:
        print(f"## {alert.name} ({alert.severity})")
        print(f"Status: {alert.status}")
        print(f"Summary: {alert.summary}\n")

        if args.summary:
            continue

        if not check_ollama(args.ollama_url):
            print("Ollama not available, attempting OpenAI fallback (if configured)...")

        print("Analyzing...")
        try:
            print(explain_alert(alert.to_prompt(), args.ollama_url, args.model))
        except ConnectionError as e:
            print(f"Error: {e}")
        print()


def _start_server(args):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            alerts = parse_alertmanager_payload(json.loads(body))
            for alert in alerts:
                print(f"Alert: {alert.name} ({alert.severity})")
                try:
                    print(explain_alert(alert.to_prompt(), args.ollama_url, args.model))
                except Exception:
                    pass
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
    HTTPServer(("0.0.0.0", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
