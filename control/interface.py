"""
    author: Joanna Sokołowska - https://github.com/jsokolowska
 """
import argparse
import os
import sys
import time
from random import shuffle

from hash.hash_table import HashTable
from text.generator import TextGenerator


def main():
    args = parse_args()

    if args.k < 1:
        print("Hashtable size must be at least 1")
        return 0
    else:
        std_flag = not (args.gen or args.test)

    if args.gen is None:
        # args.gen = [10, 50, 100, 400, 800, 1000, 2000, 5000, 8000, 10000]
        args.gen = [1000]

    if std_flag:
        instances = get_instances()
    else:
        print("Generating problem instances...")
        instances = generate_instances(args.gen)
        print("Generated.")

    print("Starting experiments...")
    # l = "am  ka i ok hy".split(" ")
    # hashtable = HashTable(1)
    # for key in l:
    #     print(key)
    #     hashtable.add(key)
    times = do_experiments(instances, args.k)
    present_results(times)


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

    parser.add_argument("k", type=int, help="max size of hashtable, must be greater than 0")

    return parser.parse_args()


def generate_instances(series) -> []:
    prob_tbl = find_file("..", "prob-tbl.csv")
    if type(series) is int:
        s = [series]
    elif type(series) is list:
        s = series
    else:
        raise TypeError("Series must be an int or a list of ints")
    generator = TextGenerator(series=s, prob_tbl=prob_tbl)
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


def do_experiments(instances: [], k) -> {}:
    times = {}
    for instance in instances:
        # todo figure out why no child note to rotate error is raised while inserting many values to the tree
        size = len(instance)
        times[size] = {}
        print("Experiments for " + str(size) + " elements")
        hashtable = HashTable(k)

        # add all keys and measure time
        print("Inserting")
        start_t = time.time()
        for key in instance:
            print(key)
            hashtable.add(key)
        end_t = time.time()
        times[size]["add"] = end_t - start_t

        # enumerate all keys and measure time
        print("Enumerating")
        start_t = time.time()
        try:
            it = iter(hashtable)
            while True:
                next(it)
        except StopIteration:
            end_t = time.time()
            times[size]["enum"] = end_t - start_t

        # delete all keys and measure time
        print("Deleting")
        shuffle(instance)
        start_t = time.time()
        for key in instance:
            hashtable.remove(key)
        end_t = time.time()
        times[size]["del"] = end_t - start_t
    return times


def present_results(results: {}):
    # todo proper presentation
    print(results)


main()
