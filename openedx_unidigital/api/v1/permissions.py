"""
Permissions for the Open edX Unidigital API.
"""

from rest_framework.permissions import BasePermission
from openedx_unidigital.edxapp_wrapper.student import CourseInstructorRole
from opaque_keys.edx.keys import CourseKey


class IsCourseInstructor(BasePermission):
    """
    Permission that checks if the user has instructor level access.
    """

    def has_permission(self, request, view):
        """Returns true if the user has instructor access."""
        return CourseInstructorRole(
            CourseKey.from_string(view.kwargs.get("course_id"))
        ).has_user(request.user)
