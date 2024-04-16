"""
Instructor generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def get_allow_student_to_bypass_entrance_exam():
    """
    Wrapper for `lms.djangoapps.instructor.permissions.ALLOW_STUDENT_TO_BYPASS_ENTRANCE_EXAM`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_INSTRUCTOR_BACKEND
    backend = import_module(backend_function)

    return backend.ALLOW_STUDENT_TO_BYPASS_ENTRANCE_EXAM


def get_enrollment_report():
    """
    Wrapper for `lms.djangoapps.instructor.permissions.ENROLLMENT_REPORT`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_INSTRUCTOR_BACKEND
    backend = import_module(backend_function)

    return backend.ENROLLMENT_REPORT


def get_give_student_extension():
    """
    Wrapper for `lms.djangoapps.instructor.permissions.GIVE_STUDENT_EXTENSION`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_INSTRUCTOR_BACKEND
    backend = import_module(backend_function)

    return backend.GIVE_STUDENT_EXTENSION


def get_override_grades():
    """
    Wrapper for `lms.djangoapps.instructor.permissions.OVERRIDE_GRADES`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_INSTRUCTOR_BACKEND
    backend = import_module(backend_function)

    return backend.OVERRIDE_GRADES


def get_view_enrollments():
    """
    Wrapper for `lms.djangoapps.instructor.permissions.VIEW_ENROLLMENTS`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_INSTRUCTOR_BACKEND
    backend = import_module(backend_function)

    return backend.VIEW_ENROLLMENTS


ALLOW_STUDENT_TO_BYPASS_ENTRANCE_EXAM = get_allow_student_to_bypass_entrance_exam()
ENROLLMENT_REPORT = get_enrollment_report()
GIVE_STUDENT_EXTENSION = get_give_student_extension()
OVERRIDE_GRADES = get_override_grades()
VIEW_ENROLLMENTS = get_view_enrollments()
