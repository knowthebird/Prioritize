"""
Contains functions to generate prioritized permutations.
"""

from collections import Counter
from collections.abc import Generator
from itertools import combinations_with_replacement
from math import floor
from sympy.utilities.iterables import multiset_permutations


def prioritized_permutations(priorities:list,
                             min_length:int = 4,
                             max_length:int = 7) -> Generator[str, None, None]:
    """
    Generates permutations of strings prioritized by the given priorities list.

    Parameters
    ----------
    priorities : list
        A list of strings to generate the permutations from.
        Order from highest priority to lowest priority is left to right.
    min_length : int
        Sets the minimum length of genereated strings. Default is 4.
    max_length : int
        Sets the maximum length of genereated strings. Default is 7.

    Returns
    -------
    Generator[str, None, None]
        Yields string permutations optimized such that each permutation
        containing a given set of priorities is yielded before any
        permutations containing lower priorities.
    """

    priorities = clean_input(priorities, max_length)

    for current_indexes in order_of_top_priorties(priorities,
                                                  min_length,
                                                  max_length):

        for combination in create_combinations(priorities,
                                               min_length,
                                               max_length,
                                               current_indexes):

            for permutation in create_permutations(priorities, combination):
                yield permutation


def clean_input(orig_priorities:list, max_length:int) -> list:
    """Checks and prepares priorities list before use by generators."""

    cleaned_priorities = []

    # If the list has more than one copy of the same element,
    # we don't know which is valid (higher or lower priority)
    dupes = [item for item, count in Counter(orig_priorities).items() if count > 1]
    if len(dupes) > 0:
        print("Warning - List of priorties contains duplicates.")
        print(dupes)
        print("Duplicates must be removed before proceeding.")
        return cleaned_priorities

    cleaned_priorities = [str(priority) for priority in orig_priorities]
    cleaned_priorities = [priority for priority in cleaned_priorities \
                          if len(priority) <= max_length]
    cleaned_priorities = remove_redundant_priorities(cleaned_priorities)
    return cleaned_priorities


def remove_redundant_priorities(orig_priorities:list) -> list:
    """If a priority can be formed from one or more higher priorities
    then its equivalent strings will be generated by those priorities
    before it is used.  Because of this, it is redundant and we can remove it.
    """

    new_priorities = []
    for priority in orig_priorities:
        if not is_made_of_substrings(priority, new_priorities):
            new_priorities.append(priority)
    return new_priorities


def is_made_of_substrings(main_string:str, sub_strings:list) -> bool:
    """Check if a string can be formed from a list of substrings."""

    if main_string in sub_strings:
        return True

    for split_point in range(len(main_string)-1):
        left_string, right_string = main_string[:split_point+1], \
                                    main_string[split_point+1:]
        if is_made_of_substrings(left_string, sub_strings) and \
           is_made_of_substrings(right_string, sub_strings):
            return True

    return False

def order_of_top_priorties(priorities:list, min_length:int, max_length:int,
                           begin:int=0, starting_indexes:list=None
                           ) -> Generator[list, None, None]:
    """Generates the indexes of the priorities list to use later when generating
    combinations."""

    end = len(priorities)
    for index in range(begin, end):
        if starting_indexes:
            current_indexes = starting_indexes + [index]
        else:
            current_indexes = [index]

        if len(current_indexes) <= max_length:
            combo_length = sum([len(priorities[index]) for index in current_indexes])
            if combo_length <= max_length:
                yield current_indexes
                yield from order_of_top_priorties(priorities, min_length,
                                                  max_length, index+1,
                                                  current_indexes)

def create_combinations(priorities:list, min_length:int, max_length:int,
                        current_indexes:list) -> Generator[list, None, None]:
    """Generates combinations (with replacements) of the given indexes to use
    later when generating permutations."""

    shortest_priority_length = min([len(priorities[index]) for index in current_indexes])
    max_replacements = floor(max_length/shortest_priority_length)
    for replacements in range(1,max_replacements+1):
        for combo in combinations_with_replacement(current_indexes,replacements):
            if all(x in combo for x in current_indexes):
                combo_length = sum([len(priorities[index]) for index in combo])
                if min_length <= combo_length <= max_length:
                    yield list(combo)

def create_permutations(priorities:list,
                        combination:list) -> Generator[str, None, None]:
    """Generates multiset permutations of a given combination and returns the
    resulting string if it is the first time the string has been made."""

    for permutation in multiset_permutations(combination):
        final_str = ""
        for inner_index in permutation:
            final_str += str(priorities[inner_index])

        if is_first_occurance(final_str, priorities, permutation):
            yield final_str

def is_first_occurance(main_string:str, priorities:list,
                       current_permutation_indexes:list) -> bool:
    """Returns if the indexes of the priorities used in the current permutation
    are the same as the indexes of the priorities that would be used to first
    make the provided string."""

    first_permutation_indexes = find_first_permutation(main_string, priorities)
    return first_permutation_indexes == current_permutation_indexes


def find_first_permutation(main_string:str, sub_strings:list) -> list:
    """Returns the indexes of substrings which would first be used to
    generate the provided string (for the implemented prioritization)."""

    first_combo = []
    remaining_string = main_string

    for sub_str_idx, sub_str in enumerate(sub_strings):
        good_sub_string = False
        if len(sub_str) > len(main_string):
            continue

        for char_idx, char in enumerate(sub_str):
            if char == main_string[char_idx]:
                good_sub_string = True
            else:
                good_sub_string = False
                break

        if good_sub_string:
            first_combo.append(sub_str_idx)
            remaining_string = main_string[len(sub_str):]
            if remaining_string != "":
                remaining_list = find_first_permutation(remaining_string, sub_strings)
                if remaining_list:
                    first_combo.extend(remaining_list)
                    break
            else:
                break

    return first_combo