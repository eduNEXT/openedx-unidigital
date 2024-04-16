"""Filters for the Open edX Unidigital plugin."""

import pkg_resources
from crum import get_current_request
from django.template import Context, Template
from django.utils.translation import gettext as _
from openedx_filters import PipelineStep
from web_fragments.fragment import Fragment

from openedx_unidigital.edxapp_wrapper.student import (
    CourseInstructorRole,
    CourseLimitedStaffRole,
)
from openedx_unidigital.edxapp_wrapper.teams import get_teams_in_teamset
from openedx_unidigital.edxapp_wrapper.xmodule import TeamsConfigurationService
from openedx_unidigital.models import CourseTeamInstructor

TEMPLATE_ABSOLUTE_PATH = "/instructor_dashboard/"
BLOCK_CATEGORY = "course_team_management"


class TeamAssignmentDashboard(PipelineStep):
    """Filter to add a section to the instructor dashboard with the team instructors management.

    This filter adds a section to the instructor dashboard with the team instructors
    for the course teams. The section includes a list of the course teams and the
    instructors for each team. In the section, the course staff can manage the
    instructors for the course teams.
    """

    def run_filter(
        self, context, template_name
    ):  # pylint: disable=unused-argument, arguments-differ
        """Execute filter that modifies the instructor dashboard context.

        Args:
            context (dict): the context for the instructor dashboard.
            _ (str): instructor dashboard template name.
        """
        course = context["course"]
        user = get_current_request().user
        if not CourseInstructorRole(course.id).has_user(user):
            return {
                "context": context,
            }

        team_sets = (
            TeamsConfigurationService().get_teams_configuration(course.id).teamsets
        )
        teams_in_teamsets = []
        for teamset in team_sets:
            teams_in_teamsets.extend(
                list(get_teams_in_teamset(str(course.id), teamset.teamset_id))
            )

        context.update(
            {
                "teams": teams_in_teamsets,
                "course_teams_instructors": [
                    {
                        "team": team,
                        "instructors": CourseTeamInstructor.objects.filter(
                            course_team_id=team.id
                        ),
                    }
                    for team in teams_in_teamsets
                ],
            }
        )

        template = Template(
            self.resource_string("static/html/course_team_management.html")
        )
        html = template.render(Context(context))
        frag = Fragment(html)
        frag.add_javascript(self.resource_string("static/js/course_team_management.js"))

        section_data = {
            "fragment": frag,
            "section_key": BLOCK_CATEGORY,
            "section_display_name": _("Courses' Team Instructors"),
            "course_id": str(course.id),
            "template_path_prefix": TEMPLATE_ABSOLUTE_PATH,
        }
        context["sections"].append(section_data)

        return {
            "context": context,
        }

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string("openedx_unidigital", path)
        return data.decode("utf8")


class TeamLimitedStaffDashboard(PipelineStep):
    """
    Pipeline step for the instructor dashboard rendering process.

    This step is used to modify the dashboard data before it's rendered filtering
    the sections list.
    """

    def run_filter(self, context, template_name):  # pylint: disable=arguments-differ
        """Pipeline step that filters the sections list for the instructor dashboard.

        Args:
            context (dict): the context for the instructor dashboard.
            _ (str): instructor dashboard template name.
        """
        course = context["course"]
        user = get_current_request().user
        if not CourseLimitedStaffRole(course.id).has_user(user):
            return {
                "context": context,
            }

        context["sections"] = [
            section
            for section in context["sections"]
            if section["section_key"] in ["course_info", "student_admin"]
        ]
        self.hide_gradebook(context)

        return {
            "context": context,
            "template_name": template_name,
        }

    @staticmethod
    def hide_gradebook(context):
        """Hide the gradebook for the instructor dashboard."""
        for section in context["sections"]:
            if section["section_key"] == "student_admin":
                section["writable_gradebook_url"] = None
                section["is_small_course"] = False
                break
