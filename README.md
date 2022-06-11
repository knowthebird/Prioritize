# Prioritize
A helper module for generating every possible string, within a range of lengths, from a set of substrings.  The order the strings are returned is determined by the order of substrings in the set.  This allows the user to "prioritize" the return of strings which are multiset permutations of higher priority substrings. Duplicates are not returned, including cases where substrings are multiset permutations of lower priority substrings.

It is most useful when you need to know the next highest priority in a list of every possible string, but to generate the entire list, store it, and then sort it would consume too much time or memory.  One example would be helping a password creacker to test every possible string in an order determined by priority, number of replacements, and order of substrings in the multiset permutation that each test password is formed from.

## Installation
Outside the standard library the module depends on sympy to generate multiset permutations.
```sh
sudo apt-get install python3-pip
sudo pip3 install sympy
```

## Usage
```python
from prioritize import prioritized_permutations

priorities = ["1st priority", "2nd priority", "3rd", "..."]
MIN_STRING_LENGTH = 4
MAX_STRING_LENGTH = 12
for result in prioritized_permutations(priorities,MIN_STRING_LENGTH,MAX_STRING_LENGTH):
    print(result)
```

See [examples.py](/examples.py) for other usage examples.

## Documentation and Resources
The module shall yield every string which can be made from the given set of substrings, per the following constraints:
  1. The length of each string yielded will be greater than or equal to the minimum length specified, and less than or equal to the maximum length specified.

The module shall yield strings in an order which conforms to the following constraints:
  1. Every permutation of a string (made from a multiset of substrings) is yielded before any string (made from a multiset of substrings) containing any substrings with a priority lower than the lowest priority substring of the string to yield.
  2. Permutations for the same multiset are yielded placing strings with the highest priority substring closest to furthest the begining of the string.
  3. Combinations with n replacements from equal sets of substrings are returned with n increasing. (Note: So shorter strings closer matching the original priorities are considered higher priority than longer strings with multiple occuraces of one ore more priorities.)

Order of priority is determined by the order of the priorities provided. This order is similar to, but not the same as lexigraphical order.

Duplicate values may be generated but will not be returned. Duplicates are only generated when a substring can be formed from a combination of lower priority substrings. Duplicates are prevented from being returned by determining what the highest priorities are the current string could be made from and checking if the priorities used to generate the current string match. This has the benefit of not needing to record which strings have already been generated.  This could be further optimized by making the algorithm check if duplicates are possible before checking for them.

## License
This module is distributed under the [MIT License](/LICENSE).
