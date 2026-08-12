"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_new_student_success(client, app_with_fresh_activities):
    """
    Test successful signup of a new student for an activity.
    
    AAA Pattern:
    - Arrange: Fresh activities, new email not in any activity
    - Act: Send POST signup request with valid activity & email
    - Assert: 200 status, message returned, participant added to activity list
    """
    # Arrange: Setup test data
    test_email = "newstudent@mergington.edu"
    test_activity = "Chess Club"
    
    # Act: Send POST signup request
    response = client.post(
        f"/activities/{test_activity}/signup",
        params={"email": test_email}
    )
    
    # Assert: Verify successful signup
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert test_activity in data["message"]
    
    # Verify participant was added to activity
    activities = client.get("/activities").json()
    assert test_email in activities[test_activity]["participants"]


def test_signup_duplicate_student_returns_400(client, app_with_fresh_activities):
    """
    Test that attempting to signup an already registered student returns 400.
    
    AAA Pattern:
    - Arrange: Fresh activities, email already in activity
    - Act: POST signup with existing participant email
    - Assert: 400 status, error detail matches "already signed up"
    """
    # Arrange: Get existing participant from fixture
    test_activity = "Chess Club"
    test_email = "michael@mergington.edu"  # Already in Chess Club
    
    # Verify the email is actually in the activity
    activities_before = client.get("/activities").json()
    assert test_email in activities_before[test_activity]["participants"]
    
    # Act: Attempt to signup with duplicate email
    response = client.post(
        f"/activities/{test_activity}/signup",
        params={"email": test_email}
    )
    
    # Assert: Verify 400 error
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client, app_with_fresh_activities):
    """
    Test that attempting to signup for a non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Valid email, invalid activity name
    - Act: POST signup with non-existent activity
    - Assert: 404 status, error detail matches "Activity not found"
    """
    # Arrange: Setup test data
    test_email = "newstudent@mergington.edu"
    invalid_activity = "Nonexistent Club"
    
    # Act: Attempt to signup for non-existent activity
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": test_email}
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_multiple_students_to_same_activity(client, app_with_fresh_activities):
    """
    Test that multiple different students can signup for the same activity.
    
    AAA Pattern:
    - Arrange: Fresh activities, prepare multiple new emails
    - Act: POST signup requests for multiple students to same activity
    - Assert: All students added successfully to activity
    """
    # Arrange: Setup test data
    test_activity = "Art Studio"
    students = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    # Act: Signup multiple students
    for student_email in students:
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": student_email}
        )
        # Assert: Each signup succeeds
        assert response.status_code == 200
    
    # Assert: All students are in the activity
    activities = client.get("/activities").json()
    for student_email in students:
        assert student_email in activities[test_activity]["participants"]


def test_signup_increases_participant_count(client, app_with_fresh_activities):
    """
    Test that signup correctly updates the participant count.
    
    AAA Pattern:
    - Arrange: Fresh activities, record initial participant count
    - Act: POST signup for new student
    - Assert: Participant count increased by 1
    """
    # Arrange: Get initial participant count
    test_activity = "Drama Club"
    test_email = "newactor@mergington.edu"
    
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before[test_activity]["participants"])
    
    # Act: Signup new student
    response = client.post(
        f"/activities/{test_activity}/signup",
        params={"email": test_email}
    )
    assert response.status_code == 200
    
    # Assert: Participant count increased
    activities_after = client.get("/activities").json()
    final_count = len(activities_after[test_activity]["participants"])
    assert final_count == initial_count + 1
