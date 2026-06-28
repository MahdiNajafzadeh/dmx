### Install package with extras

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/_llm-test.md

Example of installing a Python package with optional extras using pip.

```bash
pip install "foo[bar]"
```

--------------------------------

### Basic FastAPI Application Setup

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/how-to/extending-openapi.md

This snippet shows a minimal FastAPI application with a single path operation, serving as the base for OpenAPI extension examples.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
```

--------------------------------

### Install FastAPI with Standard Dependencies

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

Use this command to install FastAPI along with its standard dependencies, including Uvicorn and the CLI. This is the new recommended way for a full installation.

```bash
pip install "fastapi[standard]"
```

--------------------------------

### Install packages from requirements.txt

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md

Installs all packages listed in the `requirements.txt` file into the active virtual environment.

```console
$ pip install -r requirements.txt
---> 100%
```

```console
$ uv pip install -r requirements.txt
---> 100%
```

--------------------------------

### FastAPI server start command

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/_llm-test.md

Console output showing a FastAPI application starting up.

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

--------------------------------

### Declare OpenAPI-specific examples using 'openapi_examples' parameter

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md

Use the `openapi_examples` parameter with `Body()` (or other parameters) to provide multiple examples that are directly supported and displayed by Swagger UI. Each example includes a summary, description, and value.

```python
@app.post("/items/")
async def create_item(
    item: Item = Body(
        openapi_examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "bad_name": {
                "summary": "A bad name example",
                "description": "An item with a **bad name**.",
                "value": {
                    "name": "Foobar",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "long_description": {
                "summary": "Items with a long description",
                "description": "Can have a long description with Markdown",
                "value": {
                    "name": "Bar",
                    "description": "A very long description for an item that is not really that important.",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
        },
    )
):
    return item
```

--------------------------------

### Simulate In-Memory File Streaming with io.BytesIO

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/stream-data.md

Demonstrates how to simulate a file using `io.BytesIO` for in-memory streaming, allowing iteration over its contents like a real file. This example includes the full setup for a `PNGStreamingResponse`.

```python
import io
import base64

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# This is a fake image, a tiny 1x1 PNG image
image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
binary_image = base64.b64decode(image_base64)

file_like = io.BytesIO(binary_image)

class PNGStreamingResponse(StreamingResponse):
    media_type = "image/png"

@app.get("/png", response_class=PNGStreamingResponse)
async def get_png():
    def iterfile():
        yield from file_like
    return iterfile()
```

--------------------------------

### Starting FastAPI Development Server

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/index.md

This snippet demonstrates how to start the FastAPI development server using `fastapi dev`. It shows the server initialization, file watching, and provides URLs for the application and its documentation.

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">'/home/user/code/awesomeapp'</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

--------------------------------

### Declare multiple examples for Body parameter using JSON Schema 'examples'

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md

Provide multiple examples for the request body using the `examples` parameter in `Body()`. While these are part of the internal JSON Schema, Swagger UI may not display all of them directly.

```python
@app.post("/items/")
async def create_item(
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "bad_name": {
                "summary": "A bad name example",
                "description": "An item with a **bad name**.",
                "value": {
                    "name": "Foobar",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
        },
    )
):
    return item
```

--------------------------------

### Install HTTPX for TestClient

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/testing.md

Install the httpx library, which is required to use FastAPI's TestClient for testing applications.

```console
$ pip install httpx
```

--------------------------------

### Install FastAPI with all extras including pydantic-settings

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md

Install FastAPI with the `all` extras, which includes `pydantic-settings`.

```console
$ pip install "fastapi[all]"
```

--------------------------------

### Install Uvicorn with Standard Dependencies

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/manually.md

Installs Uvicorn with recommended extra dependencies, including `uvloop`, for enhanced asynchronous performance. This is useful when manually setting up the server.

```console
$ pip install "uvicorn[standard]"

---> 100%
```

--------------------------------

### Declare a single example for Body parameter using JSON Schema 'examples'

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md

Use the `examples` parameter within `Body()` to provide a single example of the expected request body data. This example is embedded in the JSON Schema.

```python
@app.post("/items/")
async def create_item(
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
        },
    )
):
    return item
```

--------------------------------

### Install FastAPI with standard extras directly

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md

Installs FastAPI and its standard dependencies directly into the active virtual environment.

```console
$ pip install "fastapi[standard]"

---> 100%
```

```console
$ uv pip install "fastapi[standard]"
---> 100%
```

--------------------------------

### Install SQLModel

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md

Installs the SQLModel library using pip, which is required for database integration with FastAPI.

```console
pip install sqlmodel
```

--------------------------------

### Example URL for multiple query parameter values

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md

This URL demonstrates how to pass multiple values for the same query parameter `q`.

```HTTP
http://localhost:8000/items/?q=foo&q=bar
```

--------------------------------

### Install pytest

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/testing.md

Installs the pytest testing framework using pip. Ensure you are in an activated virtual environment.

```console
$ pip install pytest

---> 100%
```

--------------------------------

### Example content for requirements.txt

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md

A sample `requirements.txt` file specifying FastAPI and Pydantic with their exact versions.

```requirements.txt
fastapi[standard]==0.113.0
pydantic==2.8.0
```

--------------------------------

### Install and Run FastAPI CLI in Development Mode

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This snippet shows how to install FastAPI with its latest version and then use the `fastapi dev` command to run an application in development mode, including output logs.

```console
$ pip install --upgrade fastapi

$ fastapi dev main.py


 
╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

--------------------------------

### Install python-multipart

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-form-models.md

Install the `python-multipart` library, which is required for FastAPI to handle forms. This command should be run in your virtual environment.

```console
pip install python-multipart
```

--------------------------------

### Install python-multipart

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-forms.md

Install the `python-multipart` library, which is required for FastAPI to parse form data. This should be done within an activated virtual environment.

```console
$ pip install python-multipart
```

--------------------------------

### Install pydantic-settings package

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md

Install the `pydantic-settings` package to manage application settings from environment variables.

```console
$ pip install pydantic-settings
```

--------------------------------

### Install `websockets` library

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/websockets.md

Installs the `websockets` Python library, which is required to use the WebSocket protocol with FastAPI.

```console
$ pip install websockets
```

--------------------------------

### Example .env file content

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md

This snippet shows the structure of a .env file, defining environment variables that can be loaded by Pydantic Settings.

```bash
ADMIN_EMAIL="deadpool@example.com"
APP_NAME="ChimichangApp"
```

--------------------------------

### Start FastAPI Application with Root Path (Console)

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/behind-a-proxy.md

Starts the FastAPI application using Uvicorn, allowing all forwarded IPs and setting the application's root path to /api/v1 for proxy compatibility.

```console
$ fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

--------------------------------

### Install Python Package Dependencies

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md

Use this command to install the packages listed in `requirements.txt` using `pip`.

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

--------------------------------

### Example API Request with Callback URL

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/openapi-callbacks.md

An example of a request sent to your API, including a query parameter for the external callback URL.

```HTTP
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

--------------------------------

### Install FastAPI with Standard Dependencies

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md

This command installs FastAPI along with its standard dependencies using pip. It downloads the necessary packages from PyPI and extracts them into the current Python environment.

```console
$ pip install "fastapi[standard]"
```

--------------------------------

### Install pwdlib with Argon2

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/security/oauth2-jwt.md

Installs the pwdlib package along with the Argon2 dependency, which is the recommended algorithm for secure password hashing.

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

--------------------------------

### Install and upgrade pip with ensurepip

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md

Use this command to install pip if it's missing and upgrade it, especially when encountering a 'No module named pip' error.

```console
$ python -m ensurepip --upgrade

---> 100%
```

--------------------------------

### Run FastAPI Development Server

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md

Starts the FastAPI development server, which automatically detects the application based on the `pyproject.toml` entrypoint configuration.

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

--------------------------------

### Install FastAPI with Standard Dependencies

Source: https://github.com/fastapi/fastapi/blob/master/README.md

Install FastAPI along with its standard dependencies, including Uvicorn and Pydantic, using pip. Ensure the package name is quoted for cross-terminal compatibility.

```console
$ pip install "fastapi[standard]"

---> 100%
```

--------------------------------

### Example Output of Model Dump

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/extra-models.md

Illustrates the structure and content of the dictionary returned by `.model_dump()` for a `UserIn` model instance.

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

--------------------------------

### Start Traefik with Configuration File (Console)

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/behind-a-proxy.md

Executes the Traefik binary, specifying traefik.toml as the configuration file to load entry points and providers.

```console
$ ./traefik --configFile=traefik.toml

INFO[0000] Configuration loaded from file: /home/user/awesomeapi/traefik.toml
```

--------------------------------

### HTTP Request with Extra Query Parameter

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-param-models.md

An example HTTP GET request demonstrating an extra query parameter that would be forbidden by the model configuration.

```http
https://example.com/items/?limit=10&tool=plumbus
```

--------------------------------

### Create a project directory structure

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md

Commands to set up a new project directory, including a parent 'code' directory and a project-specific directory.

```console
// Go to the home directory
$ cd
// Create a directory for all your code projects
$ mkdir code
// Enter into that code directory
$ cd code
// Create a directory for this project
$ mkdir awesome-project
// Enter into that project directory
$ cd awesome-project
```

--------------------------------

### Using FastAPI Dependencies Directly

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example shows how to define and use a dependency (`get_current_user`) directly within multiple FastAPI path operation functions, leading to some code duplication.

```Python
def get_current_user(token: str):
    # authenticate user
    return User()


@app.get("/items/")
def read_items(user: User = Depends(get_current_user)):
    ...


@app.post("/items/")
def create_item(*, user: User = Depends(get_current_user), item: Item):
    ...


@app.get("/items/{item_id}")
def read_item(*, user: User = Depends(get_current_user), item_id: int):
    ...


@app.delete("/items/{item_id}")
def delete_item(*, user: User = Depends(get_current_user), item_id: int):
    ...
```

--------------------------------

### Example JSON Response from FastAPI Endpoint

Source: https://github.com/fastapi/fastapi/blob/master/README.md

This JSON object represents the typical response structure returned by the FastAPI application when a GET request is made to the /items/{item_id} endpoint with specific path and query parameters.

```JSON
{"item_id": 5, "q": "somequery"}
```

--------------------------------

### Run FastAPI with Multiple Workers using `fastapi` command

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/server-workers.md

Use the `fastapi` command-line tool to start your application with a specified number of worker processes, improving concurrency. This command automatically handles server setup and worker management.

```console
$ fastapi run --workers 4 main.py

  FastAPI   Starting production server 🚀

             Searching for package file structure from directories with
             __init__.py files
             Importing from /home/user/code/awesomeapp

   module   🐍 main.py

     code   Importing the FastAPI app object from the module with the
             following code:

             from main import app

      app   Using import string: main:app

   server   Server started at http://0.0.0.0:8000
   server   Documentation at http://0.0.0.0:8000/docs

             Logs:

     INFO   Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to
             quit)
     INFO   Started parent process [27365]
     INFO   Started server process [27368]
     INFO   Started server process [27369]
     INFO   Started server process [27370]
     INFO   Started server process [27367]
     INFO   Waiting for application startup.
     INFO   Waiting for application startup.
     INFO   Waiting for application startup.
     INFO   Waiting for application startup.
     INFO   Application startup complete.
     INFO   Application startup complete.
     INFO   Application startup complete.
     INFO   Application startup complete.
```

--------------------------------

### Defining an Annotated Dependency

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example demonstrates how to create a reusable `Annotated` type alias for a dependency, combining the type hint and the dependency definition.

```Python
CurrentUser = Annotated[User, Depends(get_current_user)]
```

--------------------------------

### Define Router-Level Dependencies in APIRouter

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example shows how to set router-level dependencies that apply to all path operations within a specific `APIRouter`. It also demonstrates setting a path prefix directly in the router constructor.

```Python
from fastapi import APIRouter, Depends


async def some_dependency():
    return


router = APIRouter(prefix="/users", dependencies=[Depends(some_dependency)])
```

--------------------------------

### Run FastAPI CLI as a Module

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This command demonstrates how to invoke the FastAPI CLI using the Python module runner. This functionality is supported after installing FastAPI with standard dependencies.

```bash
python -m fastapi
```

--------------------------------

### Using Mixed Pydantic v1 and v2 Models in FastAPI

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example demonstrates how to define and use both Pydantic v1 and Pydantic v2 models simultaneously within a FastAPI application, facilitating a gradual migration from v1 to v2.

```Python
from fastapi import FastAPI
from pydantic import BaseModel as BaseModelV2
from pydantic.v1 import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None


class ItemV2(BaseModelV2):
    title: str
    summary: str | None = None


app = FastAPI()


@app.post("/items/", response_model=ItemV2)
def create_item(item: Item):
    return {"title": item.name, "summary": item.description}
```

--------------------------------

### Reusing Annotated Dependencies in FastAPI

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example shows how to reuse a previously defined `Annotated` dependency (`CurrentUser`) across multiple FastAPI path operation functions, significantly reducing code duplication.

```Python
CurrentUser = Annotated[User, Depends(get_current_user)]


@app.get("/items/")
def read_items(user: CurrentUser):
    ...


@app.post("/items/")
def create_item(user: CurrentUser, item: Item):
    ...


@app.get("/items/{item_id}")
def read_item(user: CurrentUser, item_id: int):
    ...


@app.delete("/items/{item_id}")
def delete_item(user: CurrentUser, item_id: int):
    ...
```

--------------------------------

### Declare Header Parameters with Pydantic Models in FastAPI

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example shows how to use a Pydantic BaseModel to define and validate HTTP header parameters, providing structured access to request headers.

```python
from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

--------------------------------

### Handle HTTPException in FastAPI Dependencies with yield

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example demonstrates how to raise `HTTPException` or custom exceptions after `yield` in a dependency. It shows how to catch a custom `OwnerError` and re-raise it as an `HTTPException` within the dependency's `except` block.

```Python
from fastapi import Depends, FastAPI, HTTPException
from typing_extensions import Annotated

app = FastAPI()


data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}


