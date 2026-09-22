#------------------- import -------------------------------------------------------------

import random
from data import karty
from stul import Obchod
import os
import subprocess
from hrac import Hrac

#------------------- class -------------------------------------------------------------

class Hra:
    def __init__(self):
        
#--------------------------------------------------------
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
        print("="*80+"\n"+" "*25+"VÍTEJTE VE HŘE MACHI KORO"+"\n"+"="*80+"\n  Vybuduj své město, vydělávej mince a postav všechny 4 dominanty \n  rychleji než tvůj soupeř!\n"
            +"-"*80+"\n [ NASTAVENÍ HRY ]\n")
    
        x = input("Zadejte jméno 1. hráče (bude začínat) >>> ")
        y = input("Zadejte jméno 2. hráče                >>> ")

        print("\n" + "=" * 80 + "\n" )
        print(" Načítání...")
        print("-" * 80)

#-------------------atributy-------------------------------------------------------------
        self.karty = karty["podniky"]
        self.dominanty = karty["dominanty"]

        self.hrac1 = Hrac(x)
        self.hrac2 = Hrac(y)
        self.hraci = [self.hrac1, self.hrac2]      #seznam s objekty hracu


        self.obchod = Obchod()
        self.index_aktualniho_hrace = 0

        self.konec = False
        self.pokracovani = True


#-------------------atributy ve funkci-------------------------------------------------------------

    @property
    def aktualni_hrac(self):
        return self.hraci[self.index_aktualniho_hrace]

    @property
    def neaktualni_hrac(self):
        if self.index_aktualniho_hrace == 0:
            return self.hraci[self.index_aktualniho_hrace + 1]
        else:
            return self.hraci[self.index_aktualniho_hrace - 1]



    def dalsi_hrac(self):
        self.index_aktualniho_hrace = (self.index_aktualniho_hrace + 1) % len(self.hraci)

    
