
import redis

red = redis.Redis(host='localhost', port=6379, decode_responses=True)


def inter_variables(**kwargs):
  """Creates variables in Redis and returns their keys.

  Values are passed in a dictionary, with the key used as the base for the Redis name.
  Lists are prefixed with '@', maps with '$', sorted sets with '%', and numeric
  values with '#' for semi-Hungarian notation.

  Kwargs:
  * kwargs: The dictionary of values to insert.

  Returns list(str): The keys used for each variable in an array parallel to the entries of
  """
  actual_args = []
  for key, value in kwargs.items():
    if isinstance(value, list):
      actual_args.append('@' + key)
      red.delete(actual_args[-1])
      red.rpush(actual_args[-1], *value)
    elif isinstance(value, (int, float)):
      actual_args.append('#' + key)
      red.delete(actual_args[-1])
      red.set(actual_args[-1], value)
    elif isinstance(value, dict) and all(isinstance(_, (int, float)) for _ in value.values()):
      actual_args.append('%' + key)
      red.delete(actual_args[-1])
      red.zadd(actual_args[-1], value)
    elif isinstance(value, dict):
      actual_args.append('$' + key)
      red.delete(actual_args[-1])
      for k, v in value.items():
        red.hset(actual_args[-1], k, v)
    else:
      # Treat it as a simple literal.
      actual_args.append(key)
      red.set(actual_args[-1], value)

  return actual_args


def print_all_variables():
  # Prints all the variables in Redis according to proper type.
  for key in red.keys():
    if key[0] == '@':
      print('%s:' % key, red.lrange(key, 0, -1))
    elif key[0] == '$':
      print('%s:' % key, red.hgetall(key))
    elif key[0] == '%':
      print('%s:' % key, red.zrange(key, 0, -1, withscores=True))
    else:
      print('%s:' % key, red.get(key))


def create_linked_list(lst):
  head_key = None
  last_key = None
  for i in range(len(lst)):
    key = 'node-%d' % i
    red.delete(key)
    red.hset(key, 'val', lst[i])
    if last_key is not None:
      red.hset(last_key, 'next', key)

    if head_key is None:
      head_key = key
    last_key = key

  return head_key


def urnoll_linked_list(head_key):
    lst = []
    ptr = head_key
    while ptr:
      lst.append(int(red.hget(ptr, 'val')))
      ptr = red.hget(ptr, 'next')

    return lst


def run_tests(name=None, eval_fn=None, test_cases=None):
  num_passes = 0
  num_failures = 0
  print('\n' + (name if name else ''))
  for fn_kwargs, expected in test_cases:
    actual_args = inter_variables(**fn_kwargs)
    actual = eval_fn(*actual_args)
    result_str = ''
    if actual == expected:
      result_str = 'Correct.'
      num_passes += 1
    else:
      result_str = '*** FAILED ***'
      num_failures += 1

    print(fn_kwargs, 'expected:', expected, '- answer:', actual, ' - result:', result_str)
    # TODO: Capture stdout on failure and print it.

  print('\nPassed %d / %d' % (num_passes, num_passes + num_failures))
  return num_passes, num_failures


def run_pluck_flowers(eval_fn):
  return run_tests(
    name='Pluck Flowers',
    eval_fn=eval_fn,
    test_cases=[
      ({'flowers': [4,5,7,3]}, 11),
      ({'flowers': [2,7,9,3,1]}, 12),
      ({'flowers': [10,1,10,10,1,10]}, 30),
      ({'flowers': [1,2,1,2,1,2,1,2,1]}, 8),
      ({'flowers': [3, 4, 10, 10, 8, 5, 9, 2, 3, 0, 4, 1, 3]}, 40),
      ({'flowers': [1, 3, 9, 3, 1, 1, 4]}, 15),
      ({'flowers': [7, 3, 9, 3, 2, 0, 6, 0, 9, 4, 9, 0, 5, 8]}, 50),
      ({'flowers': [1, 9, 7, 9, 6, 2, 1, 1, 4]}, 24),
      ({'flowers': [2, 0, 4, 3, 7, 4, 8, 9, 6, 8, 8]}, 35),
      ({'flowers': [9, 9, 4, 8, 8, 8, 1, 3, 6, 4, 1]}, 32),
    ])
