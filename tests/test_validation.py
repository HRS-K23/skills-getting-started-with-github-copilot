def test_signup_missing_email_returns_422(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"][-1] == "email" for error in errors)


def test_remove_missing_email_returns_422(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"][-1] == "email" for error in errors)
