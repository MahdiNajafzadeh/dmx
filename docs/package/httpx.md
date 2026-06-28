### Install Project Dependencies

Source: https://www.python-httpx.org/contributing

Install the project and its dependencies after cloning the repository. Navigate into the cloned directory first.

```bash
cd httpx
scripts/install
```

--------------------------------

### Send GET Request with AsyncClient

Source: https://www.python-httpx.org/api

Example of sending a GET request using the AsyncClient. Parameters are detailed in httpx.request documentation.

```python
await client.get('https://example.org', params={'key': 'value'})
```

--------------------------------

### Installing chardet for Auto-Detection

Source: https://www.python-httpx.org/advanced/text-encodings

Provides the commands to install httpx and the chardet library, which is used for character-set auto-detection.

```bash
$ pip install httpx
$ pip install chardet


```

--------------------------------

### Install HTTPX using pip

Source: https://www.python-httpx.org/

Install the core HTTPX library using pip. This is the basic installation for using HTTPX in your Python projects.

```bash
$ pip install httpx

```

--------------------------------

### Using httpx with Trio

Source: https://www.python-httpx.org/async

Demonstrates how to make an HTTP GET request using httpx within a Trio asynchronous application. Ensure the 'trio' package is installed.

```python
import httpx
import trio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com/')
        print(response)

trio.run(main)

```

--------------------------------

### Install httpx with HTTP/2 support

Source: https://www.python-httpx.org/http2

Install the optional HTTP/2 dependencies for httpx using pip.

```bash
$ pip install httpx[http2]
```

--------------------------------

### Install SOCKS Proxy Support

Source: https://www.python-httpx.org/advanced/proxies

Install the necessary third-party library to enable SOCKS proxy support in HTTPX. This is an optional feature.

```bash
$ pip install httpx[socks]
```

--------------------------------

### Import HTTPX

Source: https://www.python-httpx.org/quickstart

Start by importing the HTTPX library.

```python
>>> import httpx
```

--------------------------------

### Running AsyncIO with HTTPX

Source: https://www.python-httpx.org/async

Provides a complete example of using HTTPX with Python's built-in asyncio library to perform an asynchronous GET request.

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com/')
        print(response)

asyncio.run(main())
```

--------------------------------

### Initialize and Use AsyncClient

Source: https://www.python-httpx.org/api

Demonstrates how to initialize an AsyncClient using an asynchronous context manager and make a GET request.

```python
async with httpx.AsyncClient() as client:
    response = await client.get('https://example.org')
```

--------------------------------

### Install HTTPX with Brotli and Zstandard support

Source: https://www.python-httpx.org/

Install HTTPX with optional support for Brotli and Zstandard compression algorithms. This allows for more efficient data transfer.

```bash
$ pip install httpx[brotli,zstd]

```

--------------------------------

### Install HTTPX with HTTP/2 support

Source: https://www.python-httpx.org/

Install HTTPX with optional support for HTTP/2 protocol. This is useful for applications that need to leverage HTTP/2 features.

```bash
$ pip install httpx[http2]

```

--------------------------------

### Install HTTPX with CLI support

Source: https://www.python-httpx.org/

Install HTTPX with the optional command-line interface (CLI) dependency. This enables using HTTPX directly from your terminal.

```bash
# The command line client is an optional dependency.
$ pip install 'httpx[cli]'

```

--------------------------------

### Initialize and Use httpx.Client

Source: https://www.python-httpx.org/api

Instantiate an httpx.Client and make a GET request. The client can be shared across threads for connection pooling.

```python
>>> client = httpx.Client()
>>> response = client.get('https://example.org')
```

--------------------------------

### HTTP Basic Authentication Example

Source: https://www.python-httpx.org/advanced/authentication

Demonstrates using Basic Auth with a client instance for a specific endpoint. Requires importing httpx.

```python
>>> auth = httpx.BasicAuth(username="finley", password="secret")
>>> client = httpx.Client(auth=auth)
>>> response = client.get("https://httpbin.org/basic-auth/finley/secret")
>>> response
<Response [200 OK]>
```

--------------------------------

### Make a GET Request

Source: https://www.python-httpx.org/quickstart

Make a simple GET request to a URL and inspect the response.

```python
>>> r = httpx.get('https://httpbin.org/get')
>>> r
<Response [200 OK]>
```

--------------------------------

### httpx and httpcore Debug Log Output Example

Source: https://www.python-httpx.org/logging

Example of the debug-level output generated by httpx and httpcore when making a request. This output details connection, TLS, request, and response phases.

```text
DEBUG [2024-09-28 17:27:40] httpcore.connection - connect_tcp.started host='www.example.com' port=443 local_address=None timeout=5.0 socket_options=None
DEBUG [2024-09-28 17:27:41] httpcore.connection - connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x101f1e8e0>
DEBUG [2024-09-28 17:27:41] httpcore.connection - start_tls.started ssl_context=SSLContext(verify=True) server_hostname='www.example.com' timeout=5.0
DEBUG [2024-09-28 17:27:41] httpcore.connection - start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x1020f49a0>
DEBUG [2024-09-28 17:27:41] httpcore.http11 - send_request_headers.started request=<Request [b'GET']>
DEBUG [2024-09-28 17:27:41] httpcore.http11 - send_request_headers.complete
DEBUG [2024-09-28 17:27:41] httpcore.http11 - send_request_body.started request=<Request [b'GET']>
DEBUG [2024-09-28 17:27:41] httpcore.http11 - send_request_body.complete
DEBUG [2024-09-28 17:27:41] httpcore.http11 - receive_response_headers.started request=<Request [b'GET']>
DEBUG [2024-09-28 17:27:41] httpcore.http11 - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Content-Encoding', b'gzip'), (b'Accept-Ranges', b'bytes'), (b'Age', b'407727'), (b'Cache-Control', b'max-age=604800'), (b'Content-Type', b'text/html; charset=UTF-8'), (b'Date', b'Sat, 28 Sep 2024 13:27:42 GMT'), (b'Etag', b'"3147526947+gzip"'), (b'Expires', b'Sat, 05 Oct 2024 13:27:42 GMT'), (b'Last-Modified', b'Thu, 17 Oct 2019 07:18:26 GMT'), (b'Server', b'ECAcc (dcd/7D43)'), (b'Vary', b'Accept-Encoding'), (b'X-Cache', b'HIT'), (b'Content-Length', b'648')])
INFO [2024-09-28 17:27:41] httpx - HTTP Request: GET https://www.example.com "HTTP/1.1 200 OK"
DEBUG [2024-09-28 17:27:41] httpcore.http11 - receive_response_body.started request=<Request [b'GET']>
DEBUG [2024-09-28 17:27:41] httpcore.http11 - receive_response_body.complete
DEBUG [2024-09-28 17:27:41] httpcore.http11 - response_closed.started
DEBUG [2024-09-28 17:27:41] httpcore.http11 - response_closed.complete
DEBUG [2024-09-28 17:27:41] httpcore.connection - close.started
DEBUG [2024-09-28 17:27:41] httpcore.connection - close.complete

