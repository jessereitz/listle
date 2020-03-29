from email.message import EmailMessage
from unittest import mock, TestCase

import flask

from listle.connectors import EmailConnector
from listle.connectors.email import config
from listle.models import Record

EMAIL_CONTENT = '''
New record created in Listle. Please see below:

========== FIELDS ==========
test1: value1
test2: value2

========== RECORD META INFORMATION ==========
Record ID: 83d34ff5-ee63-4cf7-9074-ca56c0c1b5a4
Datetime: 2020-03-29T05:38:59.322915+00:00
Charset: utf-8
Headers: {"Host": "listle.test", "Content-Type": "application/json", "Content-Length": "38"}
User Agent: {"string": "", "platform": null, "browser": null, "version": null, "language": null}
'''


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

        self.config = {
            'from_email': 'test@test.com',
            'to_email': 'testto@test.com',
            'host': 'smpt.test.com',
            'port': 1234,
            'user': 'test_user',
            'password': 'test_password'
        }

    def get_connector(self):
        with self.app.test_request_context(**self.req_context):
            r = Record(flask.request)
            connector = EmailConnector(r)
            return connector

    @mock.patch('listle.connectors.email.smtplib.SMTP_SSL')
    def test_client(self, smtp_mock):
        smtp_mock_instance = mock.Mock()
        smtp_mock.return_value = smtp_mock_instance

        with mock.patch.dict(config, self.config):
            connector = self.get_connector()
            actual_client = connector.client

        self.assertEqual(actual_client, smtp_mock_instance)
        smtp_mock.assert_called_once_with(self.config['host'], self.config['port'], context=mock.ANY)
        smtp_mock_instance.login.assert_called_once_with(self.config['user'], self.config['password'])

    def test_build_message(self):
        with self.app.test_request_context(**self.req_context):
            with mock.patch.dict(config, self.config):
                r = Record(flask.request)
                r.id = '83d34ff5-ee63-4cf7-9074-ca56c0c1b5a4'
                r.datetime = '2020-03-29T05:38:59.322915+00:00'
                connector = EmailConnector(r)
                actual_msg = connector.build_message()

        self.assertIsInstance(actual_msg, EmailMessage)
        self.assertEqual(actual_msg.get_content(), EMAIL_CONTENT)
        self.assertEqual(actual_msg['Subject'], connector.EMAIL_SUBJECT)
        self.assertEqual(actual_msg['From'], self.config['from_email'])
        self.assertEqual(actual_msg['To'], self.config['to_email'])

    def test_build_content(self):
        with self.app.test_request_context(**self.req_context):
            r = Record(flask.request)
            r.id = '83d34ff5-ee63-4cf7-9074-ca56c0c1b5a4'
            r.datetime = '2020-03-29T05:38:59.322915+00:00'
            connector = EmailConnector(r)
            actual_content = connector._build_content()

        self.assertEqual(actual_content, EMAIL_CONTENT)

    @mock.patch('listle.connectors.email.EmailConnector.client', new_callable=mock.PropertyMock())
    def test_dispatch(self, client_mock):
        client_mock_instance = mock.Mock()
        client_mock.return_value = client_mock_instance

        with self.app.test_request_context(**self.req_context):
            r = Record(flask.request)
            r.id = '83d34ff5-ee63-4cf7-9074-ca56c0c1b5a4'
            r.datetime = '2020-03-29T05:38:59.322915+00:00'
            connector = EmailConnector(r)
            connector.build_message = mock.Mock(return_value='test message')
            connector.dispatch()

        connector.client.send_message.assert_called_once_with('test message')
