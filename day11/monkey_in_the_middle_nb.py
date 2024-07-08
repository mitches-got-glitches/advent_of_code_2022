#!/usr/bin/env python
# coding: utf-8

# In[172]:
from __future__ import annotations

import functools
import operator
import re
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass, field
from pprint import pprint
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple

# In[173]:
# View file contents.
with open("input.txt") as f:
    lines = [line.rstrip("\n") for line in f]

pprint(lines[:20])


# In[184]:
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(x, y):
    return x * y / gcd(x, y)


@dataclass
class Monkey:
    items: List[int]
    divisor: int
    operation: Callable[[int], int]
    true_monkey: int
    false_monkey: int

    def __post_init__(self):
        self.inspections = 0

    def throw_items(self, lcm: Optional[int] = None) -> List[Tuple[int, int]]:
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

    def keep_level_down(self, item: int, lcm: Optional[int] = None):
        if not lcm:
            item = item // 3
        elif item > lcm:
            item = item % lcm

        return item

    def throw_to(self, item: int) -> int:
        return self.true_monkey if (item % self.divisor == 0) else self.false_monkey


@dataclass
class MonkeyGame:
    monkeys: List[Monkey] = field(default_factory=list)

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


# In[185]:
def split_list_on(lst: List[Any], on: Any = "") -> List[List[Any]]:
    """Split a list using a given list item as the list separator."""
    split, part = [], []
    for item in lst:
        if item == on:
            split.append(part)
            part = []
        else:
            part.append(item)
    # Do final append.
    split.append(part)
    return split


def split_list_equal(lst: List[Any], n: int) -> List[List[Any]]:
    """Split list into n equal parts."""
    return [lst[i : i + n] for i in range(0, len(lst) - n + 1, n)]


# In[186]:
ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
}


def by_itself(a: int, op: Callable[[int, int], int]) -> int:
    """Apply an operator with both input arguments being the given value."""
    return op(a, a)


def monkey_parser(input: List[str]) -> List[Monkey]:
    monkey_info = split_list_on(list(map(str.strip, input)), on="")

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
                    func = functools.partial(by_itself, op=ops[operator_])
                else:
                    func = functools.partial(ops[operator_], int(value))
                monkey_kwargs.update({"operation": func})

            elif line.startswith("Test:"):
                monkey_kwargs.update({"divisor": int(re.search(r"\d+", line)[0])})

            elif line.startswith("If true:"):
                monkey_kwargs.update({"true_monkey": int(re.search(r"\d+", line)[0])})

            elif line.startswith("If false:"):
                monkey_kwargs.update({"false_monkey": int(re.search(r"\d+", line)[0])})

        monkeys.append(Monkey(**monkey_kwargs))

    return monkeys


monkeys = monkey_parser(lines)
monkeys
# In[187]:
# Play 20 rounds
game = MonkeyGame(monkeys)
game.play_rounds(20)
# In[188]:
game.monkey_dict
# In[189]:
list(map(lambda x: x.inspections, game.monkey_dict.values()))
# In[190]:
sorted(map(lambda x: x.inspections, game.monkey_dict.values()))
top_2 = sorted(map(lambda x: x.inspections, game.monkey_dict.values()))[-2:]
monkey_business = top_2[0] * top_2[1]
monkey_business
# In[191]:
monkeys
# In[192]:
# Play 10000 rounds
game.reset()
game.play_rounds(10000, use_lcm=True)
list(map(lambda x: x.inspections, game.monkey_dict.values()))
# In[183]:
sorted(map(lambda x: x.inspections, game.monkey_dict.values()))
top_2 = sorted(map(lambda x: x.inspections, game.monkey_dict.values()))[-2:]
monkey_business = top_2[0] * top_2[1]
monkey_business
