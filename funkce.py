from pyproj import Transformer
from math import sqrt
import json
from json.decoder import JSONDecodeError

#převedení vstupních souřadnic do S-JTSK
def prevod_souradnic(x,y):
    wgs2jtsk = Transformer.from_crs(4326,5514,always_xy=True)
    return wgs2jtsk.transform(x,y)

#výpočet vzdálenosti mezi vstupními body
def vypocet_vzdalenosti(x1,y1,x2,y2):
    return int(sqrt((x2-x1)**2 + (y2-y1)**2))

#načtení souboru a ošetření nekorektního vstupu
def nacteni_souboru(nazev_souboru):
    try:
        with open(nazev_souboru, encoding="utf-8") as s:
            return json.load(s)
    except FileNotFoundError:
        print(f"Zadaný soubor {nazev_souboru} otevřít. Soubor neexistuje, nebo je chybně zadaná cesta k jeho umístění.")
        quit()
    except PermissionError:
        print(f"Program nemá dostatečná oprávnění k souboru {nazev_souboru}.")
        quit()
    except JSONDecodeError:
        print(f"Vstupní soubor {nazev_souboru} není platný JSON.")
        quit()



