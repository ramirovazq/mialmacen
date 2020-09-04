from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib.auth.models import Group
from .models import ProfilePosition, Profile
from general.models import ProductoExactProfilePosition, Producto, ValeAlmacenGeneral
from persona.models import ProfilePosition
from llantas.models import TipoMovimiento
from llantas.utils import return_existent_profile
from decimal import Decimal

def verify_profileposition(profileposition_id):
    try:
        ProfilePosition.objects.get(id=profileposition_id)
    except ProfilePosition.DoesNotExist:
        return False
    except ValueError:
        return False
    except:
        return False
    return True

def verify_product(product_id):
    try:
        Producto.objects.get(id=product_id)
    except Producto.DoesNotExist:
        return False
    except ValueError:
        return False
    except:
        return False
    return True

def verify_int_quantity(quantity):
    try:
        quantity = int(quantity)
    except ValueError:
        return False
    except:
        return False
    esinstancia = isinstance(quantity, int)
    if esinstancia:
        return quantity > 0
    return False



def group_required(*group_names):
   def in_groups(user):
       if user.is_authenticated:
           if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)

def verify_list_profileposition(list_ids_profile_position):
    len_list_ids_profile_position = len(list_ids_profile_position)
    len_profile_position = len(ProfilePosition.objects.filter(id__in=list_ids_profile_position))
    return len_list_ids_profile_position == len_profile_position

def verify_destino(profile_id):
    try:
        Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return False
    except ValueError:
        return False
    return True

def group_profile_positions(set_ids_profile_position, list_ids_profile_position):
    '''
    recieve a list of id_profile_positions [1, 1, 2, 3, 1, 1, 3]
    recieve a set of id_profile_positions (1, 2, 3)
    {1 : 4, 2 : 1, 3 : 2}
    '''
    set_ids_profile_position =  set(list_ids_profile_position)
    dict_ids_profile_position = dict.fromkeys(set_ids_profile_position, 0)
    for x in list_ids_profile_position:
        dict_ids_profile_position[x] = dict_ids_profile_position[x] + 1
    return dict_ids_profile_position

def verify_quantity(quantity_i_want, dict_products):
    '''
    quantity_i_want: 1
    dict_products: {'Filtro de aire--1': Decimal('3.0000')}
                    [1]    -->  [1]    
                    [True] --> 1 True, => True
    return {'ok': True}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000')}
                    [1]    --> [1]
                    [True] --> 1 True, => False
    return {'ok': True}

    quantity_i_want: 4
    dict_products: {'Filtro de aire--1': Decimal('3.0000')}
                    [1]  --> []
                    [False] --> ningun True, => False
    return {'Want more than existance': False}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000'), 'Aceite--4': Decimal('0.0000')}
                    [1, 4]  -->[1]
                    [True, False] --> 1 True, => True
    return {'ok': Yes}

    quantity_i_want: 1
    dict_products: {'Filtro de aire--1': Decimal('0.0000'), 'Aceite--4': Decimal('0.0000')}
                    [1, 4]  --> []
                    [False, False] --> ningun True, => False
    return {'Not enough quantity in products': False}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000'), 'Aceite--4': Decimal('3.0000')}
                    [1, 4] --> []
                    [True, True] --> mas de un True => False
    return {'More than one product in same position': False}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000'), 'Aceite--4': Decimal('0.0000'), 'Motor--5': Decimal('4.0000')}
                    [1, 4, 5]  --> []
                    [True, False, True] --> mas de un True => False
    return {'More than one product in same position': False}


    quantity_i_want: 1
    dict_products: {}
    return {"Not enough products": False}
    ''' 

    answer = {}
    list_products = []
    quantity = Decimal(quantity_i_want)

    if len(dict_products.keys()) <= 0:
        return {"Not enough products": 1}

    check_list = []
    for producto in dict_products:
        if dict_products[producto] >= quantity:
            check_list.append(True) 
        else:
            check_list.append(False)
    quantity_ok = sum(check_list)
    if quantity_ok == 1:
        return {'ok': 0 }
    elif quantity_ok == 0:
        answer['Not enough quantity of products or Want more than existance'] = 1
    else:
        answer['More than one product in same position'] = 1
    return answer


