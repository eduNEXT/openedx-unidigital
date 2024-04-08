"""
Course Groups definitions for Open edX Quince release.
"""

from openedx.core.djangoapps.course_groups.cohorts import (  # pylint: disable=import-error, unused-import
    add_user_to_cohort,
    get_cohort_by_id,
)
from openedx.core.djangoapps.course_groups.models import CourseUserGroup  # pylint: disable=import-error, unused-import
