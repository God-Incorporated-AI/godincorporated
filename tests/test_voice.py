"""
Tests for voice API endpoints.
"""
import pytest


def test_voice_status(client):
    """Test voice module status."""
    response = client.get("/voice/status")
    assert response.status_code == 200
    data = response.json()
    assert "available" in data
    assert "tts_available" in data
    assert "stt_available" in data


def test_process_voice_no_audio(client):
    """Test processing voice without audio."""
    # This might return 503 if voice is not available
    response = client.post("/voice/process")
    # Accept both 200 (if voice is available) and 503 (if not)
    assert response.status_code in [200, 503]
