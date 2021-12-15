# Domácí úkol 3 - vzdálenost ke kontejnerům na tříděný odpad

## Vstupní data
Na vstupu bere program 2 soubory GeoJSON. Soubor s názvem `adresy.geojson` obsahuje data adresních bodů se souřadnicemi ve WGS-84. 
V atributu `@id` je uvedeno označení adresního bodu, v atributu `addr:street` jméno ulice a v atributu `addr:housenumber` číslo popisné. 
Druhý soubor s názvem `kontejnery.geojson` obsahuje data kontejnerů na tříděný odpad se souřadnicemi v S-JTSK. 
V atributu `ID` je uvedeno označení kontejneru, v atributu `STATIONNAME` adresa, kde se kontejner nachází 
a v atributu `PRISTUP` je uvedeno `volně`, pokud je kontejner veřejně přístupný, jinak `obyvatelům domu`.

## Výstup
Program vypíše, kolik bylo načteno adresních bodů a kontejnerů. Dále vrátí průměrnou nejkratší vzdálenost k veřejně dostupným kontejnerům a vypíše, 
ze které adresy je to k nejbližšímu kontejneru nejdále a o jakou vzdálenost se jedná. Na závěr vypíše medián vzdáleností.
