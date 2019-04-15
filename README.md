robotframework_rp_tools
==============================

Listener and visitor modules for integration with ReportPortal

Installation
------------

The latest stable version of library is available on PyPI:

    pip install robotframework_rp_tools

Usage
-----

For reporting results to ReportPortal you need to pass some variables to pybot run:

REQUIRED:
```
--variable RP_UUID:"your_user_uuid"
--variable RP_ENDPOINT:"your_reportportal_url"
--variable RP_LAUNCH:"launch_name"
--variable RP_PROJECT:"reportportal_project_name"
```
NOT REQUIRED:
```
--variable RP_LAUNCH_DOC:"some_documentation_for_launch"
    - Description for the launch
--variable RP_LAUNCH_TAGS:"RF Smoke"
    - Space-separated list of tags for the launch
--variable RP_LOG_BATCH_SIZE:"10"
    - Default value is "20", affects size of async batch log requests
```

If you need a listener:
```
--listener robotframework_rp_tools.Listener

```
in case of visitor
```
--prerebotmodifier robotframework_rp_tools.Visitor
```

License
-------
MIT License (see the LICENSE.txt file)
