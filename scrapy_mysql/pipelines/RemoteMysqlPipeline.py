#encoding:utf8
#auth: mavarick

import hashlib
import json
# from scrapy.utils.project import get_project_settings

# remote mysql api
import sys

if __name__ == "__main__":
    sys.path.append("../")

from scrapy_mysql.utils import SpiderDBApi
DEFALUT_DB_URL = "http://127.0.0.1:11021"
DEFAULT_AUTH_CODE = "auth_code"


class RemoteMysqlPipeline(object):
    def __init__(self, db_url=DEFALUT_DB_URL, auth_code=DEFAULT_AUTH_CODE):
        self.db_api = SpiderDBApi(db_url, auth_code)
        print "load SpiderDBApi success"

    def open_spider(self, spider):
        # check mysql server exists
        pass

    def process_item(self, item, spider):

        url = item['url']
        data = {
            "id": self._get_id(url),
            "url": url,
            "source": spider.name,
            "content": json.dumps(item._values),
            "title": item['title']

        }
        resp = self.db_api.insert(data)
        code = resp['code']
        if code != 0:
            msg = ("[RemoteMysqlPipeline]ERROR: code: [%s], msg: [%s], data: \n %s"%(
                code, resp['msg'], resp['data']
            ))
            raise Exception(msg)
        return item

    def _get_id(self, url):
        return hashlib.md5(url).hexdigest()


def __test():
    pl = RemoteMysqlPipeline()
    class Spider(object): pass
    spider = Spider()
    spider.name = "test"
    item = dict(url="test_url")
    pl.process_item(item, spider)


if __name__ == "__main__":
    __test()

