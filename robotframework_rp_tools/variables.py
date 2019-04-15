import os

from functools import lru_cache

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


@lru_cache(None)
class ConfigurationVariables:
    def __init__(self):
        self._builtin = BuiltIn()
        self.uuid = None
        self.endpoint = None
        self.launch_name = None
        self.project = None
        self.launch_doc = None
        self.launch_tags = None
        self.log_batch_size = None
        self.check_variables()

    def get_variable(self, name, default=None):
        try:
            return self._builtin.get_variable_value("${" + name + "}", default=default)
        except RobotNotRunningError:
            return os.environ.get(name, default=default)

    def check_variables(self):
        self.uuid = self._is_exist(
            self.get_variable('RP_UUID'),
            'Missing parameter RP_UUID for robot run\n'
            'You should pass -v RP_UUID:<uuid_value>'
        )

        self.endpoint = self._is_exist(
            self.get_variable('RP_ENDPOINT'),
            'Missing parameter RP_ENDPOINT for robot run\n'
            'You should pass -v RP_RP_ENDPOINT:<endpoint_value>'
        )

        self.launch_name = self._is_exist(
            self.get_variable('RP_LAUNCH'),
            'Missing parameter RP_LAUNCH for robot run\n'
            'You should pass -v RP_LAUNCH:<launch_name_value>'
        )

        self.project = self._is_exist(
            self.get_variable('RP_PROJECT'),
            'Missing parameter RP_PROJECT for robot run\n'
            'You should pass -v RP_PROJECT:<project_name_value>'
        )

        self.launch_doc = self.get_variable('RP_LAUNCH_DOC')
        self.launch_tags = self.get_variable('RP_LAUNCH_TAGS', default='').split(',')
        self.log_batch_size = int(self.get_variable('RP_LOG_BATCH_SIZE', default=20))

    @staticmethod
    def _is_exist(value, error):
        if not value:
            raise NameError(error)
        return value
