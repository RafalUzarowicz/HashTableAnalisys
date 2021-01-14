"""
    projekt: Analiza tablicy mieszającej (warianty W13 i W21)
    autor: Joanna Sokolowska - https://github.com/jsokolowska
 """
import argparse
import os
import sys
import pandas as pd
import math
import timeit

from random import shuffle, randint
from tabulate import tabulate

from text.generator import TextGenerator
from hash.hash_table import HashTable


def main():
    args = parse_args()

    if args.k < 1:
        print("Hashtable size must be at least 1")
    else:
        if args.gen and args.sizes:
            generator = TextGenerator(prob_tbl=args.prob_tbl, infile=args.infile, url=args.url)
            no_experiments_mode(args.k, args.sizes, generator)
        elif args.test:
            if args.sizes:
                sizes = args.sizes
            else:
                sizes = [1000 * i for i in range(1, 20, 1)]

            generator = TextGenerator(prob_tbl=args.prob_tbl, infile=args.infile, url=args.url)
            test_mode(args.k, args.r, sizes, generator, args.outfile)
        else:
            no_experiments_mode(args.k)


def parse_args():
    parser = argparse.ArgumentParser(description="Program takes its input (standard or generated) and proceeds to first"
                                                 " add words to hashtable (in the order they were given), then to "
                                                 "enumerate them (results are presented in the standard output) and at "
                                                 "the end to delete them from hashtable in random order. This procedure"
                                                 " is done for each given instance of the problem. If no flags are "
                                                 "given program waits for input. Fore more information please refer to "
                                                 "readme.txt.")

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("-gen", action="store_true",
                            help="generate problems instances with sizes specified on the list")
    mode_group.add_argument("-test", action="store_true",
                            help="generate predefined problem instances, measure time of execution and present results")

    parser.add_argument("-k", type=int, default=50,
                        help="max size of hashtable, must be greater than 0, defaults to 50")
    parser.add_argument("-r", type=int, default=100,
                        help="number of repetitions for tests, relevant only if test mode is used, defaults to 100")
    parser.add_argument("--outfile", "-out", type=str,
                        help="name of the results file, relevant only for test mode, defaults to out.csv")
    parser.add_argument("--sizes", nargs="+", type=int, help="sizes of problem instances")

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-in", "--infile", help="txt file to generate  probability distribution", action='store')
    group.add_argument("--prob-tbl", help="pkl file containing probability table", action='store')
    group.add_argument("--url", help="url to sample txt file for generating probability distribution", action='store')

    return parser.parse_args()


def no_experiments_mode(k, series=None, generator=None):
    if generator:
        instances = []
        for s in series:
            temp = []
            for i in range(s):
                temp.append(generator.generate())
            instances.append(temp)
    else:
        instances = std_get_keys()

    for instance in instances:
        hashtable = HashTable(k)
        print("Adding...")
        for word in instance:
            hashtable.add(word)
        if len(hashtable) == len(instance):
            print("All words added to hashtable")
        else:
            print("Error: did not add all words")

        print("Enumerating...")
        for _ in hashtable:
            pass
        print("All nodes enumerated")

        shuffle(instance)
        print("Removing all nodes..")
        for word in instance:
            hashtable.remove(word)

        if len(hashtable):
            print("ERROR: did not remove all elements")
            print(len(hashtable))
        else:
            print("Hashtable empty.")


def std_get_keys() -> []:
    instances = []
    for line in sys.stdin:
        if "" == line.rstrip():
            break
        else:
            instances.append(line.rstrip("\n").split(" "))
    return instances


