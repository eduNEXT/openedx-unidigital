"""
Student generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def get_user_by_username_or_email(*args, **kwargs):
    """
    Wrapper for `student.models.user.get_user_by_username_or_email`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_STUDENT_BACKEND
    backend = import_module(backend_function)

    return backend.get_user_by_username_or_email(*args, **kwargs)


def get_course_instructor_role():
    """
    Wrapper for `student.roles.CourseInstructorRole`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_STUDENT_BACKEND
    backend = import_module(backend_function)

    return backend.CourseInstructorRole


def get_course_limited_staff_role():
    """
    Wrapper for `student.roles.CourseLimitedStaffRole`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_STUDENT_BACKEND
    backend = import_module(backend_function)

    return backend.CourseLimitedStaffRole


CourseInstructorRole = get_course_instructor_role()
CourseLimitedStaffRole = get_course_limited_staff_role()
