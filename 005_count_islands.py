import redis

from algoredis_utils import *


def count_islands(row_keys: str) -> str:
  """Count the number of islands in a grid of zeroes and ones.

  You are given a list of keys to rows in a grid, with "0" representing water
  and "1" representing land. An island counts as any land connected vertically
  or horizontally (4-neighborhood), not diagonally. Return the count of number
  of islands on the map.

    row-key0: [1, 1, 0]
    row-key1: [1, 0, 0]
    row-key2: [1, 0, 0]

  This should return 1 for there being one island.

  Args:
  * row_keys str: Redis keys of the rows of the grid.

  Returns int: The number of islands found
  """
  # print_all_variables()
  return 0
  

run_count_islands(count_islands)
