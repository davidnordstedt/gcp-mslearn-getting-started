"""
Tests for the DELETE /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_unregister_student_success(client, app_with_fresh_activities):
    """
    Test successful unregistration of a student from an activity.
    
    AAA Pattern:
    - Arrange: Fresh activities, email is registered in activity
    - Act: DELETE signup request
    - Assert: 200 status, message returned, participant removed from activity list
    """
    # Arrange: Get existing participant
    test_activity = "Chess Club"
    test_email = "michael@mergington.edu"  # Already in Chess Club
    
    activities_before = client.get("/activities").json()
    assert test_email in activities_before[test_activity]["participants"]
    
    # Act: Send DELETE unregister request
    response = client.delete(
        f"/activities/{test_activity}/signup",
        params={"email": test_email}
    )
    
    # Assert: Verify successful unregistration
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert test_activity in data["message"]
    
    # Verify participant was removed from activity
    activities_after = client.get("/activities").json()
    assert test_email not in activities_after[test_activity]["participants"]


def test_unregister_unregistered_student_returns_404(client, app_with_fresh_activities):
    """
    Test that attempting to unregister a non-registered student returns 404.
    
    AAA Pattern:
    - Arrange: Fresh activities, email not in activity's participant list
    - Act: DELETE signup with non-participant email
    - Assert: 404 status, error detail matches "not registered"
    """
    # Arrange: Setup test data
    test_activity = "Tennis Club"
    test_email = "notregistered@mergington.edu"  # Not in any activity
    
    # Act: Attempt to unregister non-registered student
    response = client.delete(
        f"/activities/{test_activity}/signup",
        params={"email": test_email}
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower()


def test_unregister_nonexistent_activity_returns_404(client, app_with_fresh_activities):
    """
    Test that attempting to unregister from a non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Valid email, invalid activity name
    - Act: DELETE signup with non-existent activity
    - Assert: 404 status, error detail matches "Activity not found"
    """
    # Arrange: Setup test data
    test_email = "student@mergington.edu"
    invalid_activity = "Nonexistent Club"
    
    # Act: Attempt to unregister from non-existent activity
    response = client.delete(
        f"/activities/{invalid_activity}/signup",
        params={"email": test_email}
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_decreases_participant_count(client, app_with_fresh_activities):
    """
    Test that unregister correctly updates the participant count.
    
    AAA Pattern:
    - Arrange: Fresh activities, record initial participant count
    - Act: DELETE unregister for existing participant
    - Assert: Participant count decreased by 1
    """
    # Arrange: Get initial participant count
    test_activity = "Drama Club"
    test_email = "marcus@mergington.edu"  # Already in Drama Club
    
    activities_before = client.get("/activities").json()
    assert test_email in activities_before[test_activity]["participants"]
    initial_count = len(activities_before[test_activity]["participants"])
    
    # Act: Unregister student
    response = client.delete(
        f"/activities/{test_activity}/signup",
        params={"email": test_email}
    )
    assert response.status_code == 200
    
    # Assert: Participant count decreased
    activities_after = client.get("/activities").json()
    final_count = len(activities_after[test_activity]["participants"])
    assert final_count == initial_count - 1


def test_unregister_multiple_participants(client, app_with_fresh_activities):
    """
    Test that multiple participants can be unregistered from the same activity.
    
    AAA Pattern:
    - Arrange: Fresh activities, identify multiple participants in activity
    - Act: DELETE unregister requests for multiple students
    - Assert: All students removed successfully from activity
    """
    # Arrange: Get existing participants
    test_activity = "Science Club"
    activities_before = client.get("/activities").json()
    initial_participants = activities_before[test_activity]["participants"].copy()
    
    # Take first two participants for testing
    students_to_remove = initial_participants[:2]
    
    # Act: Unregister multiple students
    for student_email in students_to_remove:
        response = client.delete(
            f"/activities/{test_activity}/signup",
            params={"email": student_email}
        )
        # Assert: Each unregister succeeds
        assert response.status_code == 200
    
    # Assert: All students are removed from the activity
    activities_after = client.get("/activities").json()
    for student_email in students_to_remove:
        assert student_email not in activities_after[test_activity]["participants"]


def test_reregister_after_unregister(client, app_with_fresh_activities):
    """
    Test that a student can re-register after unregistering from an activity.
    
    AAA Pattern:
    - Arrange: Fresh activities, existing participant
    - Act: DELETE unregister, then POST signup with same email
    - Assert: Student successfully re-registered
    """
    # Arrange: Get existing participant
    test_activity = "Basketball Team"
    test_email = "alex@mergington.edu"  # Already in Basketball Team
    
    activities_before = client.get("/activities").json()
    assert test_email in activities_before[test_activity]["participants"]
    
    # Act: Unregister student
    response = client.delete(
        f"/activities/{test_activity}/signup",
        params={"email": test_email}
    )
    assert response.status_code == 200
    
    # Verify student is unregistered
    activities_after_delete = client.get("/activities").json()
    assert test_email not in activities_after_delete[test_activity]["participants"]
    
    # Act: Re-register the same student
    response = client.post(
        f"/activities/{test_activity}/signup",
        params={"email": test_email}
    )
    
    # Assert: Student successfully re-registered
    assert response.status_code == 200
    activities_after_signup = client.get("/activities").json()
    assert test_email in activities_after_signup[test_activity]["participants"]
