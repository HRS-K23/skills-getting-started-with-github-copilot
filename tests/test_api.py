def test_root_redirects_to_static_index(client):
    # Arrange
    endpoint = "/"

    # Act
    response = client.get(endpoint, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_shape(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert len(payload) == 9

    required_fields = {"description", "schedule", "max_participants", "participants"}
    for details in payload.values():
        assert required_fields.issubset(details.keys())
        assert isinstance(details["participants"], list)


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
    state_after = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert state_after[activity_name]["participants"].count(new_email) == 1


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    missing_activity = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{missing_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_succeeds(client):
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email_to_remove},
    )
    state_after = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert email_to_remove not in state_after[activity_name]["participants"]


def test_remove_participant_unknown_activity_returns_404(client):
    # Arrange
    missing_activity = "Unknown Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{missing_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_non_member_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email_not_member = "notmember@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email_not_member},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_then_get_reflects_state_change(client):
    # Arrange
    activity_name = "Debate Team"
    new_email = "statecheck@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert activities_response.status_code == 200
    assert new_email in activities_response.json()[activity_name]["participants"]


def test_remove_then_get_reflects_state_change(client):
    # Arrange
    activity_name = "Drama Club"
    existing_email = "charlotte@mergington.edu"

    # Act
    remove_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert remove_response.status_code == 200
    assert activities_response.status_code == 200
    assert existing_email not in activities_response.json()[activity_name]["participants"]
