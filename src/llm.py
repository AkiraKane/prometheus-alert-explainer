"""LLM client for explaining Prometheus alerts."""

import json
import urllib.request
import urllib.error
import os


SYSTEM_PROMPT = """You are an expert SRE explaining Prometheus alerts.

Given an alert, explain what it means and provide remediation steps.

Rules:
- Explain in plain English
- Provide specific commands to diagnose and fix
- Use markdown formatting
- Be concise and actionable"""


def explain_alert(alert_prompt: str, ollama_url: str = "http://localhost:11434", model: str = "llama3.2") -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Explain this alert:\n\n{alert_prompt}"},
        ],
        "stream": False,
        "options": {"temperature": 0.3},
    }
    try:
        req = urllib.request.Request(f"{ollama_url}/api/chat", data=json.dumps(payload).encode(),
                                    headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())["message"]["content"].strip()
    except urllib.error.URLError:
        if os.environ.get("OPENAI_API_KEY"):
            return _openai(alert_prompt, os.environ["OPENAI_API_KEY"])
        raise ConnectionError(f"Cannot connect to Ollama at {ollama_url}")


def _openai(prompt: str, key: str) -> str:
    payload = {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}], "temperature": 0.3}
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=json.dumps(payload).encode(),
                                headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"].strip()


def check_ollama(url: str = "http://localhost:11434") -> bool:
    try:
        with urllib.request.urlopen(f"{url}/api/tags", timeout=5) as resp:
            return resp.status == 200
    except:
        return False
