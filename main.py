import asyncio
from react_agent import graph
from react_agent.context import Context
import json

import os

ctx = Context(model='fireworks/accounts/fireworks/models/qwen3-8b',system_prompt="You are a helpful AI assistant.")
async def main():
    res = await graph.ainvoke(
        {"messages": [("user", "Who is the founder of LangChain?")]},
        context=ctx,
    )
    for m in res["messages"]:
        print(m.type,m.content_blocks)
    


if __name__ == "__main__":
    asyncio.run(main())