"""
    projekt: Analiza tablicy mieszającej (warianty W13 i W21)
    autor: Joanna Sokołowska - https://github.com/jsokolowska
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
        self.results = []
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
            self.__load_prob_tbl(prob_tbl)

    def __load_prob_tbl(self, prob_file):
        self.prob_tbl = pd.read_csv(prob_file, index_col=0)

    def generate(self, print_results=False) -> []:
        if self.prob_tbl is None:
            if not self.text_file:
                self.text_file = self.DEF_TEXT_FILE
                self.__get_text()
            self.__clean_text()
            self.__create_prob_table()
            self.__save_prob_table()

        self.__generate_text()
        if print_results:
            self.__show_results()
        return self.results

    def __get_text(self):
        if os.path.exists(self.text_file):
            os.remove(self.text_file)
        wget.download(self.url, self.text_file)

    def __clean_text(self):
        with open(self.text_file) as file:
            all_lines = " ".join(file)

        cleaned_text = "".join(char for char in all_lines if char in self.ACCEPTED_CHARS or char.isspace())
        cleaned_text.lower()
        words = [char for char in cleaned_text.split() if len(char) > 4]
        cleaned_text = self.WORD_BREAK.join(words)
        self.results = cleaned_text.lower()

    def __create_prob_table(self):
        table = pd.DataFrame(index=self.ACCEPTED_CHARS, columns=self.ACCEPTED_CHARS)
        table = table.fillna(0)
        i = 0

        while i < len(self.results) - 1:
            char = self.results[i]
            next_char = self.results[i + 1]
            table[next_char][char] += 1
            i += 1
        self.prob_tbl = table

    def __save_prob_table(self):
        with open(self.PROB_TABLE_FILE, "w") as file:
            file.write(self.prob_tbl.to_csv())

    def __generate_text(self):
        if not self.__is_sufficient():
            raise (ValueError("Probability table is not enough for text generation"))
        self.results = []
        self.prob_tbl['sum'] = self.prob_tbl.sum(axis=1)
        columns = self.prob_tbl.columns
        next_char = ''
        for count in self.series:
            instance = []
            for i in range(count):
                char = self.WORD_BREAK
                word = ""
                while True:
                    rand = random.randint(0, self.prob_tbl['sum'][char]-1)
                    for j in range(len(columns)):
                        occurrences = self.prob_tbl[columns[j]][char]
                        if occurrences > rand:
                            next_char = columns[j]
                            break
                        else:
                            rand -= occurrences
                    word += next_char
                    char = next_char
                    if next_char == self.WORD_BREAK:
                        instance.append(word)
                        break
            self.results.append(instance)

    def __is_sufficient(self):
        sums = list(self.prob_tbl.sum(axis=1))
        sums.sort()
        if sums[0] <= 0:
            return False
        return True

    def __show_results(self):
        temp = []
        for res in self.results:
            temp.append(self.WORD_BREAK.join(res))
        text = self.TEXT_BREAK.join(temp)
        if self.outfile:
            with open(self.outfile, "w") as file:
                file.write(text)
        else:
            print(text)
