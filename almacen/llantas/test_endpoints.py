from django.test import TestCase

# Django Rest Framework
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from llantas.utils import return_profile
from llantas.models import TipoMovimiento, Vale, Marca, Medida
from llantas.models import Posicion, Status, Llanta, Movimiento
from loguru import logger as log

class ValeLlantaTestCase(TestCase):

    def setUp(self):

        username1 = "user"
        password1 = "queonda"
        self.profile01 = return_profile(username1) # Persona.models.Profile
        self.profile02 = return_profile(username1 + '1') # Persona.models.Profile

        u = User.objects.get(username=username1)
        u.set_password(password1)
        u.save()

        self.client = APIClient()

        self.tm_entrada = TipoMovimiento.objects.create(nombre="ENTRADA")
        self.tm_salida  = TipoMovimiento.objects.create(nombre="SALIDA")

        self.client.login(username=username1, password=password1)

        self.bodega01 = return_profile("ALMACEN_GENERAL", "BODEGA")
        self.tractor01 = return_profile("TRACTOR01", "ECONOMICO")
        self.permisionario01 = return_profile("Susan", "PERMISIONARIO")

        ## llanta 01
        marca01 = Marca.objects.create(nombre="Michelin")
        medida01 = Medida.objects.create(nombre="11R245")
        posicion01 = Posicion.objects.create(nombre="T.P.")
        status_nueva = Status.objects.create(nombre="Nueva")
        #status_rodar = Status.objects.create(nombre="Rodar")
        #porcentaje_rodar_01 = 30
        #porcentaje_rodar_02 = 50
        dot01 = "2323"

        # se crea una llanta
        self.clase_llanta01 = Llanta.objects.create(
            marca=marca01,
            medida=medida01,
            posicion=posicion01,
            status=status_nueva,
            dot=dot01,
        )


        '''
        # Other authentication method
        response = self.client.post('/api/v0/login/', {
            "username": username1,
            "password": password1
        }, format="json")

        json = response.json()
        '''
        # {
        # 'token': '111111222', 
        # 'email': 'user@example.mx', 
        # 'user_id': 1, 
        # 'profile_id': 1, 
        # 'username': 'admin'
        # }


    def tearDown(self) -> None:
        self.client.logout()

    def test_genera_vale_y_movimiento(self):
        
        response = self.client.post('/api/v0/vale/', 
            {
                "vale_llantas": True,
		        "observaciones_grales": "ping",
		        "fecha_vale": "2022-07-03",
		        "tipo_movimiento": self.tm_salida.id,
		        "persona_asociada": self.profile02.id,
		        "creador_vale": self.profile01.id
		      }, format='multipart')
        log.debug(response.json())

        r_json = response.json()
        self.vale_id = r_json['id']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        vale_llantas = Vale.objects.filter(vale_llantas=True)
        self.assertEqual(len(vale_llantas), 1)

        response = self.client.post('/api/v0/movimiento/', 
            {
                "vale": self.vale_id,
		        "tipo_movimiento": self.tm_salida.id,
		        "fecha_movimiento": "2022-07-03",
                "origen": self.bodega01.id,
                "destino": self.tractor01.id,
                "cantidad": 2,
                "precio_unitario": 0,
                "creador":self.profile01.id,
                "observacion": "sin observacion",
                "permisionario": self.permisionario01.id,
                "llanta": self.clase_llanta01.id

		      }, format='multipart')

        log.debug(response.json())

        movimiento_llantas = Movimiento.objects.all()
        self.assertEqual(len(movimiento_llantas), 1)


class MarcaLlantaTestCase(TestCase):

    def setUp(self):

        username1 = "user"
        password1 = "queonda"
        self.profile01 = return_profile(username1) # Persona.models.Profile

        u = User.objects.get(username=username1)
        u.set_password(password1)
        u.save()

        self.client = APIClient()
        self.client.login(username=username1, password=password1)


    def test_genera_marca(self):
        response = self.client.post('/api/v0/marca/', 
            {"nombre": "goodyear",})
        log.debug(response.json())
        marcas = Marca.objects.all()
        self.assertEqual(len(marcas), 1)

    def test_devuelve_marca(self):

        # add on marca
        self.client.post('/api/v0/marca/', 
            {"nombre": "goodyear",})

        response = self.client.get('/api/v0/marca/')
        log.debug(response.json())
        marcas = Marca.objects.all()
        self.assertEqual(len(marcas), 1)


class LlantaTestCase(TestCase):

    def setUp(self):

        username1 = "user"
        password1 = "queonda"
        self.profile01 = return_profile(username1) # Persona.models.Profile
        self.profile02 = return_profile(username1 + '1') # Persona.models.Profile

        u = User.objects.get(username=username1)
        u.set_password(password1)
        u.save()

        self.client = APIClient()

        self.tm_entrada = TipoMovimiento.objects.create(nombre="ENTRADA")
        self.tm_salida  = TipoMovimiento.objects.create(nombre="SALIDA")

        self.client.login(username=username1, password=password1)

        self.bodega01 = return_profile("ALMACEN_GENERAL", "BODEGA")
        self.tractor01 = return_profile("TRACTOR01", "ECONOMICO")
        self.permisionario01 = return_profile("Susan", "PERMISIONARIO")

        
        ## llanta 01
        marca01 = Marca.objects.create(nombre="Michelin")
        medida01 = Medida.objects.create(nombre="11R245")
        posicion01 = Posicion.objects.create(nombre="T.P.")
        status_nueva = Status.objects.create(nombre="Nueva")
        #status_rodar = Status.objects.create(nombre="Rodar")
        #porcentaje_rodar_01 = 30
        #porcentaje_rodar_02 = 50
        dot01 = "2323"

        # se crea una llanta
        self.clase_llanta01 = Llanta.objects.create(
            marca=marca01,
            medida=medida01,
            posicion=posicion01,
            status=status_nueva,
            dot=dot01,
        )



    def test_genera_llanta(self):

        ## llanta 01
        marca02 = Marca.objects.create(nombre="Michelin2")
        log.debug(".....ping.........")
        log.debug(marca02)
        medida02 = Medida.objects.create(nombre="11R2452")
        posicion02 = Posicion.objects.create(nombre="T.P.2")
        status_rodar = Status.objects.create(nombre="Rodar")
        porcentaje_rodar_02 = 50
        dot02 = "2323"

        response = self.client.post('/api/v0/llanta/', 
            {
                "marca": "1",
		        "medida": "1",
		        "posicion": posicion02.id,
		        "status": status_rodar.id,
		        "dot": dot02,
		        "porciento_vida": porcentaje_rodar_02
		      }, format='json')

        log.debug(response.json())
        llantas = Llanta.objects.all()
        log.debug(llantas)
        self.assertEqual(len(llantas), 2)

        