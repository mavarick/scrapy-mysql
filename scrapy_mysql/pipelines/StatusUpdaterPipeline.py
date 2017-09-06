#encoding:utf8
#auth: mavarick

import sys
import hashlib
import json
import logging
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    sys.path.append("../")

try:
    from scrapy_mysql import connection
except:
    print("Module is not installed : scrapy_mysql")
    raise

logger = logging.getLogger(__name__)
settings = get_project_settings()
url_server = connection.from_settings(settings)


class StatusUpdaterPipeline(object):
    def __init__(self, status_done=1):
        self.status = status_done

    def open_spider(self, spider):
        # check mysql server exists
        pass

    def process_item(self, item, spider):

        url = item.url
        id = item.id
        if id is None:
            logger.error("No [id] in Request of url: [{}]".format(url))

        url_server.update_status(dict(id=id, status=self.status))
        return item
