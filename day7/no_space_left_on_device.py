from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Optional

from aoc_helpers import get_input_path


@dataclass
class RegexEqual(str):
    string: str
    match: re.Match = None

    def __eq__(self, pattern):
        self.match = re.search(pattern, self.string)
        return self.match is not None


@dataclass
class File:
    name: str
    size: int
    parent: Dir

    @property
    def path(self):
        """Set the path using parent path."""
        return self.parent.path / self.name


@dataclass
class Dir:
    name: str
    parent: Optional[Dir] = None
    dirs: Mapping[Path, Dir] = field(default_factory=dict)
    files: Mapping[Path, File] = field(default_factory=dict)

    @property
    def path(self):
        """Set the path using parent path."""
        if not self.parent:
            # Set path as the root if the directory has no parent.
            return Path("/")
        else:
            return self.parent.path / self.name

    def calculate_sizes(self) -> dict[Path, int]:
        """Calculate the size of all directories recursively."""
        sizes: dict[Path, int] = {}

        def inner(dir_: Dir) -> dict[Path, int]:
            total_file_size = sum([file.size for file in dir_.files.values()])
            total_dir_size = sum(
                [inner(sub_dir).get(sub_dir.path) for sub_dir in dir_.dirs.values()]
            )
            total_size = total_file_size + total_dir_size
            sizes.update({dir_.path: total_size})

            return sizes

        return inner(self)


def parse_directory_structure_from_stdout(stdout: list[str]) -> dict[Path, Dir | File]:
    """Parse the directory structure from a list of stdout messages."""
    dir_structure: dict[Path, Dir | File] = {}
    for line in stdout:
        match RegexEqual(line):
            case r"^\$ cd":  # A change directory command
                new_dir_name = re.search(r"(?<=cd\s).+", line)[0]
                match new_dir_name:
                    case "/":
                        home_dir = Dir(name=new_dir_name)
                        current_dir = home_dir
                    case "..":
                        current_dir = current_dir.parent
                    case _:
                        new_dir = Dir(new_dir_name, parent=current_dir)
                        current_dir.dirs.update({new_dir.path: new_dir})
                        current_dir = new_dir

                dir_structure.update({current_dir.path: current_dir})
            case r"^\d+":  # Is a file
                # File format is: 476347 filename.ext
                file_size, file_name = re.split(r" ", line)
                file = File(name=file_name, size=int(file_size), parent=current_dir)
                current_dir.files.update({file.path: file})
            case r"^dir":  # Is a directory
                new_dir_name = re.split(r" ", line)[-1]
                new_dir = Dir(new_dir_name, parent=current_dir)
                current_dir.dirs.update({new_dir.path: new_dir})

    return dir_structure


if __name__ == "__main__":
    with open(get_input_path()) as f:
        stdout = [line.rstrip("\n") for line in f]

    dir_structure = parse_directory_structure_from_stdout(stdout)
    root_dir: Dir = dir_structure.get(Path("/"))
    dir_sizes = root_dir.calculate_sizes()

    # Solution to part 1
    good_candidates = {
        path: size for path, size in dir_sizes.items() if size <= 100_000
    }
    print("Sum of all directory sizes where the total size is no greater than 100,000:")
    print(sum(good_candidates.values()))

    # Solution to part 2
    TOTAL_SPACE = 70000000
    used_space = dir_sizes.get(Path("/"))
    REQUIRED_SPACE = 30000000
    unused_space = TOTAL_SPACE - used_space
    if unused_space < REQUIRED_SPACE:
        target_space = REQUIRED_SPACE - unused_space

    deletion_candidates = {
        dir_: size for dir_, size in dir_sizes.items() if size >= target_space
    }
    print(
        "Size of smallest directory that if deleted, frees up enough space for the update:"
    )
    print(min(deletion_candidates.values()))
