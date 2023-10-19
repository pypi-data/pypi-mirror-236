from typing import Any
from typing import Dict
from typing import List

from aiohttp.web import Request  # type: ignore


def __init__(hub: Any) -> None:
    """
    Remember not to start your app in the __init__ function
    This function should just be used to set up the plugin subsystem
    The run.py is where your app should usually start
    """
    ...


def add_routes(hub: Any) -> None:
    """
    Add routes to the web_retriever plugin subsystem.

    :param hub: The hub object.
    :type hub: Any
    :return: None
    :rtype: None

    To set up routes, add them to the ROUTES list in the following format:
    ["verb", "location", hub function]
    e.g.
    ["post", "/api/v1/throw", hub.web_retriever.throw.post]
    """

    hub.web_retriever.init.ROUTES.extend(
        [
            ["post", "/api/v1/throw", hub.web_retriever.throw.post],
        ]
    )


async def post(hub: Any, request: Request, mods: List[Dict[str, Any]], **kwargs: Any) -> Any:
    """
    This function post data to a single URL. It returns the page response, status,
    and timestamp in a dictionary format.

    :param hub: The hub object.
    :type hub: Any
    :param request: The request object.
    :type request: Request
    :param mods: Modifications to the outbound request
    :type request: List
    :param kwargs: Additional keyword arguments.
    :type kwargs: Any
    :return: The response object.
    :rtype: Any
    """

    data: Dict[str, Any] = await request.json()
    ret, status = await hub.web_retriever.ops.request(request.headers, mods, data, method="post")
    return await hub.server.web.response_handler(ret, status=status)
