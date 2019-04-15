import logging

from robot.model import SuiteVisitor

from .visitor_model import Keyword, Test, Suite, Message
from .service import RobotService
from .variables import ConfigurationVariables


logging.getLogger(name='reportportal_client').setLevel(logging.WARNING)
logging.getLogger(name='urllib3').setLevel(logging.WARNING)


class ReportPortalVisitor(SuiteVisitor):
    def __init__(self):
        self._variables = ConfigurationVariables()
        self._service = RobotService(
            endpoint=self._variables.endpoint,
            project=self._variables.project,
            token=self._variables.token,
            log_batch_size=self._variables.log_batch_size
        )

    def end_message(self, message):
        self._service.log(Message(message))

    def start_suite(self, data):
        suite = Suite(data)
        self._service.start_suite(suite)

    def end_suite(self, data):
        suite = Suite(data)
        self._service.finish_suite(suite)

    def start_test(self, data):
        test = Test(data)
        self._service.start_test(test)

    def end_test(self, data):
        test = Test(data)
        self._service.finish_test(test)

    def start_keyword(self, data):
        keyword = Keyword(data)
        self._service.start_keyword(keyword)

    def end_keyword(self, data):
        keyword = Keyword(data)
        self._service.finish_keyword(keyword)
