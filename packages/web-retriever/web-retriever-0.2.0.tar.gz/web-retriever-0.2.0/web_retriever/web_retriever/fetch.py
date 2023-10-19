import datetime as dt
from typing import Any
from typing import Dict
from typing import List
from typing import Union

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
    ["get", "/api/v1/fetch", hub.web_retriever.fetch.get]
    """

    hub.web_retriever.init.ROUTES.extend(
        [
            ["get", "/api/v1/fetch", hub.web_retriever.fetch.get],
            ["post", "/api/v1/fetch", hub.web_retriever.fetch.get_multiple],
        ]
    )


async def get(hub: Any, request: Request, mods: List[Dict[str, Any]], **kwargs: Any) -> Any:
    """
    This function retrieves data from a single URL. It validates the query parameters
    and returns the data in a dictionary format.

    :param hub: The hub object.
    :type hub: Any
    :param request: The request object.
    :type request: Request
    :param mods: Modifications to the outbound request in fetch()
    :type request: List
    :param kwargs: Additional keyword arguments.
    :type kwargs: Any
    :return: The response object.
    :rtype: Any
    """
    params: Dict[str, Any] = dict(request.query)
    ret, status = await hub.web_retriever.ops.request(request.headers, mods, params, method="get")
    return await hub.server.web.response_handler(ret, status=status)


async def get_multiple(
    hub: Any, request: Request, mods: List[Dict[str, Any]], **kwargs: Any
) -> Any:
    """
    This function retrieves data from multiple URLs. It validates the URL data structure
    and returns the data in a dictionary format.

    :param hub: The hub object.
    :type hub: Any
    :param request: The request object.
    :type request: Request
    :param mods: Modifications to the outbound request in fetch()
    :type request: List
    :param kwargs: Additional keyword arguments.
    :type kwargs: Any
    :return: The response object.
    :rtype: Any
    """
    headers: Dict[str, str] = {}
    ret: Dict[str, Union[str, List[Dict[str, Any]], Dict[str, Any]]] = {"data": []}

    # url data validation
    try:
        data: Dict[str, List[Dict[str, Any]]] = await request.json()
        urls: List[Dict[str, Any]] = data.get("urls", [])
    except KeyError as exc:
        reason: str = "Invalid URL data structure"
        hub.log.error(f"{reason}: {exc}")
        ret = {"status": "fail", "error": reason}
        return await hub.server.web.response_handler(ret, headers=headers, status=400)

    params: Dict[str, Any] = dict(request.query)
    params["type"] = params.get("type", "text").lower()

    status_list: List[bool] = []

    for url in urls:
        url_params: Dict[str, Any] = params.copy()
        if isinstance(url, dict):
            url_params.update(url)
            url = url_params.pop("url")

        url_data: Dict[str, Any]
        status: bool

        hdrs = hub.web_retriever.ops.mods(request.headers, mods)

        url_data, status = await hub.web_retriever.ops.get(url, hdrs, method="get", **url_params)

        ret["data"].append(url_data)  # type: ignore
        status_list.append(status)

    status_string: str = "fail"
    if all(status_list):
        status_string = "success"
    elif any(status_list):
        status_string = "partial"

    ret["status"] = status_string
    ret["timestamp"] = dt.datetime.now().isoformat()

    return await hub.server.web.response_handler(ret, headers=headers)
