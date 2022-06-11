"""
Space for unit tests.
"""

from collections import Counter
from datetime import datetime
import prioritize


def duplicate_priorities():
    priorities = ["abcd", "abc", "abcd"]
    max_length = 3
    returned_priorities = prioritize.clean_input(priorities,max_length)
    expected_priorities = []
    if returned_priorities == expected_priorities:
        print("Duplicate Priorities: Pass")
    else:
        print("Duplicate Priorities: FAILED")

def clean_length():
    priorities = ["abcd", "abc", "dddd", "ab"]
    max_length = 3
    returned_priorities = prioritize.clean_input(priorities,max_length)
    expected_priorities = ["abc", "ab"]
    if returned_priorities == expected_priorities:
        print("Clean Length:         Pass")
    else:
        print("Clean Length:         FAILED")

def remove_redundant():
    priorities = ["ab", "c", "abc", "a", "bc", "Ab"]
    max_length = 3
    returned_priorities = prioritize.clean_input(priorities,max_length)
    expected_priorities = ["ab", "c", "a", "bc", "Ab"]
    if returned_priorities == expected_priorities:
        print("Remove Redundant:     Pass")
    else:
        print("Remove Redundant:     FAILED")

def simple_gen():
    priorities = ["a", "b","c"]
    min_length = max_length = 1
    results = list(prioritize.prioritized_permutations(priorities,min_length,max_length))
    if results == priorities:
        print("Simple Gen:           Pass")
    else:
        print("Simple Gen:           FAILED")

def results_count():
    priorities = list(range(0,10))
    min_length = 1
    max_length = 3
    results = list(prioritize.prioritized_permutations(priorities,min_length,max_length))
    if len(results) == 1110:
        print("Results Count:        Pass")
    else:
        print("Results Count:        FAILED")

def results_order():
    priorities = ["a", "b", "cdef"]
    min_length = 2
    max_length = 3
    results = list(prioritize.prioritized_permutations(priorities,min_length,max_length))
    expected_results = ["aa","aaa","ab","ba","aab","aba",
                        "baa","abb","bab","bba","bb","bbb"]
    if results == expected_results:
        print("Min-Max Lengths:      Pass")
    else:
        print("Min-Max Lengths:      FAILED")

    priorities = ["1", "2","3","4"]
    min_length = 1
    max_length = 4
    expected_results = ["1","11","111","1111","12","21","112","121","211","122",
                        "212","221","1112","1121","1211","2111","1122","1212",
                        "1221","2112","2121","2211","1222","2122","2212","2221",
                        "123","132","213","231","312","321","1123","1132","1213",
                        "1231","1312","1321","2113","2131","2311","3112","3121",
                        "3211","1223","1232","1322","2123","2132","2213","2231",
                        "2312","2321","3122","3212","3221","1233","1323","1332",
                        "2133","2313","2331","3123","3132","3213","3231","3312",
                        "3321","1234","1243","1324","1342","1423","1432","2134",
                        "2143","2314","2341","2413","2431","3124","3142","3214",
                        "3241","3412","3421","4123","4132","4213","4231","4312",
                        "4321","124","142","214","241","412","421","1124","1142",
                        "1214","1241","1412","1421","2114","2141","2411","4112",
                        "4121","4211","1224","1242","1422","2124","2142","2214",
                        "2241","2412","2421","4122","4212","4221","1244","1424",
                        "1442","2144","2414","2441","4124","4142","4214","4241",
                        "4412","4421","13","31","113","131","311","133","313",
                        "331","1113","1131","1311","3111","1133","1313","1331",
                        "3113","3131","3311","1333","3133","3313","3331","134",
                        "143","314","341","413","431","1134","1143","1314","1341",
                        "1413","1431","3114","3141","3411","4113","4131","4311",
                        "1334","1343","1433","3134","3143","3314","3341","3413",
                        "3431","4133","4313","4331","1344","1434","1443","3144",
                        "3414","3441","4134","4143","4314","4341","4413","4431",
                        "14","41","114","141","411","144","414","441","1114",
                        "1141","1411","4111","1144","1414","1441","4114","4141",
                        "4411","1444","4144","4414","4441","2","22","222","2222",
                        "23","32","223","232","322","233","323","332","2223","2232",
                        "2322","3222","2233","2323","2332","3223","3232","3322",
                        "2333","3233","3323","3332","234","243","324","342","423",
                        "432","2234","2243","2324","2342","2423","2432","3224",
                        "3242","3422","4223","4232","4322","2334","2343","2433",
                        "3234","3243","3324","3342","3423","3432","4233","4323",
                        "4332","2344","2434","2443","3244","3424","3442","4234",
                        "4243","4324","4342","4423","4432","24","42","224","242",
                        "422","244","424","442","2224","2242","2422","4222","2244",
                        "2424","2442","4224","4242","4422","2444","4244","4424",
                        "4442","3","33","333","3333","34","43","334","343","433",
                        "344","434","443","3334","3343","3433","4333","3344","3434",
                        "3443","4334","4343","4433","3444","4344","4434","4443","4",
                        "44","444","4444"]
    results = list(prioritize.prioritized_permutations(priorities,min_length,max_length))
    if results == expected_results:
        print("Results Order:        Pass")
    else:
        print("Results Order:        FAILED")

def no_duplicates():
    priorities = ["ab", "a","b"]
    min_length = 1
    max_length = 5
    expected_results = ["ab","abab","aba","aab","ababa","abaab","aabab","abaa",
                        "aaba","aaab","abaaa","aabaa","aaaba","aaaab","abba","aabb",
                        "baba","baab","abbaa","aabba","aaabb","babaa","baaba",
                        "baaab","abbba","aabbb","babba","baabb","bbaba","bbaab",
                        "abb","bab","ababb","abbab","babab","abbb","babb","bbab",
                        "abbbb","babbb","bbabb","bbbab","a","aa","aaa","aaaa",
                        "aaaaa","ba","baa","bba","baaa","bbaa","bbba","baaaa",
                        "bbaaa","bbbaa","bbbba","b","bb","bbb","bbbb","bbbbb"]
    results = list(prioritize.prioritized_permutations(priorities,min_length,max_length))
    if results == expected_results and len(results) == len(set(results)):
        print("No Duplicates:        Pass")
    else:
        print("No Duplicates:        FAILED")
        print("Total words generated: ")
        print(len(results))
        print("Total unique words generated")
        print(len(set(results)))
        print("Words which were duplicated:")
        print([item for item, count in Counter(results).items() if count > 1])
        print("Number of times the words were produced:")
        print([count for item, count in Counter(results).items() if count > 1])


def main():
    starttime = datetime.now()

    duplicate_priorities()
    clean_length()
    remove_redundant()
    simple_gen()
    results_count()
    results_order()
    no_duplicates()

    timeelapsed = datetime.now() - starttime
    print("Completed Test In: " + str(timeelapsed) + " seconds.")

if __name__ == "__main__":
    main()
