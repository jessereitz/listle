import json
import logging
import smtplib
import ssl
from email.message import EmailMessage

from listle.constants import EMAIL_CONNECTOR_CONFIG as config


logger = logging.getLogger(__name__)


PLAIN_TEXT_TEMPLATE = '''
New record created in Listle. Please see below:

========== FIELDS ==========
'''

PLAIN_TEXT_META_TEMPLATE = '''
========== RECORD META INFORMATION ==========
Record ID: {record_id}
Datetime: {datetime}
Charset: {charset}
Headers: {headers}
User Agent: {user_agent}
'''


class EmailConnector:
    EMAIL_SUBJECT = 'New Listle Record'
    _client = None

    def __init__(self, record):
        self.record = record
        self.from_email = config['from_email']
        self.to_email = config['to_email']
        self.host = config['host']
        self.port = config['port']
        self.user = config['user']
        self.password = config['password']

    @property
    def client(self):
        if self._client is None:
            ssl_context = ssl.create_default_context()
            self._client = smtplib.SMTP_SSL(self.host, self.port, context=ssl_context)
            self._client.login(self.user, self.password)
        return self._client

    def build_message(self):
        msg = EmailMessage()
        msg.set_content(self._build_content())
        msg['Subject'] = self.EMAIL_SUBJECT
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        return msg

    def _build_content(self):
        field_content = ''
        for field_name, field_val in self.record.fields.items():
            field_content += f'{field_name}: {field_val}\n'

        meta_info = PLAIN_TEXT_META_TEMPLATE.format(
            record_id=self.record.id,
            datetime=self.record.datetime,
            charset=self.record.charset,
            headers=json.dumps(dict(self.record.headers)),
            user_agent=json.dumps(self.record.ua_as_dict()),
        )

        content = f'{PLAIN_TEXT_TEMPLATE}{field_content}{meta_info}'
        return content

    def dispatch(self):
        logger.info('Building message')
        msg = self.build_message()
        self.client.send_message(msg)
