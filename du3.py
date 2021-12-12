from funkce import prevod_souradnic, vypocet_vzdalenosti, nacteni_souboru
from statistics import median

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

for feature in adresy['features']:
    #převedení souřadnic adresních bodů do S-JTSK
    feature["geometry"]["coordinates_sjtsk"] = list(prevod_souradnic(*feature["geometry"]["coordinates"]))
    x1,y1 = feature["geometry"]["coordinates_sjtsk"]
    id_adresa = feature["properties"]["@id"]

    #výpočet minimální vzdálenosti
    for kontejner in verejne_kontejnery:
        x2,y2 = kontejner["geometry"]["coordinates"]
        vzdalenost = vypocet_vzdalenosti(x1,y1,x2,y2)
        if vzdalenost < min_vzdalenost:
            min_vzdalenost = vzdalenost

    #kontrola, že minimální vzdálenost není větší než 10 km
    if min_vzdalenost > 10000:
        ulice = feature["properties"]["addr:place"]
        cislo_pop = feature["properties"]["addr:housenumber"]
        print(f"U adresního bodu {id_adresa} s adresou {ulice} {cislo_pop} je vzdálenost k nejbližšímu kontejneru větší než 10 km.")
        quit()
    
    #přiřazení do proměnné, pokud je vzdálenost větší než aktuální maximální vzdálenost
    if min_vzdalenost > max_vzdalenost:
        max_vzdalenost = min_vzdalenost
        ulice_max = feature["properties"]["addr:place"]
        cislo_pop_max = feature["properties"]["addr:housenumber"]

    sum_vzdalenost += min_vzdalenost
    seznam_vzdalenosti.append(min_vzdalenost)

prumerna_vzdalenost = (sum_vzdalenost / len(seznam_vzdalenosti))
median_vzdalenosti = (median(seznam_vzdalenosti))

print(f"Načteno {len(seznam_vzdalenosti)} adresních bodů.")
print(f"Načteno {counter_kontejnery} veřejných kontejnerů.\n")
print(f"Průměrná vzdálenost ke kontejneru je {prumerna_vzdalenost:.1f} m.")
print(f"K nejbližšímu kontejneru je to nejdále z adresy {ulice_max} {cislo_pop_max} a to {max_vzdalenost:.1f} m.")
print(f"Medián vzdálenosti ke kontejneru je {median_vzdalenosti:.1f} m.\n")