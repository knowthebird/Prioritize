"""
Space for showing example usages.
"""

import string
import itertools
import prioritize

def abc_priorities():
    print("*********** ABC Priorities ***********")
    min_length = 1
    max_length = 3
    for result in prioritize.prioritized_permutations(["A","B","C"],min_length,max_length):
        print(result)

def boolean_priorities():
    print("*********** Boolean Priorities ***********")
    min_length = 4
    max_length = 4
    for result in prioritize.prioritized_permutations(["0","1"],min_length,max_length):
        print(result)

def top_50_wordlists_priorities():
    print("*********** Top 50 Wordlist Priorities ***********")
    known_previos_passwords = ["MyPassWord","2FlyFast","8334"]
    common_passwords = ["password","admin", "root", "letmein"]
    data_of_birth = ["1972","72","02","2","26"]
    address = ["983", "Thomas", "Lane"]
    phone = ["703","235","5483"]
    things_they_like = ["shameless", "peaky", "blinders"]

    priorities = []
    priorities.extend(list(x for x in known_previos_passwords if x not in priorities))
    priorities.extend(list(x for x in common_passwords if x not in priorities))
    priorities.extend(list(x for x in data_of_birth if x not in priorities))
    priorities.extend(list(x for x in address if x not in priorities))
    priorities.extend(list(x for x in phone if x not in priorities))
    priorities.extend(list(x for x in things_they_like if x not in priorities))

    min_length = 8
    max_length = 10

    top_50 = itertools.islice(prioritize.prioritized_permutations(priorities,min_length,max_length), 50)
    for result in top_50:
        print(result)

def date_priorities():
    print("*********** Date Priorities ***********")
    years = list(range(2022,1950,-1))
    dates = years
    months = list(range(12,0,-1))
    dates.extend(list(x for x in months if x not in dates))
    days = list(range(31,0,-1))
    dates.extend(list(x for x in days if x not in dates))

    min_length = 6
    max_length = 8

    top_10 = itertools.islice(prioritize.prioritized_permutations(dates,min_length,max_length), 10)
    for result in top_10:
        print(result)

def punctuation_priorities():
    print("*********** Punctuation Priorities ***********")
    priorities = list(string.punctuation)
    min_length = 1
    max_length = 3

    top_10 = itertools.islice(prioritize.prioritized_permutations(priorities,min_length,max_length), 10)
    for result in top_10:
        print(result)

def main():
    abc_priorities()
    boolean_priorities()
    top_50_wordlists_priorities()
    date_priorities()
    punctuation_priorities()

if __name__ == "__main__":
    main()