```

--------------------------------

### Send OPTIONS Request with AsyncClient

Source: https://www.python-httpx.org/api

Example of sending an OPTIONS request using the AsyncClient. Parameters are detailed in httpx.request documentation.

```python
await client.options('https://example.org')
```

--------------------------------

### Send a GET Request with httpx.Client

Source: https://www.python-httpx.org/api

Send a GET request using the httpx client. Parameters are similar to httpx.request.

```python
client.get('https://example.org')
```

--------------------------------

### Send HEAD Request with AsyncClient

Source: https://www.python-httpx.org/api

Example of sending a HEAD request using the AsyncClient. Parameters are detailed in httpx.request documentation.

```python
await client.head('https://example.org')
```

--------------------------------

### Configuring Request Timeouts

Source: https://www.python-httpx.org/advanced/extensions

Provides an example of configuring various timeout values for a request using the `timeout` extension.

```python
client = httpx.Client()
response = client.get(
    "https://www.example.com",
    extensions={"timeout": {"connect": 5.0, "read": 10.0, "write": 10.0, "pool": 10.0}}
)
```

--------------------------------

### Sending a GET Request

Source: https://www.python-httpx.org/api

Use httpx.get for sending GET requests. Parameters are similar to httpx.request, but data, files, json, and content parameters are not available as GET requests should not have a body.

```python
httpx.get(_url_, _*_, _params=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _follow_redirects=False_, _verify=True_, _timeout=Timeout(timeout=5.0)_, _trust_env=True_)
```

--------------------------------

### HTTP Digest Authentication Example

Source: https://www.python-httpx.org/advanced/authentication

Demonstrates using Digest Auth with a client instance, including handling the initial 401 response. Requires importing httpx.

```python
>>> auth = httpx.DigestAuth(username="olivia", password="secret")
>>> client = httpx.Client(auth=auth)
>>> response = client.get("https://httpbin.org/digest-auth/auth/olivia/secret")
>>> response
<Response [200 OK]>
>>> response.history
[<Response [401 UNAUTHORIZED]>]
```

--------------------------------

### Make a GET Request with Client

Source: https://www.python-httpx.org/advanced/clients

Send requests using client methods like `.get()`. These accept the same arguments as top-level functions.

```python
>>> with httpx.Client() as client:
...     r = client.get('https://example.com')
...
>>> r
<Response [200 OK]>
```

--------------------------------

### Making Async Requests with AsyncClient

Source: https://www.python-httpx.org/async

Demonstrates how to use an AsyncClient within an async context manager to make asynchronous GET requests.

```python
async with httpx.AsyncClient() as client:
    r = await client.get('https://www.example.com/')

r
```

--------------------------------

### Clone HTTPX Repository

Source: https://www.python-httpx.org/contributing

Clone your fork of the HTTPX repository to start development. Replace YOUR-USERNAME with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/httpx
```

--------------------------------

### Client.get

Source: https://www.python-httpx.org/api

Sends a GET request to the specified URL with optional parameters, headers, cookies, and other configurations.

```APIDOC
## `get`

### Description
Send a `GET` request.

### Method
GET

### Endpoint
See `httpx.request`.

### Parameters
**Parameters** : See `httpx.request`.
```

--------------------------------

### Basic HTTPX GET Request

Source: https://www.python-httpx.org/

Demonstrates a simple GET request to a URL using the httpx library and accessing response attributes like status code, headers, and text content.

```python
>>> import httpx
>>> r = httpx.get('https://www.example.org/')
>>> r
<Response [200 OK]>
>>> r.status_code
200
>>> r.headers['content-type']
'text/html; charset=UTF-8'
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'

```

--------------------------------

### WSGI Transport Example with Flask

Source: https://www.python-httpx.org/advanced/transports

Configure an httpx client to use WSGITransport for direct integration with a WSGI application like Flask, useful for testing.

```python
from flask import Flask
import httpx


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

transport = httpx.WSGITransport(app=app)
with httpx.Client(transport=transport, base_url="http://testserver") as client:
    r = client.get("/")
    assert r.status_code == 200
    assert r.text == "Hello World!"
```

--------------------------------

### Monitor Download Progress with tqdm

