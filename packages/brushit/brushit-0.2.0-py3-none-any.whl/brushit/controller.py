from pathlib import Path
from textwrap import dedent
from typing import Callable
from brushit import duster
from rich.table import Table
from itertools import chain
import questionary
from brushit.git import BranchInfo, BranchName, delete_branches

from rich import print


def list_branches(root_folder: Path):
    branches = duster.branches(root_folder)
    branch_table(branches)


def dry_cleaner(branches: dict[BranchName, BranchInfo]) -> None:
    print(
        "[bold orange1] These branches will be deleted ![/],",
        " (but not really as you're doing a dry run)",
    )
    branch_table(branches)
    proceed = questionary.confirm(
        "Continue deletion?", default=False, auto_enter=True
    ).ask()
    if proceed:
        print("[bold red]DELETED[/]")
    else:
        print("Doing nothing")


def real_cleaner(branches: dict[BranchName, BranchInfo]) -> None:
    print("[bold orange1] These branches will be deleted ![/]")
    branch_table(branches)
    proceed = questionary.confirm(
        "Continue deletion?", default=False, auto_enter=True
    ).ask()
    if proceed:
        delete_branches(branches)
        print("[bold red]DELETED[/]")
    else:
        print("Doing nothing")


def branch_table(branches: dict[BranchName, BranchInfo], title=None) -> None:
    table = Table(title=title)
    table.add_column("branch name")
    table.add_column("remote")
    table.add_column("remote exists")

    for branch_info in chain(
        duster.filter_branch_info(branches, duster.local_only),
        duster.filter_branch_info(branches, duster.existing_remote_branches),
        duster.filter_branch_info(branches, duster.removede_remote_branches),
    ):
        exists_text = ""
        if branch_info.upstream and branch_info.upstream.exists:
            exists_text = "[bold red]yes[/]"
        if branch_info.upstream and not branch_info.upstream.exists:
            exists_text = "[bold green]no[/]"

        row = [
            f"[bold]{branch_info.name}[/]",
            branch_info.upstream.name if branch_info.upstream else "[bold green]no[/]",
            exists_text,
        ]
        table.add_row(*row)

    assert table.row_count == len(branches)
    print(table)


def clean_branches(
    root_folder: Path, cleaner: Callable[[dict[BranchName, BranchInfo]], None]
):
    branches = duster.branches(root_folder)
    message = """
        [bold orange1]IMPORTANT![/]
        These branches do not have a remote branch. They exist only here.
        So if you delete them they are really gone !
        """

    local_only_branches = select_branches(
        branches, filter=duster.local_only, message=message
    )

    message = """
        These branches are tracking remote branches which don't exist anymore.
        You might want to delete these.
    """
    non_existing_remote = select_branches(
        branches, filter=duster.removede_remote_branches, message=message
    )

    cleaner(
        {br: branches[br] for br in chain(local_only_branches, non_existing_remote)}
    )


def select_branches(
    branches: dict[BranchName, BranchInfo],
    filter: Callable[[BranchInfo], bool],
    message: str,
) -> list[BranchName]:
    br = list(duster.filter_branch_info(branches, filter))

    if len(br) == 0:
        return []

    print(dedent(message))

    selected_branches = questionary.checkbox(
        "Select branches to be deleted.", choices=[branch.name for branch in br]
    ).ask()
    return selected_branches
