# Prioritize
A module with functions to generate permutations in order of a given list of priorities.

## Usage
```python
from prioritize import prioritized_permutations

priorities = ["1st priority", "2nd priority", "3rd", "..."]
MIN_STRING_LENGTH = 4
MAX_STRING_LENGTH = 12
for result in prioritized_permutations(priorities,MIN_STRING_LENGTH,MAX_STRING_LENGTH):
    print(result)
```

See [testing_scratch_pad.py](/testing_scratch_pad.py) for other usage examples.

## Documentation and Resources
Generates strings for each multiset permutation for each possible
combination (with replacement, that would result in a string of length
within the min and max length specified) of a given set of priorities,
in order of their priority. Order of priority is determined by the order
of the priorities provided. This order is similar to, but not the same
as lexigraphical order. It is optimized such that any version of a
string containing a given set of priorities will be yielded before a
string containing lower priorities. Permutations for a given
combination are returned with the highest priorities occuring in the
string first. Combinations with n replacements of equal sets of priorities
are returned shortest to longest (for the final resulting string length).

Duplicate values may be generated but will not be returned.
Duplicates are only generated when a priority can be formed from a
combination of one or more lower priorities.

**TODO:** Make the algorithm check if duplicates are possible before checking for them

Duplicates are prevented from being returned by determining what the
highest priorities are the current string could be made from and
checking if the priorities used to generate the current string match.
This has the benefit of not requiring a recording of which strings have
already been generated.

**TODO:** Need to find out what that kind of ordering is called...

The originally intended application was generating strings for password
crackers, such that a complete word list did not need to be generated,
stored, and sorted in order to optimize it.

## License
This module is distributed under the [MIT License](/LICENSE).
