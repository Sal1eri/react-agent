import asyncio
from react_agent import graph
from react_agent.context import Context
import json

import os

ctx = Context(model='fireworks/accounts/fireworks/models/qwen3-8b',system_prompt="You are a helpful AI assistant.")
async def main():
    res = await graph.ainvoke(
        {"messages": [("user", "Were Scott Derrickson and Ed Wood of the same nationality?")]},
        context=ctx,
    )

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(str(res))

    print("Saved raw string to result.txt")



if __name__ == "__main__":
    asyncio.run(main())