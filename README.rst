Open edX Unidigital Plugin
#############################

|ci-badge| |license-badge| |status-badge|

Purpose
*******

This plugin is designed to configure the Open edX platform for use within the
Unidigital project, an initiative funded by the Spanish Government in 2023.

As an open-source contribution to the Open edX platform, this plugin enhances
its functionality to align with the requirements of the Unidigital project.

Deployment
**********

To deploy this plugin in your Open edX platform within the Unidigital project,
execute the following command:

.. code-block::

    pip install git+https://github.com/eduNEXT/openedx-unidigital.git@main

This command installs the necessary dependencies and adds the plugin to the list
of installed plugins in the platform.


**Note**: Ensure that you use the specified branch of the edx-platform repository:
`Unidigital release <https://github.com/eduNEXT/edunext-platform/tree/open-release/palm.4/edues>`_.
The plugin is based on the `open-release/palm.4 <https://gtihub.com/eduNEXT/edx-platform/tree/open-release/palm.4>`_
branch and is compatible with Tutor version v16.1.7.

Features
********

Aspects
=======

This plugin introduces Aspects Learner Analytics dependencies to the Open edX
platform, including:

- `openedx-event-sink-clickhouse <https://github.com/openedx/openedx-event-sink-clickhouse>`_: A plugin for sending events to a Clickhouse database.
- `event-routing-backends <https://github.com/openedx/event-routing-backends>`_: A plugin for routing events to different backends.

XBlocks
=======

- `LimeSurvey XBlock <https://github.com/eduNEXT/xblock-limesurvey>`_: An XBlock for embedding Limesurvey surveys within a course.
- `Mindmap XBlock <https://github.com/eduNEXT/xblock-mindmap>`_: An XBlock for embedding Mindmaps within a course.
- `Images Gallery XBlock <https://github.com/eduNEXT/xblock-imagesgallery>`_: An XBlock for embedding an image gallery within a course.
- `Files Manager XBlock <https://github.com/eduNEXT/xblock-filesmanager>`_: An XBlock for sharing files with students within a course.
- `H5P XBlock <https://github.com/eduNEXT/h5pxblock>`_: An XBlock for embedding H5P content within a course.
- `Feedback XBlock <https://github.com/eduNEXT/FeedbackXBlock>`_: An XBlock for embedding a Feedback form within a course.
- `edx-ora2 <https://github.com/eduNEXT/edx-ora2>`_: An XBlock for embedding ORA2 content within a course.

Platform Plugins
================

- `Forum Email Notifier <https://github.com/eduNEXT/platform-plugin-forum-email-notifier>`_: A plugin for sending email notifications to students when there is new activity in the forums.
- `Superset <https://github.com/eduNEXT/platform-plugin-superset>`_: A plugin for embedding Superset dashboards within the platform.
- `ELM Credentials <https://github.com/eduNEXT/platform-plugin-elm-credentials>`_: A plugin that includes API to generate JSON files in ELMv3.
- `Communications <https://github.com/eduNEXT/platform-plugin-communications>`_: A plugin that extends email capabilities within the platform.
- `Teams <https://github.com/eduNEXT/platform-plugin-teams>`_: A plugin that includes a custom teams API.

Additional Features
*******************

- `Add user to team/cohort in course enrollment <./docs/1-add-user-to-team-cohort-in-course-enrollment.rst>`_
- `Assign instructors to course teams <./docs/2-assign-instructors-to-course-teams.rst>`_

License
*******

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

Contributing
************

To add a new required dependency to the plugin you need to add it to the
``requirements/stage.in`` or ``requirements/prod.in`` file, depending on the
environment where the dependency is required. The ``stage.in`` file is intended
to hold dependencies for testing purposes, so you can use branches or commits
that are not stable yet. The ``prod.in`` file is intended to hold dependencies
for production environments, so you should only use stable releases, so you
should use the ``@master`` branch, neither use it to install development
versions of the dependencies.

As dependencies can be git repositories, you can also specify a specific
branch or commit hash in the ``stage.in`` or ``prod.in`` file:

.. code-block::

    {package_name} @ git+https://github.com/{org}/{repo_name}.git@{branch_tag_or_commit_hash}


The Open edX Code of Conduct
****************************

All community members are expected to follow the `Open edX Code of Conduct`_.

.. _Open edX Code of Conduct: https://openedx.org/code-of-conduct/

People
******

The assigned maintainers for this component and other project details may be
found in `Backstage`_. Backstage pulls this data from the ``catalog-info.yaml``
file in this repo.

.. _Backstage: https://backstage.openedx.org/catalog/default/component/openedx-unidigital

Reporting Security Issues
*************************

Please do not report security issues in public. Please email security@edunext.co.

.. |pypi-badge| image:: https://img.shields.io/pypi/v/openedx-unidigital.svg
    :target: https://pypi.python.org/pypi/openedx-unidigital/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/eduNEXT/openedx-unidigital/actions/workflows/ci.yml/badge.svg?branch=main
    :target: https://github.com/eduNEXT/openedx-unidigital/actions
    :alt: CI

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/openedx-unidigital.svg
    :target: https://pypi.python.org/pypi/openedx-unidigital/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/openedx-unidigital.svg
    :target: https://github.com/eduNEXT/openedx-unidigital/blob/main/LICENSE.txt
    :alt: License

.. TODO: Choose one of the statuses below and remove the other status-badge lines.
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red
