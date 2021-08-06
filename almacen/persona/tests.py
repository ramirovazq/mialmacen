from django.test import TestCase
from persona.models import *

class PositionTestCase(TestCase):

    def setUp(self):
        gran_gran_gran = Position.objects.create(name="ANAQUEL 22")
        gran_gran = Position.objects.create(name="NIVEL DE ANAQUEL 345", parent=gran_gran_gran)
        gran = Position.objects.create(name="POSICION 67", parent=gran_gran)
        self.pos = Position.objects.create(name="SUBPOSICION 890", parent=gran)

    def test_label(self):
        p = self.pos
        self.assertEqual(p.code(), 'A22N345P67S890')
