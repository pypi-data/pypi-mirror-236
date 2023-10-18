# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import ssl
import aiohttp

from contextlib import contextmanager

from ..struct import IntEnum
from ..interface import ContextManager

from .base import Utils, AsyncCirculatorForSecond
from .buffer import FileBuffer


class STATE(IntEnum):

    PENDING = 0x00
    FETCHING = 0x01
    SUCCESS = 0x02
    FAILURE = 0x03


DEFAULT_TIMEOUT = aiohttp.client.ClientTimeout(total=60, connect=10, sock_read=60, sock_connect=10)
DOWNLOAD_TIMEOUT = aiohttp.client.ClientTimeout(total=600, connect=10, sock_read=600, sock_connect=10)

DEFAULT_SSL_CONTEXT = ssl.create_default_context(
    cafile=os.path.join(
        os.path.split(os.path.abspath(__file__))[0],
        r'../../static/cacert.pem'
    )
)


@contextmanager
def _catch_error():
    """异常捕获

    通过with语句捕获异常，代码更清晰，还可以使用Ignore异常安全的跳出with代码块

    """

    try:

        yield

    except aiohttp.ClientResponseError as err:

        if err.status < 500:
            Utils.log.warning(err)
        else:
            Utils.log.error(err)

    except Exception as err:

        Utils.log.error(err)


class _AsyncCirculator(AsyncCirculatorForSecond):

    async def _sleep(self):

        await Utils.sleep(self._current)


def _json_decoder(val, **kwargs):

    try:
        return Utils.json_decode(val, **kwargs)
    except Exception as err:
        Utils.log.warning(f'http client json decode error: {err} => {val}')


def create_timeout(total=None, connect=None, sock_read=None, sock_connect=None) -> aiohttp.client.ClientTimeout:
    """生成超时配置对象

    Args:
        total: 总超时时间
        connect: 从连接池中等待获取连接的超时时间
        sock_read: Socket数据接收的超时时间
        sock_connect: Socket连接的超时时间

    """

    return aiohttp.client.ClientTimeout(
        total=total, connect=connect,
        sock_read=sock_read, sock_connect=sock_connect
    )


def create_ssl_context(cafile, *, certfile=None, keyfile=..., password=...) -> ssl.SSLContext:

    ssl_context = ssl.create_default_context(cafile=cafile)

    if certfile is not None:
        ssl_context.load_cert_chain(certfile, keyfile, password)

    return ssl_context


class Result(dict):

    def __init__(self, status, headers, cookies, body):

        super().__init__(status=status, headers=headers, cookies=cookies, body=body)

    def __bool__(self):

        return (self.status >= 200) and (self.status <= 299)

    @property
    def status(self):

        return self.get(r'status')

    @property
    def headers(self):

        return self.get(r'headers')

    @property
    def cookies(self):

        return self.get(r'cookies')

    @property
    def body(self):

        return self.get(r'body')


class _HTTPClient:
    """HTTP客户端基类
    """

    def __init__(self, retry_count=5, timeout=DEFAULT_TIMEOUT, *, ssl_context=DEFAULT_SSL_CONTEXT, **kwargs):

        self._ssl_context = ssl_context
        self._retry_count = retry_count

        self._session_config = kwargs
        self._session_config[r'timeout'] = timeout
        self._session_config.setdefault(r'raise_for_status', True)

    def _encode_body(self, headers, data):

        if headers is None:
            headers = {}

        if isinstance(data, dict):
            headers.setdefault(r'Content-Type', r'application/x-www-form-urlencoded')

        return headers, data

    async def _handle_response(self, response):

        return await response.read()

    def create_form_data(self) -> aiohttp.FormData:

        return aiohttp.FormData()

    async def send_request(
            self, method, url, data=None, params=None, cookies=None, headers=None, **settings
    ) -> Result:

        response = None

        headers, data = self._encode_body(headers, data)

        settings[r'data'] = data
        settings[r'params'] = params
        settings[r'cookies'] = cookies
        settings[r'headers'] = headers

        Utils.log.debug(
            r'{0} {1} => {2}'.format(
                method,
                url,
                str({key: val for key, val in settings.items() if isinstance(val, (str, list, dict))})
            )
        )

        settings.setdefault(r'ssl', self._ssl_context)

        async for times in _AsyncCirculator(max_times=self._retry_count):

            try:

                async with aiohttp.ClientSession(**self._session_config) as _session:

                    async with _session.request(method, url, **settings) as _response:

                        response = Result(
                            _response.status,
                            dict(_response.headers),
                            {key: val.value for key, val in _response.cookies.items()},
                            await self._handle_response(_response)
                        )

            except aiohttp.ClientResponseError as err:

                # 重新尝试的话，会记录异常，否则会继续抛出异常

                if err.status < 500:
                    raise err
                elif times >= self._retry_count:
                    raise err
                else:
                    Utils.log.warning(err)
                    continue

            except aiohttp.ClientError as err:

                if times >= self._retry_count:
                    raise err
                else:
                    Utils.log.warning(err)
                    continue

            else:

                Utils.log.info(f'{method} {url} => status:{response.status}')
                break

            finally:

                if times > 1:
                    Utils.log.warning(f'{method} {url} => retry:{times}')

        return response


