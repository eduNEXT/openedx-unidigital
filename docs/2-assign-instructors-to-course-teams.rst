Assign instructors to course teams
**********************************

In campus education settings there is often an instructor figure that handles some of the
load of managing students in a large course. So, this feature allows you to assign
instructors to course teams. This means that when assigned to a course team, the
instructor will be able to manage student grades for the students in the course
team.

So, a courses' team instructor is a user with the role of "limited staff" that's assigned
to at least one course team.

This feature consists of:

1. A new tab in the Instructor Dashboard UI allows you to assign/remove/view
   instructors to course teams. This tab is only visible to users with the role
   of "course admin" in the Instructor Dashboard UI.
2. A filter that will limit the tabs of the Instructor Dashboard UI to only Course
   Info and Student Admin, so the user can only manage student grades. This filter
   is necessary to prevent the user from accessing the other tabs of the Instructor
   Dashboard UI. The tab is on if and only if a user with limited staff role is
   assigned to at least one course team.
3. A custom authentication backend that allows/denies users to perform actions based on
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

To assign an instructor to a course team, you need instructor-level access, known as "course admin" in the Instructor Dashboard UI. You can assign an instructor to a course
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

Managing grades as a Course Team Instructor
-------------------------------------------

As a course team instructor, you can manage student grades for the students in the course team you are assigned to.
You can access the Instructor Dashboard UI and see the Course Info and Student Admin tabs. You can manage
student grades by clicking on the "Student Admin" tab. A Course Team Instructor can manage grades of a student if and only if:

1. The user has the role of "limited staff".
2. The user is assigned to at least one course team.
3. The user is assigned to the course team that the student is in.
4. The user does not need to join the team to manage grades.

API Access for associating instructors with teams
-------------------------------------------------

To assign an instructor to a course team, you need instructor-level access, known as "course admin" in the Instructor Dashboard UI. You can assign an instructor to a course
team via the available rest API by following these steps:
 
Make a POST request to `<lms_host>/oauth2/access_token/` to generate a token for the user. As mentioned before, the user must be course admin, global staff or superadmin. 
The content type of the request must be application/x-www-form-urlencoded. 

**Body parameters**

- **client_id**: Client ID of the OAuth2 application. You can find it in the Django admin panel. Normally, it is login-service-client-id.
- **grant_type**: Grant type of the OAuth2 application. 
- **token_type**: Type of the token. By default, it is bearer. This API uses JWT.

You can create a new application in the Django admin panel. The body parameters are the same as the previous endpoint, but you must use the client_id and client_secret of the new application. The grant_type must be client_credentials.

**Response**

- **access_token**: Access token of the user. You must use this token in the Authorization header of the requests to the API.

Then, you are ready to use the API. The next endpoints are available:

- GET ``<lms_host>/courses/<course_id>/api/v1/course-team-instructor/``: list all assignments.
- GET ``<lms_host>/courses/<course_id>/api/v1/course-team-instructor/?course_team_id=<course_team_id>``: list users assigned to `course_team_id`.
- POST ``<lms_host>/courses/<course_id>/api/v1/course-team-instructor/``: create a new assignment.

  **Body parameters**

  - ``user``: instructors' username.
  - ``course_team_id``: team ID to which the user will be assigned.
  - ``course_team_name``: team name to which the user will be assigned.

- DELETE ``<lms_host>/courses/<course_id>/api/v1/course-team-instructor/<assignment_id>``: delete the assignment ``<assignment_id>``.
