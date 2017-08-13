import six
from scrapy.utils.misc import load_object

from . import defaults

# api to remote mysql web server
from utils.SpiderUrlApi import SpiderUrlApi


def get_mysql_from_settings(settings):
    """Returns a mysql client instance from given Scrapy settings object.

    This function uses ``get_client`` to instantiate the client and uses
    ``defaults.MYSQL_PARAMS`` global as defaults values for the parameters. You
    can override them using the ``MYSQL_PARAMS`` setting.

    Parameters
    ----------
    settings : Settings
        A scrapy settings object. See the supported settings below.

    Returns
    -------
    server
        Redis client instance.

    Other Parameters
    ----------------
    MYSQL_URL : str, optional
        Server connection URL.
    MYSQL_HOST : str, optional
        Server host.
    MYSQL_PORT : str, optional
        Server port.
    MYSQL_ENCODING : str, optional
        Data encoding.
    MYSQL_PARAMS : dict, optional
        Additional client parameters.

    """
    params = defaults.MYSQL_REMOTE_PARAMS.copy()
    params.update(settings.getdict('MYSQL_URL_REMOTE_PARAMS'))

    return get_mysql(**params)


# Backwards compatible alias.
from_settings = get_mysql_from_settings


def get_mysql(**kwargs):
    """Returns a mysql client instance.

    Parameters
    ----------
    mysql_cls : class, optional
        Defaults to ``mysql.StrictRedis``.
    url : str, optional
        If given, ``mysql_cls.from_url`` is used to instantiate the class.
    **kwargs
        Extra parameters to be passed to the ``mysql_cls`` class.

    Returns
    -------
    server
        Redis client instance.

    """
    server = kwargs['server']
    auth_code = kwargs['auth_code']
    url_server = SpiderUrlApi(server, auth_code)

    return url_server


class StartServerException(Exception):
    pass