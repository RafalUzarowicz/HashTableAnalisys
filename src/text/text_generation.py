"""
    author: Joanna Sokołowska - https://github.com/jsokolowska
"""

import wget
import pickle

BREAK_CHAR = " "
PROB_TABLE_FILE = "prob_table.pkl"


def get_text(url: str = "https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt", file_name: str = "text.txt"):
    wget.download(url, file_name)


def clean_text(file_name: str = "text.txt") -> str:
    with open(file_name) as file:
        all_lines = " ".join(file)

    cleaned_text = "".join(char for char in all_lines if char.isalpha() or char.isspace())
    cleaned_text.lower()
    cleaned_text = BREAK_CHAR.join(cleaned_text.split())
    return cleaned_text


def create_prob_table (file_name: str = "text.txt") -> dict:
    cleaned_text = clean_text(file_name)

    # CREATE PROB TABLE
    return None


def load_prob_table () -> dict:
    with open(PROB_TABLE_FILE, "rb") as file:
        return pickle.load(file)


def save_prob_table (prob_table: dict):
    with open(PROB_TABLE_FILE, "wb") as file:
        pickle.dump(prob_table, file)

