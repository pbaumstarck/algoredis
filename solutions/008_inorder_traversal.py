import redis
import solutions

from algoredis_utils import *


def inorder_traversal(head_key: str) -> str:
  red.delete('@traversal')
  if not head_key:
    return '@traversal'

  red.delete('@stack')
  red.rpush('@stack', head_key)
  while red.llen('@stack'):
    val = red.lpop('@stack')
    if not val.startswith('$'):
      # It's not a key, so it's a value we put in the stack; just emit it.
      red.rpush('@traversal', val)
    else:
      # Put (left)-(root value)-(right) on the stack for evaluation (via l-pushing).
      if red.hexists(val, 'right'):
        red.lpush('@stack', red.hget(val, 'right'))
      red.lpush('@stack', red.hget(val, 'val'))
      if red.hexists(val, 'left'):
        red.lpush('@stack', red.hget(val, 'left'))

  return '@traversal'


run_inorder_traversal(inorder_traversal)
