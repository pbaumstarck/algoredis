import redis
import solutions

from algoredis_utils import *


def merge_sorted_lists(list_keys: list[str]):
  # Pointers into all the lists.
  red.delete('@js')
  red.rpush('@js', *([0] * len(list_keys)))

  red.delete('@merged')
  while True:
    # Sorted set for the minimum head element.
    red.delete('%min_elems')
    for i in range(red.llen('@js')):
      j = int(red.lindex('@js', i))
      if j < red.llen(list_keys[i]):
        red.zadd('%min_elems', {i: red.lindex(list_keys[i], j)})

    if not red.exists('%min_elems'):
      return '@merged'

    i = int(red.zrange('%min_elems', 0, 0)[0])
    j = int(red.lindex('@js', i))
    red.rpush('@merged', red.lindex(list_keys[i], j))
    red.lset('@js', i, j + 1)

  return '@merged'


run_merge_sorted_lists(merge_sorted_lists)
