import redis
import solutions

from algoredis_utils import *


def count_islands(row_keys: list[str]) -> int:
  red.set('#num_islands', 0)
  for r in range(len(row_keys)):
    for c in range(red.llen(row_keys[r])):
      if red.lindex(row_keys[r], c) == '1':
        red.delete('@flood_fill')
        red.rpush('@flood_fill', *(r, c))
        while red.llen('@flood_fill'):
          rr, cc = map(int, red.lpop('@flood_fill', count=2))
          if red.lindex(row_keys[rr], cc) == '1':
            red.lset(row_keys[rr], cc, '0')
            if rr > 0:
              red.rpush('@flood_fill', *(rr - 1, cc))
            if rr + 1 < len(row_keys):
              red.rpush('@flood_fill', *(rr + 1, cc))
            if cc > 0:
              red.rpush('@flood_fill', *(rr, cc - 1))
            if cc + 1 < red.llen(row_keys[r]):
              red.rpush('@flood_fill', *(rr, cc + 1))

        red.incr('#num_islands')

  return int(red.get('#num_islands'))


run_count_islands(count_islands)
