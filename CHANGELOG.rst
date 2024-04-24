Change Log
##########

..
   All enhancements and patches to openedx_unidigital will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
**********

*

0.14.5 - 2024-04-24
**********************************************

Changed
=======

* Upgrade ``xblock-content-restrictions`` to ``v0.3.1`` in stage and prod requirements
* Upgrade ``xblock-controlled-navigation`` to ``v0.2.1`` in stage and prod requirements

0.14.4 - 2024-04-23
**********************************************

Changed
=======

* Install ``xblock-content-restrictions`` with temp branch in stage requirements

0.14.3 - 2024-04-22
**********************************************

Changed
=======

* Upgrade ``xblock-content-restrictions`` to ``0.3.0`` in prod requirements

0.14.2 - 2024-04-19
**********************************************

Changed
=======

* Upgrade ``platform-plugin-aspects`` to ``0.7.2`` in prod requirements

0.14.1 - 2024-04-19
**********************************************

Changed
=======

* Remove unnecessary requirement from prod requirements after platform-plugin-aspects upgrade.

0.14.0 - 2024-04-18
**********************************************

Changed
=======

* Upgrade ``platform-plugin-aspects`` to ``0.7.1`` in prod requirements
* Upgrade ``edx-event-routing-backends`` to ``9.0.0`` in prod requirements

0.13.0 - 2024-04-16
**********************************************

Added
=====

* Added ``xblock-content-restrictions`` in prod requirements.
* Added ``xblock-controlled-navigation`` in prod requirements.

0.12.0 - 2024-04-15
**********************************************

Updated
=======

* Moved Additional Features section to ``docs`` folder.

Added
=====

* Added ``default`` key in membership by language configuration.

0.11.0 - 2024-04-10
**********************************************

Added
=====

* Add user to team/cohort depending on their language preference in course enrollment event.

0.10.9 - 2024-04-02
**********************************************

Changed
=======

* Upgrade ``edx-ora2`` with latest changes in ``5.5.5/edues/santander`` branch in stage requirements

0.10.8 - 2024-04-01
**********************************************

Changed
=======

* Upgrade ``feedback-xblock`` to ``master`` branch in stage requirements

0.10.7 - 2024-03-20
**********************************************

Changed
=======

* Upgrade ``platform-plugin-elm-credentials`` to ``v0.3.1`` in stage and prod requirements

0.10.6 - 2024-03-19
**********************************************

Changed
=======

* Upgrade ``platform-plugin-elm-credentials`` to ``v0.3.0`` in stage and prod requirements

0.10.5 - 2024-03-19
**********************************************

Changed
=======

* Update feedback-block branch ``1.4.0/edues`` fixing lms rating content

0.10.4 - 2024-03-19
**********************************************

Changed
=======

* Use feedback-block with ``1.4.0/edues`` branch in stage requirements

0.10.3 - 2024-03-18
**********************************************

Added
=====

* Use feedback-block with branch ``bav/show-parents-display-name`` in stage requirements

0.10.2 - 2024-03-11
**********************************************

Added
=====

* xblock-filesmanager updated to v0.8.1

0.10.1 - 2024-03-11
**********************************************

Added
=====

* Add ``seb-openedx`` with branch ``bav/quince-support-tmp`` in stage requirements

0.10.0 - 2024-03-07
**********************************************

Added
=====

* xblock-filesmanager updated to v0.8.0

0.9.1 - 2024-03-06
**********************************************

Changed
=======

* Replace ``openedx-event-sink-clickhouse`` by ``platform-plugin-aspects==0.2.0`` in production requirements

0.9.0 - 2024-02-01
**********************************************

Added
=====

* Remove extra character from feedback-block in stage requirements

0.8.0 - 2024-01-31
**********************************************

Added
=====

* Add ``platform-plugin-turnitin`` in stage requirements

0.7.0 - 2024-01-31
**********************************************

Added
=====

* Add quince.1 support for edues project

0.6.2 - 2024-01-29
**********************************************

Changed
=======

* Update ``platform-plugin-elm-credentials`` in stage and prod requirements

0.6.1 - 2024-01-23
**********************************************

Changed
=======

* Add ``openedx-events`` in stage requirements

0.6.0 - 2024-01-23
**********************************************

Added
=====

* Add extras require for stage and prod environments

0.5.0 - 2024-01-23
**********************************************

Added
=====

* platform-plugin-elm-credentials v0.2.0

0.4.1 - 2024-01-04
**********************************************

Changed
=======

* xblock-filesmanager updated to v0.7.0

0.4.0 - 2023-12-06
**********************************************

Added
=====

* platform-plugin-teams v0.2.0

0.3.2 - 2023-12-04
**********************************************

Added
=====

* platform-plugin-communications updated to v0.3.1

0.3.1 - 2023-12-01
**********************************************

Added
=====

* xblock-filesmanager updated to v0.6.4

0.3.0 - 2023-12-01
**********************************************

Added
=====

* platform-plugin-communications v0.3.0

0.2.3 - 2023-11-30
**********************************************

Added
=====

* xblock-filesmanager updated to v0.6.3

0.2.2 - 2023-12-01
**********************************************

Added
=====

* xblock-filesmanager updated to v.0.6.2

0.2.1 - 2023-11-28
**********************************************

Added
=====

* xblock-filesmanager updated to v.0.6.1

0.2.0 - 2023-11-27
**********************************************

Added
=====

* xblock-filesmanager updated to v.0.6.0

0.1.0 - 2023-11-23
**********************************************

Added
=====

* Initial release of openedx_unidigital.
* Added Unidigital required dependencies.
