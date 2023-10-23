from pathlib import Path
from typing import Callable, Iterator
from brushit.git import BranchInfo, BranchName, branch_info
import questionary
from rich import print


def branches(root_folder: Path) -> dict[BranchName, BranchInfo]:
    branches = branch_info(working_folder=root_folder)
    return branches


def filter_branch_info(
    branch_info: dict[BranchName, BranchInfo],
    branch_filter: Callable[[BranchInfo], bool],
) -> Iterator[BranchInfo]:
    yield from filter(
        branch_filter,
        branch_info.values(),
    )


def local_only(branch_info: BranchInfo) -> bool:
    return branch_info.upstream is None


def existing_remote_branches(branch_info: BranchInfo) -> bool:
    return branch_info.upstream is not None and branch_info.upstream.exists


def removede_remote_branches(branch_info: BranchInfo) -> bool:
    return branch_info.upstream is not None and not branch_info.upstream.exists


def select_local_only_branches(all_branches: dict[BranchName, BranchInfo]) -> list[int]:
    local_branches = {
        name: branch for name, branch in all_branches.items() if branch.upstream is None
    }

    print(
        "These are branches without a remote. Deleting it here will probably result "
        "in loss of data."
    )

    result = questionary.checkbox(
        "Select the branches you want to delete", choices=list(local_branches.keys())
    ).ask()
    return result
