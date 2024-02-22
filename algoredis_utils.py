
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
    is_escaped = key[0] in ('@', '#', '%', '$')
    if key[0] == '*':
      # It's an escape, so just add the arg literally without going through Redis.
      actual_args.append(value)
    elif isinstance(value, list):
      if value and isinstance(value[0], list):
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
    else:
      # Treat it as a simple literal.
      actual_args.append(key)
      red.set(actual_args[-1], value)

  return actual_args


def _get_variable(key):
  """Retrieves a valuable by appropriate type from Redis."""
  if key[0] == '@':
    values = red.lrange(key, 0, -1)
    # Convert numbers as a convenience.
    if values and all(_.lstrip('-').isdigit() for _ in values):
      return list(map(int, values))
  elif key[0] == '$':
    return red.hgetall(key)
  elif key[0] == '%':
    return red.zrange(key, 0, -1, withscores=True)
  else:
    return red.get(key)


def print_all_variables():
  # Prints all the variables in Redis according to proper type.
  for key in red.keys():
    print('%s:' % key, _get_variable(key))


def _create_linked_list(lst):
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


def _urnoll_linked_list(head_key):
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
  for fn_kwargs, expected, verifiers in test_cases:
    actual_args = _inter_variables(**fn_kwargs)
    actual = eval_fn(*actual_args)

    print_args = [fn_kwargs]

    result = True
    if expected is not None:
      result = actual == expected
      print_args.extend(['expected:', expected, '- actual:', actual])
    else:
      for key, value in verifiers.items():
        value_actual = _get_variable(key)
        print_args.extend(['expected ' + key + ':', value, '- actual:', value_actual])
        result &= value == value_actual

    result_str = ''
    if result:
      result_str = 'Correct.'
      num_passes += 1
    else:
      result_str = '*** FAILED ***'
      num_failures += 1

    print_args.extend([' --- result:', result_str])
    print(*print_args)
    # print(fn_kwargs, 'expected:', expected, '- answer:', actual, ' - result:', result_str)
    # TODO: Capture stdout on failure and print it.

  print('\nPassed %d / %d' % (num_passes, num_passes + num_failures))
  return num_passes, num_failures


def run_pluck_flowers(eval_fn):
  return run_tests(
    name='Pluck Flowers',
    eval_fn=eval_fn,
    test_cases=[
      ({'flowers': [4,5,7,3]}, 11, None),
      ({'flowers': [2,7,9,3,1]}, 12, None),
      ({'flowers': [10,1,10,10,1,10]}, 30, None),
      ({'flowers': [1,2,1,2,1,2,1,2,1]}, 8, None),
      ({'flowers': [3, 4, 10, 10, 8, 5, 9, 2, 3, 0, 4, 1, 3]}, 40, None),
      ({'flowers': [1, 3, 9, 3, 1, 1, 4]}, 15, None),
      ({'flowers': [7, 3, 9, 3, 2, 0, 6, 0, 9, 4, 9, 0, 5, 8]}, 50, None),
      ({'flowers': [1, 9, 7, 9, 6, 2, 1, 1, 4]}, 24, None),
      ({'flowers': [2, 0, 4, 3, 7, 4, 8, 9, 6, 8, 8]}, 35, None),
      ({'flowers': [9, 9, 4, 8, 8, 8, 1, 3, 6, 4, 1]}, 32, None),
    ])


def run_merge_sorted_lists(eval_fn):
  return run_tests(
    name='Merge Sorted Lists',
    eval_fn=eval_fn,
    test_cases=[
      ({'list_keys': [[1,4,5],[1,3,4]], '@solution': []}, None, {'@solution': [1,1,3,4,4,5]}),
      ({'list_keys': [[],[4,5,6,7]], '@solution': []}, None, {'@solution': [4,5,6,7]}),
      ({'list_keys': [[4,5,6,7,8],[]], '@solution': []}, None, {'@solution': [4,5,6,7,8]}),
      ({'list_keys': [[8,9,10],[-4,-3,-2,0]], '@solution': []}, None, {'@solution': [-4,-3,-2,0,8,9,10]}),
      ({'list_keys': [[-100,101],[-200,202]], '@solution': []}, None, {'@solution': [-200,-100,101,202]}),
    ])

  # print('')
  # list_keys = []
  # for i in range(len(lists)):
  #   list_i_key = 'list-%d' % i
  #   list_keys.append(list_i_key)
  #   red.delete(list_i_key)
  #   if lists[i]:
  #     red.rpush(list_i_key, *lists[i])

  # check_result(lambda: merge_sorted_lists(list_keys), expected, 'lists', lists)


def run_valid_brackets(eval_fn):
  return run_tests(
    name='Valid Brackets',
    eval_fn=eval_fn,
    test_cases=[
      ({'str': '()'}, True, None),
      ({'str': 'a(b)'}, True, None),
      ({'str': '()[]{}'}, True, None),
      ({'str': '(]'}, False, None),
      ({'str': '[[[{{{999(((000)))}}}]]]'}, True, None),
      ({'str': '[[[{{{999(((000)))]]]}}}'}, False, None),
      ({'str': 'asdf[qwerty()zxcv{}]'}, True, None),
      ({'str': 'asdf[qwerty()zxcv{}yuiop'}, False, None),
      ({'str': '   no_bracket_at_all   '}, True, None),
      ({'str': ''}, True, None),
    ])
