import redis
import solutions

from algoredis_utils import *


def reverse_linked_list(head_key: str) -> str:
  if not head_key:
    return None

  red.set('ptr', head_key)
  red.delete('reverse_ptr')
  while red.get('ptr'):
    ptr = red.get('ptr')
    ptr_next = red.hget(ptr, 'next')
    if red.get('reverse_ptr'):
      red.hset(ptr, 'next', red.get('reverse_ptr'))
    else:
      red.hdel(ptr, 'next')

    red.set('reverse_ptr', ptr)

    if ptr_next:
      red.set('ptr', ptr_next)
    else:
      red.delete('ptr')

  return red.get('reverse_ptr')


run_reverse_linked_list(reverse_linked_list)
