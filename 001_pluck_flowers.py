import redis

from algoredis_utils import *


def pluck_flowers(flowers_key: str) -> int:
  """Pluck the most flowers from an array of bouquets given constraints.

  You are at a flower store picking out buoqets. The bouquets are arranged in a row
  where `flowers[i]` represents the number of flowers in that bouquet. You can
  pick any bouquets subject to the constraint that you can't pick two bouquets that
  are next to each other, as that will leave too big of a gap in the shopkeeper''
  display.

    @flowers: [4, 5, 7, 3]

  The answer here is 11 since you can pick the 0th bouquet with 4 flowers and the
  2nd bouquet with 7 flowers for a total of 11.

  Args:
  * flowers_key: The key for the buoquets list.

  Returns:
  The maximum number of flowers you can
  """
  # print_all_variables()
  return None


run_pluck_flowers(pluck_flowers)
