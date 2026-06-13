import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import pytest
from alert_handler import Alert, parse_alertmanager_payload


class TestAlert:
    def test_to_prompt(self):
        alert = Alert(name="HighCPU", status="firing", severity="critical", description="CPU > 90%", summary="High CPU")
        prompt = alert.to_prompt()
        assert "HighCPU" in prompt
        assert "critical" in prompt


class TestParseAlertmanagerPayload:
    def test_empty(self):
        assert parse_alertmanager_payload({}) == []

    def test_valid(self):
        payload = {"alerts": [{"status": "firing", "labels": {"alertname": "Test", "severity": "warning"}, "annotations": {"summary": "Test alert"}}]}
        alerts = parse_alertmanager_payload(payload)
        assert len(alerts) == 1
        assert alerts[0].name == "Test"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
