from funkce import vypocet_vzdalenosti, nacteni_souboru
from statistics import median
from pyproj import Transformer

#definice konstanty maximální vzdálenosti, kterou nesmí minimální vzdálenost překročit
MAX_VZD = 10000

#načtení vstupních souborů
adresy = nacteni_souboru("adresy.geojson")
kontejnery = nacteni_souboru("kontejnery.geojson")

#výběr jen veřejných kontejnerů
verejne_kontejnery = []
counter_kontejnery = 0
for feature in kontejnery["features"]:
    if feature["properties"]["PRISTUP"] == "volně":
        verejne_kontejnery.append(feature)
        counter_kontejnery += 1

#hledání nejbližšího kontejneru
min_vzdalenost = float('inf')
max_vzdalenost = 0
sum_vzdalenost = 0
seznam_vzdalenosti = []

#vytvoření Transformer objektu pro převod souřadnic
wgs2jtsk = Transformer.from_crs(4326,5514,always_xy=True)

for feature in adresy['features']:
    #načtení informací o adresním bodu
    id_adresa = feature["properties"]["@id"]
    ulice = feature["properties"]["addr:street"]
    cislo_pop = feature["properties"]["addr:housenumber"]

    #převedení souřadnic adresních bodů do S-JTSK
    try:
        feature["geometry"]["coordinates_sjtsk"] = list(wgs2jtsk.transform(*feature["geometry"]["coordinates"]))
        x1,y1 = feature["geometry"]["coordinates_sjtsk"]
    except TypeError:
        print(f"U adresního bodu {id_adresa} s adresou {ulice} {cislo_pop} jsou chybí jedna nebo obě souřadnice a program ho přeskočí.")
        continue

    #výpočet minimální vzdálenosti
    try:
        for kontejner in verejne_kontejnery:
            id_kontejner = kontejner["properties"]["ID"]
            adr_kontejner = kontejner["properties"]["STATIONNAME"]
            x2,y2 = kontejner["geometry"]["coordinates"]
            vzdalenost = vypocet_vzdalenosti(x1,y1,x2,y2)
            if vzdalenost < min_vzdalenost:
                min_vzdalenost = vzdalenost
    except ValueError:
        print(f"U kontejneru {id_kontejner} na adrese {adr_kontejner} jsou chybně zadané souřadnice nebo jedna či obě chybí a program ho přeskočí.")

    #kontrola, že minimální vzdálenost není větší než definovaná maximální vzdálenost
    if min_vzdalenost > MAX_VZD:
        print(f"U adresního bodu {id_adresa} s adresou {ulice} {cislo_pop} je vzdálenost k nejbližšímu kontejneru větší než 10 km.")
        quit()
    
    #přiřazení do proměnné, pokud je vzdálenost větší než aktuální maximální vzdálenost
    if min_vzdalenost > max_vzdalenost:
        max_vzdalenost = min_vzdalenost
        ulice_max = feature["properties"]["addr:street"]
        cislo_pop_max = feature["properties"]["addr:housenumber"]

    sum_vzdalenost += min_vzdalenost
    seznam_vzdalenosti.append(min_vzdalenost)

prumerna_vzdalenost = (sum_vzdalenost / len(seznam_vzdalenosti))
median_vzdalenosti = (median(seznam_vzdalenosti))

print(f"Načteno {len(seznam_vzdalenosti)} adresních bodů.")
print(f"Načteno {counter_kontejnery} veřejných kontejnerů.\n")
print(f"Průměrná vzdálenost ke kontejneru je {prumerna_vzdalenost:.0f} m.")
print(f"K nejbližšímu kontejneru je to nejdále z adresy {ulice_max} {cislo_pop_max} a to {max_vzdalenost:.0f} m.")
print(f"Medián vzdálenosti ke kontejneru je {median_vzdalenosti:.0f} m.\n")