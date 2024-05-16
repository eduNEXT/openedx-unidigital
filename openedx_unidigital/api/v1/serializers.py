"""Serializers for the API endpoints of the openedx_unidigital app."""

from rest_framework import serializers
from django.contrib.auth import get_user_model

from openedx_unidigital.models import CourseTeamInstructor


User = get_user_model()

class CourseTeamInstructorSerializer(serializers.ModelSerializer):
    """
    Serializer for the CourseTeamInstructor model.
    """

    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        model = CourseTeamInstructor
        fields = "__all__"
