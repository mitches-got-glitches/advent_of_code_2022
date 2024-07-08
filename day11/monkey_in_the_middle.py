from __future__ import annotations

import functools
import operator
import re
from collections import OrderedDict
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


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(x, y):
    return x * y / gcd(x, y)


@dataclass
class Monkey:
    items: list[int]
    divisor: int
    operation: Callable[[int], int]
    true_monkey: int
    false_monkey: int

    def __post_init__(self):
        self.inspections = 0

    def throw_items(self, lcm: int | None = None) -> list[tuple[int, int]]:
        throws = []
        for item in self.items:
            new_worry_level = self.inspect_item(item)
            new_worry_level = self.keep_level_down(new_worry_level, lcm)
            monkey_no = self.throw_to(new_worry_level)
            throws.append((monkey_no, new_worry_level))

        self.items = []
        return throws

    def inspect_item(self, item: int) -> int:
        self.inspections += 1
        return self.operation(item)

    def keep_level_down(self, item: int, lcm: int | None = None):
        if not lcm:
            item = item // 3
        elif item > lcm:
            item = item % lcm

        return item

    def throw_to(self, item: int) -> int:
        return self.true_monkey if (item % self.divisor == 0) else self.false_monkey


@dataclass
class MonkeyGame:
    monkeys: list[Monkey] = field(default_factory=list)

    def __post_init__(self):
        self.monkey_dict = self.create_monkey_dict()
        # The lowest common multiple of the divisors is used in the modulo
        # function to keep the worry levels down, as it won't affect future
        # monkey divisor tests.
        self.lcm = int(functools.reduce(lcm, [m.divisor for m in self.monkeys]))

    def play_round(self, use_lcm: bool = False):
        for monkey_no, monkey in self.monkey_dict.items():
            if use_lcm:
                throws = monkey.throw_items(self.lcm)
            else:
                throws = monkey.throw_items()

            for to_monkey, item in throws:
                self.monkey_dict[to_monkey].items.append(item)

    def play_rounds(self, n_rounds: int, use_lcm: bool = False):
        for _ in range(n_rounds):
            self.play_round(use_lcm)

    def create_monkey_dict(self):
        monkey_copies = [deepcopy(m) for m in self.monkeys]
        return OrderedDict(zip(range(len(self.monkeys)), monkey_copies))

    def reset(self):
        self.monkey_dict = self.create_monkey_dict()


def by_itself(a: int, op: Callable[[int, int], int]) -> int:
    """Apply an operator with both input arguments being the given value."""
    return op(a, a)


def monkey_parser(input: list[str]) -> list[Monkey]:
    monkey_info = split_list([s.strip() for s in input], "")

    monkeys = []
    for monkey in monkey_info:
        monkey_kwargs = {}
        for line in monkey:
            if line.startswith("Starting items:"):
                monkey_kwargs.update(
                    {"items": [int(s) for s in re.findall(r"\d+", line)]}
                )
            elif line.startswith("Operation:"):
                # Get two match groups for the operator and value.
                res = re.search(r"([\+\-\*\\%]+)\s(\d+|old)", line)
                operator_, value = res[1], res[2]
                # Partial returns a callable object with pre-supplied params.
                if value == "old":
                    func = functools.partial(by_itself, op=OPERATOR_MAP[operator_])
                else:
                    func = functools.partial(OPERATOR_MAP[operator_], int(value))
                monkey_kwargs.update({"operation": func})

            elif line.startswith("Test:"):
                monkey_kwargs.update({"divisor": int(re.search(r"\d+", line)[0])})

            elif line.startswith("If true:"):
                monkey_kwargs.update({"true_monkey": int(re.search(r"\d+", line)[0])})

            elif line.startswith("If false:"):
                monkey_kwargs.update({"false_monkey": int(re.search(r"\d+", line)[0])})

        monkeys.append(Monkey(**monkey_kwargs))

    return monkeys


if __name__ == "__main__":
    with open(get_input_path()) as f:
        monkey_notes = [line.rstrip("\n") for line in f]

    monkeys = monkey_parser(monkey_notes)
    game = MonkeyGame(monkeys)
    game.play_rounds(20)
    top_2 = sorted(map(lambda x: x.inspections, game.monkey_dict.values()))[-2:]
    print("The level of monkey business after 20 rounds is:")
    print(top_2[0] * top_2[1])

    game.reset()
    game.play_rounds(10000, use_lcm=True)
    top_2 = sorted(map(lambda x: x.inspections, game.monkey_dict.values()))[-2:]
    print("The level of monkey business after 10000 rounds is:")
    print(top_2[0] * top_2[1])
