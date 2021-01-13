"""
    projekt: Analiza tablicy mieszającej (warianty W13 i W21)
    autor: Joanna Sokołowska - https://github.com/jsokolowska
"""

import os
import random
import wget
import pandas as pd


class TextGenerator:
    WORD_BREAK = " "
    PROB_TABLE_FILE = "prob-tbl.csv"
    DEF_TEXT_FILE = "text.txt"
    SUM = "sum"
    ACCEPTED_CHARS = [chr(x) for x in range(ord('a'), ord('z') + 1) if x not in [ord('x'), ord('v'), ord('q')]] + \
                     ["ą", "ć", "ę", "ł", "ń", "ó", "ś", "ź", "ż", WORD_BREAK]
    MAX_LEN = 20

    def __init__(self, *, infile=None, outfile=None, url=None, prob_tbl=None):
        self.outfile = outfile
        self.text_file = infile

        if url:
            self.url = url
        else:
            self.url = "https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt"

        if os.path.isfile(prob_tbl):
            self.__load_prob_tbl(prob_tbl)
        else:
            self.prob_tbl = None

    def __load_prob_tbl(self, prob_file):
        self.prob_tbl = pd.read_csv(prob_file, index_col=0)

    def generate(self) -> str:
        if self.prob_tbl is None:
            if not self.text_file:
                self.text_file = self.DEF_TEXT_FILE
                self.__get_text()
            self.__create_prob_table()
            self.__save_prob_table()
        return self.__generate_text()

    def __get_text(self) -> None:
        if os.path.exists(self.text_file):
            os.remove(self.text_file)
        wget.download(self.url, self.text_file)

    def __create_prob_table(self) -> None:
        with open(self.text_file) as file:
            text = file.read()

        table = pd.DataFrame(index=self.ACCEPTED_CHARS, columns=self.ACCEPTED_CHARS)
        table = table.fillna(0)
        i = 0
        char = self.WORD_BREAK

        while i < len(text)-1:
            next_char = text[i].lower()
            if next_char.isspace():
                if not char.isspace():
                    table[self.WORD_BREAK][char] += 1
                char = self.WORD_BREAK
            elif next_char in self.ACCEPTED_CHARS:
                table[next_char][char] += 1
                char = next_char
            i += 1

        self.prob_tbl = table
        self.prob_tbl['sum'] = self.prob_tbl.sum(axis=1)

    def __save_prob_table(self) -> None:
        with open(self.PROB_TABLE_FILE, "w") as file:
            file.write(self.prob_tbl.to_csv())

    def __generate_text(self) -> str:
        if not self.__is_sufficient():
            raise (ValueError("Probability table is not enough for text generation"))

        columns = self.prob_tbl.columns
        word = ""
        char = self.WORD_BREAK
        next_char = ""

        for i in range(self.MAX_LEN):
            rand = random.randint(0, self.prob_tbl['sum'][char] - 1)
            for j in range(len(columns)):
                occurrences = self.prob_tbl[columns[j]][char]
                if occurrences > rand:
                    next_char = columns[j]
                    break
                else:
                    rand -= occurrences
            char = next_char
            if next_char == self.WORD_BREAK:
                break
            word += next_char
        return word

    def __is_sufficient(self):
        sums = list(self.prob_tbl.sum(axis=1))
        sums.sort()
        if sums[0] <= 0:
            return False
        return True