# ----------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------- FUNKCE FAZI ------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------

    def hod_kostkou(self):
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

        hod2 = 0
        tah_na_vic = False

        print("=" * 80 + "\n HOD KOSTKOU \n" + "-" * 80)

        if (self.aktualni_hrac).dominanty["nadrazi"] and (input("Máš postavené Nádraží! Chceš házet 1 nebo 2 kostkami? (1/2) >>> ")) == "2":
            hod2 = random.randint(1, 6)
            hod1 = random.randint(1, 6)
            print(f"\nHráč {(self.aktualni_hrac).jmeno} hází 2 kostkami... Padlo {hod1} a {hod2} (Celkem {hod1 + hod2})")

        else:
            hod1 = random.randint(1, 6)
            print(f" Hráč {self.aktualni_hrac.jmeno} hází 1 kostkou... Padlo {hod1}\n")


        if (self.aktualni_hrac).dominanty["vysilac"] and (str(input("-" * 80 +" Máš postavený Vysílač! Chceš kostky přehodit? (a/n) >>> ")).lower() == "a"):
            hod2 = 0
            if (self.aktualni_hrac).dominanty["nadrazi"] and (input("Máš postavené Nádraží! Chceš házet 1 nebo 2 kostkami? (1/2) >>> ")) == "2":
                hod2 = random.randint(1, 6)
                hod1 = random.randint(1, 6)
                print(f"Přehazuješ kostkami...\nhrac {(self.aktualni_hrac).jmeno} hodil {hod1} a {hod2} = {hod1 + hod2}")
            else:
                hod1 = random.randint(1, 6)
                print(f"\nHráč {(self.aktualni_hrac).jmeno} hází 1 kostkou... Padlo {hod1})")


        if (self.aktualni_hrac).dominanty["zabavni_park"] and hod1 == hod2:
            print("Padly stejné hodnoty a máš Zábavní park! Získáváš tah navíc!" + "=" * 80)
            tah_na_vic = True
        else:
            print("=" * 80)

        input("[ Stiskněte Enter pro pokračování ]\n ")
        return hod1, hod2, tah_na_vic

                
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def prijmi_a_vydaje(self, hod):

        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
        print("="*80 + f"\n PŘÍJMY A VÝDAJE    HOD[{hod}]\n" + "-" * 80)


        puvodni_penize_aktualni = self.aktualni_hrac.penize
        puvodni_penize_neaktualni = self.neaktualni_hrac.penize

        log_aktualni = []
        log_neaktualni = []
        #cervene -souper

        for karta, pocet in self.neaktualni_hrac.karty.items():
            if self.karty[karta]["barva"] == "cervena" and self.neaktualni_hrac.karty[karta] > 0 and hod in self.karty[karta]["aktivace"]:
                platba = self.karty[karta]["vynos"]
                dodatek = ""

                if self.neaktualni_hrac.dominanty["nakupni_centrum"]:
                    platba += 1
                    dodatek = "+ Nákupní cent."
        
                platba_final = min(platba * pocet, self.aktualni_hrac.penize)
                if platba_final > 0:

                    self.neaktualni_hrac.penize +=  platba_final
                    self.aktualni_hrac.penize -= platba_final

                    pocet_txt =  f" {pocet}x" if pocet > 1 else ""
                    log_aktualni.append(f"-{platba_final} mince ({self.karty[karta]['jmeno']}{pocet_txt} -> {self.neaktualni_hrac.jmeno})")
                    log_neaktualni.append(f"+{platba_final} mince ({self.karty[karta]['jmeno']}{pocet_txt} <- {self.aktualni_hrac.jmeno})")




        #aktualni modra zelena
        for karta, pocet in self.aktualni_hrac.karty.items():
            vynos = 0
            if self.karty[karta]["barva"] in ["modra", "zelena"] and pocet > 0 and hod in self.karty[karta]["aktivace"]:
                if "vynos_za_symbol" in self.karty[karta].keys():
                    for karta_2, pocet_2 in self.aktualni_hrac.karty.items():
                        if pocet_2 > 0 and self.karty[karta_2]["symbol"] == self.karty[karta]["vynos_za_symbol"]:
                            vynos += self.karty[karta]["vynos"] * pocet * pocet_2
                            dodatek = f"za {pocet_2}x {self.karty[karta_2]['jmeno']}"
                else:
                    if self.aktualni_hrac.dominanty["nakupni_centrum"] and self.karty[karta]["symbol"] == "obchod":
                        vynos += pocet
                        dodatek = "+ Nákupní cent."
                    else:
                        dodatek = ""

                    vynos += self.karty[karta]["vynos"] * pocet

                if vynos > 0:
                    self.aktualni_hrac.penize += vynos

                    pocet_txt =  f" {pocet}x" if pocet > 1 else ""
                    log_aktualni.append(f"+{vynos} mince ({self.karty[karta]['jmeno']}{pocet_txt} {dodatek})")




        #souper modra
        for karta, pocet in self.neaktualni_hrac.karty.items():
            vynos = 0
            if self.karty[karta]["barva"] == "modra" and pocet > 0 and hod in self.karty[karta]["aktivace"]:
                vynos += self.karty[karta]["vynos"] * pocet

                if vynos > 0:
                    self.neaktualni_hrac.penize += vynos
                    pocet_txt =  f" {pocet}x" if pocet > 1 else ""
                    log_neaktualni.append(f"+{vynos} mince ({self.karty[karta]['jmeno']} {pocet_txt})")
                    


        #fialove - aktualni

        if (self.aktualni_hrac.karty["stadion"] > 0 and hod in self.karty["stadion"]["aktivace"]):
            castka = min(self.karty["stadion"]["vynos"]* self.aktualni_hrac.karty["stadion"], self.neaktualni_hrac.penize)
            if castka > 0:
                self.aktualni_hrac.penize += castka
                self.neaktualni_hrac.penize -= castka

                pocet_txt =  f" {self.aktualni_hrac.karty['stadion']}x" if pocet > 1 else ""

                log_aktualni.append(f"+{castka} mince ({self.karty['stadion']['jmeno']}{pocet_txt} <- {self.neaktualni_hrac.jmeno})")
                log_neaktualni.append(f"-{castka} mince ({self.karty['stadion']['jmeno']}{pocet_txt} -> {self.aktualni_hrac.jmeno})")

        if (self.aktualni_hrac.karty["televizni_studio"] > 0 and hod in self.karty["televizni_studio"]["aktivace"]):
            castka = min(self.karty["televizni_studio"]["vynos"] * self.aktualni_hrac.karty["televizni_studio"], self.neaktualni_hrac.penize)
            if castka > 0:
                self.aktualni_hrac.penize += castka
                self.neaktualni_hrac.penize -= castka

                pocet_txt =  f" {self.aktualni_hrac.karty['televizni_studio']}x" if pocet > 1 else ""

                log_aktualni.append(f"+{castka} mince ({self.karty['televizni_studio']['jmeno']}{pocet_txt} <- {self.neaktualni_hrac.jmeno})")
                log_neaktualni.append(f"-{castka} mince ({self.karty['televizni_studio']['jmeno']}{pocet_txt} -> {self.aktualni_hrac.jmeno})")

        vymena_probehla=False
        vzpis = ""
        if self.aktualni_hrac.karty["kancelarska_budova"] > 0 and hod in self.karty["kancelarska_budova"]["aktivace"]:

            print("=" * 80 + "\n AKCE: KANCELÁŘSKÁ BUDOVA — VÝMĚNA KARTY\n" + "-" * 80 + " Můžeš vyměnit 1 svoji budovu za 1 soupeřovu budovu (nelze měnit symbol věže)" + "-" * 80)

            print(f"TVOJE BUDOVY K ODEVZDÁNÍ ({self.aktualni_hrac.jmeno}):")

            slovnik_odevzano = {}
            for idx, (k, p) in enumerate(self.aktualni_hrac.karty.items(), 1):
                if self.karty[k]['symbol'] != 'vez' and self.aktualni_hrac.karty[k] > 0:
                    slovnik_odevzano[idx] = k
                    print(f" [{idx}] {self.karty[k]['jmeno']} ({p}x)")



            print(f"\nSOUPEŘOVY BUDOVY K ODEVZDÁNÍ ({self.neaktualni_hrac.jmeno}):")

            slovnik_ziskano = {}
            for idx, (k, p) in enumerate(self.neaktualni_hrac.karty.items(), 1):
                if self.karty[k]['symbol'] != 'vez' and self.neaktualni_hrac.karty[k] > 0:
                    slovnik_ziskano[idx] = k
                    print(f" [{idx}] {self.karty[k]['jmeno']} ({p}x)")


            print("-"*80)

            if input(" Chceš provést výměnu karet? (a/n) >>> ").lower() == "a":
                vymena_svoje = int(input(" Zadej číslo SVOJÍ budovy k odevzdání >>> "))
                vymnena_soupere = int(input(" Zadej číslo SOUPEŘOVY budovy k získání >>> "))

                print("="*80)
                print(" - Výměna proběhla úspěšně!")
                print(f"   Odevzdáno: {self.karty[slovnik_odevzano[vymena_svoje]]['jmeno']}  <--->  Získáno: {self.karty[slovnik_ziskano[vymnena_soupere]]['jmeno']}")
                print("="*80)

                self.aktualni_hrac.pridat_kartu(slovnik_ziskano[vymnena_soupere])
                self.aktualni_hrac.odebrat_kartu(slovnik_odevzano[vymena_svoje])

                self.neaktualni_hrac.pridat_kartu(slovnik_odevzano[vymena_svoje])
                self.neaktualni_hrac.odebrat_kartu(slovnik_ziskano[vymnena_soupere])
                vymena_probehla = True
                vzpis = f"  EFEKT KANCELÁŘSKÉ BUDOVY:\n  {self.aktualni_hrac.jmeno} vyměnil/a [{vymena_svoje}] za [{vymnena_soupere}]"


        def formatuj(jmeno, role, log, zmena, orig, nov):
            hdr = f"{jmeno} ({role})"
            zm = f"{'+' if zmena >= 0 else ''}{zmena} mincí"
            pen = f"{orig} -> {nov} mincí"

            if not log:
                return f"  {hdr:<16}  (Žádný pohyb mincí){'':<16} {zm:<10} {pen}"

            radky = []
            for polozka in log:
                if not radky:
                    radky.append(f"  {hdr:<16}  {polozka:<36} {zm:<10} {pen}")
                else:
                    radky.append(f"  {'':<16}  {polozka:<36}")

            return "\n".join(radky)

        zmena_akt = self.aktualni_hrac.penize - puvodni_penize_aktualni
        zmena_neakt = self.neaktualni_hrac.penize - puvodni_penize_neaktualni

        blok_akt = formatuj(
            self.aktualni_hrac.jmeno,
            "na tahu",
            log_aktualni,
            zmena_akt,
            puvodni_penize_aktualni,
            self.aktualni_hrac.penize,
        )
        blok_neakt = formatuj(
            self.neaktualni_hrac.jmeno,
            "soupeř",
            log_neaktualni,
            zmena_neakt,
            puvodni_penize_neaktualni,
            self.neaktualni_hrac.penize,
        )






        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
        print("="*80 + f"\n PŘÍJMI A VÝDAJE      HOD [{hod}]\n" + "="*80)
        print(f"  HRÁČ             PŘÍJEM / VÝDAJ (DŮVOD)               BILANCE    PENÍZE")
        print(" "+"-"*78+" ")
        print(blok_akt)
        print(" "+"-"*78+" ")
        print(blok_neakt)
        print("="*80)
        if vymena_probehla:
            print(vzpis)
        input(" [ Stiskněte ENTER pro pokračování do fáze nákupu ] \n ")
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def stavba(self):

