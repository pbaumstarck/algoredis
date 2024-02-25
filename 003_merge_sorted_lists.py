import redis

from algoredis_utils import *


def merge_sorted_lists(list_keys: list[str]):
  """Merge the sorted lists whose keys are given.

  You are given several keys pointing to sorted lists in Redis:

    @list_keys-0: [1, 4, 5]
    @list_keys-1: [1, 3, 4]

  You are also given the key of an empty destination list:

    @solution: []

  Merge the given input lists into the output list `@solution` in sorted order:

    @solution: [1, 1, 3, 4, 4, 5]

  You can modify any of the input lists.

  Args:
  * list_keys: The keys for the lists in Redis to sort.
  * output_key: The key to write the results into.

  Returns str: The head of the merged linked list.
  """
  # print_all_variables()
  pass


run_merge_sorted_lists(merge_sorted_lists)
