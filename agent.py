import time
from tools import tools_map
from prompt import gen_prompt
import os
from openai import OpenAI
from dotenv import load_dotenv
from model_provider import ModelProvider
"""
todo:
    1.从命令行输入
    2.搭建基础的模型
    3.环境变量引入
    4.工具引入
    5.prompt模板
    6.从模型回答中获得json格式数据，同时进行action判断
    7.action到对应函数的映射

"""

load_dotenv()
mp = ModelProvider()

def parse_thinking(response):
    """
    response格式
    {
        action: {
            "name": "action_name",
            "args": {
                "args_name": "args_value"
            }
        },
        thinking: {
            "text": "thought",
            "plan": "plan",
            "criticize": "criticize",
            "observation": "observation",
            "reasoning": "reasoning"
        }
    }
    """
    try:
        thinking = response.get("thinking")
        plan = thinking.get("plan")
        reasoning = thinking.get("reasoning")
        criticize = thinking.get("criticize")
        observation = thinking.get("observation")
        prompt = f"plan:{plan}\nreasoning:{reasoning}\ncriticize:{criticize}\nobservation:{observation}"
        return prompt
    except Exception as err:
        print("parse_thinking err:",err)
        return "{}".format(err)



def agent_execute(query , max_request_time = 3):
    cur_request_times = 0
    chat_history = []
    agent_scratch = ""
    while cur_request_times < max_request_time:
        cur_request_times += 1
        
        prompt = gen_prompt(query , agent_scratch)
        
        start_time = time.time()
        print(f"开始尝试第{cur_request_times}次调用大模型......",flush=True)
        # call llm
        print("chat_history: ",chat_history)
        print("prompt:",prompt)
        response = mp.chat(prompt,chat_history)
        print("\n")
        print(response)
        print("\n")
        end_time = time.time()
        print(f"第{cur_request_times}次调用大模型结束，耗时{(end_time - start_time)}s",flush=True)
        if not response or not isinstance(response,dict):
            print("调用大模型错误，正在重新调用......",response)
            continue
        """
        response格式
        {
            action: {
                "name": "action_name",
                "args": {
                    "args_name": "args_value"
                }
            },
            thinking: {
                "text": "thought",
                "plan": "plan",
                "criticize": "criticize",
                "observation": "observation",
                "reasoning": "reasoning"
            }
        }
        """

        action_info = response.get("action")
        action_name = action_info.get("name")
        action_args = action_info.get("args")
        print(f"当前采取的action: {action_name}")

        if action_name == "finish":
            final_answer = action_args.get("final_answer")
            return final_answer
        observation = f"Step{cur_request_times}:\n" +response.get("thinking").get("observation")
        try:
            """
            action名到action函数的映射{action_name : actionfunc}
            """
            func = tools_map.get(action_name)
            observation = f"{observation}\n" + f"This is what i got using {action_name}:\n" + func(**action_args)
        except Exception as err:
            print("调用工具异常",err)
            observation = observation + " but an error occured" + err
        agent_scratch = agent_scratch  + "\n" + observation

        user_msg = query
        assistant_msg = parse_thinking(response)

        chat_history.append([user_msg,assistant_msg])


def main():
    max_request_time = 10
    "持续监视用户调用"
    while True:
        query = input("请输入您的问题，输入exit以退出:")
        if query.lower() == "exit":
            print("对话已结束.")
            break
        output = agent_execute(query = query,max_request_time = max_request_time)
        print("assistant:\n",output)


if __name__ == "__main__":
    main()