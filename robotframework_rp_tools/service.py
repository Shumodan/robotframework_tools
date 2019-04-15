import traceback
from functools import lru_cache

from reportportal_client import ReportPortalServiceAsync

from .variables import ConfigurationVariables


@lru_cache(None)
class RobotService:
    status_mapping = {
        'PASS': 'PASSED',
        'FAIL': 'FAILED',
        'SKIP': 'SKIPPED'
    }

    log_level_mapping = {
        'INFO': 'INFO',
        'FAIL': 'ERROR',
        'TRACE': 'TRACE',
        'DEBUG': 'DEBUG',
        'WARN': 'WARN'
    }

    def __init__(self, endpoint, project, token, log_batch_size):
        self._first_suite_id = 's1'
        self.rp = ReportPortalServiceAsync(
            endpoint=endpoint,
            project=project,
            token=token,
            error_handler=lambda x: traceback.print_exception(*x),
            log_batch_size=log_batch_size
        )

    def start_suite(self, suite):
        if suite.robot_id == self._first_suite_id:
            self._start_launch(suite)
        else:
            self.rp.start_test_item(
                name=suite.name,
                description=suite.doc,
                tags=suite.tags,
                start_time=suite.start_time,
                item_type=suite.entity_type
            )

    def finish_suite(self, suite, issue=None):
        if suite.robot_id == self._first_suite_id:
            self._finish_launch(suite)
            self._terminate_service()
        else:
            self.rp.finish_test_item(
                end_time=suite.end_time,
                status=self.status_mapping[suite.status],
                issue=issue
            )

    def start_test(self, test):
        self.rp.start_test_item(
            name=test.name,
            description=test.doc,
            tags=test.tags,
            start_time=test.start_time,
            item_type=test.entity_type
        )

    def finish_test(self, test, issue=None):
        self.rp.finish_test_item(
            end_time=test.end_time,
            status=self.status_mapping[test.status],
            issue=issue
        )

    def start_keyword(self, keyword):
        self.rp.start_test_item(
            name=keyword.name,
            description=keyword.doc,
            tags=keyword.tags,
            start_time=keyword.start_time,
            item_type=keyword.entity_type
        )

    def finish_keyword(self, keyword, issue=None):
        self.rp.finish_test_item(
            end_time=keyword.end_time,
            status=self.status_mapping[keyword.status],
            issue=issue
        )

    def log(self, message):
        self.rp.log(
            time=message.timestamp,
            message=message.message,
            level=self.log_level_mapping[message.level],
            attachment=message.attachment
        )

    def _terminate_service(self):
        self.rp.terminate()

    def _start_launch(self, launch, mode=None):
        self.rp.start_launch(
            name=ConfigurationVariables().launch_name,
            start_time=launch.start_time,
            description=ConfigurationVariables().launch_doc,
            mode=mode,
            tags=ConfigurationVariables().launch_tags
        )

    def _finish_launch(self, launch):
        self.rp.finish_launch(
            end_time=launch.end_time,
            status=self.status_mapping[launch.status]
        )
