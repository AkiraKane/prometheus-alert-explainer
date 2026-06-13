"""Handle Prometheus Alertmanager webhooks."""

import json
from dataclasses import dataclass, field


@dataclass
class Alert:
    """A Prometheus alert."""
    name: str
    status: str
    severity: str
    description: str
    summary: str
    labels: dict[str, str] = field(default_factory=dict)
    annotations: dict[str, str] = field(default_factory=dict)

    def to_prompt(self) -> str:
        return f"""Alert: {self.name}
Status: {self.status}
Severity: {self.severity}
Summary: {self.summary}
Description: {self.description}
Labels: {json.dumps(self.labels)}"""


def parse_alertmanager_payload(payload: dict) -> list[Alert]:
    """Parse Alertmanager webhook payload."""
    alerts = []
    for alert_data in payload.get("alerts", []):
        labels = alert_data.get("labels", {})
        annotations = alert_data.get("annotations", {})
        alerts.append(Alert(
            name=labels.get("alertname", "Unknown"),
            status=alert_data.get("status", "firing"),
            severity=labels.get("severity", "warning"),
            description=annotations.get("description", ""),
            summary=annotations.get("summary", ""),
            labels=labels,
            annotations=annotations,
        ))
    return alerts
