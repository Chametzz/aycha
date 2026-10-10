import subprocess

from domain.errors.git_error import GitError
from domain.services.git_service import GitService


class GitServiceImpl(GitService):
    def get_staged_diff(self) -> str:
        return self._run_command(["git", "diff", "--staged"]).stdout.strip()

    def execute_commit(self, message: str) -> None:
        if not message or not message.strip():
            raise GitError("Commit message cannot be empty.")
        self._run_command(["git", "commit", "-m", message])

    def _run_command(self, command: list[str]) -> subprocess.CompletedProcess[str]:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )
            return result
        except FileNotFoundError:
            raise GitError("Git is not installed or not found in PATH.")
        except subprocess.CalledProcessError as e:
            error_details = e.stderr.strip() if e.stderr else e.stdout
            raise GitError(f"Git command failed: {error_details}")
