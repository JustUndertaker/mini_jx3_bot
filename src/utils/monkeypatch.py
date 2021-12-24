import asyncio
import platform

from uvicorn import config
from uvicorn.loops import asyncio as _asyncio


def asyncio_setup():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


@property
def should_reload(self):
    return False


def monkeypatch():
    if platform.system() == "Windows":
        _asyncio.asyncio_setup = asyncio_setup
        config.Config.should_reload = should_reload