class OwnerError(Exception):
    pass


def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")


@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item
```

--------------------------------

### Managing Context Variables in FastAPI Dependencies with Yield (Python)

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example shows how to correctly set and reset `contextvars` within a dependency using `yield`. It ensures the context is preserved and reset properly, addressing a previous issue.

```Python
from contextvars import ContextVar
from typing import Any, Dict, Optional


legacy_request_state_context_var: ContextVar[Optional[Dict[str, Any]]] = ContextVar(
    "legacy_request_state_context_var", default=None
)

async def set_up_request_state_dependency():
    request_state = {"user": "deadpond"}
    contextvar_token = legacy_request_state_context_var.set(request_state)
    yield request_state
    legacy_request_state_context_var.reset(contextvar_token)
```

--------------------------------

### Declare Form Fields with Pydantic Models in FastAPI

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example demonstrates how to declare form fields using a Pydantic `BaseModel` in FastAPI, allowing structured validation for incoming form data.

```python
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
```

--------------------------------

### FastAPI `response_model` with Implicit `None` (Invalid)

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md

This example shows a FastAPI path operation that implicitly returns `None` under certain conditions. If `response_model` does not include `None`, this will also result in an internal server error.

```Python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: Optional[float] = None
    owner_ids: Optional[List[int]] = None

