from datetime import datetime, timezone
from unittest import mock, TestCase

import flask
from freezegun import freeze_time

from listle.models import Record

now = datetime.now(timezone.utc)


class TestRecord(TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        self.req_context = {
            'path': '/blah',
            'base_url': 'http://listle.test',
            'json': {
                'test1': 'value1',
                'test2': 'value2'
            }
        }

    @freeze_time(now)
    def test_as_dict(self):
        expected_dict = {
            'id': mock.ANY,
            'meta': {
                'charset': 'utf-8',
                'url': f"{self.req_context['base_url']}{self.req_context['path']}",
                'datetime': now.isoformat(),
                'headers': {'Host': 'listle.test', 'Content-Type': 'application/json', 'Content-Length': '38'},
                'user_agent': {'string': '', 'platform': None, 'browser': None, 'version': None, 'language': None}
            },
            'fields': {'test1': 'value1', 'test2': 'value2'},
        }

        with self.app.test_request_context(**self.req_context):
            r = Record(flask.request)
            actual_dict = r.as_dict()
            self.assertDictEqual(actual_dict, expected_dict)

    @freeze_time(now)
    @mock.patch('listle.models.uuid')
    def test_iter(self, uuid_mock):
        uuid_mock.uuid4.return_value = 'test-uuid'
        expected_dict = {
            'id': 'test-uuid',
            'meta': {
                'charset': 'utf-8',
                'url': f"{self.req_context['base_url']}{self.req_context['path']}",
                'datetime': now.isoformat(),
                'headers': {'Host': 'listle.test', 'Content-Type': 'application/json', 'Content-Length': '38'},
                'user_agent': {'string': '', 'platform': None, 'browser': None, 'version': None, 'language': None}
            },
            'fields': {'test1': 'value1', 'test2': 'value2'},
        }

        with self.app.test_request_context(**self.req_context):
            r = Record(flask.request)
            actual_dict = dict(r)
            self.assertDictEqual(actual_dict, expected_dict)
