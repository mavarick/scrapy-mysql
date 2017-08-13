from scrapy.utils.reqser import request_to_dict, request_from_dict
import hashlib
from . import picklecompat


# EMPTY QUEUE RETURN CODE
EMPTY_QUEUE_CODE = -1


class Base(object):
    """Per-spider base queue class"""

    def __init__(self, server, spider, key, serializer=None):
        """Initialize per-spider redis queue.

        Parameters
        ----------
        server : StrictRedis
            remote client instance.
        spider : Spider
            Scrapy spider instance.
        key: str
            remote key where to put and get messages.
        serializer : object
            Serializer object with ``loads`` and ``dumps`` methods.

        """
        if serializer is None:
            # Backward compatibility.
            # TODO: deprecate pickle.
            serializer = picklecompat
        if not hasattr(serializer, 'loads'):
            raise TypeError("serializer does not implement 'loads' function: %r"
                            % serializer)
        if not hasattr(serializer, 'dumps'):
            raise TypeError("serializer '%s' does not implement 'dumps' function: %r"
                            % serializer)

        self.server = server
        self.spider = spider
        self.key = key % {'spider': spider.name}
        self.serializer = serializer

    def _encode_request(self, request):
        """Encode a request object"""
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):
        """Push a request"""
        raise NotImplementedError

    def pop(self, timeout=0):
        """Pop a request"""
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)


class RemoteQueue(Base):
    """url remote server queue for inserting and fetching url. Scrapy's Request may contains cookie, header, 
    refer to "scrapy/utils/reqser.py"
    """
    def push(self, request):
        url = request.url
        id = hashlib.md5(url).hexdigest()
        priority = request.priority
        req_data = self._encode_request(request)
        source = self.spider.name
        data = dict(
            id=id,
            url=url,
            priority=priority,
            source=source,
            content=req_data
        )

        resp = self.server.insert(data)
        self.check_resp(resp)

    def pop(self, queue="", by="", timeout=0):
        """ get url result from remote server, TODO
        
        :param queue: queue name, usually spider name
        :param by: 'lifo', 'fifo', 'priority'
        :param timeout: 
        :return: request content
        """
        resp = self.server.get(queue="", sort="", timeout=timeout)
        code = resp['code']
        if code == EMPTY_QUEUE_CODE:
            # queue is empty
            raise Exception("Queue is empty")
        wrapped_request = resp['data']
        content = wrapped_request['content']
        if content:
            return self._decode_request(content)

    def check_resp(self, resp):
        code = resp['code']
        if code != 0:
            msg = "Error. code: [%s], msg: [%s], data: \n%s"%(code, resp['msg'], resp['data'])
            raise QueueException(msg)

    def __len__(self):
        pass


class QueueException(Exception):
    pass


# TODO: Deprecate the use of these names.
SpiderQueue = RemoteQueue
SpiderStack = RemoteQueue
SpiderPriorityQueue = RemoteQueue
