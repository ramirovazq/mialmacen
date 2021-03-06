from django.db import models
from persona.models import Profile
import decimal

class Marca(models.Model): 
    nombre = models.CharField( # AmerSteel, Dunlop, Michellin, etc
            blank=True,
            null = True,
            max_length=100,
            unique=True
    )

    def __str__(self):
        return "{} {}".format(self.id, self.nombre)

class Medida(models.Model): 
    nombre = models.CharField( # 11R225, 11R245, 15R225
            blank=True,
            null = True,
            max_length=100,
            unique=True
    )

    class Meta:
        verbose_name_plural = "medidas"

    def __str__(self):
        return "{} {}".format(self.id, self.nombre)


class Posicion(models.Model): 
    nombre = models.CharField( # T.P, Tracción
            blank=True,
            null = True,
            max_length=100,
            unique=True
    )

    class Meta:
        verbose_name_plural = "posiciones"

    def __str__(self):
        return "{} {}".format(self.id, self.nombre)


class Status(models.Model): 
    nombre = models.CharField( # Nueva, Renovada, Rodar
            blank=True,
            null = True,
            max_length=100,
            unique=True
    )

    class Meta:
        verbose_name_plural = "status"

    def __str__(self):
        return "{}".format(self.nombre)


class TipoMovimiento(models.Model): # catálogo de tipos de movimiento, ENTRADA, SALIDA
    nombre = models.CharField(
            blank=True,
            null = True,
            max_length=100,
            unique=True
    )

    class Meta:
        verbose_name_plural = "tipo de movimientos"

    def __str__(self):
        return "{}".format(self.nombre)


class Vale(models.Model): # catálogo de tipos de movimiento, ENTRADA, SALIDA
    no_folio = models.CharField( # Una referencia externa del movimiento
            blank=True,
            null = True,
            max_length=100
    )

    observaciones_grales = models.TextField(
        blank=True,
        null=True
    )

    tipo_movimiento = models.ForeignKey( #entrada o salida
        TipoMovimiento,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)

    fecha_vale = models.DateField()
    fecha_created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created
    fecha_edited = models.DateTimeField(auto_now=True) # Automatically set the field when the object is edited

    persona_asociada = models.ForeignKey( ## quien entrega para vale salida, o Proveedor para un Vale de entrada
        Profile,
        blank=True,
        null=True,        
        related_name='persona_asociada',
        on_delete=models.PROTECT,
        db_index=True)

    creador_vale = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='creador_vale',
        on_delete=models.PROTECT,
        db_index=True)

    con_iva = models.BooleanField(default=True)

    vale_llantas = models.BooleanField(default=True)

    def movimientos(self):
        return Movimiento.objects.filter(vale=self)

    def total(self):
        return sum([m.precio_total() for m in Movimiento.objects.filter(vale=self)])


    class Meta:
        verbose_name_plural = "Vales"

    VALE_FOLIO_INIT = "1"

    @staticmethod
    def siguiente_folio(tipo_movimiento_id=2): # 2 default salida
        vales = Vale.objects.filter(tipo_movimiento__id=tipo_movimiento_id).order_by('-id')
        if len(vales) > 0:
            for vale in vales:
                try:
                    next_folio = "{}".format(int(vale.no_folio) + 1)
                    return next_folio
                except TypeError:
                    pass
                except ValueError:
                    pass
            ultima = vales[0]
            return "{}-ID".format(int(ultima.id) + 1)
        else:
            return Vale.VALE_FOLIO_INIT


    def __str__(self):
        return "id {}, {}".format(self.id, self.no_folio)

class ValeBasura(models.Model): # catálogo de tipos de movimiento, ENTRADA, SALIDA
    vale_asociado = models.ForeignKey( #puede estar asociado a un vale de salida, por ejemplo
        Vale,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)

    observaciones_grales = models.TextField(
        blank=True,
        null=True
    )

    tipo_movimiento = models.ForeignKey( #entrada o salida, normalmente solo entrada
        TipoMovimiento,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)

    fecha_vale = models.DateField()
    fecha_created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created
    fecha_edited = models.DateTimeField(auto_now=True) # Automatically set the field when the object is edited

    persona_asociada = models.ForeignKey( ## aqui debe venir el origen, que debe ser un tractor o caja
        Profile,
        blank=True,
        null=True,        
        related_name='tractor_asociado_basura',
        on_delete=models.PROTECT,
        db_index=True)

    creador_vale = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='creador_vale_basura',
        on_delete=models.PROTECT,
        db_index=True)

    vale_llantas = models.BooleanField(default=True)

    def movimientos(self):
        return MovimientoBasura.objects.filter(vale=self)

    class Meta:
        verbose_name_plural = "Vales de Basura"

    def __str__(self):
        return "{}".format(self.id)


