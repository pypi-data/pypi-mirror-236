"""some cli"""
from pathlib import Path
from pydantic import BaseModel, DirectoryPath, ValidationError
import tyro
from brushit import controller
from rich import print


class List(BaseModel):
    root_folder: DirectoryPath = Path.cwd()
    """The repo root folder."""

    def main(self):
        controller.list_branches(self.root_folder)


class Clean(BaseModel):
    """Clean your repo branches."""

    dry_run: bool = True

    root_folder: DirectoryPath = Path.cwd()
    """The repo root folder."""

    def main(self):
        if self.dry_run:
            cleaner = controller.dry_cleaner
        else:
            cleaner = controller.real_cleaner
        controller.clean_branches(self.root_folder, cleaner=cleaner)


if __name__ == "__main__":
    try:
        out = tyro.cli(Clean | List)  # type: ignore
        out.main()
    except ValidationError as err:
        print(err)
