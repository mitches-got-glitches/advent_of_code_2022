from dataclasses import dataclass, field
from operator import itemgetter

from aoc_helpers.core import get_input_path


@dataclass
class VideoSystem:
    cycle: int = 0
    x: int = 1
    signal_strengths: list[int] = field(default_factory=list)
    pixels: list[str] = field(default_factory=list)

    def run_cycles(self, commands: list[str]):
        for command in commands:
            if command == "noop":
                self.noop_cycle()
            elif command[:4] == "addx":
                val = int(command.split(" ")[1])
                self.add_cycle(val)

    def noop_cycle(self):
        self.write_pixel()
        self.cycle += 1
        self.check_signal()

    def add_cycle(self, val: int):
        self.write_pixel()
        self.cycle += 1
        self.check_signal()

        self.write_pixel()
        self.cycle += 1
        self.check_signal()

        self.x += val

    def get_signal_strength(self):
        return self.cycle * self.x

    def check_signal(self):
        self.signal_strengths.append(self.get_signal_strength())

    def write_pixel(self):
        sprite_pos = (self.x - 1, self.x, self.x + 1)
        if (self.cycle % 40) in sprite_pos:
            self.pixels.append("#")
        else:
            self.pixels.append(".")


if __name__ == "__main__":
    with open(get_input_path()) as f:
        instructions = [line.rstrip("\n") for line in f]

    video_sys = VideoSystem()
    video_sys.run_cycles(instructions)
    observation_cycles = [i - 1 for i in [20, 60, 100, 140, 180, 220]]
    # Solution - part 1:
    print("Sum of the signal strengths at the observation cycles is:")
    print(sum(itemgetter(*observation_cycles)(video_sys.signal_strengths)))

    print("The hidden letters are:")
    pixels = video_sys.pixels
    n = 40
    for i in range(0, len(pixels) - n + 1, n):
        batch = pixels[i : i + n]
        print("".join(batch))
