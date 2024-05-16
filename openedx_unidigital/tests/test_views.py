"""Test cases for the views of the openedx_unidigital app."""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from openedx_unidigital.models import CourseTeamInstructor

User = get_user_model()


class CourseTeamInstructorAPITestCase(APITestCase):
    """Test suite for the CourseTeamInstructor API."""

    patch_permissions = patch(
        "openedx_unidigital.api.v1.permissions.IsCourseInstructor.has_permission",
        return_value=True,
    )

    def setUp(self):
        self.user = User.objects.create_user(username="john_doe", password="123456")
        self.client.force_authenticate(user=self.user)
        self.course_team_instructor_data = {
            "course_team_id": 1,
            "course_team_name": "team_name",
            "user": "john_doe",
        }
        self.invalid_course_team_instructor_data = {"course_team_id": 2, "username": ""}
        self.url = reverse("openedx-unidigital-api:v1:course-team-instructor")

    @patch_permissions
    def test_create_course_team_instructor(self, _):
        """Test creating a new course team instructor.

        Expected behavior:
        - The response status code should be 201.
        - The course team instructor should be created.
        - The course team instructor username should be john_doe.
        """
        response = self.client.post(
            self.url, self.course_team_instructor_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseTeamInstructor.objects.count(), 1)
        self.assertEqual(CourseTeamInstructor.objects.get().user.username, "john_doe")

    @patch_permissions
    def test_create_invalid_course_team_instructor(self, _):
        """Test creating a new course team instructor with invalid data.

        Expected behavior:
        - The response status code should be 400.
        - The course team instructor should not be created.
        """
        response = self.client.post(
            self.url, self.invalid_course_team_instructor_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CourseTeamInstructor.objects.count(), 0)

    @patch_permissions
    def test_list_course_team_instructors(self, _):
        """Test listing all course team instructors.

        Expected behavior:
        - The response status code should be 200.
        - The response data should contain all course team instructors.
        """
        CourseTeamInstructor.objects.create(course_team_id=1, user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @patch_permissions
    def test_filter_course_team_instructors_by_course_team_id(self, _):
        """Test filtering course team instructors by course team id.

        Expected behavior:
        - The response status code should be 200.
        - The response data should contain only the course team instructor with course_team_id=1.
        """
        CourseTeamInstructor.objects.create(course_team_id=1, user=self.user)
        CourseTeamInstructor.objects.create(course_team_id=2, user=self.user)
        CourseTeamInstructor.objects.create(course_team_id=3, user=self.user)

        response = self.client.get(self.url, {"course_team_id": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], "john_doe")

    @patch_permissions
    def test_delete_course_team_instructor(self, _):
        """Test deleting a course team instructor.

        Expected behavior:
        - The response status code should be 204.
        - The course team instructor should be deleted.
        """
        course_team_instructor = CourseTeamInstructor.objects.create(
            course_team_id=1, user=self.user
        )

        response = self.client.delete(
            reverse(
                "openedx-unidigital-api:v1:course-team-instructor",
                kwargs={"pk": course_team_instructor.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CourseTeamInstructor.objects.count(), 0)
