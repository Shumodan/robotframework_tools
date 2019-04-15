from datetime import datetime


ENTITY_MAP = {
    'TestSuite': 'SUITE',
    'TestCase': 'TEST',
    'Keyword': 'STEP',
    'TestSuiteKeyword': 'STEP',
    'TestCaseKeyword': 'STEP',
    'KeywordKeyword': 'STEP',
    'TestSuiteSetup': 'BEFORE_SUITE',
    'TestSuiteTeardown': 'AFTER_SUITE',
    'TestCaseSetup': 'BEFORE_TEST',
    'TestCaseTeardown': 'AFTER_TEST',
    'KeywordSetup': 'BEFORE_TEST',
    'KeywordTeardown': 'AFTER_TEST',
}


def get_item_time(item_time):
    if not item_time:
        return item_time
    return str(int(
        datetime.strptime(item_time, '%Y%m%d %H:%M:%S.%f').timestamp() * 1000
    ))


class Entity:
    def __init__(self, data):
        self.name = data.name
        self.doc = data.doc
        self.status = data.status
        self.message = data.message
        self.robot_id = data.id
        self.tags = [str(item) for item in getattr(data, 'tags', [])]
        self.entity_type = ENTITY_MAP[data.__class__.__name__]
        self.start_time = get_item_time(getattr(data, 'starttime', None))
        self.end_time = get_item_time(getattr(data, 'endtime', None))


class Suite(Entity):
    def __init__(self, data):
        super().__init__(data)
        self.name = data.longname
        self.suites = data.suites
        self.tests = data.tests
        self.source = data.source
        self.total_tests = data.test_count
        self.metadata = data.metadata
        self.statistics = data.statistics


class Test(Entity):
    def __init__(self, data):
        super().__init__(data)
        self.longname = data.longname
        self.critical = data.critical


class Keyword(Entity):
    def __init__(self, data):
        super().__init__(data)
        self.libname = data.libname
        self.keyword_name = data.kwname
        self.args = data.args
        self.assign = data.assign

        parent_entity_type = self._get_parent_type(data.parent)
        if parent_entity_type and data.type != 'kw':
            self.entity_type = ENTITY_MAP[f'{parent_entity_type}{data.type.capitalize()}']

        assign = ', '.join(self.assign)
        assignment = f'{assign} = ' if self.assign else ''
        arguments = ', '.join(self.args)
        self.name = f'{assignment}{self.name} ({arguments})'[:256]

    @staticmethod
    def _get_parent_type(data):
        if not data:
            return None
        return data.__class__.__name__


class Message:
    def __init__(self, data):
        self.message = data.message
        self.level = data.level
        self.attachment = getattr(data, 'attachment', None)
        self.timestamp = get_item_time(data.timestamp)
        self.html = data.html
