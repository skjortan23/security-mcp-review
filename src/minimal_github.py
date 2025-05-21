import os
from typing import Dict, Any, Optional
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.github import GithubTools
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv

from src.tools.github_extra_tools import GithubExtraTools

def run_security_analysis(github_token: str, repo_name: str, pr_number: Optional[int] = None) -> Dict[str, Any]:
    """
    Run a security analysis on a GitHub pull request and generate a comment.
    This is a wrapper function that encapsulates the main functionality of minimal_github.py.

    Args:
        github_token: GitHub access token
        repo_name: Repository name in the format "owner/repo"
        pr_number: Optional pull request number. If not provided, the latest PR will be analyzed

    Returns:
        A dictionary containing the analysis results and comment
    """
    # Initialize the model
    model = Ollama(host="http://ai:11434", id="qwen3", options={"temperature": 0.1})

    # Create the analysis agent
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

    # Create the ticket agent
    ticket_agent = Agent(
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

    # Run the analysis
    if pr_number:
        prompt = (
            "/nothink \n" +
            "Instructions: \n" +
            f"1. Get the details of pull request #{pr_number}.\n" +
            "2. Make note of anything that is a security risk and that could be used to exploit the system. \n"
        )
    else:
        prompt = (
            "/nothink \n" +
            "Instructions: \n" +
            "1. Get the latest pull request id then get the details of the pull request.\n" +
            "2. Make note of anything that is a security risk and that could be used to exploit the system. \n"
        )

    res = analysis_github_agent.run(prompt, markdown=True)

    # Extract the content after </think>
    analysis = res.content.split("</think>")[1] if "</think>" in res.content else res.content

    # Generate the comment
    comment_prompt = (
        "/nothink \n" +
        "Goal: based on the content create 1 (one) pull request comment with security issues on the latest pull request. \n" +
        "Based on the content add your recommendations whether it should be merged or not."
        "\n" +
        f"content: {analysis}\n"
    )

    comment_res = ticket_agent.run(comment_prompt, markdown=True)
    comment = comment_res.content

    return {
        "analysis": analysis,
        "comment": comment,
        "repo_name": repo_name,
        "pr_number": pr_number
    }

# Main execution when script is run directly
if __name__ == "__main__":
    load_dotenv("../.env")
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = "skjortan23/sec-t-jopaerdy"

    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")

    result = run_security_analysis(github_token, repo_name)

    print("Analysis:")
    print(result["analysis"])
    print("\nComment:")
    print(result["comment"])
