from os import getenv
from textwrap import dedent
import nest_asyncio
import asyncio
from agno.agent import Agent
from agno.models.ollama import Ollama  # Import Ollama model instead of OpenAI
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv
from mcp import StdioServerParameters

# Allow nested event loops
nest_asyncio.apply()

agent_storage_file: str = "../tmp/agents.db"

load_dotenv('../../.env')

github_token = getenv("GITHUB_TOKEN") 
if not github_token:
    raise ValueError("GITHUB_TOKEN environment variable is required")

async def run_server() -> None:
    """Run the GitHub agent server."""
    # Initialize the MCP server


    github_token = getenv("GITHUB_TOKEN") or getenv("GITHUB_ACCESS_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")

    # Create a client session to connect to the MCP server
    async with MCPTools("npx -y @modelcontextprotocol/server-github") as mcp_tools:
        agent = Agent(
            name="MCP GitHub Agent",
            tools=[mcp_tools],
            instructions=dedent(f"""\
                /nothink\n 
                You are a GitHub assistant. Help users explore repositories and their activity.
                - Use headings to organize your responses
                instructions=[
                "Use your tools to answer questions about the repo: `skjortan23/sec-t-jopaerdy`",
                "Do not create any issues or pull requests unless explicitly asked to do so",
            """),
            model=Ollama(
                host="http://ai:11434",
                id="qwen2.5"
            ),  # Use Ollama with qwen3 model
            storage=SqliteAgentStorage(
                table_name="basic_agent",
                db_file=agent_storage_file,
                auto_upgrade_schema=True,
            ),
            add_history_to_messages=True,
            num_history_responses=3,
            add_datetime_to_instructions=True,
            markdown=True,
        )
        playground = Playground(agents=[agent])
        app = playground.get_app()

        # Serve the app while keeping the MCPTools context manager alive
        serve_playground_app(app)


if __name__ == "__main__":
    asyncio.run(run_server())