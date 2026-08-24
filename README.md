# Prioritize

`Prioritize` is a Python generator for enumerating strings made from a ranked set of substrings **without first materializing and sorting the full result space**.

It is useful when the candidate space can become extremely large, but results still need to be produced in a deliberate order. The caller can consume results incrementally, stop when enough results have been examined, and avoid storing every possible output in memory.

## Why This Exists

A straightforward approach to this class of problem is:

1. Generate every valid string.
2. Remove duplicates.
3. Store the entire result set.
4. Sort it according to the desired priority rules.

That approach becomes expensive quickly as the number of substrings, substitutions, and permitted output lengths grow.

`Prioritize` instead generates candidates lazily. Higher-priority substrings are considered before lower-priority ones, combinations are expanded only as needed, and duplicate strings are rejected without keeping a global set of every previously generated result.

This makes the module useful for large ordered search spaces where **early results matter more than exhaustive precomputation**.

## Core Properties

- **Lazy generation:** results are yielded one at a time through a Python generator.
- **Priority-aware ordering:** the order of the input substrings influences when candidate families are explored.
- **Bounded output lengths:** minimum and maximum string lengths constrain generation.
- **Duplicate suppression:** duplicate output strings are avoided without retaining the complete generated result set.
- **Incremental consumption:** iteration state is retained between calls, so callers can process results in batches and stop or resume without regenerating the full search space.
- **Substring support:** priorities may be multi-character strings rather than individual characters.

## Example

```python
from prioritize import prioritized_permutations

priorities = ["Top", "Second", "Last"]

for result in prioritized_permutations(
    priorities,
    min_length=1,
    max_length=13,
):
    print(result)
```

Early results begin with candidates composed from the highest-priority substrings before progressively incorporating lower-priority ones.

## How It Works

The generator operates in several stages:

1. **Clean the priorities** by rejecting duplicates, removing entries that cannot fit within the maximum length, and removing priorities that can already be formed entirely from higher-priority substrings.
2. **Enumerate priority-index groups** so groups containing higher-priority entries are considered earlier.
3. **Generate combinations with replacement** for each priority group while enforcing the requested output-length bounds.
4. **Generate multiset permutations** of each combination.
5. **Suppress duplicate strings** by determining whether the current substring decomposition is the first decomposition that would produce that string under the priority rules.
6. **Yield immediately** rather than collecting the complete search space.

The implementation uses `itertools.combinations_with_replacement` and SymPy's `multiset_permutations` for the combinatorial operations.

## Why Lazy Ordering Matters

For a combinatorial space, the total number of candidates may be impractical to generate or retain even when the first useful candidates can be reached quickly.

A generator-based interface means the consumer controls the amount of work performed:

```python
generator = prioritized_permutations(
    ["alpha", "beta", "gamma"],
    min_length=5,
    max_length=20,
)

for candidate in generator:
    if evaluate(candidate):
        break
```

The full candidate space does not need to exist in memory before useful work begins.

Potential applications include prioritized combinatorial search, structured test-data generation, ranked identifier generation, grammar-like candidate exploration, and security research such as ordered password-candidate generation. The algorithm itself is general-purpose and is not specific to any one application.

## Installation

The module depends on SymPy for multiset permutation generation.

```bash
python -m pip install sympy
```

Then import the generator directly:

```python
from prioritize import prioritized_permutations
```

## API

```python
prioritized_permutations(
    priorities: list,
    min_length: int = 4,
    max_length: int = 7,
)
```

### `priorities`

Strings ordered from highest priority to lowest priority.

### `min_length` / `max_length`

Minimum and maximum lengths of yielded strings.

## Duplicate Handling

One difficult case occurs when the same final string can be produced from different substring decompositions. For example, one priority may itself be constructible from several other priorities.

The implementation first removes priorities that are completely redundant with higher-priority entries. During generation, `find_first_permutation()` determines the first priority-index decomposition that would produce a candidate string. A candidate is yielded only when the current permutation corresponds to that first decomposition.

This avoids maintaining a potentially massive in-memory set solely for duplicate detection.

## Tests and Examples

- [`examples.py`](examples.py) contains usage examples.
- [`tests.py`](tests.py) exercises the generation and ordering behavior.
- [`prioritize.py`](prioritize.py) contains the implementation.

## Project Status

This is a focused algorithmic utility rather than a full application or packaged service. The implementation dates from 2022 and is kept here primarily as a reusable demonstration of priority-ordered lazy combinatorial generation.

## Reference Output and Ordering

The following tables preserve two useful reference views from the original project documentation.

### Priority-group enumeration

For four priorities, the generator considers unique priority-index groups in this order before expanding them with replacements and permutations:

| i | Priority indexes |
| ---: | --- |
| 1 | `[0]` |
| 2 | `[0, 1]` |
| 3 | `[0, 1, 2]` |
| 4 | `[0, 1, 2, 3]` |
| 5 | `[0, 1, 3]` |
| 6 | `[0, 2]` |
| 7 | `[0, 2, 3]` |
| 8 | `[0, 3]` |
| 9 | `[1]` |
| 10 | `[1, 2]` |
| 11 | `[1, 2, 3]` |
| 12 | `[1, 3]` |
| 13 | `[2]` |
| 14 | `[2, 3]` |
| 15 | `[3]` |

### Priority ordering compared with lexical ordering

For input priorities `["c", "b", "a"]`, the generator's order is intentionally different from either sorting the priorities first or lexically sorting the final strings:

| Prioritized results | Results with sorted priorities | Lexically sorted results |
| --- | --- | --- |
| c | a | a |
| cc | aa | aa |
| ccc | aaa | aaa |
| cb | ab | aab |
| bc | ba | aac |
| ccb | aab | ab |
| cbc | aba | aba |
| bcc | baa | abb |
| cbb | abb | abc |
| bcb | bab | ac |
| bbc | bba | aca |
| cba | abc | acb |
| cab | acb | acc |
| bca | bac | b |
| bac | bca | ba |
| acb | cab | baa |
| abc | cba | bab |
| ca | ac | bac |
| ac | ca | bb |
| cca | aac | bba |
| cac | aca | bbb |
| acc | caa | bbc |
| caa | acc | bc |
| aca | cac | bca |
| aac | cca | bcb |
| b | b | bcc |
| bb | bb | c |
| bbb | bbb | ca |
| ba | bc | caa |
| ab | cb | cab |
| bba | bbc | cac |
| bab | bcb | cb |
| abb | cbb | cba |
| baa | bcc | cbb |
| aba | cbc | cbc |
| aab | ccb | cc |
| a | c | cca |
| aa | cc | ccb |
| aaa | ccc | ccc |

These examples are not meant to prescribe one universal notion of priority; they make the implemented ordering concrete and easier to inspect.

## License

This project is distributed under the [MIT License](LICENSE).
