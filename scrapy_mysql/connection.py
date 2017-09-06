# api to remote mysql web server
import logging
from .utils.SpiderUrlApi import SpiderUrlApi
from . import defaults
from .logger import sm_log


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
    server = kwargs['SERVER']
    auth_code = kwargs['AUTH_CODE']
    url_server = SpiderUrlApi(server, auth_code)

    return url_server


class Connection(object):
    def __init__(self):
        from scrapy.utils.project import get_project_settings
        settings = get_project_settings()
        conn = from_settings(settings)
        self.conn = conn

    def update_status(self, id, status=10, content=None):
        data = dict(id=id, status=status)
        if content is not None:
            data['content'] = ""
        resp = self.conn.update(data)
        code = resp['code']
        if code != 0:
            msg = resp['msg']
            data = resp['data']
            sm_log.error("error to update status of id[%s] with code: [%s], msg:[%s], data:[%s]" % (
                id, status, msg, data))


conn = Connection()
