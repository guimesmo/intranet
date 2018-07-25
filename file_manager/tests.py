from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.crypto import get_random_string

from file_manager.models import user_directory_path, UserFile

User = get_user_model()


class UserFileModelTestCase(TestCase):
    def test_user_filepath(self):
        username = get_random_string(10)
        user = User.objects.create(username=username, password="lorem")

        obj = UserFile(owner=user)
        filename = "lorem.txt"
        formated_date = datetime.now().strftime("%Y/%m/%d")
        expected_path = 'uploads/{0}/{1}/{2}'.format(username, formated_date, filename)

        self.assertEqual(expected_path, user_directory_path(obj, filename))
