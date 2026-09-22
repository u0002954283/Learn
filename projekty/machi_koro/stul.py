from data import *

class Obchod:
    def __init__(self):
        self.karty = karty
        self.obchod = pocet_budov


    def je_karta_skladem(self, karta):
        return self.obchod[karta]

    def odebrat_kartu(self, odkoupena_karta):
        self.obchod[odkoupena_karta] -= 1
        return self.obchod
