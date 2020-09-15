from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import *

class UserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.username)


class CategoriaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj)


class GastoForm(ModelForm):

    user = UserChoiceField(
        required=True,
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class':'form-control m-b', 'disabled': ''})
    )
    concepto = forms.CharField(
        required=True,
        help_text="* Campo Requerido.",
        label='Concepto', 
        max_length="100",
        widget=forms.TextInput(
            attrs={
            'class':'form-control',
            'placeholder':'Ejemplo: café latte grande'
            })
    )
    monto  = forms.DecimalField(
        required=True,
        help_text="* Campo Requerido.",
        max_digits=8,
        decimal_places=2,
        widget=forms.TextInput(
        attrs={ 
        'class':'form-control mb-2 mr-sm-2',
        'placeholder':'Ejemplo: 80.5'
        })
    )
    fecha = forms.DateField(
        required=False,
        label='Fecha ',
        input_formats=["%d-%m-%Y"],
        widget=forms.TextInput(
        attrs={ 
        'class':'form-control',
        'placeholder':'dd-mm-yyyy'
        })
    )
    categoria = CategoriaChoiceField(
        required=True,
        queryset=CategoriaGastos.objects.all().order_by('categoria'),
        widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})
    )
    class Meta: 
        model = Gasto
        fields = [
            'user',
            'concepto',
            'monto',
            'fecha',
            'categoria'
            ]
