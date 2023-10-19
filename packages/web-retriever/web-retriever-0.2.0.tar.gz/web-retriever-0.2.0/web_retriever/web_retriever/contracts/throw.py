def call_post(hub, ctx):
    return hub.web_retriever.ops.rule_handler(ctx)
