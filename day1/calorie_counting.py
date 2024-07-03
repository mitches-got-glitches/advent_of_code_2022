from dataclasses import dataclass, field

from aoc_helpers import get_input_path, split_list


@dataclass
class Elf:
    """An Elf class.

    Attributes:
        food_item_calories: A list of calorie values for each food item
            in the elf's possesion.
        total_calories: The total calorific value of all the elf's food
            items.
    """

    food_item_calories: list[int] = field(default_factory=list)

    @property
    def total_calories(self):
        return sum(self.food_item_calories)

    def add_food_item_calories(self, item: int):
        self.food_item_calories.append(item)


if __name__ == "__main__":
    # Read the input file.
    with open(get_input_path()) as f:
        inventories = [line.strip() for line in f]

    elves = [
        Elf([int(cals) for cals in item_calories])
        for item_calories in split_list(inventories, "")
    ]

    # Solution to part 1.
    total_calories_per_elf = sorted(elf.total_calories for elf in elves)
    max_total_calories = total_calories_per_elf[-1]
    print(f"The max calories that any elf is carrying is: {max_total_calories}.")

    # Solution to part 2.
    top3_total_calories = sum(total_calories_per_elf[-3:])
    print(f"The total calories carried by the top 3 elves is: {top3_total_calories}.")
