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
from statistics import median
import math


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
                sizes = [5, 10, 100, 5000, 10000, 50000]  # , 100, 5000, 10000, 50000, 100000, 500000, 1000000]
            test_mode(args.k, args.r, sizes, args.outfile)
        else:
            standard_mode(args.k)


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
    sizes.sort()
    df = pd.DataFrame(columns=["add", "enum", "del"], index=sizes)

    for size in sizes:
        print("Experiments for size: ", size)

        # preparations
        series = [size] * repetitions
        instances = generate_instances(series)
        keys_to_add = generate_instances([repetitions])[0]

        # create hashtables and add previously generated keys to it
        tables = []
        for instance in instances:
            table = HashTable(k)
            for key in instance:
                table.add(key)
            tables.append(table)

        # randomly choose keys that will be later removed from table
        keys_to_remove = []
        for instance in instances:
            keys_to_remove.append(choice(instance))

        # sanity check
        if len(tables) != repetitions:
            raise ValueError("Did not create right number of tables")

        # measure enumerating time
        start_time = timeit.default_timer()
        for table in tables:
            for item in table:
                pass
        end_time = timeit.default_timer()
        df["enum"][size] = (end_time - start_time) * 1000 / repetitions

        # measure adding time
        start_time = timeit.default_timer()
        for i in range(repetitions):
            tables[i].add(keys_to_add[i])
        end_time = timeit.default_timer()
        df["add"][size] = (end_time - start_time) * 1000 / repetitions

        # delete previously added keys (to keep the right problem size)
        for i in range(repetitions):
            tables[i].remove(keys_to_add[i])

        # measure delete time
        start_time = timeit.default_timer()
        for i in range(repetitions):
            tables[i].remove(keys_to_remove[i])
        end_time = timeit.default_timer()
        df["del"][size] = (end_time - start_time) * 1000 / repetitions

        df.to_csv(outfile)
    present_results(df, sizes)


def text_mode(k):
    instances = []
    for line in sys.stdin:
        if "" == line.rstrip():
            break
        else:
            instances.append(line.split(" "))
    no_experiments_mode(instances, k)


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


def present_results(df: pd.DataFrame, sizes):
    # calculate median values
    if len(sizes) % 2 == 0:
        med_size = sizes[len(sizes) / 2]
        med_add = df["add"][med_size]
        med_del = df["del"][med_size]
        med_enum = df["enum"][med_size]
    else:
        med_l = sizes[(len(sizes) - 1) // 2]
        med_r = sizes[(len(sizes) + 1) // 2]
        med_size = (med_r + med_l) / 2
        med_add = (df["add"][med_l] + df["add"][med_r]) / 2
        med_del = (df["add"][med_l] + df["add"][med_r]) / 2
        med_enum = (df["add"][med_l] + df["add"][med_r]) / 2

    med_add_theory = math.log(med_size)
    med_del_theory = math.log(med_size)
    med_enum_theory = med_size

    add = pd.DataFrame(df["add"], columns=["add"])
    add["q(n)"] = df["add"].divide([math.log(x) for x in sizes]) * med_add_theory / med_add
    delete = pd.DataFrame(df["del"], columns=["del"])
    delete["q(n)"] = df["del"].divide([math.log(x) for x in sizes]) * med_del_theory / med_del
    enum = pd.DataFrame(df["enum"], columns=["enum"])
    enum["q(n)"] = df["enum"].divide(sizes) * med_enum_theory / med_enum

    print("Results for adding")
    print(tabulate(add, headers=["n"] + add.columns.tolist(), tablefmt="pretty"))
    print("Results for deleting")
    print(tabulate(delete, headers=["n"] + delete.columns.tolist(), tablefmt="pretty"))
    print("Results for enumerating")
    print(tabulate(enum, headers=["n"] + enum.columns.tolist(), tablefmt="pretty"))
    add.to_csv("add.csv")
    delete.to_csv("delete.csv")
    enum.to_csv("enum.csv")


print(timeit.default_timer())
main()
