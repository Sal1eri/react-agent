import asyncio
from react_agent import graph
from react_agent.context import Context
import tqdm
import json
import os
from datetime import datetime
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
class Benchmark:
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

    def get_dataset(self):
        dataset_name = self.dataset_name + '_500'
        for file in os.listdir("dataset/"):
            if file.endswith(".json") and dataset_name in file:
                with open(os.path.join("dataset/", file), "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data


async def get_react_response(question: str, ctx: Context):
    return await graph.ainvoke(
        {"messages":[{
            "role":"user",
            "content":question
        }]},
        context=ctx
    )

async def eval_benchmark(Bench: Benchmark, ctx: Context):
    log = []
    dataset = Bench.get_dataset()

    for item in tqdm.tqdm(dataset):
        question = item['question']
        ground_truth = item['answer']
        row = {"question": question, "ground_truth": ground_truth, "react_loop": []}
        res = await get_react_response(question, ctx)
        # exceed rate limit, sleep for a while and retry
        await asyncio.sleep(3)
        for m in res["messages"]:
            entry = {
                "role": getattr(m, "type", None),
                "content_blocks": getattr(m, "content_blocks", None)
            }
            row["react_loop"].append(entry)
        log.append(row)
    
    log.append({
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_prompt": ctx.system_prompt,
        "base_model": ctx.model,
        "samples": len(dataset),
        "benchmark": Bench.dataset_name
    })
    return log



if __name__ == "__main__":
   benchmark = Benchmark('hpqa')
   ctx = Context(
    model="fireworks/accounts/fireworks/models/qwen3-8b",
    system_prompt=syspm,
    )
   log = asyncio.run(eval_benchmark(benchmark, ctx))
   with open("benchmark_log.json", "w", encoding="utf-8") as f:
       json.dump(log, f, ensure_ascii=False, indent=4)