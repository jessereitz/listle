from unittest import mock, TestCase

import flask

from listle.connectors import FirestoreConnector
from listle.models import Record


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
            r.id = '83d34ff5-ee63-4cf7-9074-ca56c0c1b5a4'
            r.datetime = '2020-03-29T05:38:59.322915+00:00'
            connector = FirestoreConnector(r)
            return connector, r

    @mock.patch('listle.connectors.firestore.firestore')
    def test_client(self, firestore_mock):
        client_mock = mock.Mock(return_value='test client')
        firestore_mock.Client = client_mock

        connector, _ = self.get_connector()
        actual_client = connector.client

        self.assertEqual(actual_client, 'test client')

    @mock.patch('listle.connectors.firestore.FirestoreConnector.client')
    def test_dispatch(self, client_mock):
        doc_ref_mock = mock.Mock()
        collection_ref_mock = mock.Mock()
        collection_ref_mock.document.return_value = doc_ref_mock
        client_mock.collection.return_value = collection_ref_mock

        expected_dict = {'id': '83d34ff5-ee63-4cf7-9074-ca56c0c1b5a4', 'meta': {'charset': 'utf-8', 'url': 'http://listle.test/blah', 'datetime': '2020-03-29T05:38:59.322915+00:00', 'headers': {'Host': 'listle.test', 'Content-Type': 'application/json', 'Content-Length': '38'}, 'user_agent': {'string': '', 'platform': None, 'browser': None, 'version': None, 'language': None}}, 'fields': {'test1': 'value1', 'test2': 'value2'}}

        with self.app.test_request_context(**self.req_context):
            connector, record = self.get_connector()
            connector.dispatch()

        client_mock.collection.assert_called_once_with(connector.RECORD_COLLECTION)
        collection_ref_mock.document.assert_called_once_with(record.id)
        doc_ref_mock.set.assert_called_once_with(expected_dict)
