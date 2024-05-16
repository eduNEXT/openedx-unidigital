"""Model for Course Team Instructors for the Unidigital project."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CourseTeamInstructor(models.Model):
    """
    Django model for Course Team Instructors.

    A Course Team Instructor is a user that:
     - Is part of a team that is part of a course.
     - Has the role of Limited Staff in the course, so they can access the
     instructor dashboard.

    Attributes:
        course_team_id (int): The ID of the course team.
        course_team_name (str): The name of the course team.
        username (str): The username of the user.

    .. no_pii:
    """

    course_team_id = models.IntegerField(null=False)
    course_team_name = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Meta options for the CourseTeamInstructor model."""

        unique_together = ("course_team_id", "user")
        verbose_name = "Course Team Instructor"
        verbose_name_plural = "Course Team Instructors"

    def __str__(self):
        """Return the string representation of the CourseTeamInstructor object."""
        return f"Team name: {self.course_team_name} ({self.course_team_id}) - Username: {self.user.username}"

    @classmethod
    def get_teams_for_user(cls, username):
        """
        Get CourseTeamInstructor objects for a user.

        Args:
            username (str): The username.

        Returns:
            QuerySet: The teams that the user is part of.
        """
        return cls.objects.filter(username=username).values_list(
            "course_team_id",
            flat=True,
        )


admin.site.register(CourseTeamInstructor)
