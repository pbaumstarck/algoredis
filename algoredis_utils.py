
import redis

red = redis.Redis(host='localhost', port=6379, decode_responses=True)
red.flushall()


def _inter_variables(**kwargs):
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
    is_escaped = key[0] in ('@', '#', '%', '$', '&',)
    # if key[0] == '*':
    #   # It's an escape, so just add the arg literally without going through Redis.
    #   actual_args.append(value)
    if isinstance(value, list):
      if key[0] == '!':
        # Linked list.
        actual_args.append(_create_linked_list('$' + key[1:], value))
      elif value and isinstance(value[0], list):
        # Nested lists.
        actual_args.append([])
        for i in range(len(value)):
          sub_key = (key if is_escaped else '@' + key) + '-' + str(i)
          actual_args[-1].append(sub_key)
          red.delete(sub_key)
          if value[i]:
            red.rpush(sub_key, *value[i])
      else:
        actual_args.append(key if is_escaped else '@' + key)
        red.delete(actual_args[-1])
        if value:
          red.rpush(actual_args[-1], *value)
    elif isinstance(value, (int, float)):
      actual_args.append(key if is_escaped else '#' + key)
      red.delete(actual_args[-1])
      red.set(actual_args[-1], value)
    elif isinstance(value, dict) and all(isinstance(_, (int, float)) for _ in value.values()):
      actual_args.append(key if is_escaped else '%' + key)
      red.delete(actual_args[-1])
      red.zadd(actual_args[-1], value)
    elif isinstance(value, dict):
      actual_args.append(key if is_escaped else '$' + key)
      red.delete(actual_args[-1])
      for k, v in value.items():
        red.hset(actual_args[-1], k, v)
    elif isinstance(value, set):
      actual_args.append(key if is_escaped else '&' + key)
      red.delete(actual_args[-1])
      for v in value:
        red.sadd(actual_args[-1], v)
    else:
      # Treat it as a simple literal.
      actual_args.append(key)
      red.set(actual_args[-1], value)

  return actual_args

inter_variables = _inter_variables

def _get_variable(key):
  """Retrieves a valuable by appropriate type from Redis."""
  def list_convenience(values):
    if isinstance(values, list) and all(_.lstrip('-').isdigit() for _ in values):
      return list(map(int, values))
    else:
      return values

  if key is None:
    return None
  elif key[0] == '@':
    return list_convenience(red.lrange(key, 0, -1))
  elif key[0] == '$':
    return red.hgetall(key)
  elif key[0] == '%':
    return red.zrange(key, 0, -1, withscores=True)
  elif key[0] == '&':
    return red.smembers(key)
  else:
    return red.get(key)


def print_all_variables():
  # Prints all the variables in Redis according to proper type.
  for key in sorted(red.keys()):
    print('%s:' % key, _get_variable(key))


def _create_linked_list(prefix_key, items):
  """Creates a linked list and returns the head key."""
  head_key = None
  last_key = None
  for i in range(len(items)):
    key = '%s-node-%d' % (prefix_key, i)
    red.delete(key)
    red.hset(key, 'val', items[i])
    if last_key is not None:
      red.hset(last_key, 'next', key)

    if head_key is None:
      head_key = key
    last_key = key

  return head_key


def _read_linked_list(head_key):
  """Reads all the values in a linked list."""
  lst = []
  ptr = head_key
  while ptr:
    lst.append(red.hget(ptr, 'val'))
    ptr = red.hget(ptr, 'next')

  if all(_.lstrip('-').isdigit() for _ in lst):
    lst = list(map(int, lst))

  return lst


def run_tests(name=None, eval_fn=None, test_cases=None, return_fn=None):
  num_passes = 0
  num_failures = 0
  print('\n' + (name if name else ''))
  for fn_kwargs, expected in test_cases:
    actual_args = _inter_variables(**fn_kwargs)
    return_actual = eval_fn(*actual_args)
    if return_fn:
      print('return_actual', return_actual)
      return_actual = return_fn(return_actual)

    print_args = [fn_kwargs]

    result = return_actual == expected
    print_args.extend(['expected:', expected, '- actual:', return_actual])

    result_str = ''
    if result:
      result_str = 'Correct.'
      num_passes += 1
    else:
      result_str = '*** FAILED ***'
      num_failures += 1

    print_args.extend([' --- result:', result_str])
    print(*print_args)
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


