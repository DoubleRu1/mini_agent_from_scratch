
"""
    1.写文件
    2.读文件
    3.追加文件
    4.网络搜索
"""
import os
from langchain_community.tools.tavily_search import TavilySearchResults
import json

def _get_workdir_root():
    workdir_root  = os.environ.get("WORKDIR_ROOT",'./data/llm_result')

    return workdir_root

WORKDIR_ROOT = _get_workdir_root()

def read_file(filename):
    filename = os.path.join(WORKDIR_ROOT,filename)

    if not os.path.exists(filename):
        return f"{filename} not exist."
    with open(filename,'r') as f:
        return "\n".join(f.readlines())
    
def write_file(filename,content):
    if not os.path.exists(WORKDIR_ROOT):
        os.makedirs(WORKDIR_ROOT)
    filename = os.path.join(WORKDIR_ROOT,filename)
    with open(filename,'a') as f:
        f.write(content)
    return f"write to file {filename} success"

def append_file(filename,content):
    filename = os.path.join(WORKDIR_ROOT,filename)
    if not os.path.exists(filename):
        return f"{filename} not exist."
    with open(filename,'a') as f:
        f.write(content)
    
    return f"append to file {filename} success"

def search(query):
    tool = TavilySearchResults(
        max_results=5,
        include_answer=True,
        include_raw_content=True,
        include_images=True,
    )
    try:
        ret = tool.invoke({"query":query})

        content_list = [obj["content"] for obj in ret]
        return "\n".join(content_list)
    except Exception as err:
        return f"search error, {err}" 
    

tools_info = [
    {
        "name":"finish",
        "description": "if you are confident to answer the query, take this action to output your final answer to user referring to Agent Scratch",
        "args":[{
            "name": "final_answer",
            "type": "string",
            "description": "your final answer of user's query"
        }]
    },
    {
        "name":"read_file",
        "description":"read file from agent generate, should write file before read",
        "args":[{
            "name":"filename",
            "type":"string",
            "description":"read file name"
        }]
    },
    {
        "name":"write_file",
        "description":"write llm content into a file",
        "args":[{
            "name":"filename",
            "type":"string",
            "description":"file name"
        },
        {
            "name":"content",
            "type":"string",
            "description":"write to file content"
        },
        ]
    },
    {
        "name":"append_file",
        "description":"append llm content into a file",
        "args":[{
            "name":"filename",
            "type":"string",
            "description":"file name"
        },
        {
            "name":"content",
            "type":"string",
            "description":"append to file content"
        },
        ]
    },
    {
        "name":"search",
        "description":"this is a search engine, you can get additional knowledge when you are not sure about what large language model return",
        "args":[{
            "name":"query",
            "type":"string",
            "description":"the query you want to search"
        }]
    }
]


tools_map = {
    "read_file":read_file,
    "write_file":write_file,
    "append_file":append_file,
    "search":search,
}

def gen_tools_desc():
    tools_desc = []
    for idx , t in enumerate(tools_info):
        args_desc = []
        for info in t["args"]:
            args_desc.append({
                "name" : info["name"],
                "type":info["type"],
                "description":info["description"]
            })
        args_desc = json.dumps(args_desc,ensure_ascii=False)
        tool_desc = f"\t{idx + 1}.tool_name: {t['name']}\n\ttool_description: {t['description']}\n\targs:{args_desc}"
        tools_desc.append(tool_desc)
    tools_prompt = "\n".join(tools_desc)
    return tools_prompt

if __name__ == "__main__":
    print(gen_tools_desc())