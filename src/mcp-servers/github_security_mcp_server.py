from fastmcp import FastMCP
import os
import sys
from typing import Dict, Any, Optional

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the wrapper function from minimal_github.py
from src.minimal_github import run_security_analysis

# Create the MCP server
mcp = FastMCP(name="GitHubSecurityMCPServer")

@mcp.tool()
def github_security_analysis(github_token: str, repo_name: str, pr_number: Optional[int] = None) -> Dict[str, Any]:
    """
    Run a security analysis on a GitHub pull request and generate a comment.

    Args:
        github_token: GitHub access token
        repo_name: Repository name in the format "owner/repo"
        pr_number: Optional pull request number. If not provided, the latest PR will be analyzed

    Returns:
        A dictionary containing the analysis results and comment
    """
    # Call the wrapper function from minimal_github.py
    return run_security_analysis(github_token, repo_name, pr_number)

if __name__ == "__main__":
    # Run the server on SSE transport on port 8080
    mcp.run(transport="sse", port=8080)
