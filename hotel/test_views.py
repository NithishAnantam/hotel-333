import pytest
import csv
from unittest.mock import patch, mock_open
from django.test import RequestFactory
from django.shortcuts import reverse
# from hotel.views import login_activity_read, login_view  # Replace with your actual app
from hotel.views import login_activity_read, login_view

# Mock settings.BASE_DIR
@pytest.fixture
def mock_base_dir(tmp_path, monkeypatch):
    fake_base_dir = tmp_path / "csv_data"
    fake_base_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("hotel.settings.BASE_DIR", fake_base_dir)
    return fake_base_dir

# Test login_activity_read
@patch("builtins.open", new_callable=mock_open, read_data="username,email,password,role\nuser1,user1@example.com,pass123,user\nadmin1,admin@example.com,admin123,admin\n")
def test_login_activity_read(mock_file, mock_base_dir):
    users = login_activity_read()
    assert len(users) == 2  # Ensure two users are loaded
    assert users[0] == ["user1", "user1@example.com", "pass123", "user"]
    assert users[1] == ["admin1", "admin@example.com", "admin123", "admin"]

@patch("builtins.open", side_effect=FileNotFoundError)
def test_login_activity_read_file_not_found(mock_file, mock_base_dir):
    users = login_activity_read()
    assert users == []  # Expect empty list when file is missing

# Test login_view
@pytest.mark.django_db  # Ensure Django test database is used
@patch("hotel.views.login_activity_read", return_value=[["user1", "user1@example.com", "pass123", "user"]])
def test_login_view_success(mock_login_activity_read):
    factory = RequestFactory()
    request = factory.post("/login/", {"username": "user1", "password": "pass123"})

    response = login_view(request)
    assert response.status_code == 302  # Redirect expected
    assert response.url == reverse("user_dashboard")

@pytest.mark.django_db
@patch("hotel.views.login_activity_read", return_value=[])
def test_login_view_no_users(mock_login_activity_read):
    factory = RequestFactory()
    request = factory.post("/login/", {"username": "user1", "password": "pass123"})

    response = login_view(request)
    assert response.status_code == 200
    assert b"No users registered." in response.content

@pytest.mark.django_db
@patch("hotel.views.login_activity_read", return_value=[["user1", "user1@example.com", "pass123", "user"]])
def test_login_view_invalid_credentials(mock_login_activity_read):
    factory = RequestFactory()
    request = factory.post("/login/", {"username": "wrong", "password": "wrongpass"})

    response = login_view(request)
    assert response.status_code == 200
    assert b"Invalid username or password." in response.content
