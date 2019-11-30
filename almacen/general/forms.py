from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.db.models import Q
from .models import *
from persona.models import Profile
from llantas.utils import agrupacion_dots, devuelve_llanta
from llantas.forms import TipoMovimientoChoiceField, OrigenChoiceField, DestinoChoiceField, OrigenDestinoChoiceField, ProfileChoiceField, ValeForm, EntradaForm


class FilterMovimientoForm(ModelForm):
    
    tipo_movimiento = TipoMovimientoChoiceField(
                required=False,
                queryset=TipoMovimiento.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )
    
    fecha_movimiento_inicio = forms.DateField(
                required=False,
                label='Fecha movimiento inicio', 
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
                }
    ))
    fecha_movimiento_fin = forms.DateField(
                required=False,
                label='Fecha movimiento fin',
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
                }
    ))

    date_created_inicio = forms.DateField(
                required=False,
                label='Fecha creacion inicio', 
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
                }
    ))
    date_created_fin = forms.DateField(
                required=False,
                label='Fecha creacion fin',
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
                }
    ))

    no_folio = forms.CharField(
            required=False,
            label='No Folio', 
            max_length="100",
            widget=forms.TextInput(
                attrs={
                'class':'form-control',
                'placeholder':'Ejemplo: AAAA'
                }
    ))


    exporta_xls = forms.BooleanField(
                required=False,
                label='Exporta XLS', 
    )



    exporta = forms.BooleanField(
                required=False,
            label='Exporta CSV', 
    )

    origen = OrigenDestinoChoiceField(
                required=False,
                queryset=TipoMovimiento.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    class Meta: 
        model = MovimientoGeneral
        fields = ['tipo_movimiento', 'fecha_movimiento_inicio', 'fecha_movimiento_fin',\
                   'date_created_inicio', 'date_created_fin',\
                   'no_folio', 'origen', 'destino', \
                   'creador', 'exporta_xls', 'exporta']



class ValeAlmacenGeneralForm(ValeForm):

    class Meta: 
        model = ValeAlmacenGeneral
        fields = ['no_folio', 'observaciones_grales',\
                   'tipo_movimiento', 'fecha_vale', 'persona_asociada', 'creador_vale']


class ProductoSearchChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        cadena = "{}".format(obj.nombre)
        for x in obj.numeros_de_parte_format():
            cadena = cadena + " {}".format(x)
        return cadena


class SearchSalidaGeneralForm(ModelForm):

    nombre = ProductoSearchChoiceField(
                required=False,
                label='Producto', 
                queryset=Producto.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    class Meta: 
        model = Producto
        fields = ['nombre']

class UnidadMedidaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} ({}) {}".format(obj.nombre, obj.simbolo, obj.categoria)


class MovimientoSalidaGeneralForm(ModelForm):
    cantidad  = forms.IntegerField(
                required=True,
                min_value=1,
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control mb-2 mr-sm-2',
                'placeholder':'Ejemplo: 2'
                }
    ))
    
    observacion = forms.CharField(
                required=False,
                label='Observacion', 
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control mb-2 mr-sm-2',
                'placeholder':'Ejemplo: se llevan las llantas a renovacion'
                }
    ))
    '''
    origen = OrigenChoiceField(
                required=True,
                queryset=Profile.objects.filter(tipo__nombre="BODEGA"),
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})
    )
    '''

    destino = DestinoChoiceField(
                required=True,
                queryset=Profile.objects.filter(tipo__nombre="ECONOMICO").order_by('user__username'),#NOECONOMICO
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})
    )

    unidad = UnidadMedidaChoiceField(
                required=True,
                queryset=UnidadMedida.objects.all().order_by('nombre'),#NOECONOMICO
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})

    )
    class Meta: 
        model = MovimientoGeneral
        fields = ['cantidad',\
                  'observacion',\
                  'unidad',
                  'destino']



class EntradaGeneralForm(EntradaForm):
    class Meta: 
        model = ValeAlmacenGeneral
        fields = ['no_folio', 'observaciones_grales',\
                   'tipo_movimiento', 'fecha_vale', \
                   'persona_asociada', 'creador_vale',\
                   'con_iva']

class MovimientoEntradaGeneralForm(ModelForm):
    '''
    origen = OrigenChoiceField(
                required=True,
                queryset=Profile.objects.filter(tipo__nombre="BODEGA"),
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})
    )
    '''

    producto = ProductoSearchChoiceField(
                required=True,
                help_text="* Campo Requerido.",
                label='Producto', 
                queryset=Producto.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    unidad = UnidadMedidaChoiceField(
                required=True,
                help_text="* Campo Requerido.",
                queryset=UnidadMedida.objects.all().order_by('nombre'),#NOECONOMICO
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})

    )

    cantidad  = forms.IntegerField(
                required=True,
                help_text="* Campo Requerido.",
                min_value=1,
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control mb-2 mr-sm-2',
                'placeholder':'Ejemplo: 2'
                }
    ))

    precio_unitario  = forms.DecimalField(
                required=True,
                help_text="* Campo Requerido.",
                max_digits=8,
                decimal_places=2,
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control mb-2 mr-sm-2',
                'placeholder':'Ejemplo: 480.5'
                }
    ))

    observacion = forms.CharField(
                required=False,
                label='Observacion', 
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control mb-2 mr-sm-2',
                'placeholder':'Ejemplo: se llevan las llantas a renovacion'
                }
    ))
    '''
    destino = DestinoChoiceField(
                required=True,
                queryset=Profile.objects.filter(tipo__nombre="ECONOMICO").order_by('user__username'),#NOECONOMICO
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})
    )
    '''
    class Meta: 
        model = MovimientoGeneral
        fields = [
                  #'origen',
                  'producto',
                  'unidad',
                  'cantidad',\
                  'precio_unitario',
                  'observacion',\
                  ]

class ExactPositionChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj)


class PositionForm(ModelForm):

    exactposition = ExactPositionChoiceField(
                required=True,
                queryset=ProfilePosition.objects.all().order_by('profile'),#NOECONOMICO
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})

    )


    class Meta:
        model = ProductoExactProfilePosition
        fields = [
                    'exactposition',
                ]
  
class NumeroParteForm(ModelForm):

    numero_de_parte =  forms.CharField(
        label='Numero de parte',
        min_length=2,
        max_length=69,
        required=True,
        help_text="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo, numero de parte que tiene el proveedor: AX11R'
            }
        )
    )



    class Meta:
        model = NumeroParte
        fields = [
                    'numero_de_parte',
                ]