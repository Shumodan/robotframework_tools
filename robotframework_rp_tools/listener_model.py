from datetime import datetime


ENTITY_MAP = {
    'Keyword': 'STEP',
    'SuiteKeyword': 'STEP',
    'TestKeyword': 'STEP',
    'KeywordKeyword': 'STEP',
    'SuiteSetup': 'BEFORE_SUITE',
    'SuiteTeardown': 'AFTER_SUITE',
    'TestSetup': 'BEFORE_TEST',
    'TestTeardown': 'AFTER_TEST',
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
    def __init__(self, name, **attributes):
        self.name = name
        self.longname = attributes.get('longname', '')
        self.doc = attributes['doc']
        self.status = attributes.get('status')
        self.message = attributes.get('message')
        self.robot_id = attributes.get('id')
        self.start_time = get_item_time(attributes.get('starttime'))
        self.end_time = get_item_time(attributes.get('endtime'))


class Suite(Entity):
    def __init__(self, name, **attributes):
        super().__init__(name, **attributes)
        self.suites = attributes['suites']
        self.tests = attributes['tests']
        self.source = attributes['source']
        self.total_tests = attributes['totaltests']
        self.metadata = attributes['metadata']
        self.statistics = attributes.get('statistics')
        self.entity_type = 'SUITE'


class Test(Entity):
    def __init__(self, name, **attributes):
        super().__init__(name, **attributes)
        self.critical = attributes['critical']
        self.template = attributes['template']
        self.tags = attributes['tags']
        self.entity_type = 'TEST'


class Keyword(Entity):
    def __init__(self, name, **attributes):
        super().__init__(name, **attributes)
        self.libname = attributes['libname']
        self.keyword_name = attributes['kwname']
        self.tags = attributes['tags']
        self.args = attributes['args']
        self.assign = attributes['assign']
        self.keyword_type = attributes['type']
        self.parent_type = attributes.get('parent_type', '')

        self.entity_type = ENTITY_MAP[f'{self.parent_type}{self.keyword_type}']
        assign = ', '.join(self.assign)
        assignment = f'{assign} = ' if self.assign else ''
        arguments = ', '.join(self.args)
        self.name = f'{assignment}{self.name} ({arguments})'[:256]


class Message:
    def __init__(self, **attributes):
        self.message = attributes['message']
        self.level = attributes.get('level', 'INFO')
        self.attachment = attributes.get('attachment')
        self.timestamp = get_item_time(attributes.get('timestamp'))
        self.html = attributes['html']
