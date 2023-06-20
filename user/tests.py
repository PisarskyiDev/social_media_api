import tempfile
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.core.files.uploadedfile import SimpleUploadedFile

from user.serializers import UserSerializer

User = get_user_model()


def create_test_image():
    image = Image.new("RGB", (100, 100))
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(temp_file)
    temp_file.seek(0)
    return temp_file


class UserAvatarTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com", password="password123", sex="male"
        )
        self.client.force_authenticate(user=self.user)

        temp_image = create_test_image()
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=temp_image.read(),
            content_type="image/jpeg",
        )
        temp_image.close()

    def test_can_upload_avatar(self):
        data = {
            "email": "test@test.com",
            "password": "password123",
            "avatar": self.image,
        }
        response = self.client.put(
            reverse("user:my_profile"),
            data,
            format="multipart",
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        self.assertIsNotNone(self.user.avatar)


class CreateUserViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {"email": "test@test.com", "password": "password123", "sex": "male"}

    def test_can_create_user(self):
        response = self.client.post(reverse("user:create_profile"), self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@test.com")


class UserViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="password123",
            sex="male",
        )
        self.client.force_authenticate(user=self.user)
        self.data = {
            "email": "test@test.com",
            "sex": "female",
            "password": "password123",
        }

    def test_can_retrieve_user(self):
        response = self.client.get(
            reverse("user:profile-detail", kwargs={"pk": self.user.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, UserSerializer(self.user).data)

    def test_can_update_my_profile(self):
        response = self.client.put(reverse("user:my_profile"), self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        self.assertEqual(self.user.email, "test@test.com")
        self.assertEqual(self.user.sex, "female")

    def test_regular_user_cannot_update_other_users(self):
        other_user = User.objects.create_user(
            email="other@test.com",
            password="password123",
            sex="male",
            is_staff=True,
            is_superuser=True,
        )
        self.data = {
            "email": "updated@test.com",
            "sex": "unknown",
            "password": "password123",
        }
        response = self.client.put(
            reverse("user:profile-detail", kwargs={"pk": other_user.pk}), self.data
        )
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        other_user.refresh_from_db()

        self.assertNotEqual(other_user.email, "updated@test.com")
        self.assertNotEqual(other_user.sex, "female")

    def test_can_list_users(self):
        User.objects.create_user(
            email="another@test.com", password="password123", sex="female"
        )
        response = self.client.get(reverse("user:profile-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
