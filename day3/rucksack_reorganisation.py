import string
from functools import reduce
from itertools import chain, zip_longest
from typing import Any, Collection, Iterable, List, MutableSet

from aoc_helpers import get_input_path


def get_intersection(x: Collection[Any], y: Collection[Any]) -> MutableSet[Any]:
    """Get the set intersection of two collections."""
    return set(x).intersection(set(y))


# Use zip_longest from itertools to chunk the list up into groups of 3.
def group_elements(iterable: Iterable, n: int) -> List[List[int]]:
    """Group elements of a list into lists of size n."""
    return list(zip_longest(*[iter(iterable)] * n))


if __name__ == "__main__":
    # View file contents.
    with open(get_input_path()) as f:
        rucksacks = [line.strip() for line in f]

    lower_alphabet = list(string.ascii_lowercase)
    upper_alphabet = list(string.ascii_uppercase)
    priority_map = dict(zip(lower_alphabet + upper_alphabet, range(1, 53)))

    # Only 1 item should exist in both compartments, so we find it by getting
    # the intersection of the set.
    items_in_both_compartments = []

    for rucksack in rucksacks:
        bag_size = len(rucksack)
        midpoint = int(bag_size / 2)
        compartments = (rucksack[:midpoint], rucksack[midpoint:])
        common_items = reduce(get_intersection, compartments)
        items_in_both_compartments += list(common_items)

    # Solution: part 1
    # Now we have the list of items, map across the priority values and get the sum.
    priorities = map(priority_map.get, items_in_both_compartments)
    print(f"Sum of priorities for common items in each compartment: {sum(priorities)}")

    # Solution: part 2
    elf_groups = group_elements(rucksacks, 3)
    # Get the intersection across all 3 elves in each group.
    badge_items = chain.from_iterable(
        map(lambda x: reduce(get_intersection, x), elf_groups)
    )

    # Now we have the list of badge items, map across the priority values and get the sum.
    priorities = map(priority_map.get, badge_items)
    print(f"Sum of priorities for all elf group badges is: {sum(priorities)}")
