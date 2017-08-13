#encoding:utf8
#auth: mavarick
#date: {DATETIME}

import sys
sys.path.append("/Users/mavarick/github/scrapy_mysql")

from scrapy.http import Request
from scrapy_mysql.scheduler import Scheduler


class Setting(object):
    def __init__(self):
        self.data = {}

    def getbool(self, k):
        return self.data.get(k, None)

    def getint(self, k):
        return self.data.get(k, 0)

    def get(self, k):
        return self.data.get(k, None)

    def getdict(self, k):
        return self.data.get(k, {})


def test_scheduler():
    sch = Scheduler.from_settings(Setting())

    url = "htto://www.baidu.com"
    req = Request(url)


    class Spider(): pass
    spider = Spider()
    spider.name = 'sptest'
    def log(v): print v
    spider.log = log

    sch.open(spider)
    sch.enqueue_request(req)
    r = sch.next_request()
    print "return: "
    print r


if __name__ == "__main__":
    test_scheduler()