#------------------- set ---------------------------------------------------------------------------------------------------------------------------------------------
        id_budov = {
            1: "psenicne_pole", 2: "statek", 3: "les", 4: "dul", 5: "jablonovy_sad",
            6: "pekarna", 7: "samoobsluha", 8: "mlekarna", 9: "tovarna_na_nabytek",
            10: "obchodni_dum", 11: "kavarna", 12: "restaurace", 13: "stadion",
            14: "televizni_studio", 15: "kancelarska_budova"
        }
        id_dominant = {
            "N": "nadrazi",
            "C": "nakupni_centrum",
            "P": "zabavni_park",
            "V": "vysilac"
        }

#----------------print------------------------------------------------------------------------------------------------------------------------------------------------



        while True:
            self.info_stavba()
            volba = input(" Zadej volbu >>> ").strip().upper()

#--------------koupe budovy--------------------------------------------------------------------------------------------------------------------------------------------------
            if volba == "K":
                bud_kod = input(" Zadej ID budovy >>> ").strip().upper()
                if bud_kod.isdigit():
                    bud_kod = int(bud_kod)
                    if bud_kod in id_budov:
                        bud_klic = id_budov[bud_kod]
                        bud_info = self.karty[bud_klic]

                    # 1. Kontrola skladu
                        if self.obchod.obchod[bud_klic]<1:
                            input("\n Tato budova už není skladem! (Stiskněte ENTER)")
                            continue

                    # 2. Kontrola fialových karet (max 1 ks od každé)
                        if bud_info["barva"] == "fialova" and self.aktualni_hrac.karty[bud_klic] > 0:
                            input("\n Fialovou budovu (věž) můžeš mít pouze jednou! (Stiskněte ENTER)")
                            continue

                    # 3. Kontrola peněz
                        if self.aktualni_hrac.penize < bud_info["cena"]:
                            input(f"\n Nemáš dostatek mincí! Chybí ti {bud_info['cena'] - self.aktualni_hrac.penize} mincí. (Stiskněte ENTER)")
                            continue

                    # Provedení stavby
                        self.aktualni_hrac.penize -= bud_info["cena"]
                        self.aktualni_hrac.karty[bud_klic] += 1
                        self.obchod.odebrat_kartu(bud_klic)

                        print(f"\n Úspěšně jsi koupil/a [{bud_info['jmeno']}]!")
                        input(" [ Stiskněte ENTER pro ukončení tahu ] ")
                        break
                    else:
                        input("\n Neplatné ID budovy. (Stiskněte ENTER)")
                else:
                    input("\n Neplatné ID budovy. (Stiskněte ENTER)")