app = FastAPI()

@app.get("/items/invalidnone", response_model=Item)
def get_invalid_none():
    if flag:
        return {"name": "foo"}
    # if flag is False, at this point the function will implicitly return None
```

--------------------------------

### HTTP GET Request with Requests and FastAPI

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/alternatives.md

These snippets demonstrate the intuitive design similarities between making a GET request using the Requests client library and defining a GET path operation in FastAPI.

```Python
response = requests.get("http://example.com/some/url")
```

```Python
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

--------------------------------

### Install Pydantic with Email Extras

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/response-model.md

Installs Pydantic with the `email` extra, which includes `email-validator`.

```console
$ pip install "pydantic[email]"
```

--------------------------------

### Create Database Tables on Application Startup

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md

Registers a startup event handler in FastAPI to call 'create_db_and_tables', ensuring the database schema is initialized when the application starts.

```python
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

--------------------------------

### Run FastAPI App with --entrypoint CLI Option

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/fastapi-cli.md

Use the `--entrypoint` option with `fastapi dev` to explicitly define the app's import string from the command line.

```console
fastapi dev --entrypoint main:app
```

--------------------------------

### Instantiate ASGI Middleware Directly

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/middleware.md

This shows the general way to instantiate an ASGI middleware directly, passing an existing ASGI app. FastAPI provides a simpler method for better error handling.

```python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

