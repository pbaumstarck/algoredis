import redis
import solutions

from algoredis_utils import *


def pluck_flowers(flowers_key: str) -> int:
  red.set('#do_pick', red.lindex(flowers_key, 0))
  red.set('#dont_pick', 0)
  for i in range(1, red.llen(flowers_key)):
    red.set('#new_dont', max(int(red.get('#do_pick')), int(red.get('#dont_pick'))))
    red.set('#do_pick', int(red.lindex(flowers_key, i)) + int(red.get('#dont_pick')))
    red.rename('#new_dont', '#dont_pick')

  return max(int(red.get('#do_pick')), int(red.get('#dont_pick')))


run_pluck_flowers(pluck_flowers)
