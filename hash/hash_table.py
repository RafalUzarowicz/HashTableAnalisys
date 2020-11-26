import hashlib
"""
    Author: Rafał Uzarowicz - https://github.com/RafalUzarowicz
"""

class HashTable:
    def __init__(self, length : int):
        self.k = length
        self.table = [None] * self.k

    def add(self, value : str):
        # TODO: liczenie klucza z hash
        key = int(hashlib.md5(value.encode()).hexdigest(), 16)%self.k
        if self.table[key] is None:
            # TODO: wstaw nowa strukture drzewa
            pass
        else:
            # TODO: dodaj do istniejacego drzewa
            pass

    def remove(self, value):
        if isinstance(value, int):
            # TODO: co jak indeks
            pass
        elif isinstance(value, str):
            # TODO: co jak klucz
            pass

    def __getitem__(self, item : int ):
        # TODO: opis co zwraca funkcja itp
        return self.table[item]
