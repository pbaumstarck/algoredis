import redis
import solutions

from algoredis_utils import *


def pluck_flowers(flowers_key: str) -> int:
  red.set('#do', red.lindex(flowers_key, 0))
  red.set('#dont', 0)
  for i in range(1, red.llen(flowers_key)):
    red.set('new_dont', max(int(red.get('#do')), int(red.get('#dont'))))
    red.set('#do', int(red.lindex(flowers_key, i)) + int(red.get('#dont')))
    red.rename('new_dont', '#dont')

  return max(int(red.get('#do')), int(red.get('#dont')))


run_pluck_flowers(pluck_flowers)
