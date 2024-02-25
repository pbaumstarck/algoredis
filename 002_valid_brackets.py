import redis

from algoredis_utils import *


def valid_brackets(str_key: str) -> bool:
  """Determine if the brackets in a string are in a valid configuration.

  `str_key` will contain a simple string value containing brackets of "()",
  "[]", and "{}". Return true only if the brackets are in a valid configuration.

    str: 'foo(bar)'
    Returns: True

    str: 'foo(bar]'
    Returns: False

  Args:
  * str_key: The Redis key for the string being stored.

  Returns bool: For whether the brackest are valid.
  """
  # print_all_variables()
  return None


run_valid_brackets(valid_brackets)
