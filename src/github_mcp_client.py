#!/usr/bin/env python3
"""
Client script for the GitHub Security MCP Server.
This script connects to the MCP server running on port 8080 and calls the security analysis endpoint.
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional
from urllib.parse import urlparse

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

async def run_security_analysis(
    github_token: str,
    repo_name: str,
    pr_number: Optional[int] = None,
    server_url: str = "http://localhost:8080/sse"
) -> Dict[str, Any]:
    """
    Connect to the MCP server and run a security analysis.

    Args:
        github_token: GitHub access token
        repo_name: Repository name in the format "owner/repo"
        pr_number: Optional pull request number. If not provided, the latest PR will be analyzed
        server_url: URL of the MCP server's SSE endpoint

    Returns:
        The analysis results from the server
    """
    # Connect to the MCP server using SSE
    async with sse_client(server_url) as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            # Initialize the session
            await session.initialize()

            # Call the github_security_analysis tool
            call_result = await session.call_tool(
                "github_security_analysis",
                {
                    "github_token": github_token,
                    "repo_name": repo_name,
                    "pr_number": pr_number
                }
            )
            # Convert the CallToolResult object to a dictionary
            return call_result.model_dump()

async def main():
    """Main function to run the client."""
    # Get the GitHub token from the environment
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        return

    # Repository to analyze
    repo_name = "skjortan23/sec-t-jopaerdy"  # Replace with your repository
    server_url = "http://localhost:8080/sse"

    print(f"Connecting to MCP server at {server_url}...")
    print(f"Running security analysis on {repo_name}...")

    try:
        # Run the security analysis
        print("Calling run_security_analysis...")
        result = await run_security_analysis(github_token, repo_name, server_url=server_url)

        # Print the results
        print("\nSecurity Analysis Result:")
        print(json.dumps(result, indent=2))

        # Extract the actual result from the response
        if 'content' in result and result['content'] and 'text' in result['content'][0]:
            # Parse the JSON string in the text field
            actual_result = json.loads(result['content'][0]['text'])

            # Print a summary
            print("\nSummary:")
            print(f"Repository: {actual_result['repo_name']}")
            print(f"PR Number: {actual_result['pr_number'] or 'Latest'}")
            print(f"Analysis length: {len(actual_result['analysis'])} characters")
            print(f"Comment length: {len(actual_result['comment'])} characters")
        else:
            print("\nCould not extract result details from the response.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print("Make sure the MCP server is running on port 8080 with SSE transport.")

if __name__ == "__main__":
    asyncio.run(main())
