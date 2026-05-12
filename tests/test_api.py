from app import app


def test_scan_endpoint():
    client = app.test_client()
    response = client.post("/api/scan")
    assert response.status_code == 200
    assert response.is_json


def test_results_endpoint():
    client = app.test_client()
    client.post("/api/scan")
    response = client.get("/api/results")
    assert response.status_code == 200
    assert response.is_json
