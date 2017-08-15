import six
import hashlib


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s


def get_default_id(request, spider):
    url = request.url
    return hashlib.md5(url).hexdigest()

