"""
Pytest configuration and fixtures for Mergington High School API tests.
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient instance for making requests to the app.
    """
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Provide a fresh deep copy of activities for each test to ensure isolation.
    This prevents test pollution where one test's modifications affect another.
    """
    return copy.deepcopy(activities)


@pytest.fixture
def app_with_fresh_activities(monkeypatch, fresh_activities):
    """
    Monkeypatch the app's activities module with a fresh copy for the test.
    This ensures each test gets an isolated, unmodified copy of activities data.
    """
    import src.app
    monkeypatch.setattr(src.app, "activities", fresh_activities)
    return app
