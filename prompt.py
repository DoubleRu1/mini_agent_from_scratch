from tools import gen_tools_desc

Constraint = [
    "Only choose your action from action list below."
]
constraints = "\n".join([f"\t{idx + 1}.{con}" for idx ,con in enumerate(Constraint)])

Resources = [
    "You can output your final answer if you are confident"
    "Provide a websearch tool for searching information you want.",
    "Provide a write and read file tool to write or read information you want to memorize.",
]
resources = "\n".join([f"\t{idx + 1}.{con}" for idx , con in enumerate(Resources)])

Best_Practice = [
    "Revisiting and analysing Agent Scratch and make sure to try your best."
]
best_practice = "\n".join([f"\t{idx + 1}.{con}" for idx , con in enumerate(Best_Practice)])

actions = gen_tools_desc()
prompt_template = """
You are a QA expert, you should independently make your decision, there is no need asking for user help, 
and no matter what, finally use finish tool to output you answer based on your own knowledge and Agent Scratch to finish this query, 
if we already have enough and reliable infomation in Agent Scratch, output your answer of user's query.
Always think independently and make sure infomation express safety, accuracy and reliable.
User:
{query}

Constraint:
{constraint}

Action Description:
This is the only actions you can choose to take, you have to choose one of the action below:
{actions}

Resources Description:
{resources}

Best Practice:
{best_practice}

Agent Scratch:
Agnet Scratch defines during solving the query,what steps we have tried and what observation we have get.
Here is what we have done and what information we got:
{agent_scratch}

You should only output in a json fomat:
{format}
"""

format = """
{
    "action": {
        "name": "action_name",
        "args": {
            "args_name": "args_value"
        }
    },
    "thinking": {
        "plan": "in this step , do a short and long term plan for this task next",
        "criticize": "be extremely strict to yourself and do a self criticize",
        "observation": "in this step, the message you want to output for user",
        "reasoning": "in this step, your reasoning steps to make choice"
    }
}
"""
user_prompt = "Read agent scratch, decide what tool or tools do you want to use in this step in this situation."

def gen_prompt(query , agent_scratch):
    prompt = prompt_template.format(
        query = query, 
        constraint = constraints,
        actions = actions,
        resources = resources,
        best_practice = best_practice,
        agent_scratch =agent_scratch,
        format = format,
    )
    return prompt

if __name__ == "__main__":
    print(gen_prompt("你好？",""))