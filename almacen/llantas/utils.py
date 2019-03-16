from django.contrib.auth.models import User
from persona.models import Profile, Tipo

def return_or_create_user(username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        u = User.objects.create_user(username, '{}@fletesexpress.com.mx'.format(username), 'esteesunpasswordtest785412')
    return u

def create_profile(user, tipo="STAFF"):

    tipo, flag = Tipo.objects.get_or_create(nombre=tipo)
    try:
        p = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        p = Profile.objects.create(user=user, tipo=tipo)
    return p

def return_profile(username, tipo="STAFF"):
    u = return_or_create_user(username)
    return create_profile(u, tipo)

def split_list(lista):
    return [(x[0].split("__"), x[1])for x in lista]
