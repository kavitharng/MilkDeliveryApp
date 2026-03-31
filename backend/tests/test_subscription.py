from fastapi.testclient import TestClient
from app.main import app


def test_add_subscription():
    with TestClient(app) as client:
        response = client.post("/api/vendors", json={"name": "Anand"})
        vendor_id = response.json()["id"]
        response = client.post("/api/customers", json={"name": "Anjali"})
        customer_id = response.json()["id"]
        
        print(customer_id, vendor_id)
        response = client.post(f"/api/customers/{customer_id}/subscription", json={"vendor_id": vendor_id})
        print(response.json())

        response = client.get(f"/api/customers/{customer_id}")
        updated_customer = response.json()
        print(updated_customer)

    assert updated_customer["name"] == "Anjali"
    assert len(updated_customer["vendors"]) == 1
    assert updated_customer["vendors"][0]["name"] == "Anand"