Source: https://www.python-httpx.org/advanced/clients

Monitor the download progress of large files using `httpx.stream` and the `tqdm` library. This example writes the downloaded content to a temporary file and updates a progress bar based on `response.num_bytes_downloaded`.

```python
import tempfile

import httpx
from tqdm import tqdm

with tempfile.NamedTemporaryFile() as download_file:
    url = "https://speed.hetzner.de/100MB.bin"
    with httpx.stream("GET", url) as response:
        total = int(response.headers["Content-Length"])

        with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="B") as progress:
            num_bytes_downloaded = response.num_bytes_downloaded
            for chunk in response.iter_bytes():
                download_file.write(chunk)
                progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                num_bytes_downloaded = response.num_bytes_downloaded
```

--------------------------------

### Send PUT Request with AsyncClient

Source: https://www.python-httpx.org/api

Example of sending a PUT request with data using the AsyncClient. Parameters are detailed in httpx.request documentation.

```python
await client.put('https://example.org', data={'key': 'value'})
```

--------------------------------

### Monitor Download Progress with rich

Source: https://www.python-httpx.org/advanced/clients

Monitor download progress using `httpx.stream` and the `rich` library's progress display. This example shows a progress bar with percentage, download speed, and transfer speed.

```python
import tempfile
import httpx
import rich.progress

with tempfile.NamedTemporaryFile() as download_file:
    url = "https://speed.hetzner.de/100MB.bin"
    with httpx.stream("GET", url) as response:
        total = int(response.headers["Content-Length"])

        with rich.progress.Progress(
            "[progress.percentage]{task.percentage:>3.0f}%",
            rich.progress.BarColumn(bar_width=None),
            rich.progress.DownloadColumn(),
            rich.progress.TransferSpeedColumn(),
        ) as progress:
            download_task = progress.add_task("Download", total=total)
            for chunk in response.iter_bytes():
                download_file.write(chunk)
                progress.update(download_task, completed=response.num_bytes_downloaded)
```

--------------------------------

### ASGI Transport Example with Starlette

Source: https://www.python-httpx.org/advanced/transports

Configure an httpx AsyncClient to use ASGITransport for direct integration with an ASGI application like Starlette, useful for testing.

```python
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route


async def hello(request):
    return HTMLResponse("Hello World!")


app = Starlette(routes=[Route("/", hello)])

transport = httpx.ASGITransport(app=app)

async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
    r = await client.get("/")
    assert r.status_code == 200
    assert r.text == "Hello World!"
```

--------------------------------

### Send PATCH Request with AsyncClient

Source: https://www.python-httpx.org/api

Example of sending a PATCH request with content using the AsyncClient. Parameters are detailed in httpx.request documentation.

```python
await client.patch('https://example.org', content='update data')
```

--------------------------------

### Send DELETE Request with AsyncClient

Source: https://www.python-httpx.org/api

Example of sending a DELETE request using the AsyncClient. Parameters are detailed in httpx.request documentation.

```python
await client.delete('https://example.org')
```

--------------------------------

### Monitor Upload Progress with tqdm

Source: https://www.python-httpx.org/advanced/clients

Monitor the progress of uploading large data using a request content generator with the `tqdm` library. This example simulates uploading random bytes and displays a progress bar.

```python
import io
import random

import httpx
from tqdm import tqdm


def gen():
    """
    this is a complete example with generated random bytes.
    you can replace `io.BytesIO` with real file object.
    """
    total = 32 * 1024 * 1024  # 32m
    with tqdm(ascii=True, unit_scale=True, unit='B', unit_divisor=1024, total=total) as bar:
        with io.BytesIO(random.randbytes(total)) as f:
            while data := f.read(1024):
                yield data
                bar.update(len(data))


httpx.post("https://httpbin.org/post", content=gen())
```

--------------------------------

### Send POST Request with AsyncClient

Source: https://www.python-httpx.org/api

Example of sending a POST request with JSON data using the AsyncClient. Parameters are detailed in httpx.request documentation.

```python
await client.post('https://example.org', json={'key': 'value'})
```

--------------------------------

### Send a Request Instance with a Client

Source: https://www.python-httpx.org/advanced/clients

Dispatch a pre-built `Request` instance over the network using the `.send()` method of a `httpx.Client`. Ensure the client is properly managed, for example, using a `with` statement.

```python
with httpx.Client() as client:
    response = client.send(request)
    ...
```

--------------------------------

### Sync and Async Authentication Flows with Locks

Source: https://www.python-httpx.org/advanced/authentication

Implement separate synchronous and asynchronous authentication flows using `sync_auth_flow` and `async_auth_flow`. This example demonstrates using thread and asyncio locks for thread-safe token retrieval.

```python
import asyncio
import threading
import httpx


class MyCustomAuth(httpx.Auth):
    def __init__(self):
        self._sync_lock = threading.RLock()
        self._async_lock = asyncio.Lock()

    def sync_get_token(self):
        with self._sync_lock:
            ...

    def sync_auth_flow(self, request):
        token = self.sync_get_token()
        request.headers["Authorization"] = f"Token {token}"
        yield request

    async def async_get_token(self):
        async with self._async_lock:
            ...

    async def async_auth_flow(self, request):
        token = await self.async_get_token()
        request.headers["Authorization"] = f"Token {token}"
        yield request
```

--------------------------------

### Implement a Basic Custom Transport

Source: https://www.python-httpx.org/advanced/transports

Subclass httpx.BaseTransport to create a custom transport. This example, HelloWorldTransport, always returns a JSON response.

