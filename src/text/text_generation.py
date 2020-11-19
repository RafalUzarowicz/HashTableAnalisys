"""
    author: Joanna Sokołowska - https://github.com/jsokolowska
"""

import wget
import pickle
import random
import os

BREAK_CHAR = " "
PROB_TABLE_FILE = "prob-table.pkl"
OCC_SUM = "sum"


def get_text(url: str = "https://wolnelektury.pl/media/book/txt/narcyssa-i-wanda.txt", file_name: str = "text.txt"):
    if os.path.exists(file_name):
        os.remove(file_name)
    wget.download(url, file_name)


def clean_text(file_name: str = "text.txt") -> str:
    with open(file_name) as file:
        all_lines = " ".join(file)

    cleaned_text = "".join(char for char in all_lines if char.isalpha() or char.isspace())
    cleaned_text.lower()
    cleaned_text = BREAK_CHAR.join(cleaned_text.split())
    return cleaned_text.lower()


def create_prob_table(file_name: str = "text.txt") -> dict:
    cleaned_text = clean_text(file_name)
    prob_table = {}

    unique_chars = set(cleaned_text)
    for char in unique_chars:
        prob_table[char] = {}
        for other_char in unique_chars:
            prob_table[char][other_char] = 0

    # count occurences of word pairs
    i = 0
    while i < len(cleaned_text) - 1:
        char = cleaned_text[i]
        next_char = cleaned_text[i+1]
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

        prob_table[char][OCC_SUM] = occ_sum
        if occ_sum == 0:
            prob_table.pop(char)

    return prob_table


def load_prob_table() -> dict:
    with open(PROB_TABLE_FILE, "rb") as file:
        return pickle.load(file)


def save_prob_table(prob_table: dict):
    with open(PROB_TABLE_FILE, "wb") as file:
        pickle.dump(prob_table, file)


def generate_text(prob_table: dict, word_count: int) -> str:
    text = ""
    for i in range(word_count):
        char = BREAK_CHAR
        while True:
            upper = prob_table[char][OCC_SUM]
            rand = random.randint(0, upper-1)
            next_char = ""
            for c in prob_table[char].keys():
                occurences = prob_table[char][c]
                if occurences > rand:
                    next_char = c
                    break
                else:
                    rand -= occurences
            text += next_char
            char = next_char
            if next_char == BREAK_CHAR:
                break
    return text


get_text()
table = create_prob_table()
print(generate_text(table, 1000))
