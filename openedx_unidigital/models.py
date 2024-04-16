"""Model for Course Team Instructors for the Unidigital project."""

from django.contrib import admin
from django.db import models


class CourseTeamInstructor(models.Model):
    """Django model for Course Team Instructors.

    A Course Team Instructor is a user that:
     - Is part of a team that is part of a course.
     - Has the role of Limited Staff in the course, so they can access the
     instructor dashboard.

    Attributes:
        course_team_id (int): The ID of the course team.
        course_team_name (str): The name of the course team.
        username (str): The username of the user.
    """

    course_team_id = models.IntegerField(null=False)
    course_team_name = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ("course_team_id", "username")
        verbose_name = "Course Team Instructor"
        verbose_name_plural = "Course Team Instructors"

    def __str__(self):
        return f"{self.course_team_name} - {self.username}"

    @classmethod
    def get_teams_for_user(cls, username):
        """Get CourseTeamInstructor objects for a user.

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
