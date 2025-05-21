#!/usr/bin/env python3
"""
Test script for the GitHub Security MCP Server.
This script demonstrates how to use the MCP server to analyze GitHub pull requests.
"""

import asyncio
import json
import os
import subprocess
import sys
import time

from mcp import MCPClient

# Path to the MCP server script
MCP_SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), "mcp-servers/github_security_mcp_server.py")

async def main():
    """Run the test for the GitHub Security MCP Server."""
    # Start the MCP server in a separate process
    print("Starting the GitHub Security MCP Server...")
    server_process = subprocess.Popen(
        [sys.executable, MCP_SERVER_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Give the server a moment to start up
    time.sleep(2)

    try:
        # Connect to the MCP server
        print("Connecting to the MCP server...")
        async with MCPClient() as client:
            # Get the GitHub token from the environment
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                print("Error: GITHUB_TOKEN environment variable is not set.")
                return

            # Repository to analyze
            repo_name = "skjortan23/sec-t-jopaerdy"  # Replace with your repository

            # Call the github_security_analysis tool
            print(f"Running security analysis on {repo_name}...")
            result = await client.call(
                "github_security_analysis",
                {
                    "github_token": github_token,
                    "repo_name": repo_name,
                    # Optionally specify a PR number
                    # "pr_number": 1
                }
            )

            print("\nSecurity Analysis Result:")
            print(json.dumps(result, indent=2))

    finally:
        # Terminate the server process
        print("\nTerminating the MCP server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    asyncio.run(main())
