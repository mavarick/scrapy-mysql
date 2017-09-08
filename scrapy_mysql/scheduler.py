import importlib

import six
import time
import logging
from scrapy.utils.misc import load_object
from scrapy.core.scheduler import Scheduler as BaseScheduler

from . import connection, defaults
from .exp import EmptyQueueException
from .logger import sm_log


class Scheduler(BaseScheduler):
    """Mysql-based scheduler

    Settings
    --------
    SCHEDULER_PERSIST : bool (default: False)
        Whether to persist or clear mysql queue.
    SCHEDULER_FLUSH_ON_START : bool (default: False)
        Whether to flush mysql queue on start.
    SCHEDULER_IDLE_BEFORE_CLOSE : int (default: 0)
        How many seconds to wait before closing if no message is received.
    SCHEDULER_QUEUE_KEY : str
        Scheduler mysql key.
    SCHEDULER_QUEUE_CLASS : str
        Scheduler queue class.
    SCHEDULER_SERIALIZER : str
        Scheduler serializer.
    """

    def __init__(self, server,
                 flush_on_start=False,
                 queue_key=defaults.DEFAULT_QUEUE_KEY,
                 queue_cls=defaults.SCHEDULER_QUEUE_CLASS,
                 idle_before_close=0,
                 serializer=None,
                 func_get_id=defaults.SCHEDULER_FUNC_REQ_ID):
        """Initialize scheduler.

        Parameters
        ----------
        server : Mysql
            The mysql server instance.
        flush_on_start : bool
            Whether to flush requests on start. Default is False.
        queue_key : str
            Requests queue key.
        idle_before_close : int
            Timeout before giving up.

        """
        self.spider = None

        if idle_before_close < 0:
            raise TypeError("idle_before_close cannot be negative")

        self.server = server
        self.flush_on_start = flush_on_start
        self.queue_key = queue_key
        self.queue_cls = queue_cls
        self.idle_before_close = idle_before_close
        self.serializer = serializer
        self.stats = None
        self.func_get_id = func_get_id

    @classmethod
    def from_settings(cls, settings):

        kwargs = {
            'flush_on_start': settings.getbool('SCHEDULER_FLUSH_ON_START'),
            'idle_before_close': settings.getint('SCHEDULER_IDLE_BEFORE_CLOSE'),
        }

        # If these values are missing, it means we want to use the defaults.
        optional = {
            # TODO: Use custom prefixes for this settings to note that are
            # specific to scrapy-mysql.
            'queue_key': 'SCHEDULER_QUEUE_KEY',
            # We use the default setting name to keep compatibility.
            'serializer': 'SCHEDULER_SERIALIZER',
            'func_get_id': "SCHEDULER_FUNC_REQ_ID",
        }
        for name, setting_name in optional.items():
            val = settings.get(setting_name)
            if val:
                kwargs[name] = val

        # Support serializer as a path to a module.
        # if isinstance(kwargs.get('serializer'), six.string_types):
        #     kwargs['serializer'] = importlib.import_module(kwargs['serializer'])

        server = connection.from_settings(settings)

        # Ensure the connection is working.
        # check server is active
        resp = server.queue_status()
        code = resp['code']
        if code != 0:
            msg = "Error: code: [%s], msg: [%s], data: \n %s" % (code, resp['msg'], resp['data'])
            raise Exception(msg)

        return cls(server=server, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        instance = cls.from_settings(crawler.settings)
        # FIXME: for now, stats are only supported from this constructor
        instance.stats = crawler.stats
        return instance

    def open(self, spider):
        self.spider = spider

        # load queue module
        try:
            sm_log.info("queue class: %s" % self.queue_cls)
            self.queue = load_object(self.queue_cls)(
                server=self.server,
                spider=spider,
                key=self.queue_key % {'spider': spider.name},
                serializer=self.serializer,
            )
        except TypeError as e:
            raise ValueError("Failed to instantiate queue class '%s': %s",
                             self.queue_cls, e)

        try:
            self.get_request_id = load_object(self.func_get_id)
        except:
            raise Exception("Failed to load module [%s]" % self.func_get_id)

        # start queue
        self.spider.log("start queue")
        self.server.start_queue()
        resp = self.server.status
        code = resp['code']
        if code != 0:
            msg = "Error: code: [%s], msg: [%s], data: \n %s" % (code, resp['msg'], resp['data'])
            raise Exception(msg)
        status = resp['data']
        # qsize = q_size, tsize = table_size, start_code = start_code
        start_code = status['start_code']
        if start_code == 0:
            msg = "Error: queue is not started:  start code is 0 !"
            raise Exception(msg)
        else:
            msg = "queue is started: start_code: [%s], table_size: [%s], queue_size: [%s]" % (
                start_code, status['tsize'], status['qsize'])
            self.spider.log(msg)

    def close(self, reason):
        pass

    def flush(self):
        # if flush the queue
        pass

    def has_pending_requests(self):
        return False

    def __len__(self):
        raise Exception("ERROR: can not get length of scheduler")

    def enqueue_request(self, request):
        req_id = self.get_request_id(request, self.spider)
        setattr(request, 'id', req_id)
        self.queue.push(request)
        return True

    def next_request(self):
        block_pop_timeout = self.idle_before_close
        try_cnt = 0
        while 1:
            try:
                try_cnt += 1
                request = self.queue.pop(timeout=block_pop_timeout)
                return request
            except EmptyQueueException:
                self.spider.log("queue is empyty, Retry to get request from queue .. ")
                if try_cnt > defaults.EMPTY_QUEUE_TRY_TIME:
                    self.spider.log("[WARN]: queue is empty")
                # time.sleep(defaults.EMPTY_QUEUE_SLEEP_TIME)
                break
