"""Test suite for filters for the Open edX Unidigital plugin."""

from unittest import TestCase
from unittest.mock import Mock, patch

from django.test import override_settings
from openedx_filters.learning.filters import InstructorDashboardRenderStarted


class TestTeamAssignmentDashboard(TestCase):
    """Test suite for the TeamAssignmentDashboard filter."""

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.instructor.dashboard.render.started.v1": {
                "fail_silently": False,
                "pipeline": ["openedx_unidigital.filters.TeamAssignmentDashboard"],
            }
        }
    )
    @patch("openedx_unidigital.filters.CourseTeamInstructor")
    @patch("openedx_unidigital.filters.get_current_request")
    @patch("openedx_unidigital.filters.CourseInstructorRole")
    @patch("openedx_unidigital.filters.TeamsConfigurationService")
    @patch("openedx_unidigital.filters.get_teams_in_teamset")
    def test_run_filter_for_instructor(
        self,
        mock_get_teams_in_teamset,
        mock_teams_service,
        mock_instructor_role,
        mock_get_current_request,
        _,
    ):
        """Test run_filter method for an instructor.

        Expected behavior:
        - The filter should add a teams key to the context.
        - The filter should add a course_teams_instructors key to the context.
        - The context sections should include a new section for the course instructor teams management.
        """
        context = {
            "course": Mock(),
            "sections": [],
        }
        mock_instructor_role().has_user.return_value = True
        mock_get_current_request().user = Mock()
        mock_teams_service().get_teams_configuration().teamsets = [Mock()]
        mock_get_teams_in_teamset.return_value = [Mock()]

        InstructorDashboardRenderStarted.run_filter(
            context=context,
            template_name="instructor_dashboard",
        )

        self.assertIn("teams", context)
        self.assertIn("course_teams_instructors", context)
        self.assertEqual(len(context["sections"]), 1)
        self.assertEqual(
            context["sections"][0]["section_key"], "course_team_management"
        )

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.instructor.dashboard.render.started.v1": {
                "fail_silently": False,
                "pipeline": ["openedx_unidigital.filters.TeamAssignmentDashboard"],
            }
        }
    )
    @patch("openedx_unidigital.filters.CourseInstructorRole")
    @patch("openedx_unidigital.filters.get_current_request")
    def test_run_filter_for_non_instructor(self, _, mock_instructor_role):
        """Test run_filter method for a non-instructor.

        Expected behavior:
        - The filter should not modify the context.
        """
        context = {
            "course": Mock(),
            "sections": [],
        }
        mock_instructor_role().has_user.return_value = False

        InstructorDashboardRenderStarted.run_filter(
            context=context,
            template_name="instructor_dashboard",
        )

        self.assertNotIn("teams", context)
        self.assertNotIn("course_teams_instructors", context)
        self.assertEqual(len(context["sections"]), 0)


class TestTeamLimitedStaffDashboard(TestCase):
    """Test suite for the TeamLimitedStaffDashboard filter."""

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.instructor.dashboard.render.started.v1": {
                "fail_silently": False,
                "pipeline": ["openedx_unidigital.filters.TeamLimitedStaffDashboard"],
            }
        }
    )
    @patch("openedx_unidigital.filters.CourseLimitedStaffRole")
    @patch("openedx_unidigital.filters.get_current_request")
    @patch("openedx_unidigital.filters.CourseTeamInstructor")
    def test_run_filter_for_limited_staff(
        self, mock_course_team_instructor, _, mock_limited_staff_role
    ):
        """Test run_filter method for a limited staff user.

        Expected behavior:
        - The sections should be filtered to exclude all but course_info and student_admin sections.
        """
        context = {
            "course": Mock(),
            "sections": [
                {"section_key": "course_info"},
                {"section_key": "student_admin"},
                {"section_key": "course_team_management"},
            ],
        }
        mock_limited_staff_role().has_user.return_value = True
        mock_course_team_instructor.get_teams_for_user.return_value = [Mock()]

        InstructorDashboardRenderStarted.run_filter(
            context=context,
            template_name="instructor_dashboard",
        )

        self.assertEqual(len(context["sections"]), 2)
        self.assertEqual(context["sections"][0]["section_key"], "course_info")
        self.assertEqual(context["sections"][1]["section_key"], "student_admin")

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.instructor.dashboard.render.started.v1": {
                "fail_silently": False,
                "pipeline": ["openedx_unidigital.filters.TeamLimitedStaffDashboard"],
            }
        }
    )
    @patch("openedx_unidigital.filters.CourseLimitedStaffRole")
    @patch("openedx_unidigital.filters.get_current_request")
    def test_run_filter_for_non_limited_staff(self, _, mock_limited_staff_role):
        """Test run_filter method for a non-limited staff user.

        Expected behavior:
        - The sections should not be filtered.
        """
        context = {
            "course": Mock(),
            "sections": [
                {"section_key": "course_info"},
                {"section_key": "student_admin"},
                {"section_key": "course_team_management"},
            ],
        }
        mock_limited_staff_role().has_user.return_value = False

        InstructorDashboardRenderStarted.run_filter(
            context=context,
            template_name="instructor_dashboard",
        )

        self.assertEqual(len(context["sections"]), 3)
        self.assertEqual(context["sections"][0]["section_key"], "course_info")
        self.assertEqual(context["sections"][1]["section_key"], "student_admin")
        self.assertEqual(
            context["sections"][2]["section_key"], "course_team_management"
        )

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.instructor.dashboard.render.started.v1": {
                "fail_silently": False,
                "pipeline": ["openedx_unidigital.filters.TeamLimitedStaffDashboard"],
            }
        }
    )
    @patch("openedx_unidigital.filters.CourseLimitedStaffRole")
    @patch("openedx_unidigital.filters.get_current_request")
    @patch("openedx_unidigital.filters.CourseTeamInstructor")
    def test_run_filter_for_limited_staff_no_teams(
        self, mock_course_team_instructor, _, mock_limited_staff_role
    ):
        """Test run_filter method for a limited staff user with no teams.

        Expected behavior:
        - The sections should not be filtered.
        """
        context = {
            "course": Mock(),
            "sections": [
                {"section_key": "course_info"},
                {"section_key": "student_admin"},
                {"section_key": "course_team_management"},
            ],
        }
        mock_limited_staff_role().has_user.return_value = True
        mock_course_team_instructor.get_teams_for_user.return_value = []

        InstructorDashboardRenderStarted.run_filter(
            context=context,
            template_name="instructor_dashboard",
        )

        self.assertEqual(len(context["sections"]), 3)
        self.assertEqual(context["sections"][0]["section_key"], "course_info")
        self.assertEqual(context["sections"][1]["section_key"], "student_admin")
        self.assertEqual(
            context["sections"][2]["section_key"], "course_team_management"
        )
