import functools
import math
import operator
import re
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Callable

from aoc_helpers.core import get_input_path, split_list

OPERATOR_MAP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
}


@dataclass
class Monkey:
    items: list[int]
    divisor: int
    operation: Callable[[int], int]
    true_monkey: int
    false_monkey: int
    inspections: int = field(init=False, default=0)

    def throw_items(self, lcm: int | None = None) -> list[tuple[int, int]]:
        throws = []
        for item in self.items:
            new_worry_level = self.keep_level_down(self.inspect_item(item), lcm)
            monkey_no = self.throw_to(new_worry_level)
            throws.append((monkey_no, new_worry_level))

        # Items have all been thrown.
        self.items = []
        return throws

    def inspect_item(self, item: int) -> int:
        self.inspections += 1
        return self.operation(item)

    def keep_level_down(self, item: int, lcm: int | None = None):
        if not lcm:
            item //= 3
        elif item > lcm:
            item %= lcm

        return item

    def throw_to(self, item: int) -> int:
        return self.true_monkey if (item % self.divisor == 0) else self.false_monkey


@dataclass
class MonkeyGame:
    monkeys: list[Monkey] = field(default_factory=list)

    def __post_init__(self):
        self.monkey_dict: dict[int, Monkey] = self.create_monkey_dict()
        # The lowest common multiple of the divisors is used in the modulo
        # function to keep the worry levels down, as it won't affect future
        # monkey divisor tests.
        self.lcm = int(functools.reduce(math.lcm, [m.divisor for m in self.monkeys]))

    def play_round(self, use_lcm: bool = False):
        for monkey in self.monkey_dict.values():
            lcm = self.lcm if use_lcm else None
            throws = monkey.throw_items(lcm)
            for to_monkey, item in throws:
                self.monkey_dict[to_monkey].items.append(item)

    def play_rounds(self, n_rounds: int, use_lcm: bool = False):
        for _ in range(n_rounds):
            self.play_round(use_lcm)

    def create_monkey_dict(self) -> dict[int, Monkey]:
        monkey_copies: list[Monkey] = [deepcopy(m) for m in self.monkeys]
        return dict(zip(range(len(self.monkeys)), monkey_copies))

    def reset(self):
        self.monkey_dict = self.create_monkey_dict()

    def calculate_monkey_business(self):
        """Monkey business is product of the inspections from the two most active monkeys."""
        top_inspections = sorted(
            map(lambda x: x.inspections, self.monkey_dict.values())
        )
        monkey1, monkey2 = top_inspections[-2:]
        return monkey1 * monkey2


@dataclass
class StartsWith(str):
    string: str

    def __eq__(self, pattern):
        return self.string.startswith(pattern)


def monkey_parser(input: list[str]) -> list[Monkey]:
    monkey_info = split_list([s.strip() for s in input], "")

    monkeys = []
    for monkey in monkey_info:
        monkey_kwargs = {}
        for line in monkey:
            match StartsWith(line):
                case "Starting items:":
                    monkey_kwargs.update(
                        {"items": [int(s) for s in re.findall(r"\d+", line)]}
                    )
                case "Operation:":
                    # Get two match groups for the operator and value.
                    res = re.search(r"([\+\-\*\\%]+)\s(\d+|old)", line)
                    operator_, value = res[1], res[2]
                    # Partial returns a callable object with pre-supplied params.
                    if value == "old":
                        func = functools.partial(
                            lambda x, op: op(x, x),
                            op=OPERATOR_MAP[operator_],
                        )
                    else:
                        func = functools.partial(OPERATOR_MAP[operator_], int(value))
                    monkey_kwargs.update({"operation": func})

                case "Test:":
                    monkey_kwargs.update({"divisor": int(re.search(r"\d+", line)[0])})

                case "If true:":
                    monkey_kwargs.update(
                        {"true_monkey": int(re.search(r"\d+", line)[0])}
                    )

                case "If false:":
                    monkey_kwargs.update(
                        {"false_monkey": int(re.search(r"\d+", line)[0])}
                    )

        monkeys.append(Monkey(**monkey_kwargs))

    return monkeys


if __name__ == "__main__":
    with open(get_input_path()) as f:
        monkey_notes = [line.rstrip("\n") for line in f]

    game = MonkeyGame(*monkey_parser(monkey_notes))
    game.play_rounds(20)
    print("The level of monkey business after 20 rounds is:")
    print(game.calculate_monkey_business())

    game.reset()
    game.play_rounds(10000, use_lcm=True)
    print("The level of monkey business after 10000 rounds is:")
    print(game.calculate_monkey_business())
