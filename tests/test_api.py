from app import app


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200


def test_scan_endpoint():
    client = app.test_client()
    response = client.get("/scan")
    assert response.status_code == 200
