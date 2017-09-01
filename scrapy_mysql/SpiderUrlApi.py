#encoding:utf8


""" api wrapper for url db server, the fields should be:
must:
    id
    url
    source
should: (field, default value)
    source, ""
    title, ""
    content, ""
    status, 0
    query_cnt, 0
    tag, ""
"""

import urllib
import urlparse
import requests
import json
import logging

# logging.basicConfig()
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARN)
requests_log.propagate = True

class SpiderUrlApi(object):
    def __init__(self, url, auth_code):
        """
        用来请求urldb的wrapper

        :param url: domain:port/path1/path2...
        :param auth_code: as one parameter to add the tail of path
        """
        if not url.endswith("/"):
            url += "/"
        self.url = url
        self.auth_code = auth_code

        self.server = urlparse.urljoin(self.url, "/")
        self.insert_url = urlparse.urljoin(self.server, "api/insert/")
        self.insert_url_bulk = urlparse.urljoin(self.server, "api/insert_bulk/")
        self.update_url = urlparse.urljoin(self.server, "api/update/")
        self.update_query_url = urlparse.urljoin(self.server, "api/update_query/")
        self.update_status_url = urlparse.urljoin(self.server, "api/update_status/")
        self.clear_url = urlparse.urljoin(self.server, "api/clear/")
        self.get_url = urlparse.urljoin(self.server, "get/")
        self.start_queue_url = urlparse.urljoin(self.server, "start/")
        self.stop_queue_url = urlparse.urljoin(self.server, "stop/")
        self.queue_status_url = urlparse.urljoin(self.server, "api/status/")
        # self.api_queue_status_url = urlparse.urljoin(self.server, "api/status/")

        self._auth_code = json.dumps(dict(auth_code=auth_code))

    def insert(self, data):
        """
        id*, url*,
        source, title, content, status, query_cnt

        *: must
        """
        return self._request(self.insert_url, data)

    def insert_bulk(self, items):
        """
        批量insert内容, 其中content为内容的list, 元素是有id的内容列表
        """
        data = dict(content=json.dumps(items))
        return self._request(self.insert_url_bulk, data)

    def update(self, data):
        return self._request(self.update_url, data)

    def update_query(self, data):
        return self._request(self.update_query_url, data)

    def update_status(self, data):
        return self._request(self.update_status_url, data)

    def clear(self):
        return self._request(self.clear_url)

    def _request(self, url, data={}, **kwargs):
        data = self._wrap_auth_code(data)
        resp = requests.post(url, data)
        resp = json.loads(resp.content)
        return resp

    def _wrap_auth_code(self, data):
        data["auth"] = self.auth_code
        return data

    def get(self, *args, **kwargs):
        d = self._request(self.get_url)
        return d

    def start_queue(self):
        return self._request(self.start_queue_url)

    def stop_queue(self):
        return self._request(self.stop_queue_url)

    def queue_status(self):
        return self._request(self.queue_status_url)

    @property
    def status(self):
        return self._request(self.queue_status_url)


def test():

    test_data = dict(
        id="111111",
        url="http://www.baidu.com",
        source="test",
        title="百度首页",
        content="""


    digg（掘客） diglog 界面 前瞻网 金融界 统计之都 简书 人人都是产品经理 36Kr 火光摇曳—机器学习博客 好东西论坛 | 好东西传送门的论坛 百度

    工具: 我的github 开源中国Git 机器学习日报 阿里云控制台 机器学习开源算法库 Lab41 · GitHub Useit 知识库-从基础到前沿 蚂蜂窝 DatasFrame Theano 0.8.2 documentation MaHua在线markdown编辑器 Django-wiki DataHub-Ecosystem Kaggle

    资讯: Zaker-传递价值咨询 [个论]马光远专栏：该搞清楚中国究竟有多少房子了 大萧条的债务 价值投资导航 - 学习价值投资从value500投资导航开始！

    教育: 百度传课 死于25岁葬于75岁
        """
    )
    sp = SpiderUrlApi("http://ikan.space:11001/", auth_code="")
    import pdb
    pdb.set_trace()
    print sp.clear()

    print sp.insert(test_data)

    print sp.update(dict(id="111111", title="百度新首页"))
    print sp.update_query(dict(id="111111", query_cnt=6))
    print sp.update_status(dict(id="111111", status=-1))


if __name__ == "__main__":
    test()
