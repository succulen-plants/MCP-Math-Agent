# MCP 工具集成示例项目


## 项目简介

本项目展示了如何使用 Machine Conversation Protocol (MCP) 将外部工具与大语言模型 (LLM) 集成，实现智能代理的自动工具发现和调用。项目通过一个简单的数学计算示例，演示了 MCP 的核心功能和工作流程。


## 功能特点
- 基于 MCP 协议的工具注册与发现
- 使用 LangChain 和 LangGraph 构建 ReAct 代理
- 支持大语言模型自动选择和调用合适的工具
- 详细的执行跟踪和可视化
- 支持本地和远程工具服务部署

.
├── README.md                 # 项目说明文档
├── test/                     # 测试和示例代码
│   ├── math_server.py        # MCP 数学工具服务器
│   ├── client.py             # 基础客户端示例
│   ├── verbose_client.py     # 带详细日志的客户端
│   └── remote_client.py      # 远程服务连接示例
└── requirements.txt          # 项目依赖


## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行示例

1. 基础示例:

```bash
python test/client.py
```

2. 带详细日志的示例:

```bash
python test/verbose_client.py
```

## 核心组件

### 1. MCP 服务器 (math_server.py)

数学服务器提供两个基本工具：加法和乘法。

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MathService")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Execute arithmetic addition operation"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Execute arithmetic multiplication operation""" 
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 2. MCP 客户端 (client.py)

客户端连接到 MCP 服务器，加载工具，并创建 ReAct 代理来执行任务。

```python
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
```

## 工作流程

1. 客户端启动 MCP 服务器进程
2. 客户端连接到服务器并初始化会话
3. 客户端发现并加载可用工具
4. 创建 ReAct 代理，将工具信息提供给大语言模型
5. 代理接收用户请求并开始思考-行动-观察循环:
   - 思考：分析问题，决定使用哪个工具
   - 行动：调用选定的工具
   - 观察：分析工具执行结果
6. 代理生成最终回答并返回给用户

## 自定义和扩展

### 添加新工具

只需在 `math_server.py` 中添加新的工具函数并使用 `@mcp.tool()` 装饰器注册:

```python
@mcp.tool()
def divide(a: float, b: float) -> float:
    """Execute arithmetic division operation"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### 连接到远程服务器

修改客户端代码以连接到远程 MCP 服务:

```python
from mcp.client.http import http_client

async def run_agent():
    async with http_client("https://your-mcp-server.com/api") as session:
        # 其余代码保持不变
        # ...
```

## 调试和跟踪

使用 `verbose_client.py` 查看详细的执行跟踪，包括:

- 可用工具列表
- 每一步的思考过程
- 工具调用和结果
- 最终响应

## 运行输出
Processing request of type ListToolsRequest
可用工具:
- add: Execute arithmetic addition operation
- multiply: Execute arithmetic multiplication operation

开始执行代理调用...

INFO:httpx:HTTP Request: POST https://** "HTTP/1.1 200 OK"
Processing request of type CallToolRequest
Processing request of type CallToolRequest
INFO:httpx:HTTP Request: POST https://** "HTTP/1.1 200 OK"

===== ReAct 执行跟踪 =====

步骤 1: 思考
模型思考并决定:

步骤 2: 工具调用
调用工具: multiply
输入: {'a': 8, 'b': 12}
输出: content='96' name='multiply' id='44f7af32-dbd5-4ab4-ad37-b45f9da0cac9' tool_call_id='call_ncJW4OzrgGBEPya0gHhRJ6cg'

步骤 3: 工具调用
调用工具: multiply
输入: {'a': 8, 'b': 12}
输出: content='96' name='multiply' id='44f7af32-dbd5-4ab4-ad37-b45f9da0cac9' tool_call_id='call_ncJW4OzrgGBEPya0gHhRJ6cg'

步骤 4: 思考
模型思考并决定: The result of \((3 + 5) \times 12\) is 96.

最终响应:
The result of \((3 + 5) \times 12\) is 96.

## 技术栈

- **MCP**: 工具注册、发现和调用协议
- **LangChain**: LLM 和工具集成框架
- **LangGraph**: ReAct 代理构建
- **OpenAI API**: 大语言模型服务

## 许可证

MIT

## 贡献

欢迎提交 Issues 和 Pull Requests!
