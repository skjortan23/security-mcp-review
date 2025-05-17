import os
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.github import GithubTools
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv

from src.tools.github_extra_tools import GithubExtraTools

model = Ollama(host="http://ai:11434",id="qwen3",options={"temperature": 0.1})

load_dotenv("../.env")
github_token = os.getenv("GITHUB_TOKEN")
repo_name = "skjortan23/sec-t-jopaerdy"

analysis_github_agent = Agent(
    model=model,
    instructions=[
        "/nothink\n",
        f"Use your tools to perform actions and answer questions about the repo: {repo_name}",
        "Always work on the pull request with the highest number.",
        f"you are using: model={model.id}"
    ],
    name="MCP GitHub Agent",

    tools=[
        GithubTools(access_token=github_token,
                    get_pull_requests=True,
                    get_pull_request=True,
                    get_pull_request_changes=True,
                    ),
        ],
)

ticketAgent = Agent(
    model=model,
    name="Ticket Agent",
    show_tool_calls=True,
    instructions=[
        "/nothink\n",
        f"Use your tools to perform actions in the repo: {repo_name}",
        "Always work on the pull request with the highest number.",
        f"you are using: model={model.id}"
    ],
    tools=[
        GithubTools(access_token=github_token,
                    get_pull_requests=True,
                    ),
        GithubExtraTools(access_token=github_token)
        ],
)

res = analysis_github_agent.run(
    "/nothink \n" +
    "Instructions: \n" +
    "1. Get the latest pull request id then get the details of the pull request.\n" +
    "2. Make note of anything that is a security risk and that could be used to exploit the system. \n"
    , markdown=True)

content = res.content.split("</think>")[1]

ticketAgent.print_response(
    "/nothink \n" +
    "Goal: based on the content create 1 (one) pull request comment with security issues on the latest pull request. \n" +
    "Based on the content add your recommendations whether it should be merged or not."
    "\n" +
    f"content: {content}\n"
    , markdown=True)
