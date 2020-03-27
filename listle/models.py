import uuid
from datetime import datetime


class Record:
    _fields = None

    def __init__(self, request):
        self._request = request
        self.charset = self._request.charset
        self.url = self._request.url
        self.headers = self._request.headers
        self.fields = self._request.json
        self.user_agent = self._request.user_agent

        self.uuid = str(uuid.uuid4())

    def __iter__(self):
        yield from self.as_dict().items()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'<Record {self.uuid}>'

    def as_dict(self):
        ua = self._request.user_agent

        ua_as_dict = {
            'string': ua.string,
            'platform': ua.platform,
            'browser': ua.browser,
            'version': ua.version,
            'language': ua.language,
        }

        d = {
            'id': self.uuid,
            'meta': {
                'charset': self.charset,
                'url': self.url,
                'datetime': datetime.now().isoformat(),
                'headers': dict(self.headers),
                'user_agent': ua_as_dict,
            },
            'fields': self.fields,
        }
        return d
