import redis
import solutions

from algoredis_utils import *


def merge_sorted_lists(list_keys: list[str], output_key: str):
  # Pointers into all the lists.
  red.delete('@ixes')
  red.rpush('@ixes', *([0] * len(list_keys)))

  red.delete(output_key)
  while True:
    # Sorted set for the minimum head element.
    red.delete('%min_elems')
    for i in range(red.llen('@ixes')):
      ix = int(red.lindex('@ixes', i))
      if ix < red.llen(list_keys[i]):
        red.zadd('%min_elems', {i: red.lindex(list_keys[i], ix)})

    if not red.exists('%min_elems'):
      return

    i = int(red.zrange('%min_elems', 0, 0)[0])
    ix = int(red.lindex('@ixes', i))
    red.rpush(output_key, red.lindex(list_keys[i], ix))
    red.lset('@ixes', i, ix + 1)


run_merge_sorted_lists(merge_sorted_lists)