def test_mode(k, repetitions, sizes, generator, outfile=None) -> None:
    print("K: ", k)
    print("Repetitions: ", repetitions)
    sizes.sort()
    df = pd.DataFrame(columns=["add", "enum", "del"], index=sizes)
    temp_file = "temp-" + str(k) + "k-" + str(repetitions) + "r.csv"

    for size in sizes:
        print("Doing experiments for size ", size)

        enum = []
        delete = []
        add = []
        for i in range(repetitions):
            print_progress_bar(i, repetitions)

            # preparations
            table = HashTable(k)
            to_add = generator.generate()
            to_del = ""
            rand = randint(0, size - 1)

            for j in range(size):
                key = generator.generate()
                table.add(key)
                if j == rand:
                    to_del = key

            # measure enumerating time
            start_time = timeit.default_timer()
            for _ in table:
                pass
            end_time = timeit.default_timer()
            enum.append(end_time - start_time)

            # measure adding time
            start_time = timeit.default_timer()
            table.add(to_add)
            end_time = timeit.default_timer()
            add.append(end_time - start_time)

            # delete previously added keys (to keep the right problem size)
            table.remove(to_add)

            # measure delete time
            start_time = timeit.default_timer()
            table.remove(to_del)
            end_time = timeit.default_timer()
            delete.append(end_time - start_time)

            print_progress_bar(i + 1, repetitions)

        df["add"][size] = sum(add) / len(add)
        df["enum"][size] = sum(enum) / len(enum)
        df["del"][size] = sum(delete) / len(delete)

        df.to_csv(temp_file)

    os.remove(temp_file)
    df = df.rename(columns={"add": "Add t(n)", "del": "Del t(n)", "enum": "Enum t(n)"})
    present_results(df, outfile)


def print_progress_bar(iteration: int, total: int, length: int = 50) -> None:
    if iteration == 0:
        print("\n")
    filled = int(length * iteration // total)
    bar = '█' * filled + '-' * (length - filled)
    print(f"\rProgress: |{bar}| " + "{0:.2f}".format(100 * (iteration / float(total))) + "% Iteration: " + str(
        iteration) + "/" + str(total), end='\r')
    if iteration == total:
        print("\n")


def present_results(df: pd.DataFrame, outfile=None):
    # calculate median values
    size = len(df.index)
    if size % 2 == 0:
        med_l = df.index[size // 2]
        med_r = df.index[size // 2 - 1]
        med_size = (med_r + med_l) / 2
        med_add = (df["Add t(n)"][med_l] + df["Add t(n)"][med_r]) / 2
        med_del = (df["Del t(n)"][med_l] + df["Del t(n)"][med_r]) / 2
        med_enum = (df["Enum t(n)"][med_l] + df["Enum t(n)"][med_r]) / 2
    else:
        med_size = df.index[(size - 1) // 2]
        med_add = df["Add t(n)"][med_size]
        med_del = df["Del t(n)"][med_size]
        med_enum = df["Enum t(n)"][med_size]

    med_add_theory = add_theory_complexity(med_size)
    med_del_theory = remove_theory_complexity(med_size)
    med_enum_theory = enumeration_theory_complexity(med_size)

    df["Add q(n)"] = df["Add t(n)"].divide([add_theory_complexity(x) for x in df.index]) * med_add_theory / med_add
    df["Del q(n)"] = df["Del t(n)"].divide([remove_theory_complexity(x) for x in df.index]) * med_del_theory / med_del
    df["Enum q(n)"] = df["Enum t(n)"].divide(
        [enumeration_theory_complexity(x) for x in df.index]) * med_enum_theory / med_enum

    print("Results for adding")
    print(tabulate(df[["Add t(n)", "Add q(n)"]], headers=["n", "Add t(n)", "Add q(n)"], tablefmt="pretty"))
    print("Results for deleting")
    print(tabulate(df[["Del t(n)", "Del q(n)"]], headers=["n", "Del t(n)", "Del q(n)"], tablefmt="pretty"))
    print("Results for enumerating")
    print(tabulate(df[["Enum t(n)", "Enum q(n)"]], headers=["n", "Enum t(n)", "Enum q(n)"], tablefmt="pretty"))

    if outfile:
        df.to_csv(outfile)


def add_theory_complexity(x):
    return math.log(x)


def remove_theory_complexity(x):
    return math.log(x)


def enumeration_theory_complexity(x):
    return x * math.log(x)


def enumeration_time(size: int, k: int):
    table = HashTable(k)
    for _ in range(size):
        table.add(" ")
    start_time = timeit.default_timer()
    for _ in table:
        pass
    end_time = timeit.default_timer()
    return start_time - end_time

main()
