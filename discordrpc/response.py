from collections import Mapping


class Response(Mapping):
    """ Read-only object that represents a response from Discord.
     Shortcuts any key value pairs in nested dict 'data'. """
    def __init__(self, status_code: int, _dict: dict = {}, **kwargs):
        self.status_code = status_code
        self._dict = _dict or dict(kwargs)
        for k in self._dict.get('data', ()):
            self._dict[k] = self._dict['data'][k]

    def __getitem__(self, value):
        return self._dict[value]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)
