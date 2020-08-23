from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib.auth.models import Group
from .models import ProfilePosition, Profile
from general.models import ProductoExactProfilePosition, Producto, ValeAlmacenGeneral
from llantas.models import TipoMovimiento
from llantas.utils import return_existent_profile

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
                    [True] --> 1 True, => True
    return {'ok': True}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000')}
                    [True] --> 1 True, => False
    return {'ok': True}

    quantity_i_want: 4
    dict_products: {'Filtro de aire--1': Decimal('3.0000')}
                    [False] --> ningun True, => False
    return {'Want more than existance': False}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000'), 'Aceite': Decimal('0.0000')}
                    [True, False] --> 1 True, => True
    return {'ok': Yes}

    quantity_i_want: 1
    dict_products: {'Filtro de aire--1': Decimal('0.0000'), 'Aceite': Decimal('0.0000')}
                    [False, False] --> ningun True, => False
    return {'Not enough quantity in products': False}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000'), 'Aceite': Decimal('3.0000')}
                    [True, True] --> mas de un True => False
    return {'More than one product in same position': False}

    quantity_i_want: 3
    dict_products: {'Filtro de aire--1': Decimal('3.0000'), 'Aceite': Decimal('0.0000'), 'Motor--1': Decimal('4.0000')}
                    [True, False, True] --> mas de un True => False
    return {'More than one product in same position': False}


    quantity_i_want: 1
    dict_products: {}
    return {"Not enough products": False}
    '''
    from decimal import Decimal 

    answer = {}
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

def analysis_results(list_results):
    '''
    list_results = [{'Not enough products': 1}, {'Not enough products': 1}, {'ok': 0}]
    '''
    ok = 0
    for dicc_result in list_results:
        ok = ok + sum(dicc_result.values())
    return ok == 0, list_results

def verify_profilepositions(list_ids_profile_position):
    '''
    recieve a list of id_profile_positions [1, 1, 2, 3]
    recieve a set of id_profile_positions (1, 2, 3)
    must check, if in each profile_position are enough stock,
    of if are more than one product in each position
    '''
    set_ids_profile_position =  set(list_ids_profile_position)
    dict_ids_profile_position = group_profile_positions(
        set_ids_profile_position, list_ids_profile_position)
    answer = False
    results = []
    list_results = []
    for id_profile_position in dict_ids_profile_position:
        pp = ProfilePosition.objects.get(id=id_profile_position)
        pp_products = pp.producto_exact_profile_positions_quantity_by_product()
        i_want = dict_ids_profile_position[id_profile_position]
        results.append(verify_quantity(i_want, pp_products))
    answer, list_results = analysis_results(results)
    return answer, list_results