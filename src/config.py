from os import environ
from log import log
from dotenv import load_dotenv
from types import MappingProxyType


log.info("load .env file")
load_dotenv()
log.success("load .env file")


log.info("init config")
config = MappingProxyType(
    {
        "PARALLEL_DOWNLOAD": int(str(environ.get("PARALLEL_DOWNLOAD", "2"))),
        "PARALLEL_CONNECTION": int(str(environ.get("PARALLEL_CONNECTION", "8"))),
        "DATABASE_PATH": str(environ.get("DATABASE_PATH", "main.db")),
        "HOST": str(environ.get("HOST", "0.0.0.0")),
        "PORT": int(str(environ.get("PORT", "3000"))),
    }
)
log.success("init config")
