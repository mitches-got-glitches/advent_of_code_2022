import itertools
from functools import reduce
from operator import mul
from typing import Any, List, Optional

from aoc_helpers import get_input_path


class TreeGrid:
    def __init__(self, grid: List[List[str]]):
        """Initiate the tree grid."""
        self._grid = grid

    @property
    def grid(self):
        """Convert strings to lists, if grid is list of strings."""
        if all(isinstance(item, str) for item in self._grid):
            return [list(s) for s in self._grid]
        else:
            return self._grid

    @property
    def grid_T(self):
        """Set the transposed grid as a property."""
        return [list(i) for i in zip(*self._grid)]

    @property
    def len_x(self) -> int:
        """Set the horizontal length as a property."""
        return len(self.grid[0])

    @property
    def len_y(self) -> int:
        """Set the vertical length as a property."""
        return len(self.grid)

    def is_on_edge(self, i: int, j: int) -> bool:
        """Return True if tree position is on the edge of the grid."""
        return (i == 0 or i == self.len_x - 1) or (j == 0 or j == self.len_y - 1)

    def generate_uniform_grid(
        self,
        fill_val: Optional[Any] = None,
    ) -> List[List[Any]]:
        """Generate a uniform filled grid in the same shape as self.grid."""
        return [[fill_val for _ in range(self.len_x)] for _ in range(self.len_y)]

    def get_aligned_tree_heights(self, i: int, j: int) -> List[List[int]]:
        """Return list of trees in each direction travelling outwards."""
        return [
            self.grid[i][:j][::-1],  # Trees to left
            self.grid[i][j + 1 :],  # Trees to right
            self.grid_T[j][:i][::-1],  # Trees above
            self.grid_T[j][i + 1 :],  # Trees below
        ]

    def mark_visible(self, marker: str = "^", other: str = ".") -> List[List[str]]:
        """Return a grid of markers where trees are visible from outside."""
        # Assume all visible to start.
        visible = self.generate_uniform_grid(marker)

        for i, j in itertools.product(range(self.len_x), range(self.len_y)):
            if not self._is_visible(i, j):
                visible[i][j] = other

        return visible

    def _is_visible(self, i: int, j: int) -> bool:
        """Return True if a tree at position is visible from any side."""
        if self.is_on_edge(i, j):
            return True

        current_tree_height = self.grid[i][j]
        for heights in self.get_aligned_tree_heights(i, j):
            if all([h < current_tree_height for h in heights]):
                return True

        return False

    def _get_scenic_score(self, i: int, j: int) -> bool:
        """Get the scenic score for a tree at a given position."""
        current_tree_height = self.grid[i][j]
        # Calculate the viewing distance in all 4 directions.
        viewing_distances = [
            self._get_viewing_distance(current_tree_height, heights)
            for heights in self.get_aligned_tree_heights(i, j)
        ]
        return reduce(mul, viewing_distances)

    @staticmethod
    def _get_viewing_distance(
        current_height: int,
        other_heights: List[int],
    ) -> int:
        """Calculate score in a direction given a set of heights.

        Returns 0 if other_heights is empty (indicates tree on outer edge).
        """
        score = 0
        for height in other_heights:
            score += 1
            # Break the loop if you can't see past the tree.
            if height >= current_height:
                break

        return score

    def calculate_scenic_score_grid(self):
        """Calculate total scenic score for each tree in grid."""
        scenic_scores = self.generate_uniform_grid(0)
        for i, j in itertools.product(range(self.len_x), range(self.len_y)):
            scenic_scores[i][j] = self._get_scenic_score(i, j)

        return scenic_scores


if __name__ == "__main__":
    with open(get_input_path()) as f:
        grid = [line.rstrip("\n") for line in f]

    tree_grid = TreeGrid(grid)
    visible_trees = tree_grid.mark_visible(marker="^", other=".")
    print(*list(map("".join, visible_trees)), sep="\n")

    # Solution to part 1
    print("The total number of trees visibile from outside the grid is:")
    print(sum(x == "^" for x in itertools.chain.from_iterable(visible_trees)))

    # Solution to part 2
    scenic_scores = tree_grid.calculate_scenic_score_grid()
    print("The highest scenic score possible for any tree is:")
    print(max(itertools.chain.from_iterable(scenic_scores)))
