from dataclasses import dataclass, field
from typing import List

from aoc_helpers import get_input_path


@dataclass
class Elf:
    """An Elf class.

    Attributes:
        food_item_calories: A list of calorie values for each food item
            in the elf's possesion.
        total_calories: The total calorific value of all the elf's food
            items.
    """

    food_item_calories: List[int] = field(default_factory=list)

    @property
    def total_calories(self):
        return sum(self.food_item_calories)

    def add_food_item_calories(self, item: int):
        self.food_item_calories.append(item)


if __name__ == "__main__":
    # Read the input file.
    with open(get_input_path()) as f:
        inventories = [line.strip() for line in f]

    # Initialise elves.
    elves: list[Elf] = []
    elf = Elf()

    for item_calories in inventories:
        if item_calories == "":
            # Save elf's inventory and start new one.
            elves += [elf]
            elf = Elf()
        else:
            elf.add_food_item_calories(int(item_calories))
    elves += [elf]

    # Solution to part 1.
    total_calories_per_elf = sorted(elf.total_calories for elf in elves)
    max_total_calories = total_calories_per_elf[-1]
    print(f"The max calories that any elf is carrying is: {max_total_calories}.")

    # Solution to part 2.
    top3_total_calories = sum(total_calories_per_elf[-3:])
    print(f"The total calories carried by the top 3 elves is: {top3_total_calories}.")
