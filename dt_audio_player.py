"""
Dariush Tasdighi Audio Player Module
"""

from __future__ import annotations

import pygame
import dt_utility as utility

from typing import (
    Final,
    Optional,
)

from dt_read_key import (
    Keys,
    read_key,
)

from rich import print
from pathlib import Path
from dt_pathlib import check_file

VERSION: Final[str] = "1.0.0"

MUSIC_END: Final[int] = pygame.USEREVENT + 1


def play_audio_file(
    filename: Optional[str],
    notify: bool = False,
    controllable: bool = False,
    deletes_path: str = "deletes",
    favorites_path: str = "favorites",
) -> None:
    """
    Play audio file
    """
    #NEW
    try:
        audio_file_path_object = check_file(
            file_path=filename,
            file_extension=".mp3",
        )

        audio_file_path: str = str(audio_file_path_object.resolve())

        if notify:
            print(f"Playing: [green]{audio_file_path}[/green]", end=" ")

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(MUSIC_END)
        pygame.mixer.music.load(filename=audio_file_path)
        pygame.mixer.music.play()

        if not controllable:
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                # Note: The below code does not work properly!
                # pygame.event.wait()
        else:
            is_paused: bool = False

            while True:
                # Press 'SPACE': pause / resume | 'l': Add to Favorites | 'DEL': Move to deletes | 'ESC': skip"
                choise: Optional[str] = read_key(timeout=100)

                for event in pygame.event.get():
                    if event.type == MUSIC_END:
                        pygame.event.clear(MUSIC_END)
                        return

                match choise:
                    case " ":
                        if is_paused:
                            is_paused = False
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                            is_paused = True

                    case Keys.ESC:
                        pygame.mixer.music.stop()
                        pygame.event.clear(MUSIC_END)
                        break

                    case "l":
                        parent_path_object: Path = audio_file_path_object.parent.parent
                        favorites_path_object: Path = parent_path_object / favorites_path
                        favorites_path_object.mkdir(exist_ok=True)
                        target_path: Path = (
                            favorites_path_object / audio_file_path_object.name
                        )
                        audio_file_path_object.copy(target=target_path)
    #NEW
    finally:
        pygame.mixer.music.unload()
        pygame.quit()

if __name__ == "__main__":
    utility.display_just_one_error_message(
        message=utility.ERROR_MESSAGE_MODULE_IS_NOT_EXECUTED_DIRECTLY,
    )
