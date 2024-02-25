import redis
import solutions

from algoredis_utils import *


def binary_tree_depth(head_key: str) -> str:
  if not head_key:
    return 0

  red.delete('@stack')
  red.rpush('@stack', *(head_key, 1))
  red.delete('%max_depth')
  while red.llen('@stack'):
    node_key, depth = red.lpop('@stack', count=2)
    red.zadd('%max_depth', {node_key: int(depth)})
    if red.hexists(node_key, 'left'):
      red.rpush('@stack', *(red.hget(node_key, 'left'), int(depth) + 1))
    if red.hexists(node_key, 'right'):
      red.rpush('@stack', *(red.hget(node_key, 'right'), int(depth) + 1))

  return int(red.zrevrange('%max_depth', 0, 0, withscores=True)[0][1])


run_binary_tree_depth(binary_tree_depth)
