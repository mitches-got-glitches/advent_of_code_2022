from functools import reduce
from typing import Any, MutableSet

from aoc_helpers import get_input_path


def parse_range(rng: str) -> range:
    """Parse an int range in string format "<start>-<end>" to a range object."""
    start, end = map(int, rng.split("-"))
    return range(start, end + 1)


def union_all(sets: list[MutableSet[Any]]) -> MutableSet[Any]:
    """Union all sets in a list."""
    return reduce(lambda x, y: x.union(y), sets)


if __name__ == "__main__":
    with open(get_input_path()) as f:
        section_assignments = [line.strip() for line in f]

    sets_fully_containing_the_other = 0
    sets_overlapping = 0

    for assignment in section_assignments:
        ranges = map(parse_range, assignment.split(","))
        # Convert to sets of integers so we can use set theory.
        sets: list = [set(rng) for rng in ranges]
        largest_set_size = max(len(s) for s in sets)

        combined_set = union_all(sets)
        # One set is contained within another if the set does not grow when
        # unioning them.
        if len(combined_set) == largest_set_size:
            sets_fully_containing_the_other += 1

        # If sets overlap, then the length of the combined set should be less
        # than the sum of the length of both individual sets.
        if len(combined_set) < sum(len(s) for s in sets):
            sets_overlapping += 1

    # Solution to part 1
    print("Part 1 - Number of assignments which fully contain the other:")
    print(sets_fully_containing_the_other)

    # Solutions to part 2
    print("Part 2 - Number of assignments which overlap each other:")
    print(sets_overlapping)
