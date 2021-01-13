"""
    author: Joanna Sokolowska - https://github.com/jsokolowska
 """
import argparse
import os
import sys
import pandas as pd
from random import choice, shuffle
from text.generator import TextGenerator
from hash.hash_table import HashTable
import timeit
from tabulate import tabulate
from matplotlib import pyplot as plt
import math


def standard_mode(k):
    instances = get_instances()
    no_experiments_mode(instances, k)


def no_experiments_mode(instances, k):
    for instance in instances:
        hashtable = HashTable(k)
        print("Adding...")
        for word in instance:
            hashtable.add(word)
        if len(hashtable) == len(instance):
            print("All words added to hashtable")
        else:
            print("Error: did not add all words")

        print(hashtable)

        print("Enumerating...")
        for item in hashtable:
            print(item)
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


def test_mode(k, repetitions, sizes, outfile=None):
    print("Value of k: ", k)
    print("Repetitions: ", repetitions)
    sizes.sort()
    df = pd.DataFrame(columns=["add", "enum", "del"], index=sizes)

    for size in sizes:
        print("Experiments for size: ", size)

        enum = []
        delete = []
        add = []
        for i in range(repetitions):
            print_progress_bar(i, repetitions)
            # preparations
            # series = [size] * repetitions
            temp = generate_instances([size + 1])[0]
            instance = temp[:-1]
            to_add = temp[-1]
            # create hashtables and add previously generated keys to it
            tables = []

            table = HashTable(k)
            for key in instance:
                table.add(key)

            # measure enumerating time
            start_time = timeit.default_timer()
            for _ in table:
                pass
            end_time = timeit.default_timer()
            enum.append(end_time - start_time)
            # enum.append(enumeration_time(size, k))

            # measure adding time
            start_time = timeit.default_timer()
            table.add(to_add)
            end_time = timeit.default_timer()
            add.append(end_time - start_time)

            # delete previously added keys (to keep the right problem size)
            table.remove(to_add)

            # measure delete time
            to_del = choice(instance)
            start_time = timeit.default_timer()
            table.remove(to_del)
            end_time = timeit.default_timer()
            delete.append(end_time - start_time)

            print_progress_bar(i + 1, repetitions)

        df["add"][size] = sum(add) / len(add)
        df["enum"][size] = sum(enum) / len(enum)
        df["del"][size] = sum(delete) / len(delete)

        df.to_csv(outfile)
    present_results(df)


def enumeration_time(size: int, k: int):
    table = HashTable(k)
    for _ in range(size):
        table.add(" ")
    start_time = timeit.default_timer()
    for _ in table:
        pass
    end_time = timeit.default_timer()
    return start_time - end_time


def text_mode(k):
    instances = []
    for line in sys.stdin:
        if "" == line.rstrip():
            break
        else:
            instances.append(line.split(" "))
    no_experiments_mode(instances, k)


def generate_instances(series) -> []:
    prob_tbl = find_file("..", "prob-tbl.csv")
    generator = TextGenerator(series=series, prob_tbl=prob_tbl)
    return generator.generate()


def find_file(current_dir, filename) -> []:
    path = current_dir + "/" + filename
    if os.path.isfile(current_dir + "/" + filename):
        return path
    else:
        for directory in os.listdir(current_dir):
            if os.path.isdir(current_dir + "/" + directory):
                return_path = find_file(current_dir + "/" + directory, filename)
                if return_path:
                    return return_path
        return None


def get_instances() -> []:
    # todo check if no keys are made of namespaces xd
    print("Enter strings divided by whitespaces. To finish an instance please press ENTER. If you want to finish "
          "inputting data please enter empty line followed by ENTER.")
    instances = []
    for line in sys.stdin:
        if "" == line.rstrip():
            break
        else:
            instances.append(line.split(" "))
    print("You have inputted " + str(len(instances)) + " problem instances")
    return instances


def present_results(df: pd.DataFrame):
    # calculate median values
    size = len(df.index)
    if size % 2 == 0:
        med_l = df.index[size // 2]
        med_r = df.index[size // 2 - 1]
        med_size = (med_r + med_l) / 2
        med_add = (df["add"][med_l] + df["add"][med_r]) / 2
        med_del = (df["add"][med_l] + df["add"][med_r]) / 2
        med_enum = (df["add"][med_l] + df["add"][med_r]) / 2
    else:
        med_size = df.index[(size - 1) // 2]
        med_add = df["add"][med_size]
        med_del = df["del"][med_size]
        med_enum = df["enum"][med_size]

    med_add_theory = add_theory_complexity(med_size)
    med_del_theory = remove_theory_complexity(med_size)
    med_enum_theory = enumeration_theory_complexity(med_size)

    add = pd.DataFrame(df["add"], columns=["add"])
    add["q(n)"] = df["add"].divide([add_theory_complexity(x) for x in df.index]) * med_add_theory / med_add
    delete = pd.DataFrame(df["del"], columns=["del"])
    delete["q(n)"] = df["del"].divide([remove_theory_complexity(x) for x in df.index]) * med_del_theory / med_del
    enum = pd.DataFrame(df["enum"], columns=["enum"])
    enum["q(n)"] = df["enum"].divide([enumeration_theory_complexity(x) for x in df.index]) * med_enum_theory / med_enum

    print("Results for adding")
    print(tabulate(add, headers=["n"] + add.columns.tolist(), tablefmt="pretty"))
    print("Results for deleting")
    print(tabulate(delete, headers=["n"] + delete.columns.tolist(), tablefmt="pretty"))
    print("Results for enumerating")
    print(tabulate(enum, headers=["n"] + enum.columns.tolist(), tablefmt="pretty"))
    add.to_csv("add.csv")
    delete.to_csv("delete.csv")
    enum.to_csv("enum.csv")


def add_theory_complexity(x):
    return math.log(x)


def remove_theory_complexity(x):
    return math.log(x)


def enumeration_theory_complexity(x):
    return x * math.log(x)


def print_progress_bar(iteration: int, total: int, length: int = 50) -> None:
    if iteration == 0:
        print("\n")
    filled = int(length * iteration // total)
    bar = '█' * filled + '-' * (length - filled)
    print(f"\rProgress: |{bar}| " + "{0:.2f}".format(100 * (iteration / float(total))) + "% Iteration: " + str(
        iteration) + "/" + str(total), end='\r')
    if iteration == total:
        print("\n")


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
    parser.add_argument("-outfile", type=str, default="out.csv",
                        help="name of the results file, relevant only for test mode, defaults to out.csv")
    parser.add_argument("-sizes", nargs="+", type=int, help="sizes of problem instances")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.k < 1:
        print("Hashtable size must be at least 1")
    else:
        if args.gen:
            text_mode(args.k)
        elif args.test:
            if args.sizes:
                sizes = args.sizes
            else:
                # sizes = [5, 10, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
                sizes = [1000 * i for i in range(1, 22, 3)]
            test_mode(args.k, args.r, sizes, args.outfile)
        else:
            standard_mode(args.k)


# print(timeit.default_timer())
main()

# dataf = pd.read_csv("out.csv", index_col=0)
# print(dataf)
# present_results(dataf)
#
# plt.plot(dataf["enum"])
# plt.show()
