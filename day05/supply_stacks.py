import re
from copy import deepcopy
from pprint import pprint
from typing import Literal

from aoc_helpers import get_input_path, split_list

Stacks = dict[int, list[str]]
CrateMoverVersion = Literal["9000", "9001"]


def parse_stacks(stacks: list[str]) -> list[list[str]]:
    """Parses the stack data to a list of stacks represented as a string of crates."""
    stacks_padded = [line.ljust(max(map(len, stacks)), " ") for line in stacks]
    # Reverse, transpose, then select only the lines which have crates (capital letters).
    transposed_stacks = [list(i) for i in zip(*stacks_padded[::-1])][1:-1:4]
    # Different stacks are different sizes, so strip the dead whitespace.
    return [list("".join(stack).strip()) for stack in transposed_stacks]


class CrateMover:
    """A class for CrateMover crane."""

    def __init__(self, version: CrateMoverVersion = "9001"):
        """Initialise the CrateMover."""
        self._version = version

    @property
    def version(self):
        """The CrateMover version - can be set to "9000" or "9001"."""
        return self._version

    @version.setter
    def version(self, version: CrateMoverVersion):
        if version not in ("9000", "9001"):
            raise ValueError("Valid CrateMover versions are '9000' and '9001'.")
        self._version = version

    def operate(
        self,
        stacks: Stacks,
        move_instructions: tuple[str, str, str],
    ) -> Stacks:
        """Operate the CrateMaster on the given stacks using the move instructions."""
        stacks_ = deepcopy(stacks)

        for number_to_move, from_, to_ in move_instructions:
            to_move = stacks_[from_][-int(number_to_move) :]
            stacks_[from_] = stacks_[from_][: -int(number_to_move)]

            # Reverse the move stack if the version is "9000", not "9001".
            stacks_[to_] += to_move if self.version == "9001" else to_move[::-1]

        return stacks_


if __name__ == "__main__":
    with open(get_input_path()) as f:
        lines = [line.rstrip("\n") for line in f]

    # Separate the input data into different sections.
    all_stack_data, moves_data = split_list(lines, "")
    stack_ids_data = all_stack_data[-1]
    stacks_data = all_stack_data[:-1]

    stacks = parse_stacks(stacks_data)
    stack_ids = re.findall(r"\d", stack_ids_data)
    starting_stacks = dict(zip(stack_ids, stacks))

    # Get the numbers from the move instructions (number_to_move, from, to).
    move_nums = [tuple(re.findall(r"\d{1,2}", move)) for move in moves_data]

    crate_mover = CrateMover(version="9000")
    stacks_result = crate_mover.operate(starting_stacks, move_nums)
    pprint(stacks_result, compact=True)
    # Solution - Part 1
    pprint("".join([v[-1] for v in stacks_result.values()]))

    crate_mover.version = "9001"
    stacks_result = crate_mover.operate(starting_stacks, move_nums)
    pprint(stacks_result, compact=True)
    # Solution - Part 2
    pprint("".join([v[-1] for v in stacks_result.values()]))
