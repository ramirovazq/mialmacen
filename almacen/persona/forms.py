from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from llantas.utils import return_profile

class BodegaForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=30,
        required=True,
        help_text="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: J11'
            }
        )
    )

    def clean_nombre(self):
        username = self.cleaned_data['nombre']
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "Ya existe una bodega con ese nombre: {}".format(username)
            )
        return username

    def save(self):
        nombre = self.cleaned_data['nombre']
        nombre = slugify(nombre)
        nombre = nombre.upper()
        profile = return_profile(nombre, tipo="BODEGA")
        return profile


class EconomicoForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=30,
        required=True,
        help_text="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: J11'
            }
        )
    )

    def clean_nombre(self):
        username = self.cleaned_data['nombre']
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "Ya existe una economico con ese nombre: {}".format(username)
            )
        return username

    def save(self):
        nombre = self.cleaned_data['nombre']
        nombre = slugify(nombre)
        nombre = nombre.upper()
        profile = return_profile(nombre, tipo="ECONOMICO")
        return profile



class ProveedorForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=120,
        required=True,
        help_text="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: Refaccionaria Bojorquez'
            }
        )
    )

    def clean_nombre(self):
        username = self.cleaned_data['nombre']
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "Ya existe una economico con ese nombre: {}".format(username)
            )
        return username

    def save(self):
        nombre = self.cleaned_data['nombre']
        nombre = slugify(nombre)
        nombre = nombre.upper()
        profile = return_profile(nombre, tipo="PROVEEDOR")
        return profile

