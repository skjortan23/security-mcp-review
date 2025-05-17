import json
from typing import Optional
from agno.tools import Toolkit
from agno.utils.log import log_debug, logger

try:
    from github import Auth, Github, GithubException
except ImportError:
    raise ImportError("`PyGithub` not installed. Please install using `pip install pygithub`")

class GithubExtraTools(Toolkit):
    def __init__(self, access_token: Optional[str] = None, **kwargs):
        super().__init__(name="github-extra", **kwargs)
        self.access_token = access_token
        self.register(self.create_pull_request_comment)


    def create_pull_request_comment(self, repo: str, pr_number: int, comment: str) -> str:
        """Create a comment on a GitHub pull request.

        This function uses the PyGithub library to interact add a comment to a pull request.

        Args:
            repo (str): The name of the repo in format "owner/repo_name".
            pr_number (int): The pull request number.
            comment (str): The comment text to add to the pull request.

        Returns:
            A JSON-formatted string containing the comment details or an error message.
        """
        try:
            auth = Auth.Token(self.access_token)
            g = Github(auth=auth)
            repo_obj = g.get_repo(repo)
            pull_request = repo_obj.get_pull(pr_number)
            
            # Create a general comment (issue comment) on the pull request
            created_comment = pull_request.create_issue_comment(comment)
            
            # Return comment details as JSON
            comment_info = {
                "id": created_comment.id,
                "body": created_comment.body,
                "created_at": created_comment.created_at.isoformat(),
                "url": created_comment.html_url,
                "user": created_comment.user.login
            }
            return json.dumps(comment_info)
        except GithubException as e:
            logger.error(f"GitHub API error: {e}")
            return "Error: " + str(e)
        except Exception as e:
            logger.error(f"Error: {e}")
            return "Error: " + str(e)