```python
import json
import httpx

class HelloWorldTransport(httpx.BaseTransport):
    """
    A mock transport that always returns a JSON "Hello, world!" response.
    """

    def handle_request(self, request):
        return httpx.Response(200, json={"text": "Hello, world!"})

```

--------------------------------

### Handle Redirects (Default Behavior)

Source: https://www.python-httpx.org/quickstart

Inspect redirection history when redirects are not followed by default. This example shows a 301 redirect from HTTP to HTTPS.

```python
r = httpx.get('http://github.com/')
r.status_code
301
r.history
[]
r.next_request
<Request('GET', 'https://github.com/')>
```

--------------------------------

### Complex httpx Logging Configuration with Dictionary

Source: https://www.python-httpx.org/logging

Configure httpx logging using a dictionary for more complex setups, directing output to stderr. This allows separate configuration for httpx and httpcore loggers.

```python
import logging.config
import httpx

LOGGING_CONFIG = {
    "version": 1,
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "http",
            "stream": "ext://sys.stderr"
        }
    },
    "formatters": {
        "http": {
            "format": "% (levelname)s [%(asctime)s] %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    'loggers': {
        'httpx': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },
        'httpcore': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
httpx.get('https://www.example.com')

```

--------------------------------

### Run Documentation Site Locally

Source: https://www.python-httpx.org/contributing

Build and serve the documentation site locally. This is useful for previewing changes to the documentation before committing.

```bash
scripts/docs
```

--------------------------------

### Mount Transports for Scheme and Domain Specificity

Source: https://www.python-httpx.org/advanced/transports

Configure mounts to control transport behavior based on scheme and domain. This example disables HTTP/2 for a specific domain.

```python
mounts = {
    "all://": httpx.HTTPTransport(http2=True),
    "all://*example.org": httpx.HTTPTransport()
}
client = httpx.Client(mounts=mounts)

```

--------------------------------

### Use Client as a Context Manager

Source: https://www.python-httpx.org/advanced/clients

The recommended way to use a Client is as a context manager to ensure proper connection cleanup.

```python
with httpx.Client() as client:
    ...
```

--------------------------------

### Using httpx with AnyIO (Trio backend)

Source: https://www.python-httpx.org/async

Shows how to use httpx with the AnyIO library, specifying the 'trio' backend for execution. AnyIO provides a unified interface for asyncio and trio.

```python
import httpx
import anyio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com/')
        print(response)

anyio.run(main, backend='trio')

```

--------------------------------

### Instantiate AsyncClient with HTTP/2 enabled

Source: https://www.python-httpx.org/http2

Create an asynchronous httpx client with HTTP/2 support enabled by setting the http2=True argument.

```python
client = httpx.AsyncClient(http2=True)
...
```

--------------------------------

### httpx.get

Source: https://www.python-httpx.org/api

Sends a GET request to the specified URL. This function is a shortcut for `httpx.request('GET', url, ...)` and does not support request body parameters.

```APIDOC
## httpx.get

### Description
Sends a `GET` request to the specified URL. This is a convenience function that simplifies making GET requests.

### Method
`get`

### Parameters
#### Path Parameters
None

#### Query Parameters
- **params** (dict | sequence) - Optional - Query parameters to include in the URL.

#### Request Body
Not applicable for GET requests.

#### Other Parameters
- **url** (string) - Required - URL for the request.
- **headers** (dict) - Optional - Dictionary of HTTP headers.
- **cookies** (dict) - Optional - Dictionary of Cookie items.
- **auth** (object) - Optional - An authentication class.
- **proxy** (string) - Optional - A proxy URL.
- **follow_redirects** (bool) - Optional - Enables or disables HTTP redirects.
- **verify** (bool | ssl.SSLContext) - Optional - SSL verification setting.
- **timeout** (Timeout) - Optional - The timeout configuration.
- **trust_env** (bool) - Optional - Enables or disables usage of environment variables.

### Request Example
```python
import httpx
response = httpx.get('https://httpbin.org/get')
```

### Response
#### Success Response (200)
- **Response** (object) - The response object from the server.

#### Response Example
```
<Response [200 OK]>
```
```

--------------------------------

### Get JSON Response Content

Source: https://www.python-httpx.org/quickstart

Parse and access JSON content from an API response.

```python
>>> r = httpx.get('https://api.github.com/events')
>>> r.json()
[{u'repository': {u'open_issues': 0, u'url': 'https://github.com/...' ...  }}]
```

--------------------------------

### Domain Routing for All Traffic on Example.com

Source: https://www.python-httpx.org/advanced/transports

Proxy all requests directed to 'example.com' through a specified transport.

```python
mounts = {
    "all://example.com": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

--------------------------------

### Get Response Text Content

Source: https://www.python-httpx.org/quickstart

Access the response content as decoded Unicode text.

```python
>>> r = httpx.get('https://www.example.org/')
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

--------------------------------

### Wildcard Domain Routing for Example.com and Subdomains

Source: https://www.python-httpx.org/advanced/transports

Route all requests to 'example.com' and any of its subdomains through a specified transport.

```python
mounts = {
    "all://*example.com": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

--------------------------------

### Get Binary Response Content

Source: https://www.python-httpx.org/quickstart

Access the response content as raw bytes, suitable for non-text responses.

```python
>>> r.content
b'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

--------------------------------

### Build and Send a Request with httpx.Client

Source: https://www.python-httpx.org/api

Demonstrates building a request object and then sending it using the client. This is equivalent to directly calling methods like client.get().

```python
request = client.build_request(...)
response = client.send(request, ...)
```

--------------------------------

### Create Image from Binary Content

Source: https://www.python-httpx.org/quickstart

Example of creating an image from binary response content using Pillow.

