"""A pickle wrapper module with protocol=-1 by default."""

try:
    import cPickle as pickle  # PY2
except ImportError:
    import pickle

import base64


def loads(s):
    s2 = base64.b64decode(s)
    return pickle.loads(s2)


def dumps(obj):
    s = pickle.dumps(obj, protocol=-1)
    return base64.b64encode(s)