class _HTTPTextMixin:
    """Text模式混入类
    """

    async def _handle_response(self, response):

        return await response.text()


class _HTTPJsonMixin:
    """Json模式混入类
    """

    async def _handle_response(self, response):

        return await response.json(encoding=r'utf-8', loads=_json_decoder, content_type=None)


class _HTTPJsonRequestMixin(_HTTPJsonMixin):
    """Json请求模式混入类
    """

    def _encode_body(self, headers, data):

        if headers is None:
            headers = {}

        if isinstance(data, (dict, list)):
            headers.setdefault(r'Content-Type', r'application/json')
            data = Utils.json_encode(data)

        return headers, data


class _HTTPTouchMixin:
    """Touch模式混入类，不接收body数据
    """

    async def _handle_response(self, response):

        return dict(response.headers)


class HTTPClient(_HTTPClient):
    """HTTP客户端，普通模式
    """

    async def get(self, url, params=None, *, cookies=None, headers=None):

        result = None

        with _catch_error():

            resp = await self.send_request(aiohttp.hdrs.METH_GET, url, None, params, cookies=cookies, headers=headers)

            result = resp.body

        return result

    async def options(self, url, params=None, *, cookies=None, headers=None):

        result = None

        with _catch_error():

            resp = await self.send_request(aiohttp.hdrs.METH_OPTIONS, url, None, params, cookies=cookies, headers=headers)

            result = resp.headers

        return result

    async def head(self, url, params=None, *, cookies=None, headers=None):

        result = None

        with _catch_error():

            resp = await self.send_request(aiohttp.hdrs.METH_HEAD, url, None, params, cookies=cookies, headers=headers)

            result = resp.headers

        return result

    async def post(self, url, data=None, params=None, *, cookies=None, headers=None):

        result = None

        with _catch_error():

            resp = await self.send_request(aiohttp.hdrs.METH_POST, url, data, params, cookies=cookies, headers=headers)

            result = resp.body

        return result

    async def put(self, url, data=None, params=None, *, cookies=None, headers=None):

        result = None

        with _catch_error():

            resp = await self.send_request(aiohttp.hdrs.METH_PUT, url, data, params, cookies=cookies, headers=headers)

            result = resp.body

        return result

    async def patch(self, url, data=None, params=None, *, cookies=None, headers=None):

        result = None

        with _catch_error():

            resp = await self.send_request(aiohttp.hdrs.METH_PATCH, url, data, params, cookies=cookies, headers=headers)

            result = resp.body

        return result

    async def delete(self, url, params=None, *, cookies=None, headers=None):

        result = None

        with _catch_error():

            resp = await self.send_request(aiohttp.hdrs.METH_DELETE, url, None, params, cookies=cookies, headers=headers)

            result = resp.body

        return result


class HTTPTextClient(_HTTPTextMixin, HTTPClient):
    """HTTP客户端，Text模式
    """
    pass


