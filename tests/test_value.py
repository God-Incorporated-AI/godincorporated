"""
Tests for value API endpoints.
"""
import pytest


def test_contribute(client):
    """Test making a contribution."""
    response = client.post(
        "/value/contribute",
        json={
            "amount": 10.0,
            "currency": "USD",
            "message": "Thank you for the wisdom"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "transaction_id" in data
    assert data["amount"] == 10.0
    assert data["status"] in ["completed", "acknowledged"]


def test_get_transaction(client):
    """Test retrieving transaction details."""
    # First make a contribution
    contribute_response = client.post(
        "/value/contribute",
        json={
            "amount": 5.0,
            "currency": "USD"
        }
    )
    transaction_id = contribute_response.json()["transaction_id"]
    
    # Then retrieve it
    response = client.get(f"/value/transaction/{transaction_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["amount"] == 5.0


def test_value_status(client):
    """Test value module status."""
    response = client.get("/value/status")
    assert response.status_code == 200
    data = response.json()
    assert "available" in data
    assert "payments_enabled" in data
