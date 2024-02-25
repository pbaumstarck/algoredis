# algoredis
Algorithms challenges for sharpening your Redis skills.

## Getting Started

Install Redis

```
% brew install redis
% pip install redis-cli
% redis-server
```

Test each problem individually:

```
% python3 001_pluck_flowers.py

Pluck Flowers
{'flowers': [4, 5, 7, 3]} expected: 11 - actual: None  --- result: *** FAILED ***
{'flowers': [2, 7, 9, 3, 1]} expected: 12 - actual: None  --- result: *** FAILED ***
{'flowers': [10, 1, 10, 10, 1, 10]} expected: 30 - actual: None  --- result: *** FAILED ***
{'flowers': [1, 2, 1, 2, 1, 2, 1, 2, 1]} expected: 8 - actual: None  --- result: *** FAILED ***
{'flowers': [3, 4, 10, 10, 8, 5, 9, 2, 3, 0, 4, 1, 3]} expected: 40 - actual: None  --- result: *** FAILED ***
{'flowers': [1, 3, 9, 3, 1, 1, 4]} expected: 15 - actual: None  --- result: *** FAILED ***
{'flowers': [7, 3, 9, 3, 2, 0, 6, 0, 9, 4, 9, 0, 5, 8]} expected: 50 - actual: None  --- result: *** FAILED ***
{'flowers': [1, 9, 7, 9, 6, 2, 1, 1, 4]} expected: 24 - actual: None  --- result: *** FAILED ***
{'flowers': [2, 0, 4, 3, 7, 4, 8, 9, 6, 8, 8]} expected: 35 - actual: None  --- result: *** FAILED ***
{'flowers': [9, 9, 4, 8, 8, 8, 1, 3, 6, 4, 1]} expected: 32 - actual: None  --- result: *** FAILED ***

Passed 0 / 10
```

Check the references solution in the `solutions/` directory:

```
% python3 solutions/001_pluck_flowers.py

Pluck Flowers
{'flowers': [4, 5, 7, 3]} expected: 11 - actual: 11  --- result: Correct.
{'flowers': [2, 7, 9, 3, 1]} expected: 12 - actual: 12  --- result: Correct.
{'flowers': [10, 1, 10, 10, 1, 10]} expected: 30 - actual: 30  --- result: Correct.
{'flowers': [1, 2, 1, 2, 1, 2, 1, 2, 1]} expected: 8 - actual: 8  --- result: Correct.
{'flowers': [3, 4, 10, 10, 8, 5, 9, 2, 3, 0, 4, 1, 3]} expected: 40 - actual: 40  --- result: Correct.
{'flowers': [1, 3, 9, 3, 1, 1, 4]} expected: 15 - actual: 15  --- result: Correct.
{'flowers': [7, 3, 9, 3, 2, 0, 6, 0, 9, 4, 9, 0, 5, 8]} expected: 50 - actual: 50  --- result: Correct.
{'flowers': [1, 9, 7, 9, 6, 2, 1, 1, 4]} expected: 24 - actual: 24  --- result: Correct.
{'flowers': [2, 0, 4, 3, 7, 4, 8, 9, 6, 8, 8]} expected: 35 - actual: 35  --- result: Correct.
{'flowers': [9, 9, 4, 8, 8, 8, 1, 3, 6, 4, 1]} expected: 32 - actual: 32  --- result: Correct.

Passed 10 / 10
```

## Rules of the Challenge

### Rule #1. All l-values must be stored in Redis

L-values are any values that can be modified, and using local variables for this purpose is disallowed:

```python
# ILLEGAL
index = 0
index += 1
```

Instead all l-values must be stored in Redis:

```python
red.set('index', 0)
red.incr('index')
```

### Rule #2. All l-values must be modified natively on Redis

This is to make sure people aren't cheating by taking variables out of Redis, modifying them locally, and then pushing them back:

```python
# ILLEGAL
red.rpush('array', *[1, 2, 3, 4]
popped = red.lindex('array', -1)
red.rpush('new_array', *red.lrange('array', 0, -2))
red.rename('new_array', 'array')
```

Instead one must use the native Redis functions to do the edits (this ensures you are actually using the syntax):

```python
red.rpush('array', *[1, 2, 3, 4])
popped = red.rpop('array')
```

### Rule #3. Local variables are still allowed if they're constant

You can still use local variables if they never change, including for and comprehension variables:

```python
# Allowed
for i in range(red.llen('array')):
  value = red.lindex('array', i)
  if value > 0:
    red.rpush('positive', value)

non_positive = sum(elem <= 0 for elem in red.lrange('array', 0, -1))
```

### Rule #4. All function parameters must be Redis keys or constants

This is to make sure one cannot use the arguments of a recursive function to simulate a stack and supplant a Redis data structure:

```python
# ILLEGAL
def recursive(index: int):
  if red.lindex('array', index):
    recursive(index + 1)
```

Instead:

```python
red.delete('@stack')
red.rpush('@stack', index)
while red.llen('@stack'):
  index = red.lpop('@stack')
  # ...
  red.rpush('@stack', index + 1)
```
