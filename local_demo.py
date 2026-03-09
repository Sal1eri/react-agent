import json
import os
import tqdm

from react_agent import graph
from react_agent.context import Context

syspm = """
You are a ReAct agent for question answering.

Use tools when needed to retrieve information.
Do not reveal intermediate reasoning or tool traces.

When you finish, output ONLY a valid JSON object:

{{
  "answer": "<short answer span>"
}}

Note that should only be a short text span without explanation.
"""

def get_dataset():
    dataset = []
    for file in os.listdir("dataset/"):
        if file.endswith(".json"):
            with open(os.path.join("dataset/", file), "r", encoding="utf-8") as f:
                data = json.load(f)
                dataset.extend(data)
    return dataset

# 改成你的本地模型路径（目录里应有 config.json / *.safetensors 等）
ctx = Context(
    model="fireworks/accounts/fireworks/models/qwen3-8b",  # <-- 改这里
    system_prompt=syspm,
)

candidate_questions = [
    "Were Scott Derrickson and Ed Wood of the same nationality?",
    "What government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?",
]

def get_react_response(question: str):
    return graph.invoke({"messages": [("user", question)]}, context=ctx)

def eval_benchmark():
    log = []
    for question in tqdm.tqdm(candidate_questions):
        row = {"question": question, "react_loop": []}
        res = get_react_response(question)
        for m in res["messages"]:
            entry = {
                "role": getattr(m, "type", None),
                "content_blocks": m.content_blocks,
            }
            row["react_loop"].append(entry)
        log.append(row)
    return log

def main():
    log = eval_benchmark()
    with open("react_agent_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()