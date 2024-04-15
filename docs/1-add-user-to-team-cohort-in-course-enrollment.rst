Add user to team/cohort in course enrollment
********************************************

This feature allows the instructor to configure a course so that any student
(depending on their language preference on the platform) is added to a
particular team or cohort of the course upon enrollment.

Add the configuration to the course in the **Advanced Settings** >
**Other Course Settings**. You should use the following format:

.. code-block::

    {
        "MEMBERSHIP_BY_LANGUAGE_CONFIG": {
            "<language-code-1>,<language-code-2>": [
                {
                    "type": "team",
                    "id": "<team-id>"
                },
                {
                    "type": "cohort",
                    "id": "<cohort-name>"
                }
            ],
            "<language-code-3>": [
                {
                    "type": "team",
                    "id": "<team-id>"
                }
            ],
            "default": [
                {
                    "type": "team",
                    "id": "<team-id>"
                },
                {
                    "type": "cohort",
                    "id": "<cohort-name>"
                }
            ]
        }
    }

The following keys are required:

The **language code** key must be in the ISO 639-1 format, the `following codes`_
are supported. The string can contain multiple language codes separated by
commas, if you want to apply the same configuration to multiple languages.

Optionally, you can use the **default** key to set a configuration for when the
user's language preference does not match any of the language codes in the
configuration.

Each language code should be a **list** of each of the teams and cohorts you
wish to assign to that language or languages.

Each team or cohort should be a dictionary with the following keys:

- **type**: The type of the group to which the user will be added. It can be
  either "team" or "cohort".
- **id**: The identifier of the team or cohort to which the user will be
  added. The value should be the team ID or cohort name. The team ID can be
  found at the end of the URL when you view the team in the LMS (<lms-domain>/courses/<course-id>/teams/#teams/<topic-id>/**<team-id>**).
  The cohort name is the name of the cohort you want to add the user to.

The following is an example of a configuration:

.. code-block::

    {
        "MEMBERSHIP_BY_LANGUAGE_CONFIG": {
            "es-419,es-es": [
                {
                    "type": "team",
                    "id": "first-team-eee5e75d1c24412e9a8bb7300951cbb8"
                },
                {
                    "type": "cohort",
                    "id": "First Cohort"
                }
            ],
            "en": [
                {
                    "type": "team",
                    "id": "second-team-e3266314f27043fe95933fa036ecc570"
                }
            ],
            "default": [
                {
                    "type": "team",
                    "id": "default-team-e80b43a577c3474a8bbc7d80a7e57259"
                },
                {
                    "type": "cohort",
                    "id": "Default Cohort"
                }
            ]
        }
    }

.. _following codes: https://github.com/openedx/frontend-app-account/blob/master/src/account-settings/site-language/constants.js

Considerations
==============

- By default, users do not have a language preference set, so each user
  should set their language preference in their account settings in **Account**
  > **Site Preferences** > **Site language**. If the user does not set a
  language preference, language will be taken from the platform default
  language.
- By definition, the users cannot belong to more than one **cohort** nor to
  more that one **team** within the same team set (topic). Therefore, the
  configuration must be consistent with this restriction.
- By definition, if a user unrolls from the course is not removed from the team
  or cohort to which they were added.
- If the configuration of a language is updated, the changes will only apply to
  new enrollments. The users who were already enrolled will not be affected by
  the changes. To apply the new configuration, the user or the instructor must
  make the changes manually.
- If a user changes their language preference, the user or the instructor
  must remove the user from the team or cohort that represents the previous
  language preference and add the user to the team or cohort that represents
  the new language preference. Alternatively, after the user is removed from
  the previous team or cohort, the user can enroll again in the course to be
  added to the new team or cohort.
