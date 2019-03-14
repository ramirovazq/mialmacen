from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import Movimiento, TipoMovimiento, Marca, Medida, Posicion, Status

class FilterForm(forms.Form):

    picking = forms.CharField(
                required=False,
            label='Picking', 
            max_length="100",
            widget=forms.TextInput(
                attrs={
                'class':'form-control',
                'placeholder':'Ejemplo: WH/IN/0000X'
                }
    ))
    producto = forms.CharField(
                required=False,
                label='Producto', 
                max_length="250",
                widget=forms.TextInput(
                    attrs={
                    'class':'form-control',
                    'placeholder':'Ejemplo: Filtro'
                    }
    ))
    compania = forms.CharField(
                required=False,
                label='Compañía o Tractor', 
                max_length="250",
               widget=forms.TextInput(
                   attrs={
                   'class':'form-control',
                   'placeholder':'Ejemplo: T23'
                   }
    ))
    propietario = forms.CharField(
                required=False,
                label='Propietario', 
                max_length="190",
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'Ejemplo: Mecánico'
                }
    ))
    detalle = forms.CharField(
                required=False,
                label='Detalle', 
                max_length="190",
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'Ejemplo: Thermos'
                }
    ))

    fecha_creacion_inicio = forms.DateField(
                required=False,
                label='Fecha creacion inicio', 
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
                }
    ))
    fecha_creacion_fin = forms.DateField(
                required=False,
                label='Fecha creacion fin',
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
                }
    ))

    ultima_actualizacion_inicio = forms.DateField(
                required=False,
                label='Última actualización inicio',
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
                }
    ))
    ultima_actualizacion_fin = forms.DateField(
                required=False,
                label='Última actualización fin',
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
                }
    ))
    fecha_programada_inicio = forms.DateField(
                required=False,
                label='Fecha programada inicio',
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
                }
    ))

    fecha_programada_fin = forms.DateField(
                required=False,
                label='Fecha programada fin',
                input_formats=["%d-%m-%Y"],
                widget=forms.TextInput(
                attrs={ 
                'class':'form-control',
                'placeholder':'dd-mm-yyyy'
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

class TipoMovimientoChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.nombre)

class OrigenDestinoChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.nombre)


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

    marca = forms.ModelChoiceField(
                required=False,
                queryset=Marca.objects.all()
    )

    medida = forms.ModelChoiceField(
                required=False,
                queryset=Medida.objects.all()
    )

    posicion = forms.ModelChoiceField(
                required=False,
                queryset=Posicion.objects.all()
    )

    status = forms.ModelChoiceField(
                required=False,
                queryset=Status.objects.all()
    )

    dot = forms.CharField(
            required=False,
            label='Dot', 
            max_length="100",
            widget=forms.TextInput(
                attrs={
                'class':'form-control',
                'placeholder':'Ejemplo: 1234'
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
        model = Movimiento
        fields = ['tipo_movimiento', 'fecha_movimiento_inicio', 'fecha_movimiento_fin',\
                   'date_created_inicio', 'date_created_fin',\
                   'no_folio', 'origen', 'destino', 'marca', 'medida', \
                   'posicion', 'status', 'dot', 'creador', 'exporta_xls', 'exporta']