class HTTPJsonClient(_HTTPJsonMixin, HTTPClient):
    """HTTP客户端，Json模式
    """
    pass


class HTTPJsonRequestClient(_HTTPJsonRequestMixin, HTTPClient):
    """HTTP客户端，Json请求模式
    """
    pass


class HTTPTouchClient(_HTTPTouchMixin, HTTPClient):
    """HTTP客户端，Touch模式
    """
    pass


class HTTPClientPool(HTTPClient):
    """HTTP带连接池客户端，普通模式
    """

    def __init__(self,
                 retry_count=5, use_dns_cache=True, ttl_dns_cache=10,
                 limit=100, limit_per_host=0, timeout=DEFAULT_TIMEOUT,
                 **kwargs
                 ):

        super().__init__(retry_count, timeout, **kwargs)

        self._tcp_connector = aiohttp.TCPConnector(
            use_dns_cache=use_dns_cache,
            ttl_dns_cache=ttl_dns_cache,
            ssl=self._ssl_context,
            limit=limit,
            limit_per_host=limit_per_host,
        )

        self._session_config[r'connector'] = self._tcp_connector
        self._session_config[r'connector_owner'] = False

    async def close(self):

        if not self._tcp_connector.closed:
            await self._tcp_connector.close()


class HTTPTextClientPool(_HTTPTextMixin, HTTPClientPool):
    """HTTP带连接池客户端，Text模式
    """
    pass


class HTTPJsonClientPool(_HTTPJsonMixin, HTTPClientPool):
    """HTTP带连接池客户端，Json模式
    """
    pass


class HTTPJsonRequestClientPool(_HTTPJsonRequestMixin, HTTPClientPool):
    """HTTP带连接池客户端，Json请求模式
    """
    pass


class HTTPTouchClientPool(_HTTPTouchMixin, HTTPClientPool):
    """HTTP带连接池客户端，Touch模式
    """
    pass


class Downloader(_HTTPClient):
    """HTTP文件下载器
    """

    def __init__(self, file, retry_count=5, timeout=DOWNLOAD_TIMEOUT, **kwargs):

        super().__init__(retry_count, timeout, **kwargs)

        self._file = file

        self._state = STATE.PENDING

        self._response = None

    @property
    def file(self):

        return self._file

    @property
    def state(self):

        return self._state

    @property
    def finished(self):

        return self._state in (STATE.SUCCESS, STATE.FAILURE)

    @property
    def response(self):

        return self._response

    async def _handle_response(self, response):

        if self._state != STATE.PENDING:
            return

        self._state = STATE.FETCHING
        self._response = response

        with open(self._file, r'wb') as stream:

            try:

                while True:

                    chunk = await response.content.read(65536)

                    if chunk:
                        stream.write(chunk)
                    else:
                        break

            except Exception as err:

                Utils.log.error(err)

                self._state = STATE.FAILURE

            else:

                self._state = STATE.SUCCESS

        if self._state != STATE.SUCCESS and os.path.exists(self._file):
            os.remove(self._file)

    async def fetch(self, url, *, params=None, cookies=None, headers=None):

        result = False

        try:

            await self.send_request(aiohttp.hdrs.METH_GET, url, None, params, cookies=cookies, headers=headers)

            result = (self._state == STATE.SUCCESS)

        except Exception as err:

            Utils.log.error(err)

            self._state = STATE.FAILURE

        return result


class DownloadBuffer(ContextManager, Downloader):
    """HTTP文件下载器(临时文件版)
    """

    def __init__(self, timeout=DOWNLOAD_TIMEOUT, **kwargs):

        super().__init__(FileBuffer(), 1, timeout, **kwargs)

    def _context_release(self):

        self.close()

    def close(self):

        self._file.close()

    async def _handle_response(self, response):

        if self._state != STATE.PENDING:
            return

        self._state = STATE.FETCHING
        self._response = response

        try:

            while True:

                chunk = await response.content.read(65536)

                if chunk:
                    self._file.write(chunk)
                else:
                    break

        except Exception as err:

            Utils.log.error(err)

            self._state = STATE.FAILURE

        else:

            self._state = STATE.SUCCESS
