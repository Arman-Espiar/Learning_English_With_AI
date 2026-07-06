"""Arman Espiar remove folder module"""

from pathlib import Path
import shutil
from dt_utility import (
    display_just_one_error_message,
    ERROR_MESSAGE_MODULE_IS_NOT_EXECUTED_DIRECTLY,
)


def clear_root_folder(folder: str = "./temp") -> None:
    """
    Delete all contents of the specified folder.
    Include files and sub folders
    """

    temp_path = Path(folder)

    if not temp_path.exists():
        return

    for item in temp_path.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


if __name__ == "__main__":
    display_just_one_error_message(
        error_message=ERROR_MESSAGE_MODULE_IS_NOT_EXECUTED_DIRECTLY,
    )
