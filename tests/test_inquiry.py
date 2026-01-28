"""
Tests for inquiry API endpoints.
"""
import pytest


def test_submit_inquiry(client):
    """Test submitting an inquiry."""
    response = client.post(
        "/inquiry/submit",
        json={
            "question": "What is the meaning of life?",
            "inquiry_type": "wisdom"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "inquiry_id" in data
    assert data["question"] == "What is the meaning of life?"
    assert "wisdom" in data
    assert "answer" in data["wisdom"]


def test_submit_inquiry_invalid(client):
    """Test submitting an invalid inquiry."""
    response = client.post(
        "/inquiry/submit",
        json={
            "question": "",
            "inquiry_type": "general"
        }
    )
    assert response.status_code == 400


def test_get_inquiry_history(client):
    """Test retrieving inquiry history."""
    # First submit an inquiry
    submit_response = client.post(
        "/inquiry/submit",
        json={
            "question": "Test question",
            "inquiry_type": "general"
        }
    )
    inquiry_id = submit_response.json()["inquiry_id"]
    
    # Then retrieve it
    response = client.get(f"/inquiry/history/{inquiry_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == inquiry_id
    assert data["question"] == "Test question"


def test_get_inquiry_not_found(client):
    """Test retrieving non-existent inquiry."""
    response = client.get("/inquiry/history/nonexistent-id")
    assert response.status_code == 404
