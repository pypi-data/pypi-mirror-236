"""
Helpers for colored output with the Rich package.
"""
from functools import lru_cache
from sys import exit
from typing import Any, Union

from rich.console import Console
from rich.panel import Panel
from rich.pretty import pprint
from rich.text import Text
from trongrid_extractoor.helpers.color_picker import ColorPicker

console = Console(color_system='256')
color_picker = ColorPicker()


def print_error_and_exit(error_msg: str) -> None:
    txt = Text('').append('ERROR', style='bright_red').append(f": {error_msg}")
    console.print(txt)
    exit(1)


def print_section_header(msg: Union[str, Text]) -> None:
    msg = str(msg)
    console.print(Panel(msg, style='reverse', width=max(40, len(msg) + 4)))


def pretty_print(obj: Any) -> None:
    """Thin wrapper around rich.pretty.pprint()."""
    pprint(obj, expand_all=True, indent_guides=False)
