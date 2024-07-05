#!/usr/bin/env python
# coding: utf-8

# In[216]:
import re
from copy import deepcopy
from pprint import pprint

# In[217]:
from aoc_helpers import get_input_path

# View file contents.
with open(get_input_path()) as f:
    lines = [line.rstrip("\n") for line in f]

pprint(lines[:20])


# In[218]:
# Separate the input data into different sections.
bin_numbers_line = lines[8]
bins_lines = lines[:8][::-1]  # Reverse the order
moves_lines = lines[10:]

pprint(bins_lines)


# In[219]:
# Get the indices that align with the numbers in the bin_numbers line
bin_number_pos = [(m.start()) for m in re.finditer(r"\d", bin_numbers_line)]

# Grab only the bin numbers.
bin_numbers = re.findall(r"\d", bin_numbers_line)
print(bin_numbers)


# In[220]:
# Select the bin value in each bin line that aligns with the bin numbers.
starting_bins = [[line[index] for index in bin_number_pos] for line in bins_lines]
# Transpose the bins
starting_bins = [list(i) for i in zip(*starting_bins)]
starting_bins


# In[221]:
# Remove empty spaces from the bins.
starting_bins = [[letter for letter in bin if letter != " "] for bin in starting_bins]
# Zip together with the bin numbers.
starting_bins = dict(zip(bin_numbers, starting_bins))
starting_bins


# In[222]:


# Get the numbers from the move instructions (number_to_move, from, to).
move_nums = [re.findall(r"\d{1,2}", move) for move in moves_lines]
pprint(move_nums[:5])


# In[223]:
# Loop through and pop the end of the from list and add to the end of
# the to list.
bins = deepcopy(starting_bins)

for number_to_move, from_, to_ in move_nums:
    for box in range(int(number_to_move)):
        to_move = bins[from_].pop()
        bins[to_].append(to_move)

pprint(bins, compact=True)


# In[224]:
# Solution to part 1.
top_of_bins = "".join([v[-1] for v in bins.values()])
top_of_bins


# In[225]:
# Loop through and grab from the end of the from list and move to the
# to list.
bins = deepcopy(starting_bins)

for number_to_move, from_, to_ in move_nums:
    number_to_move = int(number_to_move)

    to_move = bins[from_][-number_to_move:]
    bins[from_] = bins[from_][:-number_to_move]
    bins[to_] += to_move

pprint(bins, compact=True)


# In[226]:
# Solution to part 2.
top_of_bins = "".join([v[-1] for v in bins.values()])
top_of_bins
