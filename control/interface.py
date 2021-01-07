"""
    author: Joanna Sokołowska - https://github.com/jsokolowska
 """
import argparse

from hash.hash_table import HashTable

parser = argparse.ArgumentParser(description="Program takes its input (standard or generated) and proceeds to first add"
                                             "words to hashtable (in the order they were given), then to enumerate them"
                                             " (results are presented in the standard output) and at the end to delete "
                                             "them from hashtable in random order. This procedure is done for each "
                                             "given instance of the problem. If no flags are given program waits for "
                                             "input.")

mode_group = parser.add_mutually_exclusive_group()
mode_group.add_argument("-gen", nargs="+", type=int, metavar="N",
                        help="generate problems instances with sizes specified on the list")
mode_group.add_argument("-test", action="store_true",
                        help="generate predefined problem instances, measure time of execution and present results")

parser.add_argument("k", type=int, help="max size of hashtable, must be greater than 0")

args = parser.parse_args()
if args.k < 1:
    print("Hashtable size must be at least 1")
else:
    std_flag = not (args.gen or args.test)
    # get instances
    # for each instance of the problem
    #   add all
    #   enumerate all
    #   delete all
    # print results

