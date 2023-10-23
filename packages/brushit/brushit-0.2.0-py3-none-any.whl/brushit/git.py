import subprocess
from dataclasses import dataclass
from pathlib import Path


class GitException(Exception):
    ...


@dataclass
class Upstream:
    name: str
    exists: bool


@dataclass
class BranchInfo:
    name: str
    upstream: Upstream | None
    working_folder: Path


def run_subprocess(*args: str, working_folder: Path) -> list[str]:
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=working_folder,
    )
    if not result.returncode == 0:
        raise GitException(result)
    to_string = result.stdout.decode("utf-8")
    lines = [line.strip('"') for line in to_string.split("\n") if not line == ""]
    return lines


def git(*args: str, working_folder: Path) -> list[str]:
    """command runnig the git cli."""
    return run_subprocess("git", *args, working_folder=working_folder)


def git_branch(working_folder: Path) -> list[str]:
    # git branch --format="%(refname:short),%(upstream),%(upstream:track,nobracket)"
    return git(
        "branch",
        '--format="%(refname:short) , %(upstream) , %(upstream:track,nobracket)"',
        working_folder=working_folder,
    )


def _parse(line: str, working_folder: Path) -> BranchInfo:
    items = line.split(" , ")
    if not len(items) == 3:
        raise ValueError(
            (
                "Incoming branch info not in correct format. "
                f"Expected three fields separated by comma, but got {line}"
            )
        )

    name = items[0].strip()
    remote_name = items[1].strip()

    is_gone = items[2].strip()

    if is_gone == "gone":
        upstream_exists = False
    else:
        # This is a bit dangerous, but still works.
        # both branch infos will result in an upstream_exists==True,
        # while only the first line has a remote tracking branch
        #
        # main,refs/remotes/origin/main,
        # some_repo,,  <-- this repo has no remote name, but also no "gone"
        upstream_exists = True

    upstream = None
    if remote_name:
        upstream = Upstream(remote_name, upstream_exists)

    return BranchInfo(name, upstream, working_folder=working_folder)


BranchName = str


def branch_info(working_folder: Path | None) -> dict[BranchName, BranchInfo]:
    branch_info = {}
    if working_folder is None:
        working_folder = Path.cwd()

    # prune it first to sync remote with local.
    git("fetch", "-p", working_folder=working_folder)
    for info in git_branch(working_folder):
        if info.strip() == "":
            continue
        bi = _parse(info, working_folder)
        branch_info[bi.name] = bi
    return branch_info


def delete_branches(branches: dict[BranchName, BranchInfo]):
    for branch in branches.values():
        git("branch", "-D", branch.name, working_folder=branch.working_folder)
