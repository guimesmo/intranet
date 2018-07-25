from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import SimpleUploadedFile

from file_manager.models import UserFile
from user_profile.models import UserProfile

User = get_user_model()


class UserProfileModelTest(TestCase):
    def test_get_number_of_user_files(self):
        user = User.objects.create(username=get_random_string(10), password="lorem")
        UserProfile.objects.create(user=user, profile_type=101, full_address="", city_state="city_state")
        file_contents = 'lorem ipsum dolor sit amet'
        uploaded_file = SimpleUploadedFile('lorem.txt', file_contents.encode('utf-8'))
        self.assertEqual(user.userprofile.get_number_of_user_files(), 0)

        UserFile.objects.create(owner=user, upload=uploaded_file)
        self.assertEqual(user.userprofile.get_number_of_user_files(), 1)

    def test_get_volume_of_user_files(self):
        user = User.objects.create(username=get_random_string(10), password="lorem")
        UserProfile.objects.create(user=user, profile_type=101, full_address="", city_state="city_state")
        file_contents = 'lorem ipsum dolor sit amet'
        uploaded_file = SimpleUploadedFile('lorem.txt', file_contents.encode('utf-8'))
        UserFile.objects.create(owner=user, upload=uploaded_file)
        self.assertAlmostEqual(user.userprofile.get_volume_of_user_files(),
                               len(file_contents.encode('utf-8')) / (1024 * 1024))
