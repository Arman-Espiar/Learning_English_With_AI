"""
Dariush Tasdighi ReadKey Module

Cross-platform ReadKey for Windows / Linux / macOS
"""

from __future__ import annotations

import os
import sys
import dt_utility as utility

from typing import (
    Final,
    Optional,
)

VERSION: Final[str] = "1.0.0"
IS_WINDOWS: Final[bool] = sys.platform == "win32"

if IS_WINDOWS:
    import msvcrt
else:
    import tty
    import select
    import termios


class Keys:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    TAB = "\t"
    ESC = "ESC"
    ENTER = "\r"
    BACKSPACE = "\b"


def read_key(timeout: Optional[int] = None) -> Optional[str]:
    """
    Read one key.

    timeout:
        None -> Wait forever.
        0    -> Non-blocking.
        n    -> Wait n milliseconds.

    Returns:
        str | None
    """

    if not IS_WINDOWS:
        return _read_key_unix(timeout=timeout)
    else:
        return _read_key_windows(timeout=timeout)


def _read_key_windows(timeout: Optional[int]) -> Optional[str]:
    """
    Read key in windows
    """

    if timeout is None:
        while not msvcrt.kbhit():
            pass
    elif timeout == 0:
        if not msvcrt.kbhit():
            return None
    else:
        import time

        end = time.monotonic() + timeout / 1000
        while time.monotonic() < end:
            if msvcrt.kbhit():
                break
            time.sleep(0.001)
        else:
            return None

    ch = msvcrt.getwch()

    if ch == "\x03":
        raise KeyboardInterrupt

    if ch in ("\x00", "\xe0"):
        ch2 = msvcrt.getwch()

        return {
            "H": Keys.UP,
            "P": Keys.DOWN,
            "K": Keys.LEFT,
            "M": Keys.RIGHT,
        }.get(ch2, ch2)

    if ch == "\x1b":
        return Keys.ESC

    return ch


# def _read_key_unix(timeout: Optional[int]) -> Optional[str]:
#     """
#     Read key in unix
#     """

#     fd = sys.stdin.fileno()
#     old = termios.tcgetattr(fd)

#     try:
#         tty.setraw(fd)

#         if timeout is None:
#             ready = True
#         else:
#             sec = timeout / 1000
#             ready, _, _ = select.select([sys.stdin], [], [], sec)
#             ready = bool(ready)

#         if not ready:
#             return None

#         ch = sys.stdin.read(1)

#         if ch == "\x03":
#             raise KeyboardInterrupt

#         if ch == "\x1b":
#             ready, _, _ = select.select([sys.stdin], [], [], 0.0001)

#             if ready:
#                 seq = sys.stdin.read(2)

#                 return {
#                     "[A": Keys.UP,
#                     "[B": Keys.DOWN,
#                     "[C": Keys.RIGHT,
#                     "[D": Keys.LEFT,
#                 }.get(seq, Keys.ESC)

#             return Keys.ESC

#         return ch

#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _read_key_unix(timeout: Optional[int]) -> Optional[str]:
    """
    Read key in unix
    """

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)

        if timeout is None:
            ready = True
        else:
            sec = timeout / 1000
            r, _, _ = select.select([fd], [], [], sec)
            ready = bool(r)

        if not ready:
            return None

        b = os.read(
            fd, 1
        )  # raw read on fd -- NOT sys.stdin.read (buffering breaks select)

        if b == b"\x03":
            raise KeyboardInterrupt

        if b == b"\x1b":
            r, _, _ = select.select([fd], [], [], 0.05)  # 50ms, safe for ssh/tmux lag

            if not r:
                return Keys.ESC

            seq = b""
            while True:
                seq += os.read(fd, 1)
                r, _, _ = select.select([fd], [], [], 0.005)
                if not r:
                    break

            return {
                b"[A": Keys.UP,
                b"[B": Keys.DOWN,
                b"[C": Keys.RIGHT,
                b"[D": Keys.LEFT,
            }.get(seq, Keys.ESC)

        if b[0] >= 0x80:  # multi-byte utf-8 (فارسی و...)
            extra = (
                3 if b[0] >= 0xF0 else 2 if b[0] >= 0xE0 else 1 if b[0] >= 0xC0 else 0
            )
            for _ in range(extra):
                b += os.read(fd, 1)
            try:
                return b.decode("utf-8")
            except UnicodeDecodeError:
                return None

        return b.decode(encoding="ascii", errors="replace")

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


if __name__ == "__main__":
    utility.display_just_one_error_message(
        message=utility.ERROR_MESSAGE_MODULE_IS_NOT_EXECUTED_DIRECTLY,
    )
