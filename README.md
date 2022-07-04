# Prioritize
A helper module for generating every possible string, within a range of lengths, from a set of substrings.  The order the strings are returned is determined by the order of substrings in the set.  This allows the user to "prioritize" the return of strings which are multiset permutations of higher priority substrings. Duplicates are not returned, including cases where substrings are multiset permutations of lower priority substrings.

It is most useful when you need to know the next highest priority in a list of every possible string, but to generate the entire list, store it, and then sort it would consume too much time or memory.  One example would be helping a password cracker to test every possible string in an order determined by priority, number of replacements, and order of substrings in the multiset permutation that each test password is formed from.

## Installation
Outside the standard library the module depends on sympy to generate multiset permutations.
```sh
sudo apt-get install python3-pip
sudo pip3 install sympy
```

## Usage
```python
from prioritize import prioritized_permutations

priorities = ["Top","Second","Last"]
MIN_STRING_LENGTH = 1
MAX_STRING_LENGTH = 13
for result in prioritized_permutations(priorities,MIN_STRING_LENGTH,MAX_STRING_LENGTH):
    print(result)
```
Will return:
```
Top
TopTop
TopTopTop
TopTopTopTop
TopSecond
SecondTop
TopTopSecond
TopSecondTop
SecondTopTop
TopSecondLast
TopLastSecond
SecondTopLast
SecondLastTop
LastTopSecond
LastSecondTop
TopLast
LastTop
TopTopLast
TopLastTop
LastTopTop
TopLastLast
LastTopLast
LastLastTop
TopTopTopLast
TopTopLastTop
TopLastTopTop
LastTopTopTop
Second
SecondSecond
SecondLast
LastSecond
Last
LastLast
LastLastLast
```


See [examples.py](/examples.py) for other usage examples.

## Documentation and Resources
The module shall yield every string which can be made from the given set of substrings, per the input length constraints [1]. The sequence of emitting a string is as follows:
* The next unique combination of indexes for the substrings is emitted in lexicographic ordering from the input set of priorites. [2]
* The next combination with replacements (allowing individual elements to be repeated n times) from the input combination is emitted as a multiset in lexicographic ordering according to the order of the input combination. [3]
* The next unique permutation of the multiset is generated in lexicographic order
* The string is emmited from joining the substrings according to input multiset permutation of substring indexes.
* The first possible multiset permutation which could emit the input string is determined.
* If the first possible multiset permutation which could emit the current string is the same multiset permutation used to generate the string, the string is returned, and otherwise ignored as a duplicate. [4]


1. There is a cleaning function to first detect duplicates, and remove substrings which are too long or redundant prior to using this.  
2. There is also a check for if final string length would exceed length constraints, in which case the next valid unique combination is emitted. The total possible unique combinations of a set of n substrings will be 2<sup>n</sup>-1, as we can ignore the case where no values are used.
Where Combinations = {Combination<sub>0</sub>, Combination<sub>1</sub>, Combination<sub>...</sub>, Combination<sub>2<sup>n</sup>-1</sub>}, the indexes of substrings which are tested can be found using the following function: Combination<sub>i</sub> = f(i,n)
```python
def f(i, n):
  if i == 0:
      return [0]
  elif i < 2**(n-1):
      return [0]+[x+1 for x in f(i-1, n-1)]
  else:
      return [x+1 for x in f(i-2**(n-1), n-1)]
```
Example of the unique combinations to test generated with four priorities (which could all meet the length constraints).
| i  | f(i,n) n = 4 |
|----|--------------|
| 1  | [0]          |
| 2  | [0, 1]       |
| 3  | [0, 1, 2]    |
| 4  | [0, 1, 2, 3] |
| 5  | [0, 1, 3]    |
| 6  | [0, 2]       |
| 7  | [0, 2, 3]    |
| 8  | [0, 3]       |
| 9  | [1]          |
| 10 | [1, 2]       |
| 11 | [1, 2, 3]    |
| 12 | [1, 3]       |
| 13 | [2]          |
| 14 | [2, 3]       |
| 15 | [3]          |

3. Every combination of n elements is tested before increasing n.  N is increased from 1 to the maximum times a substring could generate a valid string (shorter strings are ranked higher/returned sooner).  Final combinations are checked for valid string length before emitting to generate permutations.
4. Duplicates are only generated when a substring can be formed from a combination of substrings with a higer index in the set (lower priority substrings). The method used catches these duplicates without needing to record which strings have already been generated. This could be further optimized by making the module check if duplicates are possible at different stages before requiring a check for them.

The results of the overall ordering ensures top priorities are test returned first.  Ordering the priorities in lexicographical order does not mean the results are in lexicographical order.  See below for an example of running the module with the priorities ["c","b","a"].

| results for priorities | results for sorted priorities | sorted results for priorities |
|------------------------|-------------------------------|-------------------------------|
| c                      | a                             | a                             |
| cc                     | aa                            | aa                            |
| ccc                    | aaa                           | aaa                           |
| cb                     | ab                            | aab                           |
| bc                     | ba                            | aac                           |
| ccb                    | aab                           | ab                            |
| cbc                    | aba                           | aba                           |
| bcc                    | baa                           | abb                           |
| cbb                    | abb                           | abc                           |
| bcb                    | bab                           | ac                            |
| bbc                    | bba                           | aca                           |
| cba                    | abc                           | acb                           |
| cab                    | acb                           | acc                           |
| bca                    | bac                           | b                             |
| bac                    | bca                           | ba                            |
| acb                    | cab                           | baa                           |
| abc                    | cba                           | bab                           |
| ca                     | ac                            | bac                           |
| ac                     | ca                            | bb                            |
| cca                    | aac                           | bba                           |
| cac                    | aca                           | bbb                           |
| acc                    | caa                           | bbc                           |
| caa                    | acc                           | bc                            |
| aca                    | cac                           | bca                           |
| aac                    | cca                           | bcb                           |
| b                      | b                             | bcc                           |
| bb                     | bb                            | c                             |
| bbb                    | bbb                           | ca                            |
| ba                     | bc                            | caa                           |
| ab                     | cb                            | cab                           |
| bba                    | bbc                           | cac                           |
| bab                    | bcb                           | cb                            |
| abb                    | cbb                           | cba                           |
| baa                    | bcc                           | cbb                           |
| aba                    | cbc                           | cbc                           |
| aab                    | ccb                           | cc                            |
| a                      | c                             | cca                           |
| aa                     | cc                            | ccb                           |
| aaa                    | ccc                           | ccc                           |

## License
This module is distributed under the [MIT License](/LICENSE).
