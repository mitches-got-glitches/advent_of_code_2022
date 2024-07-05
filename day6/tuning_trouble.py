import collections
import re
from itertools import islice

from aoc_helpers import get_input_path


def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = collections.deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def get_markers(signal: str, n: int) -> list[str]:
    """Get markers from signal where a marker is n-distinct consecutive chars."""
    return [
        "".join(window) for window in sliding_window(signal, n) if len(set(window)) == n
    ]


def get_marker_end_positions(signal: str, n: int) -> list[int]:
    """Return characters processed at each point a marker is detected."""
    return [re.search(marker, signal).end() for marker in get_markers(signal, n)]


if __name__ == "__main__":
    with open(get_input_path()) as f:
        signal = f.read().rstrip("\n")

    # Solution to part 1
    print("The first start-of-packet marker appears after:")
    print(get_marker_end_positions(signal, n=4)[0])
    # Solution to part 2
    print("The first start-of-message marker appears after:")
    print(get_marker_end_positions(signal, n=14)[0])
