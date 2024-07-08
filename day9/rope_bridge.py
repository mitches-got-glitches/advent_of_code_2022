from __future__ import annotations

import itertools
from copy import copy, deepcopy
from dataclasses import dataclass, field
from typing import Literal, Tuple

from aoc_helpers import get_input_path

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
        e_dist = self.head.get_euclidean_distance(self.tail)
        if e_dist > 2:
            if self.head.y != self.tail.y:
                self.tail.y += int(
                    (self.head.y - self.tail.y) / abs(self.head.y - self.tail.y)
                )
            if self.head.x != self.tail.x:
                self.tail.x += int(
                    (self.head.x - self.tail.x) / abs(self.head.x - self.tail.x)
                )
        elif e_dist == 2 and self.head.is_on_same_plane(self.tail):
            self.tail.move(direction)


class RopeTracker:
    def __init__(self, knots: int):
        self.n_knots = knots
        self.rope = [Position() for _ in range(knots)]
        self.positions = []
        # Take initial snapshot for starting positions.
        self.snapshot()

    def apply_motion(self, direction: Direction, steps: int) -> None:
        """Step in the direction for the given number of steps."""
        for _ in range(steps):
            rope = Rope(self.rope[0], self.rope[1])
            rope.move_head(direction)
            self.rope[0] = deepcopy(rope.head)
            for i, knot in enumerate(self.rope[1:]):
                previous_knot = self.rope[i]
                rope = Rope(previous_knot, knot)
                rope.move_tail(direction)
                self.rope[i + 1] = deepcopy(rope.tail)
                # try:
                #     self.ropes[i+1].head = rope.tail
                # except IndexError:
                #     pass
            self.snapshot()

    def snapshot(self):
        """Save the position of the head and tail."""
        self.positions.append([knot.snapshot() for knot in self.rope])

    def visualise(self):
        all_positions = list(itertools.chain.from_iterable(rope_tracker.positions))
        min_x = min(all_positions, key=lambda x: x[0])[0]
        max_x = max(all_positions, key=lambda x: x[0])[0]
        min_y = min(all_positions, key=lambda x: x[1])[1]
        max_y = max(all_positions, key=lambda x: x[1])[1]

        knot_markers = ["H", *[str(i) for i in range(1, self.n_knots - 1)], "T"]
        start_x = abs(min_x) + self.positions[0][0][0]
        start_y = abs(max_y) - self.positions[0][0][1]
        for rope_position in self.positions:
            grid = generate_uniform_grid(
                abs(min_x) + abs(max_x) + 1,
                abs(min_y) + abs(max_y) + 1,
                fill_val=".",
            )
            grid[start_y][start_x] = "s"
            # Go in reverse:
            for marker, knot_position in zip(knot_markers[::-1], rope_position[::-1]):
                x_pos = abs(min_x) + knot_position[0]
                y_pos = abs(max_y) - knot_position[1]
                grid[y_pos][x_pos] = marker
            print(*["".join(row) for row in grid], sep="\n")
            print("\n")


def generate_uniform_grid(x, y, fill_val: None):
    """Generate a uniform filled grid in the same shape as self.grid."""
    return [[fill_val for _ in range(x)] for _ in range(y)]


if __name__ == "__main__":
    with open(get_input_path()) as f:
        motions = [line.rstrip("\n") for line in f]

    rope_tracker = RopeTracker(knots=2)

    for motion in motions:
        direction, steps = motion.split(" ")
        steps = int(steps)
        rope_tracker.apply_motion(direction, steps)

    # Solution to part 1
    # The tail is the final position so index at -1.
    print("The amount of unique positions that the tail of the 2-knot rope visits is:")
    print(len({x[-1] for x in rope_tracker.positions}))

    # rope_tracker.visualise()

    # Solution to part 2
    rope_tracker = RopeTracker(knots=10)

    for motion in motions:
        direction, steps = motion.split(" ")
        steps = int(steps)
        rope_tracker.apply_motion(direction, steps)

    # Solution to part 2
    print("The amount of unique positions that the tail of the 10-knot rope visits is:")
    print(len({x[-1] for x in rope_tracker.positions}))

    # rope_tracker.visualise()