def return_valid_products_and_quantity(quantity_i_want, dict_products):
    '''
    quantity_i_want: 1
    dict_products: {'Filtro de aire--1': Decimal('3.0000')}
                          -->  {'Filtro de aire--1': Decimal('3.0000')}
                    [True] --> 1 True, => True
    return {'ok': True}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000')}
                         --> {'Filtro de aire--1': Decimal('3.0000')}
                    [True] --> 1 True, => False
    return {'ok': True}

    quantity_i_want: 4
    dict_products: {'Filtro de aire--1': Decimal('3.0000')}
                       --> {}
                    [False] --> ningun True, => False
    return {'Want more than existance': False}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000'), 'Aceite--4': Decimal('0.0000')}
                    [1, 4]  --> {'Filtro de aire--1': Decimal('3.0000')}
                    [True, False] --> 1 True, => True
    return {'ok': Yes}

    quantity_i_want: 1
    dict_products: {'Filtro de aire--1': Decimal('0.0000'), 'Aceite--4': Decimal('0.0000')}
                    [1, 4]  --> {}
                    [False, False] --> ningun True, => False
    return {'Not enough quantity in products': False}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000'), 'Aceite--4': Decimal('3.0000')}
                    [1, 4] --> {}
                    [True, True] --> mas de un True => False
    return {'More than one product in same position': False}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000'), 'Aceite--4': Decimal('0.0000'), 'Motor--5': Decimal('4.0000')}
                    [1, 4, 5]  --> {'Filtro de aire--1': Decimal('3.0000'), 0, 'Motor--5': Decimal('4.0000')} --> {}
                    [True, False, True] --> mas de un True => False
    return {'More than one product in same position': False}


    quantity_i_want: 1
    dict_products: {}
    [1, 4, 5]  --> {}
    return {"Not enough products": False}
    '''

    if len(dict_products.keys()) <= 0:
        return []

    quantity = Decimal(quantity_i_want)
    check_list = []
    list_results = []

    for producto in dict_products:
        if dict_products[producto] >= quantity:
            l_producto = producto.split("--")
            id_producto = l_producto[1]
            list_results.append({id_producto: quantity})
            check_list.append(True)
        else:
            check_list.append(False)

    quantity_ok = sum(check_list)

    if quantity_ok == 1:
        return list_results
    elif quantity_ok == 0:
        answer = []
    else:
        answer = []
    return answer



def analysis_results(list_results):
    '''
    list_results = [{'Not enough products': 1}, {'Not enough products': 1}, {'ok': 0}]
    '''
    ok = 0
    for dicc_result in list_results:
        ok = ok + sum(dicc_result.values())
    return ok == 0, list_results


def verify_profileposition_insert(profileposition_id, product_id, quantity):
    pp = ProfilePosition.objects.get(id=profileposition_id)
    if len(ProductoExactProfilePosition.objects.filter(exactposition=pp)) > 0:
        return False, ["Already a product in position"]
    producto = Producto.objects.get(id=product_id)
    if len(producto.movimientos(tipo="ENTRADA")) > 0:
        return False, ["Product with movements"]
    return True, []

def prepare_data_for_movimientos(product_id, quantity, profileposition_id):
    producto = Producto.objects.get(id=product_id)
    pp = ProfilePosition.objects.get(id=profileposition_id)
    return  [{f'{producto.id}': Decimal(quantity)}], [pp]

def verify_profilepositions(list_ids_profile_position):
    '''
    recieve a list of id_profile_positions [1, 1, 2, 3]
    generates a set of id_profile_positions {1:2, 2:1, 3:1}
    must check, if in each profile_position are enough stock,
    of if is more than one product in each position

    answer: Boolean, true if its posible to post, or false
    list_results = [{'Not enough products': 1}, {'Not enough products': 1}, {'ok': 0}] 
    products =  [{'Filtro de aire--1': Decimal('3.0000'), 0, 'Motor--5': Decimal('4.0000')}]
    list_id_profile_position = [1,2,3]
    '''
    set_ids_profile_position =  set(list_ids_profile_position)
    dict_ids_profile_position = group_profile_positions(
        set_ids_profile_position, list_ids_profile_position)
    answer = False
    results = []
    list_results = []
    products = []
    list_id_profile_position =[]

    for id_profile_position in dict_ids_profile_position:
        pp = ProfilePosition.objects.get(id=id_profile_position)
        pp_products = pp.producto_exact_profile_positions_quantity_by_product()
        i_want = dict_ids_profile_position[id_profile_position]
        results.append(verify_quantity(i_want, pp_products))
        products = products + return_valid_products_and_quantity(i_want, pp_products)
        list_id_profile_position.append(pp)

    answer, list_results = analysis_results(results)
    if answer:
        return answer, list_results, products, list_id_profile_position
    else:
        return answer, list_results, [], []