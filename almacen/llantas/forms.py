from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.db.models import Q
from .models import Movimiento, TipoMovimiento, Marca, Medida, Posicion, Status, Vale, Llanta, ImportacionMovimientos, AdjuntoVale
from persona.models import Profile
from .utils import agrupacion_dots, devuelve_llanta

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

class ProfileChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} {} [{}]".format(obj.user.first_name, obj.user.last_name, obj.user.username)

class LlantaMedidaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.nombre)#, obj.medida.nombre, obj.posicion.nombre, obj.status.nombre)

class LlantaMarcaSearchChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.nombre)#, obj.medida.nombre, obj.posicion.nombre, obj.status.nombre)

class LlantaPosicionSearchChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.nombre)#, obj.medida.nombre, obj.posicion.nombre, obj.status.nombre)

class PermisionarioChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj)


class ProfileSearchForm(forms.Form):

    profile = PermisionarioChoiceField(
                required=False,
                queryset=Profile.objects.filter(tipo__nombre="PERMISIONARIO"),#( Q(tipo__nombre="BODEGA") | Q(tipo__nombre="ECONOMICO")),#NOECONOMICO
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})
    )

class SearchSalidaForm(ModelForm):

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

    marca = LlantaMarcaSearchChoiceField(
                required=False,
                label='Marca', 
                queryset=Marca.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    medida = LlantaMedidaChoiceField(
                required=False,
                label='Medida', 
                queryset=Medida.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    posicion = LlantaPosicionSearchChoiceField(
                required=False,
                label='Posición',
                queryset=Posicion.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    status = LlantaMarcaSearchChoiceField(
                required=False,
                label='Status',
                queryset=Status.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )


    class Meta: 
        model = Llanta
        fields = ['dot', 'marca', 'medida', 'posicion', 'status']

class LlantaMarcaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.marca.nombre)#, obj.medida.nombre, obj.posicion.nombre, obj.status.nombre)

class SearchLlantabyMarcaForm(ModelForm):    
    llanta = LlantaMarcaChoiceField(
                required=False,
                queryset=Llanta.objects.all().order_by('marca__nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )    

    class Meta: 
        model = Movimiento
        fields = ['llanta']

class MarcaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.nombre)#, obj.medida.nombre, obj.posicion.nombre, obj.status.nombre)

class DestinoBodegaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj)


class NewLlantaForm(forms.Form):    

    marca = MarcaChoiceField(
                required=True,
                help_text="* Campo Requerido.",
                queryset=Marca.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    medida = MarcaChoiceField(
                required=True,
                help_text="* Campo Requerido.",
                queryset=Medida.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    posicion = MarcaChoiceField(
                required=True,
                help_text="* Campo Requerido.",
                queryset=Posicion.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    status = MarcaChoiceField(
                required=True,
                help_text="* Campo Requerido.",
                queryset=Status.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    dot = forms.CharField(
            required=True,
            label='Dot', 
            max_length="100",
            help_text="* Campo Requerido. Nota: cuando se agregan Dots separados por ',' la cantidad enviada en el formulario ya no es tomada en cuenta (se calcula por la cantidad de dots)",
            widget=forms.TextInput(
                attrs={
                'class':'form-control',
                'placeholder':'Un solo dot, ejemplo: 1234 ; mas de un DOT, separado por "," ejemplo: 4512,7845,8963'
                }
    ))

    destino = DestinoBodegaChoiceField(
                required=True,
                help_text="* Campo Requerido.",
                queryset=Profile.objects.filter(tipo__nombre="BODEGA"),#( Q(tipo__nombre="BODEGA") | Q(tipo__nombre="ECONOMICO")),#NOECONOMICO
                widget=forms.Select(attrs={'class':'form-control mb-2 mr-sm-2'})
    )

    permisionario = PermisionarioChoiceField(
                required=False,
                queryset=Profile.objects.filter(tipo__nombre="PERMISIONARIO"),#( Q(tipo__nombre="BODEGA") | Q(tipo__nombre="ECONOMICO")),#NOECONOMICO
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
    
    precio_unitario  = forms.FloatField(
                required=True,
                help_text="* Campo Requerido.",
                min_value=0,
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

    def save(self, obj): # obj is Vale
        marca = self.cleaned_data['marca']
        medida = self.cleaned_data['medida']
        posicion = self.cleaned_data['posicion']
        status = self.cleaned_data['status']
        dot = self.cleaned_data['dot']

        dot_list = [x.strip() for x in dot.split(",")] 
        cantidad_enviada = False
        if len(dot_list) <= 1:
            cantidad_enviada = True
        dot_diccionario = agrupacion_dots(dot_list) # de la forma {'3218': 2, '3628': 1, '3618': 2}

        destino = self.cleaned_data['destino']
        cantidad_form = self.cleaned_data['cantidad']
        precio_unitario = self.cleaned_data['precio_unitario']
        observacion = self.cleaned_data['observacion']        
        permisionario = self.cleaned_data['permisionario']

        dicc_movimiento = {
            "vale": obj,
            "tipo_movimiento":obj.tipo_movimiento,
            "fecha_movimiento": obj.fecha_vale, 
            "origen":obj.persona_asociada,
            "destino":destino,
            "precio_unitario":precio_unitario,
            "creador":obj.creador_vale,
            "observacion":observacion,
        }
        if permisionario:
            dicc_movimiento["permisionario"] = permisionario

        l_movimiento = []
        l_already_exist = []

        for dot, cantidad in dot_diccionario.items():
            llanta, ya_existia = devuelve_llanta(marca, medida, posicion, status, dot)
            l_already_exist.append(ya_existia)
            dicc_movimiento['llanta'] = llanta

            if cantidad_enviada: # se usa la cantidad enviada en el formulario cuando solo se envia un DOT
                dicc_movimiento['cantidad'] = cantidad_form
                movimiento = Movimiento(**dicc_movimiento)    
            else:
                dicc_movimiento['cantidad'] = cantidad
                movimiento = Movimiento(**dicc_movimiento)
            movimiento.save()
            l_movimiento.append(movimiento)
        return l_already_exist, l_movimiento



    '''
    def clean(self):
        super().clean()
        # validacion de almenos un grupo seleccionado
        a = self.cleaned_data['administrador']
        #b = self.cleaned_data['analista']
        c = self.cleaned_data['aplicador']
        if a or c:
            pass
        else:
            raise ValidationError(
                "Selecciona almenos un grupo para el nuevo usuario"
            )

        # valida que el email editado no exista para otro usuario de la
        # plataforma
        profile_id = self.cleaned_data['profile_id']
        email = self.cleaned_data['email']
        p = Profile.objects.get(id=profile_id)
        q_users = User.objects.filter(email=email)
        for user in q_users:
            if user.id == p.user.id:  # es decir, es el usuario que se esta editando
                pass
            else:
                raise ValidationError(
                    "Ya existe un usuario con el correo enviado."
                )
    '''


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

class OrigenChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj)

class DestinoChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj)


class MovimientoSalidaForm(ModelForm):
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
        model = Movimiento
        fields = ['cantidad',\
                  'observacion',\
                  'destino']





class ValeForm(ModelForm):
    no_folio = forms.CharField(
            required=True,
            label='No Folio', 
            max_length="100",
            widget=forms.TextInput(
                attrs={
                'class':'form-control',
                'placeholder':'Ejemplo: 05'
                }
    ))

    persona_asociada = ProfileChoiceField(
                required=True,
                queryset=Profile.objects.filter(tipo__nombre="STAFF").order_by('user__first_name'),
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    fecha_vale = forms.DateField(
                required=True,
                label='Fecha vale', 
                input_formats=["%d-%m-%Y"],
                widget=forms.DateInput(
                    format="%d-%m-%Y",
                    attrs={ 
                    'class':'form-control',
                    'placeholder':'dd-mm-yyyy'
                    }
    ))


    observaciones_grales = forms.CharField(
                required=False,
                label='Observaciones grales', 
                widget=forms.Textarea(
                attrs={ 
                'class':'form-control',
                'placeholder':'Ejemplo: se llevan las llantas a renovacion'
                }
    ))

    tipo_movimiento = TipoMovimientoChoiceField(
                required=True,
                queryset=TipoMovimiento.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b', 'disabled': ''})
    )

    creador_vale = ProfileChoiceField(
                required=True,
                queryset=Profile.objects.filter(tipo__nombre="STAFF"),
                widget=forms.Select(attrs={'class':'form-control m-b', 'disabled': ''})
    )


    class Meta: 
        model = Vale
        fields = ['no_folio', 'observaciones_grales',\
                   'tipo_movimiento', 'fecha_vale', 'persona_asociada', 'creador_vale']

class ProveedorChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.user.username)


class EntradaForm(ModelForm):
    no_folio = forms.CharField(
            required=True,
            label='No Folio', 
            max_length="100",
            widget=forms.TextInput(
                attrs={
                'class':'form-control',
                'placeholder':'Ejemplo: 05'
                }
    ))

    persona_asociada = ProveedorChoiceField( ## es el proveedor para la entrada
                required=True,
                queryset=Profile.objects.filter(Q(tipo__nombre="PROVEEDOR") | Q(tipo__nombre="ABSTRACT")).order_by('user__username'),#( Q(tipo__nombre="BODEGA") | Q(tipo__nombre="ECONOMICO")),#NOECONOMICO
                widget=forms.Select(attrs={'class':'form-control m-b'})
    )

    fecha_vale = forms.DateField(
                required=True,
                label='Fecha de factura', 
                input_formats=["%d-%m-%Y"],
                widget=forms.DateInput(
                    format="%d-%m-%Y",
                    attrs={ 
                    'class':'form-control',
                    'placeholder':'dd-mm-yyyy'
                    }
                ))

    observaciones_grales = forms.CharField(
                required=False,
                label='Observaciones grales', 
                widget=forms.Textarea(
                attrs={ 
                'class':'form-control',
                'placeholder':'Ejemplo: se llevan las llantas a renovacion'
                }
    ))

    tipo_movimiento = TipoMovimientoChoiceField(
                required=True,
                queryset=TipoMovimiento.objects.all().order_by('nombre'),
                widget=forms.Select(attrs={'class':'form-control m-b', 'disabled': ''})
    )

    creador_vale = ProfileChoiceField(
                required=True,
                queryset=Profile.objects.filter(tipo__nombre="STAFF"),
                widget=forms.Select(attrs={'class':'form-control m-b', 'disabled': ''})
    )


    class Meta: 
        model = Vale
        fields = ['no_folio', 'observaciones_grales',\
                   'tipo_movimiento', 'fecha_vale', \
                   'persona_asociada', 'creador_vale',\
                   'con_iva']

class ImportacioMovimientosForm(ModelForm):

    class Meta: 
        model = ImportacionMovimientos
        fields = ['upload']


class AdjuntoValeForm(ModelForm):

    class Meta: 
        model = AdjuntoVale
        fields = ['upload', 'vale']