```python
>>> from PIL import Image
>>> from io import BytesIO
>>> i = Image.open(BytesIO(r.content))
```

--------------------------------

### Build and Send Request with AsyncClient

Source: https://www.python-httpx.org/api

Shows how to build a request object and then send it using the AsyncClient. This is equivalent to using methods like client.get() or client.post().

```python
request = client.build_request(...)
response = await client.send(request, ...)
```

--------------------------------

### Access Specific Response Header

Source: https://www.python-httpx.org/quickstart

Retrieve a specific header value using dictionary-like access or the `get` method.

```python
r.headers['Content-Type']
```

```python
r.headers.get('content-type')
```

--------------------------------

### Pass URL Query Parameters

Source: https://www.python-httpx.org/quickstart

Include URL query parameters in a GET request using the 'params' keyword.

```python
>>> params = {'key1': 'value1', 'key2': 'value2'}
>>> r = httpx.get('https://httpbin.org/get', params=params)
```

--------------------------------

### Configuring a Proxy Server

Source: https://www.python-httpx.org/api

Define proxy server settings using the Proxy class and pass it to the Client constructor.

```python
>>> proxy = Proxy("http://proxy.example.com:8030")
>>> client = Client(proxy=proxy)

```

--------------------------------

### Client-Configured Basic Authentication

Source: https://www.python-httpx.org/advanced/authentication

Configure authentication for all requests made by a client instance. Requires importing httpx.

```python
>>> auth = httpx.BasicAuth(username="username", password="secret")
>>> client = httpx.Client(auth=auth)
>>> response = client.get("https://www.example.com/")
```

--------------------------------

### Opening and Closing AsyncClient with Context Manager

Source: https://www.python-httpx.org/async

Shows the recommended way to manage an AsyncClient's lifecycle using an 'async with' statement.

```python
async with httpx.AsyncClient() as client:
    ...
```

--------------------------------

### SSL Context with Truststore

Source: https://www.python-httpx.org/advanced/ssl

Configure a client instance to use system certificate stores via the `truststore` package for SSL verification.

```python
import ssl
import truststore
import httpx

# Use system certificate stores.
ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ctx)
```

--------------------------------

### Determine Next Redirect Request in Requests

Source: https://www.python-httpx.org/compatibility

The `requests` library uses `response.next` to get the subsequent request in a redirect chain.

```python
session = requests.Session()
request = requests.Request("GET", ...).prepare()
while request is not None:
    response = session.send(request, allow_redirects=False)
    request = response.next
```

--------------------------------

### No-Proxy Configuration for Specific Domains

Source: https://www.python-httpx.org/advanced/transports

Configure a default proxy transport while excluding 'example.com' from proxying by setting its mount to None.

```python
mounts = {
    # Route requests through a proxy by default...
    "all://": httpx.HTTPTransport(proxy="http://localhost:8031"),
    # Except those for "example.com".
    "all://example.com": None,
}
```

--------------------------------

### Configure HTTP Client with Proxy Authentication

Source: https://www.python-httpx.org/advanced/proxies

Include username and password directly in the proxy URL for authentication. Ensure the proxy URL format is correct.

```python
with httpx.Client(proxy="http://username:password@localhost:8030") as client:
    ...
```

--------------------------------

### Other HTTP Methods

Source: https://www.python-httpx.org/quickstart

Demonstrates making PUT, DELETE, HEAD, and OPTIONS requests.

```python
>>> r = httpx.put('https://httpbin.org/put', data={'key': 'value'})
>>> r = httpx.delete('https://httpbin.org/delete')
>>> r = httpx.head('https://httpbin.org/get')
>>> r = httpx.options('https://httpbin.org/get')
```

--------------------------------

### Using AsyncHTTPTransport with AsyncClient

Source: https://www.python-httpx.org/async

Demonstrates how to instantiate and use an explicit AsyncHTTPTransport with custom configurations like retries when creating an AsyncClient.

```python
import httpx
transport = httpx.AsyncHTTPTransport(retries=1)
async with httpx.AsyncClient(transport=transport) as client:
    ...
```

--------------------------------

### Send Cookies in Request

Source: https://www.python-httpx.org/quickstart

Include cookies in an outgoing request using the 'cookies' parameter. This example sends a 'peanut: butter' cookie.

```python
cookies = {"peanut": "butter"}
r = httpx.get('https://httpbin.org/cookies', cookies=cookies)
r.json()
{'cookies': {'peanut': 'butter'}}
```

--------------------------------

### Create an HTTPX Request Instance

Source: https://www.python-httpx.org/advanced/clients

Create a `httpx.Request` instance for fine-grained control over network requests. This instance can then be sent using a `httpx.Client`.

```python
request = httpx.Request("GET", "https://example.com")
```

--------------------------------

### Mocking Specific Domains

Source: https://www.python-httpx.org/advanced/transports

Mock all requests to 'example.org' using a custom handler, while other requests proceed normally.

```python
def handler(request):
    return httpx.Response(200, json={"text": "Hello, World!"})

mounts = {"all://example.org": httpx.MockTransport(handler)}
client = httpx.Client(mounts=mounts)
```

--------------------------------

### NetRC Authentication with Default File

Source: https://www.python-httpx.org/advanced/authentication

Configure a client to use the default .netrc file for authentication. Requires importing httpx.

```python
>>> auth = httpx.NetRCAuth()
>>> client = httpx.Client(auth=auth)
```

--------------------------------

### httpx.Client Initialization

Source: https://www.python-httpx.org/api

Initializes an HTTP client with configurable options for connection pooling, authentication, timeouts, and more. This client can be shared across threads.

