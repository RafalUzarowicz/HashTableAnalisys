"""
    projekt: Analiza tablicy mieszającej (warianty W13 i W21)
    autor: Joanna Sokołowska - https://github.com/jsokolowska
 """
import argparse
from text.generator import TextGenerator

parser = argparse.ArgumentParser(description="Generate text sign by sign based on probability of succesive letters. "
                                             "Probability table is generated based on a sample of polish text "
                                             "(default sample \"Pan Tadeusz\" by Adam Mickiewicz, "
                                             "requires internet connection). "
                                             "Unless output file is specified text will be generated to standard output")
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument("-in", "--infile", help="txt file to generate  probability distribution", action='store')
group.add_argument("--prob-tbl", help="pkl file containing probabilty table", action='store')
group.add_argument("--url", help="url to sample txt file for generating probability distribution", action='store')

group2 = parser.add_mutually_exclusive_group(required=True)
group2.add_argument("-c", "--count", type=int, help="problem size (number of words to generate)")
group2.add_argument("--sizes", nargs="+", type=int, metavar="N",
                    help="list of problem sizes. Program will generate texts with word counts as specified on "
                         "this list and separate them by newline.")

parser.add_argument("-out", "-outfile", help="output file", action="store")

args = parser.parse_args()
generator = TextGenerator(infile=args.infile, outfile=args.out, url=args.url, prob_tbl=args.prob_tbl)

result = ""
if args.count:
    series = [args.count]
else:
    series = args.sizes
for c in series:
    for i in range(c):
        result += generator.generate() + " "
    result += "\n"
result += "\n"

if args.out:
    with open(args.out, "w") as file:
        file.write(result)
else:
    print(result)
