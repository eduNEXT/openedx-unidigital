"""API Views for the platform_plugin_forum_email_notifier plugin."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import DestroyAPIView, ListCreateAPIView

from openedx_unidigital.api.v1.serializers import CourseTeamInstructorSerializer
from openedx_unidigital.models import CourseTeamInstructor


class CourseTeamInstructorAPIView(ListCreateAPIView, DestroyAPIView):
    """API view for Course Team Instructors.

    This view allows to create, list and filter Course Team Instructors.
    """

    queryset = CourseTeamInstructor.objects.all()
    serializer_class = CourseTeamInstructorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course_team_id", "username"]
