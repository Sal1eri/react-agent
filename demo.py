import asyncio
from react_agent import graph
from react_agent.context import Context
import tqdm
import json
import os



syspm ="""
You are a ReAct question-answering agent.

Reason briefly but carefully to solve the problem.
Use tools when you are unsure or need external information.

When you finish, output ONLY a valid JSON object:

{{
  "answer": "<short answer span>"
}}

The answer must be a short text span with no explanation.
Return ONLY the JSON object and nothing else.
"""



def get_dataset():
    dataset = []
    for file in os.listdir("dataset/"):
        if file.endswith(".json"):
            with open(os.path.join("dataset/", file), "r", encoding="utf-8") as f:
                data = json.load(f)
                dataset.extend(data)
ctx = Context(
    model="fireworks/accounts/fireworks/models/qwen3-8b",
    system_prompt=syspm,
)

candidate_questions = [
    "Were Scott Derrickson and Ed Wood of the same nationality?",
    "What government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?",
    "What science fantasy young adult series, told in first person, has a set of companion books narrating the stories of enslaved worlds and alien species?",
    "Are the Laleli Mosque and Esma Sultan Mansion located in the same neighborhood?"
]

async def get_react_response(question: str):
    return await graph.ainvoke(
        {"messages":[{
            "role":"user",
            "content":question
        }]},
        context=ctx
    )
async def eval_benchmark():
    log = []
    for question in tqdm.tqdm(candidate_questions):
        row = {"question": question, "react_loop": []}
        res = await get_react_response(question)
        for m in res["messages"]:
            entry = {
                "role": getattr(m, "type", None),
                "content_blocks": m.content_blocks
            }
            row["react_loop"].append(entry)
        log.append(row)
    return log

async def main():
    log = await eval_benchmark()
    with open("react_agent_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())