--------------------------------

### Install PyJWT

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/security/oauth2-jwt.md

Installs the PyJWT library, which is required for generating and verifying JWT tokens in Python applications.

```console
$ pip install pyjwt

---> 100%
```

--------------------------------

### Example URL for default list query parameters

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md

Accessing the endpoint without query parameters, triggering default list values for `q`.

```HTTP
http://localhost:8000/items/
```

--------------------------------

### File Structure with Test File

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/testing.md

Illustrates adding `test_main.py` to the application package for testing, allowing relative imports.

```text
.├── app│   ├── __init__.py│   ├── main.py│   └── test_main.py
```

--------------------------------

### Install email-validator for EmailStr

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/response-model.md

Installs the `email-validator` library, required for using Pydantic's `EmailStr` type.

```console
$ pip install email-validator
```

--------------------------------

### Run FastAPI Development Server

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md

Start the FastAPI development server using the `fastapi dev` command, either by specifying the file path or an explicit entry point.

```console
$ fastapi dev main.py
```

```console
$ fastapi dev --entrypoint main:app
```

--------------------------------

### Install a different package version globally

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md

This command installs a different version of a package into the global Python environment. Installing a new version will typically overwrite previous versions, potentially breaking projects that depend on the older version.

```console
$ pip install "harry==3"
```

--------------------------------

### Create a virtual environment with uv

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md

Use the `uv` tool to create a new virtual environment in the current project directory.

```console
$ uv venv
```

--------------------------------

### Run FastAPI Development Server

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/sub-applications.md

Use this command to start the FastAPI development server, making the application and its mounted sub-applications accessible locally.

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

--------------------------------

### Run FastAPI Development Server with Explicit Path

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md

Demonstrates how to run the FastAPI development server by explicitly passing the application's main file path to the `fastapi dev` command.

```console
$ fastapi dev app/main.py
```

--------------------------------

### Install Jinja2 for FastAPI Templates

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/templates.md

Install the Jinja2 package using pip to enable template rendering in your FastAPI application.

```console
$ pip install jinja2

---> 100%
```

--------------------------------

### Instantiating Pydantic Settings

Source: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md

This demonstrates how a new Pydantic Settings object is created, which would typically re-read the .env file if not cached.

```Python
Settings()
```

