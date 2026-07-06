"""
Dariush Tasdighi Custom 'pathlib' Package Module
"""

from __future__ import annotations

from typing import (
    Final,
    Optional,
)

from pathlib import Path
import dt_utility as utility

VERSION: Final[str] = "1.0.0"


def check_path(path: Optional[str]) -> Path:
    """
    Check path
    """

    message: str

    if path == None:
        message = "Path is None"
        raise Exception(message)

    path = path.strip()

    if not path:
        message = "Path is empty"
        raise Exception(message)

    path_object = Path(path).resolve()

    if not path_object.exists():
        message = f"The '{path}' path not found"
        raise Exception(message)

    if not path_object.is_dir():
        message = f"The '{path}' path is file, not directory"
        raise Exception(message)

    return path_object


def check_file(file_path: Optional[str], file_extension: Optional[str]) -> Path:
    """
    Check file path
    """

    message: str

    if file_path == None:
        message = "Filename is None"
        raise Exception(message)

    file_path = file_path.strip()

    if not file_path:
        message = "Filename is empty"
        raise Exception(message)

    file_path_object = Path(file_path).resolve()

    if not file_path_object.exists():
        message = f"The '{file_path}' path not found"
        raise Exception(message)

    if not file_path_object.is_file():
        message = f"The '{file_path}' path is directory, not file"
        raise Exception(message)

    if file_extension:
        file_extension = file_extension.strip().lower()
        if not file_path_object.name.lower().endswith(file_extension):
            message = (
                f"The '{file_path}' file does not have '{file_extension}' extension"
            )
            raise Exception(message)

    return file_path_object


if __name__ == "__main__":
    utility.display_just_one_error_message(
        message=utility.ERROR_MESSAGE_MODULE_IS_NOT_EXECUTED_DIRECTLY,
    )
