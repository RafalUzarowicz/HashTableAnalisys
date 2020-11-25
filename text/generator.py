"""
    author: Joanna Sokołowska - https://github.com/jsokolowska
 """

import os
import random
import wget
import pickle


class TextGenerator:
    WORD_BREAK = " "
    TEXT_BREAK = "\n"
    PROB_TABLE_FILE = "prob-table.pkl"
    DEF_TEXT_FILE = "text.txt"
    OCC_SUM = "sum"

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

        self.prob_tbl = prob_tbl

    def generate(self):
        if not self.prob_tbl:
            self.prob_tbl = None
            if not self.text_file:
                self.text_file = self.DEF_TEXT_FILE
                self.get_text()
            self.clean_text()
            self.create_prob_table()

        self.generate_text()
        self.display()

    def get_text(self):
        if os.path.exists(self.text_file):
            os.remove(self.text_file)
        wget.download(self.url, self.text_file)

    def save_prob_table(self):
        with open(self.PROB_TABLE_FILE, "wb") as file:
            pickle.dump(self.prob_tbl, file)

    def create_prob_table(self):
        prob_table = {}

        unique_chars = set(self.text)
        for char in unique_chars:
            prob_table[char] = {}
            for other_char in unique_chars:
                prob_table[char][other_char] = 0

        # count occurences of char pairs
        i = 0
        while i < len(self.text) - 1:
            char = self.text[i]
            next_char = self.text[i + 1]
            prob_table[char][next_char] += 1
            i += 1

        for char in prob_table.keys():
            for other_char in list(prob_table[char].keys()):
                if prob_table[char][other_char] == 0:
                    prob_table[char].pop(other_char)

        for char in list(prob_table.keys()):
            occ_sum = 0
            for other_char in list(prob_table[char].keys()):
                occ_sum += prob_table[char][other_char]

            prob_table[char][self.OCC_SUM] = occ_sum
            if occ_sum == 0:
                prob_table.pop(char)

        self.prob_tbl = prob_table

    def clean_text(self):
        with open(self.text_file) as file:
            all_lines = " ".join(file)

        cleaned_text = "".join(char for char in all_lines if char.isalpha() or char.isspace())
        cleaned_text.lower()
        cleaned_text = self.WORD_BREAK.join(cleaned_text.split())
        self.text = cleaned_text.lower()

    def generate_text(self):
        self.text = ""
        for count in self.series:
            for i in range(count):
                char = self.WORD_BREAK
                while True:
                    upper = self.prob_tbl[char][self.OCC_SUM]
                    rand = random.randint(0, upper - 1)
                    next_char = ""
                    for c in self.prob_tbl[char].keys():
                        occurences = self.prob_tbl[char][c]
                        if occurences > rand:
                            next_char = c
                            break
                        else:
                            rand -= occurences
                    self.text += next_char
                    char = next_char
                    if next_char == self.WORD_BREAK:
                        break
            self.text += self.TEXT_BREAK

    def display(self):
        if self.outfile:
            with open(self.outfile, "w") as file:
                file.write(self.text)
        else:
            print(self.text)

    def load_prob_tbl(self, prob_file):
        with open(prob_file, 'rb') as file:
            return pickle.load(file)
