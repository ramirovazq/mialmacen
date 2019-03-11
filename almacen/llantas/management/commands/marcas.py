import csv 
from ..models import *

with open('marcas.csv') as csvfile_in:
    readCSV = csv.reader(csvfile_in, delimiter=';')
    for indice, row in enumerate(readCSV):
        if indice != 0: # quit name of column
            nombre = row[0].strip().capitalize()
            codigo = row[1].strip()
            print("{} {}".format(nombre, codigo))
print("Marcas")            
Marca.objects.all()
