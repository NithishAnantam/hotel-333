from django.test import TestCase, RequestFactory
from unittest.mock import patch, mock_open
from django.urls import reverse
from hotel.views import login_activity_read, login_view

class LoginActivityReadTest(TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="username,email,password,role\nuser1,user1@example.com,pass123,user\n")
    def test_login_activity_read(self, mock_file):
        users = login_activity_read()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], ["user1", "user1@example.com", "pass123", "user"])



