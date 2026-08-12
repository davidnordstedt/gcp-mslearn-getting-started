"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client, app_with_fresh_activities):
    """
    Test that GET /activities returns all available activities.
    
    AAA Pattern:
    - Arrange: TestClient ready, fresh activities loaded
    - Act: Send GET request to /activities
    - Assert: Verify 200 status, all activities returned with correct structure
    """
    # Arrange: Setup complete (done by fixtures)
    
    # Act: Send GET request
    response = client.get("/activities")
    
    # Assert: Verify response
    assert response.status_code == 200
    activities_data = response.json()
    
    # Verify all activities are returned
    assert "Chess Club" in activities_data
    assert "Programming Class" in activities_data
    assert "Gym Class" in activities_data
    assert "Basketball Team" in activities_data
    assert "Tennis Club" in activities_data
    assert "Art Studio" in activities_data
    assert "Drama Club" in activities_data
    assert "Debate Team" in activities_data
    assert "Science Club" in activities_data


def test_activity_structure_is_correct(client, app_with_fresh_activities):
    """
    Test that each activity has the correct structure and fields.
    
    AAA Pattern:
    - Arrange: TestClient ready, fresh activities loaded
    - Act: Send GET request to /activities
    - Assert: Verify each activity has required fields with correct types
    """
    # Arrange: Setup complete (done by fixtures)
    
    # Act: Send GET request
    response = client.get("/activities")
    
    # Assert: Verify activity structure
    activities_data = response.json()
    
    for activity_name, activity_details in activities_data.items():
        # Verify all required fields are present
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        
        # Verify field types
        assert isinstance(activity_details["description"], str)
        assert isinstance(activity_details["schedule"], str)
        assert isinstance(activity_details["max_participants"], int)
        assert isinstance(activity_details["participants"], list)
        
        # Verify participants are email strings
        for participant in activity_details["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation
