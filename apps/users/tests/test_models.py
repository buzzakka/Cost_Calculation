import tempfile
import shutil

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CustomUserModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.small_png = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        cls.uploaded_image = SimpleUploadedFile(
            name='small.png',
            content=cls.small_png,
            content_type='image/gif'
        )

        cls.user = User.objects.create(
            username='user',
            email='email@mail.ru',
            first_name='Marsel',
            last_name='Rashitov',
            image=cls.uploaded_image
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_is_correct_new_user(self):
        self.assertEqual(self.user.username, 'user')
        self.assertEqual(self.user.email, 'email@mail.ru')
        self.assertEqual(self.user.first_name, 'Marsel')
        self.assertEqual(self.user.last_name, 'Rashitov')
        self.assertEqual(self.user.image.url, '/small.png')
