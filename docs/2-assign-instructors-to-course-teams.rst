Assign instructors to course teams
**********************************

In campus education often relies on Teaching Assistants to handle some of the
load of managing students in a large course. This feature allows you to assign
instructors to course teams. This means that when assigned to a course team, the
instructor will be able to manage student grades for the students in the course
team.

A "Teaching Assistant" is a user with the role of "limited staff" that's assigned
to at least one course team.

This feature consists of:

1. A new tab in the Instructor Dashboard UI that allows you to assign/remove/view
   instructors to course teams. This tab is only visible to users with the role
    of "course admin" in the Instructor Dashboard UI. The tab is only visible if
2. A filter that will limit the tabs of the Instructor Dashboard UI to only Course
    Info and Student Admin, so the user can only manage student grades. This filter
    is necessary to prevent the user from accessing the other tabs of the Instructor
    Dashboard UI. The tab is on if and only if a user with limited staff role is
    assigned to at least one course team.
3. An custom authentication that allows/denies users to perform actions based on
    their role and the course team they are assigned to.

Configuration
=============

To enable this feature, you need to add the following configuration to the
LMS environment file:

.. code-block::

    OPEN_EDX_FILTERS_CONFIG = {
        "org.openedx.learning.instructor.dashboard.render.started.v1": {
            "fail_silently": False,
            "pipeline": [
                "openedx_unidigital.filters.TeamLimitedStaffDashboard",
                "openedx_unidigital.filters.TeamAssignmentDashboard",
            ]
        },
    }

This configuration will enable custom tabs used for assigning instructors to
course teams in the Instructor Dashboard UI.

Common use cases
================

How to assign an instructor to a course team
--------------------------------------------

To assign an instructor to a course team, you need to have instructor level access,
which is known as "course admin" in the Instructor Dashboard UI. You can assign an instructor to a course
team by following these steps:

1. Go to the Instructor Dashboard UI as a user with the role of "course admin".
2. Click on the "Courses' Team Instructors" tab.
3. Select the team the instructor will be assigned to.
4. Add the username of the instructor you want to assign to the team.
5. Click on the "Assign Instructor" button.

How to remove an instructor from a course team
----------------------------------------------

To remove an instructor from a course team, you need to have instructor level access,
which is known as "course admin" in the Instructor Dashboard UI. You can remove an instructor from a course
team by following these steps:

1. Go to the Instructor Dashboard UI as a user with the role of "course admin".
2. Click on the "Courses' Team Instructors" tab.
3. Select the team the instructor will be removed from.
4. Click on the "Revoke access" button next to the instructor you want to remove from the team.

Managing grades as a Teaching Assistant
---------------------------------------

As a Teaching Assistant, you can manage student grades for the students in the course team you are assigned to.
You can access the Instructor Dashboard UI and see the tabs for Course Info and Student Admin. You can manage
student grades by clicking on the "Student Admin" tab. A Teaching Assistant can manage grades if and only if:

1. The user has the role of "limited staff".
2. The user is assigned to at least one course team.
3. The user is assigned to the course team that the student is in.
4. The user does not need to join the team to manage grades.
