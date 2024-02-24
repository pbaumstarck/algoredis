import redis

from algoredis_utils import *


def longest_unique_substring(str_key: str) -> int:
  """Find the longest unique substring in the given string.

  Given a string, find the longest substring that has only one occurrence of
  every character in it:

    str_key: "abcabcbb"
    Result: 3
    Since "abc" is the longest substring with all unique characters.

  Args:
  * str_key str: The key pointing to the string.

  Returns int: The length of the longest unique substring.
  """
  # print_all_variables()
  return -1


run_longest_unique_substring(longest_unique_substring)