def run_merge_sorted_lists(eval_fn):
  return run_tests(
    name='Merge Sorted Lists',
    eval_fn=eval_fn,
    test_cases=[
      ({'list_keys': [[1,4,5],[1,3,4]]}, [1,1,3,4,4,5]),
      ({'list_keys': [[1,4,5],[1,3,4]]}, [1,1,3,4,4,5]),
      ({'list_keys': [[],[4,5,6,7]]}, [4,5,6,7]),
      ({'list_keys': [[4,5,6,7,8],[]]}, [4,5,6,7,8]),
      ({'list_keys': [[8,9,10],[-4,-3,-2,0]]}, [-4,-3,-2,0,8,9,10]),
      ({'list_keys': [[-100,101],[-200,202]]}, [-200,-100,101,202]),
    ],
    return_fn=_get_variable)


def run_valid_brackets(eval_fn):
  return run_tests(
    name='Valid Brackets',
    eval_fn=eval_fn,
    test_cases=[
      ({'str': '()'}, True),
      ({'str': 'a(b)'}, True),
      ({'str': '()[]{}'}, True),
      ({'str': '(]'}, False),
      ({'str': '[[[{{{999(((000)))}}}]]]'}, True),
      ({'str': '[[[{{{999(((000)))]]]}}}'}, False),
      ({'str': 'asdf[qwerty()zxcv{}]'}, True),
      ({'str': 'asdf[qwerty()zxcv{}yuiop'}, False),
      ({'str': '   no_bracket_at_all   '}, True),
      ({'str': ''}, True),
    ])


def run_reverse_linked_list(eval_fn):
  return run_tests(
    name='Reverse Linked list',
    eval_fn=eval_fn,
    test_cases=[
      ({'!list': [1, 2, 3, 4, 5]}, [5, 4, 3, 2, 1]),
      ({'!list': [1, 5, 3, 2, 4]}, [4, 2, 3, 5, 1]),
      ({'!list': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
      ({'!list': [1]}, [1]),
    ],
    return_fn=_read_linked_list)


def run_count_islands(eval_fn):
  return run_tests(
    name='Count Islands',
    eval_fn=eval_fn,
    test_cases=[
      ({'rows': [
        list('1100'),
        list('1000'),
        list('1000')
        ]}, 1),
      ({'rows': [
        list('00000'),
        list('00000'),
        list('00000')
        ]}, 0),
      ({'rows': [
        list('10101'),
        list('01010'),
        list('10101')
        ]}, 8),
      ({'rows': [
        list('1100111'),
        list('1011111'),
        list('1011111')
        ]}, 2),
      ({'rows': [
        list('000000110000001100'),
        list('000011111001111100'),
        list('000000111111000100'),
        list('001000110000000000'),
        list('011100110001110011'),
        list('011110000111001110'),
        list('000111111110000000'),
        ]}, 3),
    ])


def run_largest_island(eval_fn):
  return run_tests(
    name='Largest Island',
    eval_fn=eval_fn,
    test_cases=[
      ({'rows': [
        list('1100'),
        list('1000'),
        list('1000')
        ]}, 5),
      ({'rows': [
        list('00000'),
        list('00000'),
        list('00000')
        ]}, 1),
      ({'rows': [
        list('10101'),
        list('01010'),
        list('10101')
        ]}, 5),
      ({'rows': [
        list('1100111'),
        list('1011111'),
        list('1011111')
        ]}, 18),
      ({'rows': [
        list('000000110000001100'),
        list('000011111001111100'),
        list('000000111111000100'),
        list('001000110000000000'),
        list('011100110001110011'),
        list('011110000111001110'),
        list('000111111110000000'),
        ]}, 48),
    ])


def run_longest_unique_substring(eval_fn):
  return run_tests(
    name='Longest Unique Substring',
    eval_fn=eval_fn,
    test_cases=[
      ({'str': 'abcabcbb'}, 3),
      ({'str': 'bbbbb'}, 1),
      ({'str': 'pwwkew'}, 3),
      ({'str': 'abcdaaaaaaaabcde'}, 5),
      ({'str': 'asdf[qwerty()zxcv{}]'}, 20),
      ({'str': 'qqqqqqqqqqqqqqqqq'}, 1),
    ])
