#!/usr/bin/env python3
import pop.hub  # type: ignore


def start() -> None:
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="web_retriever")
    hub["web_retriever"].init.cli()
