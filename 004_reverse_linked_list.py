import redis

from algoredis_utils import *

"""Linked list representation:

  1 -> 4 -> 9

$node-0 {"val": 1, "next": "$node-1"}
$node-1 {"val": 4, "next": "$node-2"}
$node-2 {"val": 9}

> red.hexists('$node-2', 'next')
# False
"""


def reverse_linked_list(head_key: str) -> str:
  """Reverse the elements of a linked list.

  Each node in the linked list is a key to a Redis hash map with fields "val" to
  its value, and "next" (optionally) to the name of the next node. E.g.,

    red.hget('$node-0', 'val') => '1'
    red.hreg('$node-0', 'next') => '$node-1'

  Reverse the order of all the nodes and return the key of the new head node.
  Modify the list in place.

  Args:
  * head_key str: Redis key of the head node.

  Returns str: The key of the new head node in the reversed list.
  """
  # print_all_variables()
  return None


run_reverse_linked_list(reverse_linked_list)
