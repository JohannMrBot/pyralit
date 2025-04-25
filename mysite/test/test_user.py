import unittest
from unittest.mock import MagicMock, patch

from mysite.users.views import UserView


class TestUserView(unittest.TestCase):
    def setUp(self):
        self.view = UserView(MagicMock(), MagicMock())

    @patch("mysite.users.views.HTTPFound")
    def test_user(self, mock_http_found):
        self.view.delete()
        print("TESTINGO")
        mock_http_found.assert_called_once()


