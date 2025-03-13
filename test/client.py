from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio
import os
os.environ['OPENAI_API_KEY'] = 'sk-**'
os.environ['OPENAI_BASE_URL'] = '**'
model = ChatOpenAI(model="gpt-4o")

server_params = StdioServerParameters(
    command="python",
    args=["./math_server.py"] 
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            response = await agent.ainvoke({
                "messages": "Calculate (3 + 5) × 12 using MCP tools"
            })
            return response

if __name__ == "__main__":
    print(asyncio.run(run_agent()))