# GitHub Security Analysis Tool

A tool that automatically analyzes GitHub pull requests for security vulnerabilities and provides recommendations.

## Overview

This project uses AI agents to:
1. Analyze pull requests in a GitHub repository
2. Identify potential security risks
3. Generate security recommendations
4. Comment on pull requests with findings

## Components

- **Analysis GitHub Agent**: Examines pull request changes for security issues
- **Ticket Agent**: Creates comments on pull requests with security recommendations
- **Agent UI**: Modern chat interface for interacting with the agents

## Setup

### Prerequisites

- Python 3.8+
- Node.js 14.21.3+
- Ollama server running
- GitHub access token

### Installation

1. Clone the repository
2. Create a `.env` file in the root directory with:
   ```
   GITHUB_TOKEN=your_github_token
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install UI dependencies:
   ```bash
   cd agent-ui
   pnpm install
   ```

## Usage

### Running the Security Analysis

```bash
python src/minimal_github.py
```

This will:
- Fetch the latest pull request from the configured repository
- Analyze it for security vulnerabilities
- Generate a security report
- Post findings as a comment on the pull request

### Running the Agent UI

```bash
cd agent-ui
pnpm dev
```

Access the UI at http://localhost:3000

## Configuration

Edit `src/minimal_github.py` to configure:
- Target repository
- Model settings
- Agent instructions

## License

This project is licensed under the MIT License.
