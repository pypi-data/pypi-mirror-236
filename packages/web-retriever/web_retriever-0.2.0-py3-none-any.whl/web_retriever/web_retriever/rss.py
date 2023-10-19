from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import feedparser  # type: ignore


async def get_feed(
    hub: Any,
    url: str,
    max_entries: Optional[int] = None,
    key_allowlist: Optional[Union[str, List[str]]] = None,
    key_denylist: Optional[Union[str, List[str]]] = None,
    **kwargs: Dict[str, Any],
) -> List[Dict[str, Union[str, int]]]:
    """
    Retrieve a feed from a given URL and return a list of entries.

    :param hub: The hub object.
    :type hub: Any
    :param url: The URL of the feed to retrieve.
    :type url: str
    :param max_entries: The maximum number of entries to retrieve. If not specified, all entries will be returned.
    :type max_entries: Optional[int]
    :param key_allowlist: A list of keys to include in the returned entries. If not specified, all keys will be returned.
    :type key_allowlist: Optional[Union[str, List[str]]]
    :param key_denylist: A list of keys to exclude from the returned entries. If not specified, no keys will be excluded.
    :type key_denylist: Optional[Union[str, List[str]]]
    :param kwargs: Additional keyword arguments to pass to the feedparser library.
    :type kwargs: Dict[str, Any]
    :return: A list of dictionaries representing the entries in the feed.
    :rtype: List[Dict[str, Union[str, int]]]
    :raises: None
    """
    if key_allowlist is None:
        key_allowlist = []
    elif isinstance(key_allowlist, str):
        key_allowlist = key_allowlist.split(",")

    if key_denylist is None:
        key_denylist = []
    elif isinstance(key_denylist, str):
        key_denylist = key_denylist.split(",")

    if max_entries:
        try:
            max_entries = int(max_entries)
        except (TypeError, ValueError):
            max_entries = None
            hub.log.error(f"Unable to convert {max_entries} to an index")

    feed = feedparser.parse(url)
    entries = feed.entries[:max_entries]

    if key_allowlist or key_denylist:
        for idx, entry in enumerate(entries):
            updated_entry = {
                key: entry[key]
                for key in entry
                if key not in key_denylist and (not key_allowlist or key in key_allowlist)
            }
            entries[idx] = updated_entry

    return entries
