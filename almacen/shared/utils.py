from general.models import Producto
import textdistance as textd

def compare_with_db(nombre_producto, numero_porcentaje_parecido=.5):
    '''
    esta funcion compara una cadena nombre_producto
    contra todas los productos de la db
    si el parecido es mayor o igual a numero_porcentaje_parecido, se agrega a la lista de parecidos
    finralmente se regresa la lista de parecidos, pero ordenados por los mas parecidos hasta arriba
    '''
    respuesta = False
    lista = []
    for productodb in Producto.objects.all():                                                                                                                                                    
        numero = textd.levenshtein.normalized_similarity(productodb.nombre, nombre_producto) 
        if numero >= numero_porcentaje_parecido:                                                         
            lista.append((numero, nombre_producto, productodb.nombre))
            respuesta = True

    lista_sorted = sorted(lista, key=lambda x: x[0], reverse=True)
    return respuesta, lista_sorted