#---------koupe dominanty-------------------------------------------------------------------------------------------------------------------------------------------------------

            elif volba == "D":
                dom_kod = input(" Zadej ID dominanty (N / C / P / V) >>> ").strip().upper()
                if dom_kod in id_dominant:
                    dom_klic = id_dominant[dom_kod]
                    dom_info = self.dominanty[dom_klic]

                    # 1. Kontrola, zda už není postavená
                    if self.aktualni_hrac.dominanty[dom_klic]:
                        input(f"\n Dominantu [{dom_info['jmeno']}] už máš postavenou! (Stiskněte ENTER)")
                        continue

                    # 2. Kontrola peněz
                    if self.aktualni_hrac.penize < dom_info["cena"]:
                        input(f"\n Nemáš dostatek mincí! Chybí ti {dom_info['cena'] - self.aktualni_hrac.penize} mincí. (Stiskněte ENTER)")
                        continue

                    # Provedení stavby
                    self.aktualni_hrac.penize -= dom_info["cena"]
                    self.aktualni_hrac.dominanty[dom_klic] = True

                    print(f"\n Úspěšně jsi postavil/a dominantu [{dom_info['jmeno']}]!")


                # KONTROLA VÍTĚZSTVÍ (všechny 4 dominanty postaveny)
                    if all(self.aktualni_hrac.dominanty.values()):
                        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
                        print("=" * 80)
                        print(f"   VÍTĚZEM HRY SE STÁVÁ: {self.aktualni_hrac.jmeno.upper()} !!!")
                        print("=" * 80 + "\n")
                        self.pokracovani = False
                        self.konec = True
                    break

