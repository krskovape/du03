import json
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

        #převod souřadnic adresních bodů do S-JTSK
        for feature in adresy["features"]:
            x = feature["geometry"]["coordinates"][0]
            y = feature["geometry"]["coordinates"][1]
            feature["geometry"]["souřadnice"] = prevod_souradnic(x,y)

        #hledání nejbližšího kontejneru
        max_vzdalenost = 0
        sum_vzdalenost = 0
        counter_adresy = 0

        for feature in adresy['features']:
            x1 = feature["geometry"]["souřadnice"][0]
            y1 = feature["geometry"]["souřadnice"][1]
            min_vzdalenost = 0

            #výpočet minimální vzdálenosti
            for kontejner in verejne_kontejnery:
                x2 = kontejner["geometry"]["coordinates"][0]
                y2 = kontejner["geometry"]["coordinates"][1]
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