class AdjuntoVale(models.Model):
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
    vale = models.ForeignKey(
        Vale,
        related_name='vale_del_adjunto',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True)
    fecha_created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created
    fecha_edited = models.DateTimeField(auto_now=True) # Automatically set the field when the object is edited


    def __str__(self):
        return "{} {}".format(self.id, self.vale)

class LlantaBasura(models.Model):
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        db_index=True)
    medida = models.ForeignKey(
        Medida,
        on_delete=models.PROTECT,
        db_index=True)
    posicion = models.ForeignKey(
        Posicion,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True)
    dot = models.CharField( # Una referencia externa del movimiento
            blank=True,
            null = True,
            max_length=100)
    porciento_vida = models.PositiveSmallIntegerField( # Un porcentaje de vida de la llanta por ejemplot 30%
            blank=True,
            null = True,
            default=100)

    class Meta:
        verbose_name_plural = "llantas basura"

    def __str__(self):
        return "{}".format(self.id)
        #return "{} {} {} {} {} {} {}".format(self.id, self.marca.nombre, self.medida.nombre, self.posicion.nombre, self.status.nombre, self.dot, self.porciento_vida)



class Llanta(models.Model):
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        db_index=True)
    medida = models.ForeignKey(
        Medida,
        on_delete=models.PROTECT,
        db_index=True)
    posicion = models.ForeignKey(
        Posicion,
        on_delete=models.PROTECT,
        db_index=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        db_index=True)
    dot = models.CharField( # Una referencia externa del movimiento
            blank=True,
            null = True,
            max_length=100)
    porciento_vida = models.PositiveSmallIntegerField( # Un porcentaje de vida de la llanta por ejemplot 30%
            blank=True,
            null = True,
            default=100)

    def __str__(self):
        return "{} {} {} {} {} {} {}".format(self.id, self.marca.nombre, self.medida.nombre, self.posicion.nombre, self.status.nombre, self.dot, self.porciento_vida)
        #return "{}".format(self.id)


    def movimientos_entrada(self):
        return Movimiento.objects.filter(\
            tipo_movimiento__nombre="ENTRADA",
            llanta=self)

    def movimientos_salida(self):
        return Movimiento.objects.filter(\
            tipo_movimiento__nombre="SALIDA",
            llanta=self)


    def cantidad_actual_total(self):
        lista_cantidades_entrada = [ m.cantidad for m in Movimiento.objects.filter(\
            tipo_movimiento__nombre="ENTRADA",
            llanta=self)]
        lista_cantidades_salida = [ m.cantidad for m in Movimiento.objects.filter(\
            tipo_movimiento__nombre="SALIDA",
            llanta=self)]

        entradas = sum(lista_cantidades_entrada)
        salidas = sum(lista_cantidades_salida)

        return entradas - salidas

    def ubicaciones(self):
        return Profile.objects.filter(id__in = self.movimientos_entrada().values_list('destino')) ## todos los lugares en los que estan el tipo de llanta

    def permisionarios(self):
        return Profile.objects.filter(id__in = self.movimientos_entrada().values_list('permisionario')) ## todos los lugares en los que estan el tipo de llanta


    def total_ubicaciones(self):
        localizaciones = {}
        lugares = self.ubicaciones()
        for lugar in lugares:
            localizaciones[lugar.user.username] = 0
            e = sum([m.cantidad for m in self.movimientos_entrada().filter(destino=lugar)])
            s = sum([m.cantidad for m in self.movimientos_salida().filter(origen=lugar)])
            localizaciones[lugar.user.username] = e - s
        return localizaciones


    def total_ubicaciones_detail(self):
        localizaciones = {}
        lugares = self.ubicaciones()
        permisionarios = self.permisionarios()
        
        for bodega in lugares:
            diccionario = {}
            for permisionario in permisionarios:
                e = sum([m.cantidad for m in self.movimientos_entrada().filter(destino=bodega, permisionario=permisionario)])
                s = sum([m.cantidad for m in self.movimientos_salida().filter(origen=bodega, permisionario=permisionario)])
                if (e - s) > 0 :
                    diccionario[permisionario.user.username] = e - s

            e = sum([m.cantidad for m in self.movimientos_entrada().filter(destino=bodega, permisionario__isnull=True)])
            s = sum([m.cantidad for m in self.movimientos_salida().filter(origen=bodega, permisionario__isnull=True)])
            diccionario['sin_permisionario'] = e - s


            #diccionario['sin_permisionario'] = total - total_permisionarios
            localizaciones[bodega.user.username] = diccionario
        return localizaciones


    def total_ubicaciones_detail_endpoint(self):
        localizaciones = {}
        lugares = self.ubicaciones()
        permisionarios = self.permisionarios()
        
        lista_interna = []
        for bodega in lugares:
            for permisionario in permisionarios:
                e = sum([m.cantidad for m in self.movimientos_entrada().filter(destino=bodega, permisionario=permisionario)])
                s = sum([m.cantidad for m in self.movimientos_salida().filter(origen=bodega, permisionario=permisionario)])
                diccionario = {}
                if (e - s) > 0 :
                    diccionario['bodega_id'] = bodega.id
                    diccionario['bodega'] = bodega.user.username
                    diccionario['permisionario'] = permisionario.user.username
                    diccionario['permisionario_id'] = permisionario.id
                    diccionario['cantidad'] = e - s 
                    diccionario['id'] = "{}-{}".format(bodega.user.id, permisionario.user.id)

                    #diccionario[bodega.user.username+"--"+permisionario.user.username] = e - s
                    lista_interna.append(diccionario)

            e = sum([m.cantidad for m in self.movimientos_entrada().filter(destino=bodega, permisionario__isnull=True)])
            s = sum([m.cantidad for m in self.movimientos_salida().filter(origen=bodega, permisionario__isnull=True)])
            diccionario_dos = {}
            diccionario_dos['bodega'] = bodega.user.username
            diccionario_dos['bodega_id'] = bodega.id
            diccionario_dos['permisionario'] = "sin_permisionario"
            diccionario_dos['permisionario_id'] = ""
            diccionario_dos['cantidad'] = e - s   
            diccionario_dos['id'] = "{}-{}".format(bodega.user.id, "sinperm")
            lista_interna.append(diccionario_dos)


            #diccionario['sin_permisionario'] = total - total_permisionarios
            localizaciones[bodega.user.username] = lista_interna
        return lista_interna