```APIDOC
## `Client`

### Description
An HTTP client, with connection pooling, HTTP/2, redirects, cookie persistence, etc. It can be shared between threads.

### Parameters
- **auth** (optional) - An authentication class to use when sending requests.
- **params** (optional) - Query parameters to include in request URLs, as a string, dictionary, or sequence of two-tuples.
- **headers** (optional) - Dictionary of HTTP headers to include when sending requests.
- **cookies** (optional) - Dictionary of Cookie items to include when sending requests.
- **verify** (optional) - Either `True` to use an SSL context with the default CA bundle, `False` to disable verification, or an instance of `ssl.SSLContext` to use a custom context.
- **http2** (optional) - A boolean indicating if HTTP/2 support should be enabled. Defaults to `False`.
- **proxy** (optional) - A proxy URL where all the traffic should be routed.
- **timeout** (optional) - The timeout configuration to use when sending requests.
- **limits** (optional) - The limits configuration to use.
- **max_redirects** (optional) - The maximum number of redirect responses that should be followed.
- **base_url** (optional) - A URL to use as the base when building request URLs.
- **transport** (optional) - A transport class to use for sending requests over the network.
- **trust_env** (optional) - Enables or disables usage of environment variables for configuration.
- **default_encoding** (optional) - The default encoding to use for decoding response text, if no charset information is included in a response Content-Type header. Default: "utf-8".
```

--------------------------------

### HTTP Transport with Unix Domain Socket

Source: https://www.python-httpx.org/advanced/transports

Use the 'uds' option in HTTPTransport to connect via a Unix Domain Socket, for example, to the Docker API.

```python
import httpx
# Connect to the Docker API via a Unix Socket.
transport = httpx.HTTPTransport(uds="/var/run/docker.sock")
client = httpx.Client(transport=transport)
response = client.get("http://docker/info")
response.json()
```

--------------------------------

### Simplify proxy configuration in HTTPX

Source: https://www.python-httpx.org/troubleshooting

A more concise way to configure a proxy for all requests when the proxy supports HTTP connections.

```python
proxy = "http://myproxy.org"
with httpx.Client(proxy=proxy) as client:
  ...
```

--------------------------------

### Using Default Encoding

Source: https://www.python-httpx.org/advanced/text-encodings

Demonstrates how httpx uses the Content-Type header's charset or defaults to 'utf-8' for decoding response text. No special setup is required.

```python
import httpx
# Instantiate a client with the default configuration.
client = httpx.Client()
# Using the client...
response = client.get(...)
print(response.encoding)  # This will either print the charset given in
                          # the Content-Type charset, or else "utf-8".
print(response.text)  # The text will either be decoded with the Content-Type
                      # charset, or using "utf-8".


```

--------------------------------

### SSL Context with Alternative CA Bundle

Source: https://www.python-httpx.org/advanced/ssl

Configure a client instance to use an explicitly specified certificate verification store using the standard SSL context API.

```python
import httpx
import ssl

# Use an explicitly configured certificate store.
ctx = ssl.create_default_context(cafile="path/to/certs.pem")  # Either cafile or capath.
client = httpx.Client(verify=ctx)
```

--------------------------------

### AsyncClient Initialization

Source: https://www.python-httpx.org/api

Initializes an asynchronous HTTP client with various configuration options. This client can be shared across multiple asynchronous tasks.

```APIDOC
## `AsyncClient` Constructor

### Description
An asynchronous HTTP client with connection pooling, HTTP/2, redirects, cookie persistence, etc. It can be shared between tasks.

### Parameters
- **auth** (optional) - An authentication class to use when sending requests.
- **params** (optional) - Query parameters to include in request URLs, as a string, dictionary, or sequence of two-tuples.
- **headers** (optional) - Dictionary of HTTP headers to include when sending requests.
- **cookies** (optional) - Dictionary of Cookie items to include when sending requests.
- **verify** (optional) - Either `True` to use an SSL context with the default CA bundle, `False` to disable verification, or an instance of `ssl.SSLContext` to use a custom context.
- **http2** (optional) - A boolean indicating if HTTP/2 support should be enabled. Defaults to `False`.
- **proxy** (optional) - A proxy URL where all the traffic should be routed.
- **timeout** (optional) - The timeout configuration to use when sending requests.
- **limits** (optional) - The limits configuration to use.
- **max_redirects** (optional) - The maximum number of redirect responses that should be followed.
- **base_url** (optional) - A URL to use as the base when building request URLs.
- **transport** (optional) - A transport class to use for sending requests over the network.
- **trust_env** (optional) - Enables or disables usage of environment variables for configuration.
- **default_encoding** (optional) - The default encoding to use for decoding response text, if no charset information is included in a response Content-Type header. Set to a callable for automatic character set detection. Default: "utf-8".
```

--------------------------------

### Raise HTTPStatusError on 4xx/5xx Responses

Source: https://www.python-httpx.org/advanced/event-hooks

Install a response event hook to automatically raise an httpx.HTTPStatusError for 4xx and 5xx status codes. This is useful for simplifying error handling.

```python
def raise_on_4xx_5xx(response):
    response.raise_for_status()

client = httpx.Client(event_hooks={'response': [raise_on_4xx_5xx]})
```

--------------------------------

### Configure HTTPX Client with Proxy and SSL Context

Source: https://www.python-httpx.org/contributing

Use this snippet to configure an HTTPX client to use a local proxy and a custom SSL context with a client certificate for verification. Ensure the `client.pem` path is correct.

```python
ctx = ssl.create_default_context(cafile="/path/to/client.pem")
client = httpx.Client(proxy="http://127.0.0.1:8080/", verify=ctx)
```

