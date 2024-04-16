"""Serializers for the API endpoints of the openedx_unidigital app."""

from rest_framework import serializers

from openedx_unidigital.models import CourseTeamInstructor


class CourseTeamInstructorSerializer(serializers.ModelSerializer):
    """
    Serializer for the CourseTeamInstructor model.
    """

    class Meta:
        model = CourseTeamInstructor
        fields = "__all__"
