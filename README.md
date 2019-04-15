robotframework-rp-tools
==============================

Listener and visitor modules for integration with ReportPortal

Installation
------------

The latest stable version of library is available on PyPI:

    pip install robotframework-rp-tools

Usage
-----

To run these modules you need to set the following environment variables:

REQUIRED:
```
export RP_TOKEN="your_user_uuid"
export RP_ENDPOINT="your_reportportal_url"
export RP_LAUNCH="launch_name"
export RP_PROJECT="reportportal_project_name"
```

NOT REQUIRED:
```
export RP_LAUNCH_DOC="some_documentation_for_launch"
    - Description for the launch
export RP_LAUNCH_TAGS="RF Smoke"
    - Space-separated list of tags for the launch
export RP_LOG_BATCH_SIZE="10"
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