--------------------------------

### Mount Custom Transport for Specific Schemes

Source: https://www.python-httpx.org/advanced/transports

Mount a custom transport against a specific scheme (e.g., 'http://') to control routing. This example redirects HTTP to HTTPS.

```python
import httpx

class HTTPSRedirectTransport(httpx.BaseTransport):
    """
    A transport that always redirects to HTTPS.
    """

    def handle_request(self, method, url, headers, stream, extensions):
        scheme, host, port, path = url
        if port is None:
            location = b"https://%s%s" % (host, path)
        else:
            location = b"https://%s:%d%s" % (host, port, path)
        stream = httpx.ByteStream(b"")
        headers = [(b"location", location)]
        extensions = {}
        return 303, headers, stream, extensions


# A client where any `http` requests are always redirected to `https`
mounts = {'http://': HTTPSRedirectTransport()}
client = httpx.Client(mounts=mounts)

```

--------------------------------

### Domain Routing for HTTP Requests on Example.com

Source: https://www.python-httpx.org/advanced/transports

Proxy only HTTP requests to 'example.com', allowing HTTPS and other schemes to pass through without proxying.

```python
mounts = {
    "http://example.com": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

--------------------------------

### Multi-Request Authentication Flow

Source: https://www.python-httpx.org/advanced/authentication

Implement an authentication flow that may involve multiple requests. This example shows how to resend a request with updated headers if an initial 401 response is received.

```python
class MyCustomAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
      response = yield request
      if response.status_code == 401:
          # If the server issues a 401 response then resend the request,
          # with a custom `X-Authentication` header.
          request.headers['X-Authentication'] = self.token
          yield request
```

--------------------------------

### Disabling Proxy for Specific URLs with NO_PROXY

Source: https://www.python-httpx.org/environment_variables

Configures `HTTP_PROXY` and `NO_PROXY` to route most requests through a proxy but bypass it for specified URLs. Shows examples of requests that go through the proxy and those that bypass it.

```bash
export HTTP_PROXY=http://my-external-proxy.com:1234
export NO_PROXY=http://127.0.0.1,python-httpx.org
```

```python
import httpx; httpx.get('http://example.com')
```

```python
import httpx; httpx.get('http://127.0.0.1:5000/my-api')
```

```python
import httpx; httpx.get('https://www.python-httpx.org')
```

--------------------------------

### Send an OPTIONS Request with httpx.Client

Source: https://www.python-httpx.org/api

Send an OPTIONS request using the httpx client. Parameters are similar to httpx.request.

```python
client.options('https://example.org')
```

--------------------------------

### Configure HTTP Client with Different Proxies for HTTP and HTTPS

Source: https://www.python-httpx.org/advanced/proxies

Use a dictionary of mounts to specify different HTTP transport proxies for HTTP and HTTPS requests. This allows for granular control over proxy routing.

```python
proxy_mounts = {
    "http://": httpx.HTTPTransport(proxy="http://localhost:8030"),
    "https://": httpx.HTTPTransport(proxy="http://localhost:8031"),
}

with httpx.Client(mounts=proxy_mounts) as client:
    ...
```

--------------------------------

### Configure HTTP Client with SOCKS Proxy

Source: https://www.python-httpx.org/advanced/proxies

Set up the HTTPX client to use a SOCKS proxy by specifying the SOCKS protocol and connection details in the proxy URL.

```python
httpx.Client(proxy='socks5://user:pass@host:port')
```

--------------------------------

### Default SSL Context with Certifi

Source: https://www.python-httpx.org/advanced/ssl

Configure a client instance to use the default SSL context, which relies on the certifi CA bundle for verification. This is equivalent to `verify=True`.

```python
import certifi
import httpx
import ssl

# This SSL context is equivelent to the default `verify=True`.
ctx = ssl.create_default_context(cafile=certifi.where())
client = httpx.Client(verify=ctx)
```

--------------------------------

### Client.options

Source: https://www.python-httpx.org/api

Sends an OPTIONS request to the specified URL with optional parameters, headers, cookies, and other configurations.

```APIDOC
## `options`

### Description
Send an `OPTIONS` request.

### Method
OPTIONS

### Endpoint
See `httpx.request`.

### Parameters
**Parameters** : See `httpx.request`.
```

--------------------------------

### Use AsyncClient as a context manager with HTTP/2

Source: https://www.python-httpx.org/http2

Instantiate an asynchronous httpx client with HTTP/2 support within a context manager to ensure connections are properly scoped and closed.

```python
async with httpx.AsyncClient(http2=True) as client:
    ...
```

--------------------------------

### Use `base_url` with Client

Source: https://www.python-httpx.org/advanced/clients

Configure a Client with a `base_url` to prepend a URL to all outgoing requests, simplifying request paths.

```python
>>> with httpx.Client(base_url='http://httpbin.org') as client:
...     r = client.get('/headers')
...
>>> r.request.url
URL('http://httpbin.org/headers')
```

--------------------------------

### Tracing HTTP Events with a Callback

Source: https://www.python-httpx.org/advanced/extensions

Illustrates how to use the `trace` extension to monitor the internal flow of events within the `httpcore` transport by providing a callback function.

```python
import httpx

def log(event_name, info):
    print(event_name, info)

