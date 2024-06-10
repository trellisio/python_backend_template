import os

import requests


class TestMonitoringRouter:
    service_url = os.environ.get("SERVER_URL")

    def test_healthz(self):
        resp = requests.get(f"{self.service_url}/v1/healthz")
        assert resp.status_code == 204

    def test_metrics(self):
        resp = requests.get(f"{self.service_url}/v1/metrics")
        assert resp.status_code == 204
