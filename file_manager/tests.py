import string
import random
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from file_manager.models import user_directory_path, UserFile

User = get_user_model()


class UserFileModelTestCase(TestCase):
    def test_user_filepath(self):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        user = User.objects.create(username=username, password="lorem")

        obj = UserFile(owner=user)
        filename = "lorem.txt"
        formated_date = datetime.now().strftime("%Y/%m/%d")
        expected_path = 'uploads/{0}/{1}/{2}'.format(username, formated_date, filename)

        self.assertEqual(expected_path, user_directory_path(obj, filename))
