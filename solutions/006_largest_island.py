import redis
import solutions

from algoredis_utils import *

def largest_island(row_keys: list[str]) -> int:
  if not row_keys:
      return 0

  m = len(row_keys)
  n = red.llen(row_keys[0])

  # Start island indices from 2 to not conflict with 0 and 1.
  red.set('#island_ix', 2)
  # Map from island indices to size.
  red.delete('$island_sizes')
  # Sorted set to keep track of max island size.
  red.delete('%max_island_size')
  for r in range(m):
    for c in range(n):
      if red.lindex(row_keys[r], c) == '1':
        red.set('#island_size', 0)
        red.delete('@flood_fill')
        red.rpush('@flood_fill', *(r, c))
        while red.llen('@flood_fill'):
          rr, cc = map(int, red.lpop('@flood_fill', count=2))
          if red.lindex(row_keys[rr], cc) == '1':
            red.lset(row_keys[rr], cc, red.get('#island_ix'))
            red.incr('#island_size')
            if rr > 0:
              red.rpush('@flood_fill', *(rr - 1, cc))
            if rr + 1 < m:
              red.rpush('@flood_fill', *(rr + 1, cc))
            if cc > 0:
              red.rpush('@flood_fill', *(rr, cc - 1))
            if cc + 1 < n:
              red.rpush('@flood_fill', *(rr, cc + 1))

        # Save the size of the island and increment `island_ix`.
        red.hset('$island_sizes', red.get('#island_ix'), red.get('#island_size'))
        island_size = int(red.get('#island_size'))
        red.zadd('%max_island_size', {red.get('#island_ix'): island_size})
        red.incr('#island_ix')

  if not red.hlen('$island_sizes'):
    # No islands found, so just dredge one random tile.
    return 1

  # Now search for any merges we could get betwween islands using zeroes.
  for r in range(m):
    for c in range(n):
      if red.lindex(row_keys[r], c) == '0':
        red.delete('&neighbors')
        if r > 0:
          red.sadd('&neighbors', red.lindex(row_keys[r - 1], c))
        if r + 1 < m:
          red.sadd('&neighbors', red.lindex(row_keys[r + 1], c))
        if c > 0:
          red.sadd('&neighbors', red.lindex(row_keys[r], c - 1))
        if c + 1 < n:
          red.sadd('&neighbors', red.lindex(row_keys[r], c + 1))

        red.srem('&neighbors', '0')
        if red.scard('&neighbors'):
          merged_island_size = 1 + sum(map(int, [
            red.hget('$island_sizes', _) for _ in red.smembers('&neighbors')
          ]))
          red.zadd('%max_island_size', { str((r, c)): merged_island_size })

  return int(red.zrevrange('%max_island_size', 0, 0, withscores=True)[0][1])


run_largest_island(largest_island)
