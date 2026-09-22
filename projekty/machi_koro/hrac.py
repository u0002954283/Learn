import random

class Hrac:
    def __init__(self, jmeno):
        self.jmeno = jmeno
        self.penize = 3
        self.karty = {
    "psenicne_pole": 1,
    "statek": 0,
    "les": 0,
    "dul": 0, 
    "jablonovy_sad": 0,
    "pekarna": 1,
    "samoobsluha": 0,
    "mlekarna": 0,
    "tovarna_na_nabytek": 0,
    "obchodni_dum": 0,
    "kavarna": 0,
    "restaurace": 0,
    "stadion": 0,
    "televizni_studio": 0,
    "kancelarska_budova": 0,
}
        self.dominanty = {
            "nadrazi" : False,
            "nakupni_centrum" : False,
            "zabavni_park" : False,
            "vysilac" : False,
        }

    def pridat_kartu(self, karta):
        self.karty[karta] += 1

    def odebrat_kartu(self, karta):
        self.karty[karta] -= 1