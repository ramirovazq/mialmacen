from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.db.models import Q
from .models import *
from persona.models import Profile
from llantas.utils import agrupacion_dots, devuelve_llanta
from llantas.forms import TipoMovimientoChoiceField, OrigenChoiceField, DestinoChoiceField, OrigenDestinoChoiceField, ProfileChoiceField, ValeForm


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
        return "%s" % (obj.nombre)


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
                queryset=Profile.objects.filter(tipo__nombre="ECONOMICO"),#NOECONOMICO
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})
    )

    class Meta: 
        model = MovimientoGeneral
        fields = ['cantidad',\
                  'observacion',\
                  'destino']



