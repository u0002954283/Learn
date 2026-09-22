#---------------------------------setup-----------------------------------------#
from hrac import Hrac
from data import *
from hra import Hra
from stul import Obchod



def hra_final():
    hra = Hra()

    while hra.pokracovani:


        hra.info()
        hod1, hod2, tah_na_vic = hra.hod_kostkou()
        hra.prijmi_a_vydaje(hod1 + hod2)
        hra.info()
        hra.stavba()
        if not tah_na_vic:
            hra.dalsi_hrac()


#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    hra_final()