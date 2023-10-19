import asyncio
from typing import Any
from typing import List


HEADERS: List[str] = []
ROUTES: List[str] = []


def __init__(hub: Any) -> None:
    """
    Remember not to start your app in the __init__ function
    This function should just be used to set up the plugin subsystem
    The run.py is where your app should usually start
    """
    for dyne in ["log", "acct", "exec", "server", "tool"]:
        hub.pop.sub.add(dyne_name=dyne)
    for dyne in ["exec", "server", "tool"]:
        hub.pop.sub.load_subdirs(getattr(hub, dyne), recurse=True)


def cli(hub: Any) -> None:
    hub.pop.config.load(["pop_config", "acct", "web_retriever"], cli="web_retriever")
    # Your app's options can now be found under hub.OPT.web_retriever
    dict(hub.OPT.web_retriever)

    # Initialize the asyncio event loop
    hub.pop.loop.create()

    # Get event loop
    loop = asyncio.get_event_loop()

    # decrypt the encrypted file using the given key and populate hub.acct.PROFILES with the decrypted structures
    if hub.OPT.acct.acct_file:
        coroutine = hub.acct.init.unlock(hub.OPT.acct.acct_file, hub.OPT.acct.acct_key)
        hub.pop.Loop.run_until_complete(coroutine)

        # Process profiles from subs in `hub.acct.web_retriever` and put them into `hub.acct.SUB_PROFILES`
        # return the explicitly named profile
        coroutine = hub.acct.init.gather(
            subs=["web_retriever"]  # , profile=hub.OPT.acct.acct_profile
        )
        hub.pop.Loop.run_until_complete(coroutine)

    headers = ""
    for header in hub.web_retriever.init.HEADERS:
        headers += f' "%{{{header}}}i"'

    # Add routes for each endpoint
    hub.web_retriever.fetch.add_routes()
    hub.web_retriever.throw.add_routes()

    # Start the async code
    coroutine = hub.server.web.run(
        loop=loop,
        routes=hub.web_retriever.init.ROUTES,
        access_log_format='%a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"' + headers,
    )
    hub.pop.Loop.run_until_complete(coroutine)
