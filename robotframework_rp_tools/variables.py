import os

from functools import lru_cache


@lru_cache(None)
class ConfigurationVariables:
    def __init__(self):
        self.token = None
        self.endpoint = None
        self.launch_name = None
        self.project = None
        self.launch_doc = None
        self.launch_tags = None
        self.log_batch_size = None
        self.check_variables()

    @staticmethod
    def get_variable(name, default=None):
        return os.environ.get(name, default=default)

    def check_variables(self):
        self.token = self._is_exist(
            self.get_variable('RP_TOKEN'),
            'Missing parameter RP_TOKEN for robot run'
        )

        self.endpoint = self._is_exist(
            self.get_variable('RP_ENDPOINT'),
            'Missing parameter RP_ENDPOINT for robot run'
        )

        self.launch_name = self._is_exist(
            self.get_variable('RP_LAUNCH'),
            'Missing parameter RP_LAUNCH for robot run'
        )

        self.project = self._is_exist(
            self.get_variable('RP_PROJECT'),
            'Missing parameter RP_PROJECT for robot run'
        )

        self.launch_doc = self.get_variable('RP_LAUNCH_DOC')
        self.launch_tags = self.get_variable('RP_LAUNCH_TAGS', default='').split(',')
        self.log_batch_size = int(self.get_variable('RP_LOG_BATCH_SIZE', default=20))

    @staticmethod
    def _is_exist(value, error):
        if not value:
            raise NameError(error)
        return value
