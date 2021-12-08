from pyproj import Transformer
from math import sqrt

def prevod_souradnic(x,y):
    wgs2jtsk = Transformer.from_crs(4326,5514,always_xy=True)
    return wgs2jtsk.transform(x,y)

def vypocet_vzdalenosti(x1,y1,x2,y2):
    return int(sqrt((x2-x1)**2 + (y2-y1)**2))


