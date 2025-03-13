import asyncio
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp")
logger.setLevel(logging.DEBUG)

# OpenAI 配置
import os
os.environ['OPENAI_API_KEY'] = 'sk-**'
os.environ['OPENAI_BASE_URL'] = '**'
model = ChatOpenAI(model="gpt-4o", temperature=0)

# 自定义回调
class ReActTraceHandler(BaseCallbackHandler):
    def __init__(self):
        self.steps = []
        self.current_step = {"type": None}
        
    def on_llm_start(self, serialized, prompts, **kwargs):
        self.current_step = {"type": "思考", "input": prompts[0][:100] + "..."}
        
    def on_llm_end(self, response, **kwargs):
        self.current_step["output"] = response.generations[0][0].text
        self.steps.append(self.current_step)
        
    def on_tool_start(self, serialized, input_str, **kwargs):
        self.current_step = {"type": "工具调用", "tool": serialized["name"], "input": input_str}
        
    def on_tool_end(self, output, **kwargs):
        self.current_step["output"] = output
        self.steps.append(self.current_step)
        
    def print_trace(self):
        print("\n===== ReAct 执行跟踪 =====")
        for i, step in enumerate(self.steps):
            print(f"\n步骤 {i+1}: {step['type']}")
            if step['type'] == "思考":
                print(f"模型思考并决定: {step['output']}")
            else:
                print(f"调用工具: {step['tool']}")
                print(f"输入: {step['input']}")
                print(f"输出: {step['output']}")

server_params = StdioServerParameters(
    command="python",
    args=["./math_server.py"] 
)

async def run_agent():
    trace_handler = ReActTraceHandler()
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            
            print("可用工具:")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")
            
            agent = create_react_agent(model, tools)
            
            print("\n开始执行代理调用...\n")
            response = await agent.ainvoke(
                {"messages": "Calculate (3 + 5) × 12 using MCP tools"},
                config={"callbacks": [trace_handler]}
            )
            
            trace_handler.print_trace()
            
            print("\n最终响应:")
            print(response["messages"][-1].content)
            return response

if __name__ == "__main__":
    asyncio.run(run_agent()) 