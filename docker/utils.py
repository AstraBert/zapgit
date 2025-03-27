from llama_index.tools.mcp import McpToolSpec, BasicMCPClient
from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult, ToolCall, AgentWorkflow
from llama_index.core.workflow import Context
from llama_index.llms.groq import Groq

SYSTEM_PROMPT = """\
You are a GitHub issue creator AI assistant.
Your job is to create a GitHub issue in a given Github repository, report what you did sending a message to a specified channel in a Discord server and schedule a reminder event to fix the issue on a specified date on Google Calendar.
"""
with open("/run/secrets/groq_key", "r") as f:
    groq_api_key = f.read()
f.close() 

llm = Groq(model="llama-3.3-70b-versatile", api_key=groq_api_key)

async def get_agent(tools: McpToolSpec):
    tools = await tools.to_tool_list_async()
    toolnames = [tool.metadata.name for tool in tools]
    print(toolnames)
    if not (set(['discord_send_channel_message', 'google_calendar_quick_add_event', 'github_create_issue', 'github_create_pull_request', 'github_create_comment']).issubset(toolnames) or set(['discord_send_channel_message_', 'google_calendar_quick_add_event_', 'github_create_issue', 'github_create_pull_request', 'github_create_comment']).issubset(toolnames)):
        return f"Your Zapier MCP must contain the following actions: {', '.join(['discord_send_channel_message', 'google_calendar_quick_add_event', 'github_create_issue', 'github_create_pull_request', 'github_create_comment'])} (or 'discord_send_channel_message_', 'google_calendar_quick_add_event_' as alternatives for Discord and Google Calendar)"
    agent = FunctionAgent(
        name="Agent",
        description="An agent that can review pull requests and send messages on Discord",
        tools=tools,
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
    )
    workflow = AgentWorkflow(agents=[agent], root_agent="Agent")
    return workflow

async def handle_user_message(
    message_content: str,
    agent: AgentWorkflow,
    agent_context: Context,
    verbose: bool = False,
):
    handler = agent.run(message_content, ctx=agent_context)
    process = ""
    async for event in handler.stream_events():
        if verbose and type(event) == ToolCall:
            process+=f"- Calling tool `{event.tool_name}` with arguments: {event.tool_kwargs}\n"
        elif verbose and type(event) == ToolCallResult:
            process+=f"- Tool `{event.tool_name}` returned: {event.tool_output}\n"
    response = await handler
    return str(response), process

async def run_mcp(mcp_url: str, user_input: str):
    mcp_client = BasicMCPClient(mcp_url)
    mcp_tool = McpToolSpec(client=mcp_client)
    agent = await get_agent(mcp_tool)
    if type(agent) == str:
        return agent, agent
    else:
        agent_context = Context(agent)
        response, process = await handle_user_message(user_input, agent, agent_context, verbose=True)
        return response, process

