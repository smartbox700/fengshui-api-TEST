import requests
import pytest

BASE_URL = "https://fengshui-api.onrender.com"

def test_root_health():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert "ok" in r.json()

    h = requests.get(f"{BASE_URL}/health")
    assert h.status_code == 200
    assert h.json().get("status") == "ok"

def test_evaluate_valid():
    payload = {
        "lat": 37.5665,
        "lon": 126.9780,
        "features": {"direction_south": 1, "river_distance": 0.5, "road_distance": 0.3}
    }
    r = requests.post(f"{BASE_URL}/evaluate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "total" in body and 0 <= body["total"] <= 100
    assert body["grade"] in ["A", "B", "C", "N/A"]

def test_evaluate_invalid():
    payload = {"lat": 999, "lon": 999, "features": {}}
    r = requests.post(f"{BASE_URL}/evaluate", json=payload)
    assert r.status_code == 400
    assert "error" in r.json()