class MovimientoBasura(models.Model):
    vale = models.ForeignKey(
        ValeBasura,
        related_name='vale_asociado_basura',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True)
    tipo_movimiento = models.ForeignKey( #entrada o salida
        TipoMovimiento,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)
    fecha_movimiento = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created
    date_edited = models.DateTimeField(auto_now=True) # Automatically set the field when the object is edited
    origen = models.ForeignKey(
        Profile,
        related_name='origen_del_movimiento_basura',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True)
    destino = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='destino_del_movimiento_basura',
        on_delete=models.PROTECT,
        db_index=True)

    llanta = models.ForeignKey(
        LlantaBasura,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)
    cantidad = models.PositiveIntegerField(
            default=0)

    creador = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='creadror_del_movimiento_basura',
        on_delete=models.PROTECT,
        db_index=True)

    observacion = models.TextField(
        blank=True,
        null=True
    )

    permisionario = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='permisionario_llanta_basura',
        on_delete=models.PROTECT)


    def __str__(self):
        return "{}".format(self.id)



class Movimiento(models.Model):
    vale = models.ForeignKey(
        Vale,
        related_name='vale_asociado',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True)
    tipo_movimiento = models.ForeignKey( #entrada o salida
        TipoMovimiento,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)
    fecha_movimiento = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created
    date_edited = models.DateTimeField(auto_now=True) # Automatically set the field when the object is edited
    origen = models.ForeignKey(
        Profile,
        related_name='origen_del_movimiento',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True)
    destino = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='destino_del_movimiento',
        on_delete=models.PROTECT,
        db_index=True)

    llanta = models.ForeignKey(
        Llanta,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)
    cantidad = models.PositiveIntegerField(
            default=0)
    precio_unitario = models.DecimalField(
        max_digits=8,   
        decimal_places=2,
        default=0)

    creador = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='creadror_del_movimiento',
        on_delete=models.PROTECT,
        db_index=True)

    observacion = models.TextField(
        blank=True,
        null=True
    )

    permisionario = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='permisionario_llanta',
        on_delete=models.PROTECT)


    def precio_total(self):
        if self.vale.con_iva:
            return (self.cantidad * self.precio_unitario) + ((self.cantidad * self.precio_unitario) * decimal.Decimal(0.16))        
        return self.cantidad * self.precio_unitario

    def sku(self):
        return "{}{}{}".format(self.llanta.marca,self.llanta.medida, self.llanta.posicion)

    def __str__(self):
        return "{}".format(self.id)

    @staticmethod
    def entradas(dot=""):
        tme = TipoMovimiento.objects.get(nombre="ENTRADA")
        if dot:
            return Movimiento.objects.filter(tipo_movimiento=tme, dot=dot)
        else:
            return Movimiento.objects.filter(tipo_movimiento=tme)

    @staticmethod
    def salidas(dot=""):
        tms = TipoMovimiento.objects.get(nombre="SALIDA")
        if dot:
            return Movimiento.objects.filter(tipo_movimiento=tme, dot=dot)
        else:
            return Movimiento.objects.filter(tipo_movimiento=tms)

    @classmethod
    def give_unique(self, query_movimiento, orden='marca'): 
        '''
        devuelve un diccionario y un set  
        el diccionario tiene la llave de la huella de la llanta (huella es marca__medida__posicion__dot)
        y como valor, la cantidad de llantas
        el set del diccionario
        '''
        dicc = {}
        for m in query_movimiento:
            if orden == 'marca':
                llanta_name = "{}__{}__{}__{}__{}".format(m.marca.nombre, m.medida.nombre, m.posicion.nombre, m.dot, m.status.nombre)
            elif orden == 'medida':
                llanta_name = "{}__{}__{}__{}__{}".format(m.medida.nombre, m.posicion.nombre, m.dot, m.status.nombre, m.marca.nombre)
            elif orden == 'posicion':
                llanta_name = "{}__{}__{}__{}__{}".format(m.posicion.nombre, m.dot, m.status.nombre, m.marca.nombre, m.medida.nombre)
            elif orden == 'dot':
                llanta_name = "{}__{}__{}__{}__{}".format(m.dot, m.status.nombre, m.marca.nombre, m.medida.nombre, m.posicion.nombre)
            elif orden == 'status':
                llanta_name = "{}__{}__{}__{}__{}".format(m.status.nombre, m.marca.nombre, m.medida.nombre, m.posicion.nombre, m.dot)
            else:
                llanta_name = "{}__{}__{}__{}__{}".format(m.marca.nombre, m.medida.nombre, m.posicion.nombre, m.dot, m.status.nombre)


            if llanta_name not in dicc.keys():
                dicc[llanta_name] = m.cantidad
            else:
                dicc[llanta_name] = dicc[llanta_name] + m.cantidad        
        #lista = sorted(dicc.items(), key=lambda x: x[1]) 
        #lista.reverse()
        unique = set(dicc)
        return dicc, unique

    @classmethod
    def actual_inventory(self, orden='marca', dot=""):
        if dot:
            dicc_entradas, unique_entradas = self.give_unique(self.entradas(dot), orden)
            dicc_salidas, unique_salidas   = self.give_unique(self.salidas(dot), orden)
        else:
            dicc_entradas, unique_entradas = self.give_unique(self.entradas(), orden)
            dicc_salidas, unique_salidas   = self.give_unique(self.salidas(), orden)
        actual = {}

        # set operation
        salidas_sin_entradas = unique_salidas.difference(unique_entradas)        

        for huella in dicc_entradas.keys():
            actual[huella] = 0
            try:
                num_actual_entrada = dicc_entradas[huella]                
            except KeyError:
                num_actual_entrada = 0
                #print("doesnt find huella in dictionary ENTRADA")                
            try:
                num_actual_salida = dicc_salidas[huella]
            except KeyError:
                num_actual_salida = 0
                #print("doesnt find huella in dictionary SALIDA")

            actual[huella] = num_actual_entrada - num_actual_salida

        lista = actual.items()
        #lista = sorted(actual.items(), key=lambda x: x[1]) 
        #lista.reverse()
        return actual, lista, salidas_sin_entradas


class ImportacionMovimientos(models.Model):
    upload = models.FileField(upload_to='importacion/')
    fecha_created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created
    fecha_edited = models.DateTimeField(auto_now=True) # Automatically set the field when the object is edited
    procesado = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)

    def ultimo(self):
        ultimo = ImportacionMovimientos.objects.none()
        todos = ImportacionMovimientos.objects.all().order_by('-fecha_created') 
        if len(todos) > 0:
            ultimo = todos[0]
        return ultimo

    class Meta:
        verbose_name_plural = "importacion de movimientos"
