import unittest
from unittest.mock import MagicMock, patch

from mysite.users.views import UserView


class TestUserView(unittest.TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.request.params = {'msg': 'test'}
        self.view = UserView(MagicMock(), self.request)

    @patch("mysite.users.views.HTTPFound")
    def test_user(self, mock_http_found):
        self.view.delete()
        print("TESTINGO")
        mock_http_found.assert_called_once()

    @patch("mysite.users.views.User.get_all")
    def test_list(self, mock_get_all):
        mock_get_all.return_value = []
        print("TESTLIST")
        result = self.view.list()

        self.assertEqual(result, [])

