"""URL patterns for the Open edX Unidigital API."""

from django.urls import re_path

from openedx_unidigital.api.v1 import views

app_name = "openedx_unidigital"
urlpatterns = [
    re_path(
        r"^course-team-instructor/(?P<pk>\d+)?",
        views.CourseTeamInstructorAPIView.as_view(),
        name="course-team-instructor",
    ),
]
