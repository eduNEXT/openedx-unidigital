from openedx_filters import PipelineStep


class TeamLimitedStaffDashboard(PipelineStep):
    """
    Pipeline step for testing the instructor dashboard rendering process.
    This step is used to modify the dashboard data before it's rendered emptying
    the sections list.
    """

    def run_filter(self, context, template_name):  # pylint: disable=arguments-differ
        """Pipeline step that modifies dashboard data."""
        context["sections"] = [
            section for section in context["sections"] if section["section_key"] in
            [
                "course_info",
                "student_admin"
            ]
        ]
        return {
            "context": context,
            "template_name": template_name,
        }

