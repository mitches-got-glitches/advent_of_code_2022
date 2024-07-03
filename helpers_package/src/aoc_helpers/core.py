import inspect
import itertools
from pathlib import Path
from typing import Any

from .config import settings


def split_list(lst: list, val: Any):
    return [
        list(group) for k, group in itertools.groupby(lst, lambda x: x == val) if not k
    ]


def get_input_path():
    calling_module = inspect.stack()[1].filename
    input_file = "test_input.txt" if settings.test else "input.txt"
    return Path(calling_module).with_name(input_file)
