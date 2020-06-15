import csv 
from django.conf import settings

with open(settings.BASE_DIR + '/load_init/all_medidas.csv') as csvfile_in:
    readCSV = csv.reader(csvfile_in, delimiter=';')
    lista_marcas = []
    for indice, row in enumerate(readCSV):
        if indice == 0: # quit name of column
            print("header: {}".format(row))
        else:
            nombre = row[0].strip().capitalize()
            lista_marcas.append(nombre)

print("len lista_marcas", len(lista_marcas), lista_marcas)
print("-------------------------------")
set_marcas = set(lista_marcas)
print(set_marcas)
unique_marcas = list(set_marcas)
unique_marcas.sort()
print("-------------------------------")
print(len(unique_marcas), unique_marcas)
for unique in unique_marcas:
    print(unique)

with open(settings.BASE_DIR + '/load_init/all_medidas_unique.csv', 'w') as csvfile_out:
    writer = csv.writer(csvfile_out)
    for unique in unique_marcas:
        writer.writerow([unique])
