# scrapy_mysql

  Use django+mysql as url server to push and pop url request, mainly changes are:
    
    1. add request id, set settings "SCHEDULER_FUNC_REQ_ID" to custom your self funciton (request, spider)
    2. use 'SpierUrlApi.py' to connect to remote server. The remote server will record every handlerd url. Use `status` to tag url crawling status. So use this api in `errback` to change url status in remote server
    3. use mysql deduplicating funciton by unique key. 
    4. Cause url are serialized, so increasing scrawling and distributing scrawling are supported

## Castrated Functions
  
  some functions are CASTRATED:
  
    1. Queue. Only one queue now is supported with one remote server. Of cause, you could set multiple remote server for multi spiders
    2. speed. the speed maybe much slower, cause network data transfering.

## How to Use

  1. set `scheduler`:

```python
SCHEDULER_QUEUE_CLASS = 'scrapy_mysql.queue.RemoteQueue'
```
     
  2. set `MYSQL_REMOTE_PARAMS`
  
```python
MYSQL_REMOTE_PARAMS = {
    'SERVER': 'http://127.0.0.1:11011',
    'AUTH_CODE': 'auth_code',
}
```

  3. set get id function:
  
```python
SCHEDULER_FUNC_REQ_ID = "scrapy_mysql.utils.get_default_id"
```
     
  4. use `ResponseErrMiddleware`. Main function is to change the request's status in remote database by calling relevant api in `SpiderUrlApi.py`
  
```python
DOWNLOADER_MIDDLEWARES = {
    # lower number: Engine side
    'scrapy_mysql.ResponseErrMiddleware.ResponseErrMiddleware': 901,
    # higher number : Downloader side
}

```

  5. `SpiderUrlApi.py`. The Scheduler use this module to insert and fetch url request from remote database. 
    
     to save cookie and header data, use:
       
        1. request_to_dict(request, self.spider)
        2. pickle.dumps(obj, protocol=-1)
        3. base64.b64decode(obj)
     
     more detail see, `queue.py`

## Future work

  1. mutilple queue in one server
  2. better way, other than django+mysql, to support functions above.
