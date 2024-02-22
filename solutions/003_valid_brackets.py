import redis
import solutions

from algoredis_utils import *


def valid_brackets(str_key: str) -> bool:
  red.hset('closing_chars', mapping={'(': ')','{': '}','[': ']'})
  red.delete('stack')
  for ch in red.get(str_key):
    if ch in ('(', '[', '{'):
      red.rpush('stack', ch)
    elif ch not in (')', ']', '}'):
      continue
    elif not red.llen('stack'):
      return False
    elif red.hget('closing_chars', red.rpop('stack')) != ch:
      return False

  # Stack must be empty at the end.
  return not red.llen('stack')


run_valid_brackets(valid_brackets)
