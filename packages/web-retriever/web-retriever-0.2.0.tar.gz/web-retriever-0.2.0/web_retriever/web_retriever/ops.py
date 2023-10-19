import asyncio
import datetime as dt
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import rule_engine  # type: ignore
from multidict import CIMultiDict  # type: ignore


async def _async_run(hub: Any, func: Any) -> Any:
    return await hub.pop.loop.unwrap(func)


async def request(
    hub: Any,
    headers: Dict[str, str],
    mods: List[Dict[str, Any]],
    data: Dict[str, Any],
    method: str,
    **kwargs: Any,
) -> Tuple[Dict[str, Any], int]:
    """
    Function to validate url and pass to associated request
    """
    ret: Dict[str, Union[str, List[Dict[str, Any]], Dict[str, Any]]] = {}
    url_data: Dict[str, Any]
    status: bool = False

    hdrs = hub.web_retriever.ops.mods(headers, mods)

    try:
        url: str = data["url"]
        data.pop("url")
    except KeyError as exc:
        reason: str = "url not included"
        hub.log.error(f"{reason}: {exc}")
        ret = {"status": "fail", "error": reason}
        return ret, 400

    if method == "post":
        url_data, status = await hub.web_retriever.ops.post(url, data, hdrs, method)

    if method == "get":
        url_data, status = await hub.web_retriever.ops.get(url, hdrs, method, **data)

    status_string: str = "fail"
    if status:
        status_string = "success"

    ret = {
        "status": status_string,
        "data": [url_data],
        "timestamp": dt.datetime.now().isoformat(),
    }
    return ret, 200


async def get(
    hub: Any, url: str, hdrs: Dict[str, str], method: str, **kwargs: Any
) -> Tuple[Dict[str, Any], bool]:
    """
    Function to execute get command
    """
    status: bool = True
    content_type: str = kwargs.get("type", "text").lower()
    try:
        if content_type == "json":
            content: Any = await hub.web_retriever.web.request(
                url, method, headers=hdrs, content_type="json"
            )
        elif content_type == "rss":
            content = await hub.web_retriever.rss.get_feed(url, **kwargs)
        else:
            content = await hub.web_retriever.web.request(url, method, headers=hdrs)
    except Exception:
        content = {}

    if not content:
        status = False

    url_data: Dict[str, Any] = {
        "url": url,
        "type": content_type,
        "content": content,
    }
    return url_data, status


async def post(
    hub: Any, url: str, data: Dict[str, Any], hdrs: Dict[str, str], method: str
) -> Tuple[Dict[str, Any], bool]:
    """
    Function to execute post command
    """
    status: bool = True
    content_type: str = data.get("type", "").lower()
    data.pop("type")
    try:
        content: Any = await hub.web_retriever.web.request(
            url, method, content_type, hdrs, kwargs=data
        )
    except Exception:
        content = {}

    if not content:
        status = False

    url_data: Dict[str, Any] = {
        "url": url,
        "type": content_type,
        "content": content,
    }
    return url_data, status


def rule_handler(hub: Any, ctx: Any) -> Any:
    request: Any = ctx.args[1]
    rules: List[Any] = hub.OPT.web_retriever.rules or []

    result: Union[List[Dict[str, Any]], Dict[str, str]] = hub.web_retriever.ops.process_rules(
        request, rules
    )

    if isinstance(result, dict):
        return _async_run(
            hub,
            hub.server.web.response_handler(result, status=403),
        )

    ret: Any = ctx.func(*ctx.args, result, **ctx.kwargs)
    if asyncio.iscoroutinefunction(ctx.func):
        return _async_run(hub, ret)
    return ret


def process_rules(
    hub: Any, request: Any, rules: List[Dict[str, Any]]
) -> Union[List[Dict[str, Any]], Dict[str, str]]:
    mods: List[Dict[str, Any]] = []

    rule_ctx: Any = rule_engine.Context(resolver=rule_engine.engine.resolve_attribute)

    for idx, rule in enumerate(rules):
        rtype: Union[str, None] = rule.get("rule_type")

        if not rtype or rtype.lower() not in ["allow", "deny", "transform"]:
            continue

        rstr: Union[str, None] = rule.get("rule_string")
        transform: Union[None, Dict[str, Any]] = rule.get("transform")

        if rstr and rtype.lower() in ["allow", "deny"]:
            try:
                robj: Any = rule_engine.Rule(rstr, context=rule_ctx)
                match: bool = robj.matches(request)
            except (
                rule_engine.RuleSyntaxError,
                rule_engine.SymbolResolutionError,
            ) as exc:
                hub.log.error(f"pre rule {idx}: {exc.message}")
                return {"error": f"pre rule {idx} failure"}

            if rtype.lower() == "allow" and not match or rtype.lower() == "deny" and match:
                # return forbidden
                hub.log.debug(f"rule {idx} validation failed")
                return {"error": f"forbidden by pre rule {idx}"}
        elif rtype.lower() == "transform" and transform:
            mods.append(transform)

    return mods


def mods(hub: Any, headers: Dict[str, Any], mods: List[Dict[str, Any]]) -> Any:
    """
    Function to modify request headers
    """
    hdrs: Dict[str, str] = CIMultiDict()
    for mod in mods:
        if mod.get("pass_request_headers"):
            hdrs.update(headers)
        for key, val in mod.get("request_headers", {}).get("add", {}).items():
            hdrs[key] = val
        for key in mod.get("request_headers", {}).get("remove", []):
            if key in hdrs:
                hdrs.pop(key)
    return hdrs
