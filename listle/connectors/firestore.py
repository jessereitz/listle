import json
import logging

from google.cloud import firestore

logger = logging.getLogger(__name__)


class FirestoreConnector:
    RECORD_COLLECTION = 'records'

    _client = None

    def __init__(self, record):
        self.record = record

    @property
    def client(self):
        if self._client is None:
            self._client = firestore.Client()
        return self._client

    def dispatch(self):
        collection_ref = self.client.collection(self.RECORD_COLLECTION)
        doc_ref = collection_ref.document(self.record.id)
        doc_ref.set(dict(self.record))
