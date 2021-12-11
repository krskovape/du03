from funkce import prevod_souradnic, vypocet_vzdalenosti, nacteni_souboru

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
counter_adresy = 0

for feature in adresy['features']:
    #převedení souřadnic adresních bodů do S-JTSK
    try:
        feature["geometry"]["coordinates_sjtsk"] = list(prevod_souradnic(*feature["geometry"]["coordinates"]))
        x1,y1 = feature["geometry"]["coordinates_sjtsk"]
        id_adresa = feature["properties"]["@id"]
    except ValueError:
        print(f"U adresního bodu {id_adresa} jsou chybně zadané souřadnice a program ho přeskočí.") 
        continue

    #výpočet minimální vzdálenosti
    for kontejner in verejne_kontejnery:
        try:
            x2,y2 = kontejner["geometry"]["coordinates"]
            id_kontejner = kontejner["properties"]["ID"]
        except ValueError:
            print(f"U kontejneru {id_kontejner} jsou chybně zadané souřadnice a program ho přeskočí.")
            continue

        vzdalenost = vypocet_vzdalenosti(x1,y1,x2,y2)
        if vzdalenost < min_vzdalenost:
            min_vzdalenost = vzdalenost

    #kontrola, že minimální vzdálenost není větší než 10 km
    if min_vzdalenost > 10000:
        print(f"U adresního bodu {id_adresa} je vzdálenost k nejbližšímu kontejneru větší než 10 km.")
        quit()
    
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