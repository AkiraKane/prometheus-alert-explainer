# Prometheus Alert Explainer 🚨🤖

A webhook server that intercepts Prometheus Alertmanager alerts and enriches them with AI-powered explanations and remediation steps.

## Quick Start

```bash
# Process alerts from file
python src/main.py alert.json

# Start webhook server
python src/main.py --webhook --port 9100
```

## Alertmanager Config

```yaml
receivers:
  - name: ai-explainer
    webhook_configs:
      - url: 'http://ai-explainer:9100/alerts'
        send_resolved: true
```

## Features

- Alertmanager webhook integration
- AI-powered alert explanations
- Remediation suggestions
- Multiple alert support

## Requirements

- Python 3.11+
- Ollama or OPENAI_API_KEY

## Interview Talking Points

- Alert enrichment pattern
- Prometheus ecosystem integration
- AI-powered incident response

## License

MIT
