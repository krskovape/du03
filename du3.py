import json
from json.decoder import JSONDecodeError
from funkce import prevod_souradnic, vypocet_vzdalenosti

try:
    with open("adresy.geojson", encoding="utf-8") as a,\
        open("kontejnery.geojson", encoding="utf-8") as k:

        adresy = json.load(a)
        kontejnery = json.load(k)

        #výběr jen veřejných kontejnerů
        verejne_kontejnery = []
        counter_kontejnery = 0
        for feature in kontejnery["features"]:
            if feature["properties"]["PRISTUP"] == "volně":
                verejne_kontejnery.append(feature)
                counter_kontejnery += 1

        #hledání nejbližšího kontejneru
        max_vzdalenost = 0
        sum_vzdalenost = 0
        counter_adresy = 0

        for feature in adresy['features']:
            #převedení souřadnic adresních bodů do S-JTSK
            try:
                feature["geometry"]["souřadnice"] = prevod_souradnic(feature["geometry"]["coordinates"][0], feature["geometry"]["coordinates"][1])
                x1 = float(feature["geometry"]["souřadnice"][0])
                y1 = float(feature["geometry"]["souřadnice"][1])
                id_adresa = feature["properties"]["@id"]
                min_vzdalenost = 0
            except ValueError:
                print(f"U adresního bodu {id_adresa} jsou chybně zadané souřadnice a program ho přeskočí.") 
                continue

            #výpočet minimální vzdálenosti
            for kontejner in verejne_kontejnery:
                try:
                    x2 = float(kontejner["geometry"]["coordinates"][0])
                    y2 = float(kontejner["geometry"]["coordinates"][1])
                    id_kontejner = kontejner["properties"]["ID"]
                except ValueError:
                    print(f"U kontejneru {id_kontejner} jsou chybně zadané souřadnice a program ho přeskočí.")
                    continue

                vzdalenost = vypocet_vzdalenosti(x1,y1,x2,y2)
                if min_vzdalenost == 0:
                    min_vzdalenost = vzdalenost
                if vzdalenost < min_vzdalenost:
                    min_vzdalenost = vzdalenost

            #kontrola, že minimální vzdálenost není větší než 10 km
            try:
                min_vzdalenost < 10000
            except:
                print("Vzdálenost k nejbližšímu kontejneru je větší než 10 km.")
            
            if min_vzdalenost > max_vzdalenost:
                max_vzdalenost = min_vzdalenost
                ulice = feature["properties"]["addr:place"]
                cislo_pop = feature["properties"]["addr:housenumber"]

            sum_vzdalenost += min_vzdalenost
            counter_adresy += 1
        
        prumerna_vzdalenost = int(sum_vzdalenost / counter_adresy)

        print(f"Načteno {counter_adresy} adresních bodů.")
        print(f"Načteno {counter_kontejnery} veřejných kontejnerů.\n")
        print(f"Průměrná vzdálenost ke kontejneru je {prumerna_vzdalenost} m.")
        print(f"K nejbližšímu kontejneru je to nejdále z adresy {ulice} {cislo_pop} a to {max_vzdalenost} m.\n")

except FileNotFoundError:
    print("Zadaný soubor se vstupními daty nelze otevřít. Soubor neexistuje, nebo je chybně zadaná cesta k jeho umístění.")
except PermissionError:
    print("Program nemá dostatečná oprávnění ke vstupnímu nebo výstupnímu programu.")
except JSONDecodeError:
    print("Vstupní soubor není platný JSON.")
