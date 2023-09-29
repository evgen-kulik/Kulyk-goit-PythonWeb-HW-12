from unittest.mock import MagicMock, patch

import pytest

from src.database.models import User


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def test_repeat_create_user(client, user):
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed_email(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


def test_login_user(client, session, user):
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": "password"},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_login_wrong_email(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": "email", "password": user.get("password")},
    )
    assert response.status_code == 401, response.text


# -----------------------------------------------------------------------------------


@pytest.fixture
def mock_decode_refresh_token():
    with patch("src.services.auth.auth_service.decode_refresh_token") as mock:
        yield mock


@pytest.fixture
def mock_find_user_by_email():
    with patch("src.repository.users.find_user_by_email") as mock:
        yield mock


def test_refresh_token_valid_token(
    client, mock_decode_refresh_token, mock_find_user_by_email
):
    mock_decode_refresh_token.return_value = "example"
    mock_user = MagicMock()
    mock_user.refresh_token = "valid_refresh_token"
    mock_find_user_by_email.return_value = mock_user
    response = client.get(
        "/api/auth/refresh_token",
        headers={"Authorization": "Bearer valid_refresh_token"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid_token(
    client, mock_decode_refresh_token, mock_find_user_by_email
):
    mock_decode_refresh_token.return_value = "example"
    mock_user = MagicMock()
    mock_user.refresh_token = "valid_refresh_token"
    mock_find_user_by_email.return_value = mock_user
    response = client.get(
        "/api/auth/refresh_token", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid refresh token"}


@pytest.fixture
def mock_get_email_from_token():
    with patch("src.services.auth.auth_service.get_email_from_token") as mock:
        yield mock


def test_confirmed_email_non_user(
    client, mock_get_email_from_token, mock_find_user_by_email
):
    mock_get_email_from_token.return_value = "example@gmail.com"
    mock_find_user_by_email.return_value = None
    response = client.get("/api/auth/confirmed_email/{token_test}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Verification error"}


def test_confirmed_email_confirmed_user(
    client, mock_get_email_from_token, mock_find_user_by_email
):
    mock_get_email_from_token.return_value = "example@gmail.com"
    mock_find_user_by_email.return_value.confirmed = True
    response = client.get("/api/auth/confirmed_email/{token_test}")
    assert response.status_code == 200
    assert response.json() == {"message": "Your email is already confirmed"}


def test_confirmed_email_not_confirmed_user(
    client, mock_get_email_from_token, mock_find_user_by_email
):
    mock_get_email_from_token.return_value = "example@gmail.com"
    mock_find_user_by_email.return_value.confirmed = False
    response = client.get("/api/auth/confirmed_email/{token_test}")
    assert response.status_code == 200
    assert response.json() == {"message": "Email confirmed"}


def test_request_email_confirmed_user(client, mock_find_user_by_email):
    mock_find_user_by_email.return_value.confirmed = True
    response = client.post(
        "/api/auth/request_email", json={"email": "example@gmail.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Your email is already confirmed"}


# @pytest.fixture
# def mock_send_email():
#     with patch("src.services.email.send_email") as mock:
#         yield mock


def test_request_email_not_confirmed_user(client, mock_find_user_by_email):
    mock_find_user_by_email.return_value = MagicMock(
        email="example@gmail.com", confirmed=False
    )
    response = client.post(
        "/api/auth/request_email", json={"email": "example@gmail.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Check your email for confirmation"}
