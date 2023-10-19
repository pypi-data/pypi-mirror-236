from types import SimpleNamespace
from typing import Any
from typing import Dict
from typing import Optional


async def request(
    hub: Any,
    url: str,
    method: str,
    content_type: str = "raw",
    headers: Optional[Dict[str, str]] = None,
    **kwargs: Any,
) -> Optional[str]:
    """
    This function retrieves the raw text of a web page at the given URL using the specified content type and headers
    or sends a post request to a web page depending on the method.
    It returns the raw text as a string, or None if the request failed.

    :param hub: The hub object.
    :type hub: Any
    :param url: The URL to retrieve.
    :type url: str
    :param method: request method
    :type method: str
    :param content_type: The content type of the response. Defaults to "raw".
    :type content_type: str
    :param headers: The headers to include in the request. Defaults to None.
    :type headers: Optional[Dict[str, str]]
    :param kwargs: Additional keyword arguments to pass to the request method.
    :type kwargs: Any
    :return: The raw text of the retrieved web page, or None if the request failed.
    :rtype: Optional[str]

    The `url` parameter is the URL of the web page to retrieve. The `content_type` parameter specifies the content type of the response, which can be "raw", "json", or any other valid content type.
    The `headers` parameter is an optional dictionary of headers to include in the request.
    Additional keyword arguments can be passed using the `kwargs` parameter.
    """
    # open the URL and read the data
    ctx = SimpleNamespace(acct={})

    try:
        web_call = getattr(hub.exec.request, content_type)
    except AttributeError as exc:
        hub.log.error(f"Invalid content_type for pop-aiohttp: {exc}")
        web_call = hub.exec.request.raw

    if method == "get":
        ret = await web_call.get(
            ctx,
            url=url,
            headers=headers,
        )
    if method == "post":
        ret = await web_call.post(ctx, url=url, headers=headers, **kwargs["kwargs"])

    if ret["status"] == 200:
        remote_page = ret["ret"]
    else:
        hub.log.error(f"Unable to retrieve URL: {url}")
        return None

    if content_type != "json":
        try:
            remote_page = remote_page.decode("utf-8")
        except AttributeError:
            return None

    return remote_page
