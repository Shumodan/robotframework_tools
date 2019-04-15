from collections import deque

from .variables import ConfigurationVariables
from .service import RobotService
from .listener_model import Keyword, Test, Suite, Message


class ReportPortalListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self._variables = ConfigurationVariables()
        self._service = RobotService(
            endpoint=self._variables.endpoint,
            project=self._variables.project,
            token=self._variables.token,
            log_batch_size=self._variables.log_batch_size
        )
        self._parent_types = deque()

    def start_suite(self, name, attributes):
        suite = Suite(name, **attributes)
        self._parent_types.append('Suite')
        self._service.start_suite(suite)

    def end_suite(self, name, attributes):
        suite = Suite(name, **attributes)
        self._parent_types.pop()
        self._service.finish_suite(suite)

    def start_test(self, name, attributes):
        test = Test(name, **attributes)
        self._parent_types.append('Test')
        self._service.start_test(test)

    def end_test(self, name, attributes):
        test = Test(name, **attributes)
        self._parent_types.pop()
        self._service.finish_test(test)

    def start_keyword(self, name, attributes):
        parent_type = self._parent_types[-1]
        self._parent_types.append('Keyword')
        keyword = Keyword(name, parent_type=parent_type, **attributes)
        self._service.start_keyword(keyword)

    def end_keyword(self, name, attributes):
        self._parent_types.pop()
        parent_type = self._parent_types[-1]
        keyword = Keyword(name, parent_type=parent_type, **attributes)
        self._service.finish_keyword(keyword)

    def log_message(self, message):
        msg = Message(**message)
        self._service.log(msg)
