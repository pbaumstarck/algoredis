import redis

from algoredis_utils import *


def largest_island(row_keys: list[str]) -> int:
  """Find the largest island possible by dredging up a single piece of ocean.

  You are given a grid map with '0' representing ocean and '1' representing land.
  With the ability to dredge up just one ocean tile and turn it into land, find
  the size of the largest island you can create. Island's are patches of land that
  are connected vertically and horizontally (4-connected neighborhood, not
  diagonally). Example:

    $grid-0: 1100
    $grid-1: 1001
    $grid-2: 0111

  Answer: dredge up (2, 0) or (1, 1) to produce an island of size 8.

  Args:
  * row_keys list[str]: The keys to the rows of the island.

  Returns int: The size of the largest island.
  """
  # print_all_variables()
  return -1


run_largest_island(largest_island)
