#!/usr/bin/env python
# coding: utf-8

# In[36]:
import re
from itertools import tee
from pprint import pprint

# In[8]:
# View file contents.
with open("input.txt") as f:
    signal = [line.rstrip("\n") for line in f][0]

pprint(signal)


# In[31]:
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def quadwise(iterable):
    "Return overlapping quads from an iterable."
    # quadwise('ABCDEFG') --> ABCD BCDE CDEF DEFG EFGH
    for ((a, b), (_, _)), ((_, _), (c, d)) in pairwise(pairwise(pairwise(iterable))):
        yield a, b, c, d


pprint(list(quadwise(signal))[:10])
# In[40]:
markers = [quad for quad in quadwise(signal) if len(set(quad)) == 4]
pprint(markers[:10])
# In[53]:
# Solution to part 1
first_marker = markers[0]
# Search finds the first match which is what we want.
match = re.search("".join(first_marker), signal)
match.end()
# In[54]:
from collections import deque
from itertools import islice


def get_distinct_items(iterable, n: int):
    """Yield each group of n distinct consecutive items in the iterable."""
    group = deque(islice(iterable, n))
    if len(set(group)) == n:
        yield list(group)

    for i in islice(iterable, n, None):
        group.popleft()
        group.append(i)
        if len(set(group)) == n:
            yield list(group)


message_markers = list(get_distinct_items(signal, 14))
print(message_markers[0])
# In[55]:
# Solution to part 2
first_message = message_markers[0]
match = re.search("".join(first_message), signal)
match.end()
