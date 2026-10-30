from fastapi.testclient import TestClient
from main import app


def test_analytics_status():
    with TestClient(app) as client:
        response = client.get("/analytics")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
def test_order_pagination():
    with TestClient(app) as client:
        response = client.get("/orders?limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2

def test_create_order_validation_error():
    with TestClient(app) as client:
        bad_payload = {
            "item": "Бракованный товар",
            "price": -500,
            "client_id": 1
        }
        response = client.post("/orders", json=bad_payload)
        assert response.status_code == 422
    
