#!/usr/bin/env python
# coding: utf-8

# In[232]:
from __future__ import annotations

from copy import copy, deepcopy
from dataclasses import dataclass, field
from pprint import pprint
from typing import List, Literal, Tuple

# In[233]:
# View file contents.
with open("input.txt") as f:
    motions = [line.rstrip("\n") for line in f]

pprint(motions[:30], compact=True)
# In[243]:
Direction = Literal["U", "D", "R", "L"]


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def move(self, direction: Direction) -> None:
        move_options = {
            "U": lambda x: x.move_up(),
            "D": lambda x: x.move_down(),
            "R": lambda x: x.move_right(),
            "L": lambda x: x.move_left(),
        }
        return move_options[direction](self)

    def move_up(self) -> None:
        self.y += 1

    def move_down(self) -> None:
        self.y -= 1

    def move_right(self) -> None:
        self.x += 1

    def move_left(self) -> None:
        self.x -= 1

    def snapshot(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def get_euclidean_distance(self, other: Position) -> int:
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2

    def is_on_same_plane(self, other: Position) -> bool:
        """Return True if either both x or both y are equal."""
        return (other.x == self.x) or (other.y == self.y)


@dataclass
class Rope:
    head: Position = field(default_factory=Position)
    tail: Position = field(default_factory=Position)

    def move_head(self, direction: Direction):
        self.head.move(direction)

    def move_tail(self, direction: Direction) -> None:
        """Move the tail to follow the head."""
        if self.get_euclidean_distance() > 2:
            self.tail.move(direction)
            # The rope needs to move diagonally in this scenario. So
            # force the tail to be on the same plane as the head.
            if direction in "UD":
                self.tail.x = self.head.x
            elif direction in "LR":
                self.tail.y = self.head.y

        elif self.tail_too_far():
            self.tail.move(direction)

    def get_euclidean_distance(self) -> int:
        return self.head.get_euclidean_distance(self.tail)

    def is_on_same_plane(self) -> bool:
        """Return True if head an tail are aligned on the same plane."""
        return self.head.is_on_same_plane(self.tail)

    def tail_too_far(self) -> bool:
        """Return True if the tail is too far from the head."""
        e_dist = self.get_euclidean_distance()
        # If the euclidean distance is more than 2 then the tail isn't
        # adjacent to the head. If it equals 2, and they're on the same
        # plane i.e. diagonal, then it is also too far away.
        if e_dist > 2 or (e_dist == 2 and self.is_on_same_plane()):
            return True
        else:
            return False


class RopeTracker:
    def __init__(self, knots: int):
        # self.n_knots = knots
        self.rope = [Position() for _ in range(knots)]
        self.positions = []
        # Take initial snapshot for starting positions.
        self.snapshot()

    def apply_motion(self, direction: Direction, steps: int) -> None:
        """Step in the direction for the given number of steps."""
        for _ in range(steps):
            rope = Rope(self.rope[0], self.rope[1])
            rope.move_head(direction)
            self.rope[0] = copy(rope.head)
            for i, knot in enumerate(self.rope[1:]):
                previous_knot = self.rope[i]
                rope = Rope(previous_knot, knot)
                rope.move_tail(direction)
                self.rope[i + 1] = copy(rope.tail)
                # try:
                #     self.ropes[i+1].head = rope.tail
                # except IndexError:
                #     pass
            self.snapshot()

    def snapshot(self):
        """Save the position of the head and tail."""
        self.positions.append([knot.snapshot() for knot in self.rope])


# In[244]:
rope_tracker = RopeTracker(knots=2)

for motion in motions:
    direction, steps = motion.split(" ")
    steps = int(steps)
    rope_tracker.apply_motion(direction, steps)

# Solution to part 1
len(set(map(lambda x: x[-1], rope_tracker.positions)))
# In[245]:
rope_tracker = RopeTracker(knots=10)

for motion in motions:
    direction, steps = motion.split(" ")
    steps = int(steps)
    rope_tracker.apply_motion(direction, steps)

# Solution to part 2
len(set(map(lambda x: x[-1][-1], rope_tracker.positions)))


# In[246]:
def generate_uniform_grid(x, y, fill_val: None):
    """Generate a uniform filled grid in the same shape as self.grid."""
    return [[fill_val for _ in range(x)] for _ in range(y)]


def print_grid(grid):
    print(list(map("".join, grid)))


grid = generate_uniform_grid(200, 300, ".")
# print_grid(grid)