client = httpx.Client()
response = client.get("https://www.example.com/", extensions={"trace": log})
```

--------------------------------

### Connecting to an IP Address with SNI Hostname Extension

Source: https://www.python-httpx.org/advanced/extensions

Demonstrates connecting to an explicit IP address while specifying a server hostname for SSL verification using the `sni_hostname` extension.

```python
# Connect to '185.199.108.153' but use 'www.encode.io' in the Host header,
# and use 'www.encode.io' when SSL verifying the server hostname.
client = httpx.Client()
headers = {"Host": "www.encode.io"}
extensions = {"sni_hostname": "www.encode.io"}
response = client.get(
    "https://185.199.108.153/path",
    headers=headers,
    extensions=extensions
)
```

--------------------------------

### Apply Custom Headers to All Requests with Client

Source: https://www.python-httpx.org/advanced/clients

Configure a Client with default headers that will be applied to all outgoing requests.

```python
>>> url = 'http://httpbin.org/headers'
>>> headers = {'user-agent': 'my-app/0.0.1'}
>>> with httpx.Client(headers=headers) as client:
...     r = client.get(url)
...
>>> r.json()['headers']['User-Agent']
'my-app/0.0.1'
```

--------------------------------

### Send a HEAD Request with httpx.Client

Source: https://www.python-httpx.org/api

Send a HEAD request using the httpx client. Parameters are similar to httpx.request.

```python
client.head('https://example.org')
```

--------------------------------

### Construct Server-Wide OPTIONS * Requests

Source: https://www.python-httpx.org/advanced/extensions

Employ the 'target' extension with a value of b"*" to send server-wide OPTIONS requests, commonly used in proxy scenarios.

```python
extensions = {"target": b"*"}
response = httpx.request("CONNECT", "https://www.example.com", extensions=extensions)
```

--------------------------------

### Setting Request Timeouts with Extensions

Source: https://www.python-httpx.org/advanced/extensions

Demonstrates how to set request timeouts using the `timeout` extension. This ensures timeouts are handled throughout the call stack.

```python
client = httpx.Client()
response = client.get(
    "https://www.example.com",
    extensions={"timeout": {"connect": 5.0}}
)
response.request.extensions["timeout"]
```

--------------------------------

### `AsyncClient.build_request`

Source: https://www.python-httpx.org/api

Builds and returns a request instance, merging client-level configuration like base_url, params, headers, and cookies with the provided request arguments.

```APIDOC
## `AsyncClient.build_request`

### Description
Build and return a request instance. The `params`, `headers`, and `cookies` arguments are merged with any values set on the client. The `url` argument is merged with any `base_url` set on the client.

### Method
Not applicable (builds a request object)

### Endpoint
Not applicable

### Parameters
Accepts `method`, `url`, `content`, `data`, `files`, `json`, `params`, `headers`, `cookies`, `timeout`, and `extensions`.

### Request Example
```json
{
  "example": "Request object construction details"
}
```

### Response
Returns an `httpx.Request` instance.

### Response Example
```json
{
  "example": "Request object representation"
}
```

See also: Request instances
```

--------------------------------

### Client.build_request

Source: https://www.python-httpx.org/api

Builds and returns a request instance, merging client-level configuration with provided arguments.

```APIDOC
## `Client.build_request`

### Description
Build and return a request instance. The `params`, `headers`, and `cookies` arguments are merged with any values set on the client. The `url` argument is merged with any `base_url` set on the client.

### Method
`build_request(_self_, _method_, _url_, *_ , _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _timeout=_, _extensions=None_)

### Parameters
See `httpx.request` for detailed parameter information.

### See also
Request instances
```

--------------------------------

### NetRC Authentication with Environment Variable

Source: https://www.python-httpx.org/advanced/authentication

Configure a client to use a .netrc file specified by the NETRC environment variable, falling back to the default. Requires importing httpx and os.

```python
>>> import os
>>> auth = httpx.NetRCAuth(file=os.environ.get("NETRC"))
>>> client = httpx.Client(auth=auth)
```

--------------------------------

### Make a POST Request

Source: https://www.python-httpx.org/quickstart

Make an HTTP POST request with data.

```python
>>> r = httpx.post('https://httpbin.org/post', data={'key': 'value'})
```

--------------------------------

### Fine-tune Timeout Configuration

Source: https://www.python-httpx.org/advanced/timeouts

Configure detailed timeout behavior including connect, read, write, and pool timeouts for a client instance.

```python
timeout = httpx.Timeout(10.0, connect=60.0)
client = httpx.Client(timeout=timeout)

response = client.get('http://example.com/')
```

--------------------------------

### Basic httpx Logging Configuration

Source: https://www.python-httpx.org/logging

Configure basic logging to output debug information from httpx to stdout. This is useful for inspecting network behavior during requests.

```python
import logging
import httpx

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

httpx.get("https://www.example.com")

```

--------------------------------

### Port Routing for HTTPS on Example.com:1234

Source: https://www.python-httpx.org/advanced/transports

Proxy specific HTTPS requests on port 1234 to 'example.com' through a defined transport.

```python
mounts = {
    "https://example.com:1234": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

--------------------------------

### Enabling Auto-Detection with chardet

Source: https://www.python-httpx.org/advanced/text-encodings

Demonstrates configuring an httpx client to use the 'chardet' library for automatically detecting the character encoding when response headers lack this information.

```python
import httpx
import chardet

def autodetect(content):
    return chardet.detect(content).get("encoding")

# Using a client with character-set autodetection enabled.
client = httpx.Client(default_encoding=autodetect)
response = client.get(...)
print(response.encoding)  # This will either print the charset given in
                          # the Content-Type charset, or else the auto-detected
                          # character set.
print(response.text)


```

--------------------------------

### Configure HTTP Client with a Single Proxy

Source: https://www.python-httpx.org/advanced/proxies

Route all traffic through a specified HTTP proxy by passing its URL during client initialization.

```python
with httpx.Client(proxy="http://localhost:8030") as client:
    ...
```

