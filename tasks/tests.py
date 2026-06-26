from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Task


def get_test_status():
    status_field = Task._meta.get_field("status")

    if status_field.choices:
        return status_field.choices[0][0]

    return "pending"


class TaskAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.task = Task.objects.create(
            title="Test task",
            description="Test description",
            status=get_test_status(),
            owner=self.user,
        )

        self.api_client = APIClient()

    def test_authenticated_user_can_list_tasks_from_api(self):
        self.api_client.force_authenticate(user=self.user)

        response = self.api_client.get("/api/tasks/")

        self.assertEqual(response.status_code, 200)

        titles = [item["title"] for item in response.data]
        self.assertIn("Test task", titles)

    def test_api_create_assigns_logged_in_user_as_owner(self):
        self.api_client.force_authenticate(user=self.user)

        response = self.api_client.post(
            "/api/tasks/",
            {
                "title": "New API task",
                "description": "Created from API",
                "status": get_test_status(),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        created_task = Task.objects.get(title="New API task")
        self.assertEqual(created_task.owner, self.user)