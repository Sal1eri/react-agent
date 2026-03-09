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

    log = []

    record = {
        "question": "who is the founder of LangChain?",
        "messages": [],
    }
    for m in res["messages"]:
        entry = {
            "role": getattr(m, "type", None),
            "content_blocks": m.content_blocks
        }

        
        log.append(entry)

    with open("content_blocks_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    asyncio.run(main())