#-----------------informace o karte-----------------------------------------------------------------------------------------------------------------------------------------------


            elif volba == "INFO":
                dotaz = input(" Zadej ID budovy (1–15) nebo dominanty (N/C/P/V) >>> ").lower().strip()

                if dotaz.isdigit() and int(dotaz) in id_budov:
                    dotaz = int(dotaz)
                    inf =  self.karty[id_budov[dotaz]]
                    print(f"Jméno: {inf['jmeno']}\nCena: {inf['cena']}\nAktivace: {inf['aktivace']}\nBarva: {inf['barva']}\nSymbol: {inf['symbol']}\nVýnos: {inf['vynos']}\nPopis: {inf['popis']}\n")
                elif dotaz in id_dominant:
                    inf = self.dominanty[id_dominant[dotaz]]
                    print(f"Jméno: {inf['jmeno']}\ncena:{inf['cena']}\npopis:{inf['popis']}\n")
                else:
                    print("\n Karta nenalezena.")
                    input("\n [ Stiskněte ENTER pro návrat ] ")

#-------------- preskoceni kola --------------------------------------------------------------------------------------------------------------------------------------------------

            elif volba in ["PASS", "P"]:
                print("Přeskočil/a jsi fázi nákupu.")
                input(" [ Stiskněte ENTER pro předání tahu ] ")
                break


            else:
                input("\n Neplatná volba. Vyber K, D, INFO nebo PASS. (Stiskněte ENTER)")


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------- UI a vypis informaci -------------------------------------------------------------

    def info(self):
       # priprava dat

        budovy_aktualni_hrac = "\n".join(f" - {self.karty[karta]['jmeno']:<18} [{pocet}x]" for karta, pocet in self.aktualni_hrac.karty.items() if pocet != 0)
       
        budovy_neaktualni_hrac = "\n".join([f" - {self.karty[karta]['jmeno']:<18} [{pocet}x]" for karta, pocet in self.neaktualni_hrac.karty.items() if pocet != 0])

        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

        return input(f"""

================================================================================
                                MACHI KORO
================================================================================
--------------------------------------------------------------------------------
1. HRÁČ NA TAHU: {self.aktualni_hrac.jmeno}
--------------------------------------------------------------------------------
* Mince: {self.aktualni_hrac.penize}
* Dominanty: Nadrazi [{'X' if self.aktualni_hrac.dominanty["nadrazi"] else ' '}] | Nakupni centrum [{'X' if self.aktualni_hrac.dominanty["nakupni_centrum"] else ' '}] | Zabavni park [{'X' if self.aktualni_hrac.dominanty["zabavni_park"] else ' '}] | Vysilac [{'X' if self.aktualni_hrac.dominanty["vysilac"] else ' '}]
* Postavené budovy:
{budovy_aktualni_hrac}
--------------------------------------------------------------------------------
2. SOUPEŘ: {self.neaktualni_hrac.jmeno}
--------------------------------------------------------------------------------
* Mince: {self.neaktualni_hrac.penize}
* Dominanty: Nadrazi [{'X' if self.neaktualni_hrac.dominanty["nadrazi"] else ' '}] | Nakupni centrum [{'X' if self.neaktualni_hrac.dominanty["nakupni_centrum"] else ' '}] | Zabavni park [{'X' if self.neaktualni_hrac.dominanty["zabavni_park"] else ' '}] | Vysilac [{'X' if self.neaktualni_hrac.dominanty["vysilac"] else ' '}]
* Postavené budovy:
{budovy_neaktualni_hrac}
================================================================================
3. OBCHOD
--------------------------------------------------------------------------------
ID | NAZEV BUDOVY           | CENA | AKTIVACE | TYP/BARVA | SKLADEM
--------------------------------------------------------------------------------
1  | Psenicne pole          |  1   |    1     |  Modra    |  {self.obchod.obchod["psenicne_pole"]} ks
2  | Statek                 |  1   |    2     |  Modra    |  {self.obchod.obchod["statek"]} ks
3  | Les                    |  3   |    5     |  Modra    |  {self.obchod.obchod["les"]} ks
4  | Dul                    |  6   |    9     |  Modra    |  {self.obchod.obchod["dul"]} ks
5  | Jablonovy sad          |  3   |    10    |  Modra    |  {self.obchod.obchod["jablonovy_sad"]} ks
6  | Pekarna                |  1   |  2   3   |  Zelena   |  {self.obchod.obchod["pekarna"]} ks
7  | Samoobsluha            |  2   |    4     |  Zelena   |  {self.obchod.obchod["samoobsluha"]} ks
8  | Mlekarna               |  5   |    7     |  Zelena   |  {self.obchod.obchod["mlekarna"]} ks
9  | Tovarna na nabytek     |  3   |    8     |  Zelena   |  {self.obchod.obchod["tovarna_na_nabytek"]} ks
10 | Obchodni dum           |  2   |  11  12  |  Zelena   |  {self.obchod.obchod["obchodni_dum"]} ks
11 | Kavarna                |  2   |    3     |  Cervena  |  {self.obchod.obchod["kavarna"]} ks
12 | Restaurace             |  3   |  9   10  |  Cervena  |  {self.obchod.obchod["restaurace"]} ks
13 | Stadion                |  6   |    6     |  Fialova  |  {self.obchod.obchod["stadion"]} ks
14 | Televizni studio       |  7   |    6     |  Fialova  |  {self.obchod.obchod["televizni_studio"]} ks
15 | Kancelarska budova     |  8   |    6     |  Fialova  |  {self.obchod.obchod["kancelarska_budova"]} ks
================================================================================
4. DOMINANTY
--------------------------------------------------------------------------------
ID | NAZEV DOMINANTY        | CENA | STAV U HRÁČE {self.aktualni_hrac.jmeno}
--------------------------------------------------------------------------------
N  | Nadrazi                |  4   | {'Postaveno' if self.aktualni_hrac.dominanty["nadrazi"] else 'Chybí    '} [{'X' if self.aktualni_hrac.dominanty["nadrazi"] else ' '}]
C  | Nakupni centrum        | 10   | {'Postaveno' if self.aktualni_hrac.dominanty["nakupni_centrum"] else 'Chybí    '} [{'X' if self.aktualni_hrac.dominanty["nakupni_centrum"] else ' '}]
P  | Zabavni park           | 16   | {'Postaveno' if self.aktualni_hrac.dominanty["zabavni_park"] else 'Chybí    '} [{'X' if self.aktualni_hrac.dominanty["zabavni_park"] else ' '}]
V  | Vysilac                | 22   | {'Postaveno' if self.aktualni_hrac.dominanty["vysilac"] else 'Chybí    '} [{'X' if self.aktualni_hrac.dominanty["vysilac"] else ' '}]
================================================================================
6. AKCE
--------------------------------------------------------------------------------
[ENTER] pokračovat do další fáze
>>>  """)
    

    def info_stavba(self):
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
        print(f"""
================================================================================
 STAVBA A NÁKUPU   │  Hráč na tahu: {self.aktualni_hrac.jmeno}  │  Mince: {self.aktualni_hrac.penize}
================================================================================

3. OBCHOD   (Dostupné podniky ke koupi)
--------------------------------------------------------------------------------
ID | NAZEV BUDOVY           | CENA | AKTIVACE | TYP/BARVA | SKLADEM
--------------------------------------------------------------------------------
1  | Psenicne pole          |  1   |    1     |  Modra    |  {self.obchod.obchod["psenicne_pole"]} ks
2  | Statek                 |  1   |    2     |  Modra    |  {self.obchod.obchod["statek"]} ks
3  | Les                    |  3   |    5     |  Modra    |  {self.obchod.obchod["les"]} ks
4  | Dul                    |  6   |    9     |  Modra    |  {self.obchod.obchod["dul"]} ks
5  | Jablonovy sad          |  3   |    10    |  Modra    |  {self.obchod.obchod["jablonovy_sad"]} ks
6  | Pekarna                |  1   |  2   3   |  Zelena   |  {self.obchod.obchod["pekarna"]} ks
7  | Samoobsluha            |  2   |    4     |  Zelena   |  {self.obchod.obchod["samoobsluha"]} ks
8  | Mlekarna               |  5   |    7     |  Zelena   |  {self.obchod.obchod["mlekarna"]} ks
9  | Tovarna na nabytek     |  3   |    8     |  Zelena   |  {self.obchod.obchod["tovarna_na_nabytek"]} ks
10 | Obchodni dum           |  2   |  11  12  |  Zelena   |  {self.obchod.obchod["obchodni_dum"]} ks
11 | Kavarna                |  2   |    3     |  Cervena  |  {self.obchod.obchod["kavarna"]} ks
12 | Restaurace             |  3   |  9   10  |  Cervena  |  {self.obchod.obchod["restaurace"]} ks
13 | Stadion                |  6   |    6     |  Fialova  |  {self.obchod.obchod["stadion"]} ks
14 | Televizni studio       |  7   |    6     |  Fialova  |  {self.obchod.obchod["televizni_studio"]} ks
15 | Kancelarska budova     |  8   |    6     |  Fialova  |  {self.obchod.obchod["kancelarska_budova"]} ks

 ------------------------------------------------------------------------------
  DOMINANTY HRÁČE ({self.aktualni_hrac.jmeno})
--------------------------------------------------------------------------------
ID | NAZEV DOMINANTY        | CENA | STAV
--------------------------------------------------------------------------------
N  | Nadrazi                |  4   | {'Postaveno' if self.aktualni_hrac.dominanty["nadrazi"] else 'Chybí    '} [{'X' if self.aktualni_hrac.dominanty["nadrazi"] else ' '}]
C  | Nakupni centrum        | 10   | {'Postaveno' if self.aktualni_hrac.dominanty["nakupni_centrum"] else 'Chybí    '} [{'X' if self.aktualni_hrac.dominanty["nakupni_centrum"] else ' '}]
P  | Zabavni park           | 16   | {'Postaveno' if self.aktualni_hrac.dominanty["zabavni_park"] else 'Chybí    '} [{'X' if self.aktualni_hrac.dominanty["zabavni_park"] else ' '}]
V  | Vysilac                | 22   | {'Postaveno' if self.aktualni_hrac.dominanty["vysilac"] else 'Chybí    '} [{'X' if self.aktualni_hrac.dominanty["vysilac"] else ' '}]

   MOŽNÉ AKCE:
 ------------------------------------------------------------------------------
  - Zadáním [K]         -> Koupíš odpovídající budovu z obchodu
  - Zadáním [D]         -> postavíš dominantu
  - Zadáním [INFO]      -> Zobrazíš detailní popis karty
  - Zadáním [PASS]      -> Přeskočíš nákup a předáš tah soupeři

================================================================================
"""
)