import redis

from algoredis_utils import *

"""Binary tree node representation:

  [1, 4, 9]

$node-0 {"val": 1, "left": "$node-1", "right": "$node-2"}
$node-1 {"val": 4}
$node-2 {"val": 9}

> red.hexists('$node-1', 'left')
# False
> red.hexists('$node-1', 'right')
# False
"""


def inorder_traversal(head_key: str) -> str:
  """Given the head of a binary search tree, return its in-order traversal.

  Each node in the tree is a key to a Redis hash map with fields "val" to
  its value, and "left" and "right" (optionally) to the keys of those child nodes,
  e.g.:

    red.hget('$node-0', 'val') => '1'
    red.hexists('$node-0', 'left') => True
    red.hreg('$node-0', 'left') => '$node-1'
    red.hexists('$node-0', 'right') => False

  Return the key to an array that holds the in-order traversal of the tree's values.

  Args:
  * head_key str: Redis key of the head node.

  Returns str: The key of the list holding the in-order traversal.
  """
  # print_all_variables()
  return None


run_inorder_traversal(inorder_traversal)
