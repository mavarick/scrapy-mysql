#encoding:utf8
#auth: mavarick
#date: {DATETIME}

import logging
from scrapy.utils.project import get_project_settings

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


logger = logging.getLogger(__name__)

try:
    from scrapy_mysql import connection
except:
    print("Module is not installed : scrapy_mysql")
    raise

settings = get_project_settings()
url_server = connection.from_settings(settings)


HTTP_ERROR_CODE = -1
DNS_ERROR_CODE = -2
TIMEOUT_CODE = -3
UNKNOWN_HTTP_ERROR = -4


class ResponseErrMiddleware(object):
    def process_exception(self, request, exception, spider):
        url = request.url
        id = getattr(request, "id", None)
        if id is None:
            logger.error("No [id] in Request of url: [{}]".format(url))

        if isinstance(exception, HttpError):
            logger.error("HttpError: {}".format(url))
            url_server.update_status(dict(id=id, status=HTTP_ERROR_CODE))
        elif isinstance(exception, DNSLookupError):
            logger.error("DNSLookupError: {}".format(url))
            url_server.update_status(dict(id=id, status=DNS_ERROR_CODE))
        elif isinstance(exception, TimeoutError) or isinstance(exception, TCPTimedOutError):
            logger.error("TimeoutError: {}".format(url))
            url_server.update_status(dict(id=id, status=TIMEOUT_CODE))
        else:
            logger.error("Unknown Http Error: {}".format(url))
            url_server.update_status(dict(id=id, status=UNKNOWN_HTTP_ERROR))
