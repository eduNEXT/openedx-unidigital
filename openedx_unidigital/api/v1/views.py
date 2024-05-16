"""API Views for the platform_plugin_forum_email_notifier plugin."""

from django_filters.rest_framework import DjangoFilterBackend
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.permissions import IsStaff, IsSuperuser
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import DestroyAPIView, ListCreateAPIView

from openedx_unidigital.api.v1.permissions import IsCourseInstructor
from openedx_unidigital.api.v1.serializers import CourseTeamInstructorSerializer
from openedx_unidigital.models import CourseTeamInstructor


class CourseTeamInstructorAPIView(ListCreateAPIView, DestroyAPIView):
    """API view for Course Team Instructors.

    This view allows to create, list and filter Course Team Instructors.
    """

    authentication_classes = [
        JwtAuthentication,
        SessionAuthentication,
    ]
    permission_classes = (IsStaff | IsSuperuser | IsCourseInstructor,)
    queryset = CourseTeamInstructor.objects.all()
    serializer_class = CourseTeamInstructorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course_team_id"]
