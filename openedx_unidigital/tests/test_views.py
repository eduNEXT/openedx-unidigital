"""Test cases for the views of the openedx_unidigital app."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from openedx_unidigital.models import CourseTeamInstructor


class CourseTeamInstructorAPITestCase(APITestCase):
    """Test suite for the CourseTeamInstructor API."""

    def setUp(self):
        self.course_team_instructor_data = {
            "course_team_id": 1,
            "course_team_name": "team_name",
            "username": "john_doe",
        }
        self.invalid_course_team_instructor_data = {"course_team_id": 2, "username": ""}
        self.url = reverse("openedx-unidigital-api:v1:course-team-instructor")

    def test_create_course_team_instructor(self):
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
        self.assertEqual(CourseTeamInstructor.objects.get().username, "john_doe")

    def test_create_invalid_course_team_instructor(self):
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

    def test_list_course_team_instructors(self):
        """Test listing all course team instructors.

        Expected behavior:
        - The response status code should be 200.
        - The response data should contain all course team instructors.
        """
        CourseTeamInstructor.objects.create(course_team_id=1, username="john_doe")
        CourseTeamInstructor.objects.create(course_team_id=2, username="jane_doe")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_course_team_instructors_by_course_team_id(self):
        """Test filtering course team instructors by course team id.

        Expected behavior:
        - The response status code should be 200.
        - The response data should contain only the course team instructor with course_team_id=1.
        """
        CourseTeamInstructor.objects.create(course_team_id=1, username="john_doe")
        CourseTeamInstructor.objects.create(course_team_id=2, username="jane_doe")

        response = self.client.get(self.url, {"course_team_id": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "john_doe")

    def test_filter_course_team_instructors_by_username(self):
        """Test filtering course team instructors by username.

        Expected behavior:
        - The response status code should be 200.
        - The response data should contain only the course team instructor with username=jane_doe.
        """
        CourseTeamInstructor.objects.create(course_team_id=1, username="john_doe")
        CourseTeamInstructor.objects.create(course_team_id=2, username="jane_doe")

        response = self.client.get(self.url, {"username": "jane_doe"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "jane_doe")

    def test_delete_course_team_instructor(self):
        """Test deleting a course team instructor.

        Expected behavior:
        - The response status code should be 204.
        - The course team instructor should be deleted.
        """
        course_team_instructor = CourseTeamInstructor.objects.create(
            course_team_id=1, username="john_doe"
        )

        response = self.client.delete(
            reverse(
                "openedx-unidigital-api:v1:course-team-instructor",
                kwargs={"pk": course_team_instructor.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CourseTeamInstructor.objects.count(), 0)
