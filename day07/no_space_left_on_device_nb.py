#!/usr/bin/env python
# coding: utf-8

# In[44]:
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from typing import Mapping, Optional

# In[45]:
# View file contents.
with open("input.txt") as f:
    lines = [line.rstrip("\n") for line in f]

pprint(lines[:20])


# In[46]:
@dataclass
class File:
    name: str
    size: int
    parent: Dir

    @property
    def path(self):
        """Set the path using parent path."""
        return self.parent.path.joinpath(self.name)


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
            # Set path as the root if no parent given.
            return Path("/")
        else:
            return self.parent.path.joinpath(self.name)


# In[47]:
# Parse the bash history and build out the file tree starting from the
# home directory "/".
home_dir = Dir(name="home")
current_dir = home_dir

for stdout in lines:
    if re.search(r"^\$ cd", stdout):
        new_dir_name = re.search(r"(?<=cd\s).+", stdout)[0]
        if new_dir_name == "/":
            continue
        if new_dir_name == "..":
            current_dir = current_dir.parent
        else:
            new_dir = Dir(new_dir_name, parent=current_dir)
            current_dir.dirs.update({new_dir.path: new_dir})
            current_dir = new_dir
    elif re.search(r"^\d+", stdout):
        # File format is: 476347 filename.ext
        file_size, file_name = re.split(r" ", stdout)
        file = File(name=file_name, size=int(file_size), parent=current_dir)
        current_dir.files.update({file.path: file})
    elif re.search(r"^dir", stdout):
        new_dir_name = re.split(r" ", stdout)[-1]
        new_dir = Dir(new_dir_name, parent=current_dir)
        current_dir.dirs.update({new_dir.path: new_dir})


# In[48]:
def calculate_sizes() -> callable[Dir, dict[Path, int]]:
    """Calculate the size of all directories recursively."""
    sizes = {}

    def inner(dir_: Dir):
        total_file_size = sum([file.size for file in dir_.files.values()])
        total_dir_size = sum(
            [inner(sub_dir).get(sub_dir.path) for sub_dir in dir_.dirs.values()]
        )
        total_size = total_file_size + total_dir_size
        sizes.update({dir_.path: total_size})

        return sizes

    return inner


size_calculator = calculate_sizes()
dir_sizes = size_calculator(home_dir)

good_candidates = {path: size for path, size in dir_sizes.items() if size <= 10e4}
pprint(good_candidates)
# In[49]:
# Solution to part 1
sum(good_candidates.values())
# In[50]:
total_space = 70000000
used_space = dir_sizes.get(Path("/"))
required_space = 30000000
unused_space = total_space - used_space
if unused_space < required_space:
    target_space = required_space - unused_space

print(target_space)

deletion_candidates = {
    dir_: size for dir_, size in dir_sizes.items() if size >= target_space
}
pprint(deletion_candidates)
# In[51]:
# Solution to part 2
min(deletion_candidates.values())
