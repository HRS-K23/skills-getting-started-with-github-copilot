from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    """Provide a TestClient for API tests."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activities state before/after each test."""
    # Arrange
    original_state = deepcopy(activities)

    yield

    # Assert cleanup
    activities.clear()
    activities.update(original_state)
