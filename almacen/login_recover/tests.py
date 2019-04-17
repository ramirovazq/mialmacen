from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

# Create your tests here.
'''
http --form POST http://127.0.0.1:8000/api/v0/login/ username="usuario" password="unpasswordcorrecto" #200 Forbidden
http --form POST http://127.0.0.1:8000/api/v0/login/ username="usuario" password="unpassword"    #401 Forbidden
http --form POST http://127.0.0.1:8000/api/v0/login/ username="admin"                         #400 Forbidden
'''

class RecoverTestCase(TestCase):

  def setUp(self):

    self.username = "usuario"
    self.username1 = "usuario1"
    self.password = "unpasswordcorrecto"
    self.password1 = "1esteeselpasswordusuario"

    self.usuario  = User.objects.create_user(self.username, "usuario@hola.com", self.password)
    self.tokenusuario = Token.objects.create(user=self.usuario)

    self.usuario1  = User.objects.create_user(self.username1, "usuario1@hola.com", self.password1)
    self.client = APIClient()


  def test_api_login(self):
    response = self.client.post('/api/v0/login/', {'username': self.username, 'password': self.password})    
    self.assertEqual(response.status_code, 200)#osea ok
    r_json = response.json()
    self.assertNotEqual(r_json['token'],'')
  
  def test_api_wrong_login(self):
    response = self.client.post('/api/v0/login/', {'username': self.username, 'password': 'unmalpassword'})    
    self.assertEqual(response.status_code, 401)#forbidden
  
  def test_api_wrong_parameters_login(self):
    response = self.client.post('/api/v0/login/', {'username': self.username})    
    self.assertEqual(response.status_code, 400)# bad request

  def test_api_wrong_empty_login(self):
    response = self.client.post('/api/v0/login/', {})    
    self.assertEqual(response.status_code, 400)# bad request  

  def test_api_login_notoken(self):
    response = self.client.post('/api/v0/login/', {'username': self.username1, 'password': self.password1})    
    self.assertEqual(response.status_code, 404)#osea not found
  
  def test_api_login_creating_token(self):
    Token.objects.create(user=self.usuario1)
    response = self.client.post('/api/v0/login/', {'username': self.username1, 'password': self.password1})    
    self.assertEqual(response.status_code, 200)#osea ok

  def test_api_login_wrong(self):
    response = self.client.post('/api/v0/login/', {'username': self.username, 'password': self.password+'wrong'})
    self.assertEqual(response.status_code, 401)#forbidden  
    