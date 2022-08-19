"""Run a chain of analysis tools and linters: isort → black → pylint → bandit."""

from subprocess import run

from git import Repo


def run_with_separator(args):
    """Print a horizontal rule to console and run a subprocess."""
    print("\n", "=" * 80, "\n")
    return run(args, check=False)


if __name__ == "__main__":
    ISORT = run_with_separator(
        [
            "isort",
            "--apply",
            "--atomic",
            "--recursive",
            "--combine-as",
            "--combine-star",
            "--multi-line=3",
            "--trailing-comma",
            "--force-grid-wrap=0",
            "--use-parentheses",
            "--line-width=88",
        ]
    )

    if ISORT.returncode == 0:
        BLACK = run_with_separator(["black", "-l100", "-tpy38", "."])

        if BLACK.returncode == 0:
            run_with_separator(["pylint", "--extension-pkg-whitelist=lxml.etree", "umldotcs"])
            run_with_separator(["bandit", "--recursive", "--format", "txt", "umldotcs"])

    if Repo(".").git.diff("origin/main", ".travis.yml"):
        run_with_separator(["travis", "lint"])
