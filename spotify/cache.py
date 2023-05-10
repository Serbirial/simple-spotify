# TODO add caching

class Cache:
    """ This is for internal use, nothing will be explained. """
    def __init__(self):
        self._data = {}

    def get(self, key):
        try:
            return self._data[key]
        except KeyError:
            return False

    def put(self, key: str, value):
        if key in self._data:
            return False # dont override, this should not happen, the only thing that should happen is similar metadata is found for another URL
        self._data[key] = value

    @property
    def data():
        return self._data

    def __iter__(self):
        for k in self._data.keys():
            yield k