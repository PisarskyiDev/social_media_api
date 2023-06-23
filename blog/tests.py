from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from PIL import Image
import io

from blog.serializers import PostSerializer
from blog.models import Post, Commentary
from user.models import User


class TestPostSerializer(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        # Create a dummy (blank) image file
        image = Image.new("RGB", (100, 100))
        file = io.BytesIO()
        image.save(file, "JPEG")
        file.name = "test.jpg"
        file.seek(0)

        self.image = SimpleUploadedFile(
            name="test.jpg", content=file.read(), content_type="image/jpeg"
        )

        self.post = Post.objects.create(
            owner=self.user,
            title="Test post",
            content="This is a test post.",
            image=self.image,
        )

    def test_update_post(self):
        # Ensure the post has an image to start
        self.assertIsNotNone(self.post.image)

        serializer = PostSerializer(
            instance=self.post,
            data={
                "email": "test@test.com",
                "title": "Updated test post",
                "content": "This is an updated test post.",
                # Leave out the 'image' field
            },
            partial=True,
        )
        self.assertTrue(serializer.is_valid())

        serializer.save()
        updated_post = Post.objects.get(pk=self.post.id)

        # Check that the post has been updated but the image is still there
        self.assertEqual(updated_post.title, "Updated test post")
        self.assertEqual(updated_post.content, "This is an updated test post.")
        self.assertIsNotNone(updated_post.image)

    def tearDown(self):
        # Delete the created objects
        self.user.delete()
        self.post.delete()


class TestCommentaryViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            email="test@test.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        # Create a test post
        self.post = Post.objects.create(
            owner=self.user,
            title="Test post",
            content="This is a test post.",
        )

    def test_create_commentary(self):
        # Test creating a commentary
        response = self.client.post(
            f"/api/blog/posts/{self.post.id}/commentary/",
            {"content": "This is a test comment."},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Commentary.objects.count(), 1)
        self.assertEqual(Commentary.objects.first().content, "This is a test comment.")

    def test_list_commentaries(self):
        # Create a test commentary
        Commentary.objects.create(
            owner=self.user,
            post=self.post,
            content="This is a test comment.",
        )

        # Test listing commentaries
        response = self.client.get(f"/api/blog/posts/{self.post.id}/commentary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_update_commentary(self):
        # Create a test commentary
        commentary = Commentary.objects.create(
            owner=self.user,
            post=self.post,
            content="This is a test comment.",
        )

        # Test updating a commentary
        response = self.client.put(
            f"/api/blog/posts/{self.post.id}/commentary/{commentary.id}/",
            {"content": "This is an updated comment."},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        commentary.refresh_from_db()
        self.assertEqual(commentary.content, "This is an updated comment.")

    def tearDown(self):
        # Clean up the created objects
        self.user.delete()
        self.post.delete()
