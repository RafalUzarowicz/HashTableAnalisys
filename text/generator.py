"""
    author: Joanna Sokołowska - https://github.com/jsokolowska
 """

import os
import random
import wget
import pandas as pd


class TextGenerator:
    # as generating probability table can take a few minutes, depending on how long text sample is
    # it is advised to use it only once and then proceed generating with created csv file
    WORD_BREAK = " "
    TEXT_BREAK = "\n"
    PROB_TABLE_FILE = "prob-tbl.csv"
    DEF_TEXT_FILE = "text.txt"
    OCC_SUM = "sum"
    ACCEPTED_CHARS = [chr(x) for x in range(ord('a'), ord('z') + 1) if x not in [ord('x'), ord('v'), ord('q')]] + \
                     ["ą", "ć", "ę", "ł", "ń", "ó", "ś", "ź", "ż", WORD_BREAK]

    def __init__(self, *, infile=None, outfile=None, url=None,
                 count=None, prob_tbl=None, series=None):
        self.outfile = outfile
        self.text = ""
        self.text_file = infile

        if url:
            self.url = url
        else:
            self.url = "https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt"

        if series and len(series):
            self.series = series
        else:
            self.series = [count]
        self.prob_tbl = None
        if prob_tbl:
            self.load_prob_tbl(prob_tbl)

    def load_prob_tbl(self, prob_file):
        self.prob_tbl = pd.read_csv(prob_file, index_col=0)

    def generate(self):
        if self.prob_tbl is None:
            if not self.text_file:
                self.text_file = self.DEF_TEXT_FILE
                self.get_text()
            self.clean_text()
            self.create_prob_table()
            self.save_prob_table()

        self.generate_text()
        self.print_results()

    def get_text(self):
        if os.path.exists(self.text_file):
            os.remove(self.text_file)
        wget.download(self.url, self.text_file)

    def clean_text(self):
        with open(self.text_file) as file:
            all_lines = " ".join(file)

        cleaned_text = "".join(char for char in all_lines if char in self.ACCEPTED_CHARS or char.isspace())
        cleaned_text.lower()
        words = [char for char in cleaned_text.split() if len(char) > 4]
        cleaned_text = self.WORD_BREAK.join(words)
        self.text = cleaned_text.lower()

    def create_prob_table(self):
        table = pd.DataFrame(index=self.ACCEPTED_CHARS, columns=self.ACCEPTED_CHARS)
        table = table.fillna(0)
        i = 0

        while i < len(self.text) - 1:
            char = self.text[i]
            next_char = self.text[i + 1]
            table[next_char][char] += 1
            i += 1
        self.prob_tbl = table

    def save_prob_table(self):
        with open(self.PROB_TABLE_FILE, "w") as file:
            file.write(self.prob_tbl.to_csv())

    def generate_text(self):
        if not self.is_sufficient():
            raise (ValueError("Probability table is not enough for text generation"))
        self.text = ""
        self.prob_tbl['sum'] = self.prob_tbl.sum(axis=1)
        columns = self.prob_tbl.columns
        next_char = ''
        for count in self.series:
            for i in range(count):
                char = self.WORD_BREAK
                while True:
                    rand = random.randint(0, self.prob_tbl['sum'][char])
                    for j in range(len(columns)):
                        occurrences = self.prob_tbl[columns[j]][char]
                        if occurrences > rand:
                            next_char = columns[j]
                            break
                        else:
                            rand -= occurrences
                    self.text += next_char
                    char = next_char
                    if next_char == self.WORD_BREAK:
                        break
            self.text += self.TEXT_BREAK

    def is_sufficient(self):
        sums = list(self.prob_tbl.sum(axis=1))
        sums.sort()
        if sums[0] <= 0:
            return False
        return True

    def print_results(self):
        if self.outfile:
            with open(self.outfile, "w") as file:
                file.write(self.text)
        else:
            print(self.text)
