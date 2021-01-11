"""
    author: Joanna Sokołowska - https://github.com/jsokolowska
 """
import argparse
import os
import sys
from random import choice, shuffle
from text.generator import TextGenerator
from hash.hash_table import HashTable
import timeit


def main():
    args = parse_args()

    if args.k < 1:
        print("Hashtable size must be at least 1")
    else:
        if args.gen:
            text_mode(args.k, args.gen)
        elif args.test:
            test_mode(args.k, args.r)
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
        # todo print hashtable
        try:
            # todo proper enumeration xd
            print("Enumerating...")
            it = iter(hashtable)
            while True:
                print(next(it))
        except StopIteration:
            print("All nodes enumerated.")
            pass

        shuffle(instance)
        print("Removing all nodes..")
        for word in instance:
            hashtable.remove(word)

        if len(hashtable):
            print("ERROR: did not remove all elements")
            print(len(hashtable))
        else:
            print("Hashtable empty.")


def test_mode(k, repetitions):
    enum = "enum"
    add = "add"
    delete = "del"
    sizes = [5, 10, 50]  # , 100, 1000, 10000]
    results = {}

    for size in sizes:
        print("Experiments for size: ", size)
        size_result = {}

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
            enumerate(table)
        end_time = timeit.default_timer()
        size_result[enum] = end_time - start_time

        # measure adding time
        start_time = timeit.default_timer()
        for i in range(repetitions):
            tables[i].add(keys_to_add[i])
        end_time = timeit.default_timer()
        size_result[add] = end_time - start_time

        # delete previously added keys (to keep the right problem size)
        for i in range(repetitions):
            tables[i].remove(keys_to_add[i])

        # measure delete time
        start_time = timeit.default_timer()
        for i in range(repetitions):
            tables[i].remove(keys_to_remove[i])
        end_time = timeit.default_timer()
        size_result[delete] = end_time - start_time

        results[size] = size_result
        print(size_result)
    # print(results)
    present_results(results)


def text_mode(k, series):
    instances = generate_instances(series)
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
    mode_group.add_argument("-gen", nargs="+", type=int, metavar="N",
                            help="generate problems instances with sizes specified on the list")
    mode_group.add_argument("-test", action="store_true",
                            help="generate predefined problem instances, measure time of execution and present results")

    parser.add_argument("-k", type=int, default=50,
                        help="max size of hashtable, must be greater than 0, defaults to 50")
    parser.add_argument("-r", type=int, default=100,
                        help="number of repetitions for tests, relevant only if test mode is used, defaults to 100")
    parser.add_argument("-save", type=str, default="out.csv",
                        help="name of the results file, relevant only for test mode, defaults to out.csv")

    return parser.parse_args()


def generate_instances(series) -> []:
    prob_tbl = find_file("..", "prob-tbl.csv")
    generator = TextGenerator(series=series, prob_tbl=prob_tbl)
    return generator.generate()


def find_file(current_dir, filename) -> []:
    # todo change for while loop
    path = current_dir + "/" + filename
    if os.path.isfile(current_dir + "/" + filename):
        return path
    else:
        for directory in os.listdir(current_dir):
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


def present_results(results: {}):
    # todo proper presentation
    print(results)


main()
