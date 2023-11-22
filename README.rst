openedx-unidigital
#############################

|pypi-badge| |ci-badge| |pyversions-badge|
|license-badge| |status-badge|

Purpose
*******

A plugin that setups the Open edX platform to be used in the context
of the Unidigital project.

This plugin has been created as an open source contribution to the Open edX platform
and has been funded by the Unidigital project from the Spanish Government - 2023.

Deploying
*********

This plugin is meant to be used in the context of the Unidigital project.

To deploy this plugin in a Open edX platform, you can use the following
command:

.. code-block:: bash

    pip install openedx-unidigital

This will install all the required dependencies and will add the plugin
to the list of installed plugins in the platform.


.. note::

    This plugin is meant to be used in the context of the Unidigital project.
    You need to use the following branch of the edx-platform repository:
    https://github.com/eduNEXT/edunext-platform/tree/open-release/palm.4/edues

    It's based on the open-release/palm.4 branch of the edx-platform repository
    and it's compatible with tutor version v16.1.7


Features
********

This plugin adds the following features to the Open edX platform:

Aspects
=======
This plugin adds the Aspects Learner Analytics dependencies to the platform.

- openedx-event-sink-clickhouse: A plugin to send events to a Clickhouse database.
- event-routing-backends: A plugin to route events to different backends.

XBlocks
=======

Limesurvey XBlock
-----------------

This plugin adds a new XBlock to the platform that allows to embed a Limesurvey
survey in a course.

Mindmap XBlock
---------------

This plugin adds a new XBlock to the platform that allows to embed a Mindmap
in a course.

Files Manager XBlock
--------------------

This plugin adds a new XBlock to the platform that allows to share files to the
students in a course.

H5P XBlock
----------

This plugin adds a new XBlock to the platform that allows to embed H5P content.
This specific version has multiple improvements over the original H5P XBlock:

- Allow to view H5P content in the CMS
- Improvements to the H5P studio view

Feedback XBlock
---------------

This plugin adds a new XBlock to the platform that allows to embed a Feedback
form in a course. This specific version has multiple improvements over the
original Feedback XBlock:

- Improved translations
- Instructor dashboard integration to view the feedback results
- A new star icon likert set

edx-ora2
--------

This specific version of the edx-ora2 has multiple improvements over the
original edx-ora2 XBlock:



Platform plugins
================

Forum Email Notifier
--------------------

This plugin adds a new feature to the platform that allows to send email notifications
to the students when there is new activity in the forums. It also allows to configure
the frequency of the notifications for instructors in each course.

Superset
--------

This plugin adds a new feature to the platform that allows to embed Superset dashboards
in the platform.

License
*******

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

Contributing
************

Contributions are very welcome.
Please read `How To Contribute <https://openedx.org/r/how-to-contribute>`_ for details.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

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

.. |ci-badge| image:: https://github.com/eduNEXT/openedx-unidigital/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/openedx-unidigital/actions
    :alt: CI

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/openedx-unidigital.svg
    :target: https://pypi.python.org/pypi/openedx-unidigital/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/openedx-unidigital.svg
    :target: https://github.com/eduNEXT/openedx-unidigital/blob/main/LICENSE.txt
    :alt: License

.. TODO: Choose one of the statuses below and remove the other status-badge lines.
.. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red
