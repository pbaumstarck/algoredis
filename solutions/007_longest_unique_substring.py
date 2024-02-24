import redis
import solutions

from algoredis_utils import *


def longest_unique_substring(str_key: str) -> int:
  s = red.get(str_key)

  # Count a pointer to the left-most index in the unique range.
  red.set('#left', 0)
  # Sorted set to count longest unique substring.
  red.delete('%max_len')
  red.zadd('%max_len', {0: 0})
  # Map with keys of characters and values of the last index that character was seen at.
  red.delete('$last_seen_ix')
  red.hset('$last_seen_ix', s[0], 0)

  # Iterate through the string.
  red.set('#right', 1)
  while int(red.get('#right')) < len(s):
    ch = s[int(red.get('#right'))]
    while red.hexists('$last_seen_ix', ch):
      # Must forget all characters up to here.
      red.hdel('$last_seen_ix', s[int(red.get('#left'))])
      red.incr('#left')

    # Record that we saw `ch` at `right`.
    red.hset('$last_seen_ix', ch, red.get('#right'))
    red.zadd('%max_len', {red.zcard('%max_len'): int(red.get('#right')) - int(red.get('#left')) + 1})
    red.incr('#right')

  return int(red.zrange('%max_len', -1, -1, withscores=True)[0][-1])


run_longest_unique_substring(longest_unique_substring)
