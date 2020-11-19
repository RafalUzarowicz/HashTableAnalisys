"""
    author: Joanna Sokołowska - https://github.com/jsokolowska
 """
import argparse

parser = argparse.ArgumentParser(description="Generate text sign by sign based on probability of succesive letters. "
                                             "Probablity table is generated based on a sample of polish text "
                                             "(default option \"Pan Tadeusz\" by Adam Mickiewicz. "
                                             "By default text is generated to standard output.")
parser.add_argument("--infile", help="txt file to generate succesive letters probability distribution", action='store')
parser.add_argument("--outfile", help="output file", action="store")
parser.add_argument("--prob_tbl", help="pkl file containing probabilty table")
parser.add_argument("--word_cnt", help="number of words that sould be generated")
args = parser.parse_args()
