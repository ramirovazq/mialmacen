from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Tipo(models.Model):
    nombre = models.CharField(
            blank=True,
            null = True,
            max_length=70
    )

    def __str__(self):
        return "{}".format(self.nombre)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    tipo = models.ForeignKey(
        Tipo,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="tipo_profile"
    )

    def __str__(self):
        return "{} [{}]".format(self.user, self.tipo)

class Position(models.Model):
    name = models.CharField( #anaquel 1 
            blank=True,
            null = True,
            max_length=70
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        db_index=True,
        related_name="parent_position",
        null=True,
        blank=True
        )

    def __str__(self):
        if self.parent:
            return "{}>>{}".format(self.parent, self.name)
        else:
            return "{}".format(self.name)

    def code(self):
        if self.parent:
            return "{}{}{}".format(self.parent.code(), self.name[0],self.name[-1])
        else:
            return "{}{}".format(self.name[0],self.name[-1])


class ProfilePosition(models.Model):
    profile = models.ForeignKey( # self.bodega01 = return_profile("ALMACEN_GENERAL", "BODEGA")
        Profile,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="profileposition_profile_set",
    )
    position = models.ForeignKey( # nivel_one = Position.objects.create(name="Nivel de Anaquel 1", parent=anaquel_one)
        Position,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="profileposition_position_set",
    )

    def __str__(self):
        return "{} {}".format(self.profile, self.position)

    def in_words(self):
        bodega = "{}>>{}".format(self.profile.user.username, self.position.__str__())
        return bodega

    def in_code(self):
        bodega = "{}{}".format(self.profile.user.username[0], self.position.code())
        return bodega

    
    def producto_exact_profile_positions(self):
        from general.models import ProductoExactProfilePosition
        return ProductoExactProfilePosition.objects.filter(exactposition=self)

    def producto_exact_profile_positions_quantity(self):
        '''
        returns how many things exists in specific exact_position
        important: in exact_position could be more than 1 type of product
        '''
        total_entrada = 0
        total_salida  = 0
        answer = {}

        lista_product_exact_profile_positions = self.producto_exact_profile_positions()
        for x in lista_product_exact_profile_positions:
            if x.movimiento.tipo_movimiento.nombre == 'ENTRADA':
                total_entrada = total_entrada + (x.movimiento.cantidad*x.movimiento.unidad.ratio)
            elif x.movimiento.tipo_movimiento.nombre == 'SALIDA':
                total_salida = total_salida + (x.movimiento.cantidad*x.movimiento.unidad.ratio)
            answer[x.exactposition] = total_entrada - total_salida
        return answer

    def producto_exact_profile_positions_what(self):
        answer = []
        lista_product_exact_profile_positions = self.producto_exact_profile_positions()
        for x in lista_product_exact_profile_positions:
            if x.movimiento.producto.nombre not in answer:
                answer.append(x.movimiento.producto.nombre)
        return answer

    def producto_exact_profile_list_products_with_id(self):
        '''
        Returns list of products names plus id of product, example: ACEITE--234
        id of product helps avoid confusing products with similar names
        '''
        answer = []
        lista_product_exact_profile_positions = self.producto_exact_profile_positions()
        for x in lista_product_exact_profile_positions:
            product_name_with_id = x.movimiento.producto.nombre + "--" +str(x.movimiento.producto.id)
            if product_name_with_id not in answer:
                answer.append(product_name_with_id)
        return answer


    def producto_exact_profile_list_products_with_only_id(self):
        '''
        Returns list of products names plus id of product, example: 234
        id of product helps avoid confusing products with similar names
        '''
        answer = []
        lista_product_exact_profile_positions = self.producto_exact_profile_positions()
        for x in lista_product_exact_profile_positions:
            product_name_with_id = str(x.movimiento.producto.id)
            if product_name_with_id not in answer:
                answer.append(product_name_with_id)
        return answer

    def producto_exact_profile_positions_quantity_by_product_only_id(self):
        products_list = self.producto_exact_profile_list_products_with_only_id()
        dicc_products = { product: 0 for product in products_list }

        lista_product_exact_profile_positions = self.producto_exact_profile_positions()
        for x in lista_product_exact_profile_positions:
            producto = str(x.movimiento.producto.id)
            if x.movimiento.tipo_movimiento.nombre == 'ENTRADA':
                dicc_products[producto] = dicc_products[producto] +  (x.movimiento.cantidad*x.movimiento.unidad.ratio)
            elif x.movimiento.tipo_movimiento.nombre == 'SALIDA':
                dicc_products[producto] = dicc_products[producto] -  (x.movimiento.cantidad*x.movimiento.unidad.ratio)

        return dicc_products


    def producto_exact_profile_positions_quantity_by_product(self):
        products_list = self.producto_exact_profile_list_products_with_id()
        dicc_products = { product: 0 for product in products_list }

        lista_product_exact_profile_positions = self.producto_exact_profile_positions()
        for x in lista_product_exact_profile_positions:
            producto = x.movimiento.producto.nombre + "--" + str(x.movimiento.producto.id)
            if x.movimiento.tipo_movimiento.nombre == 'ENTRADA':
                dicc_products[producto] = dicc_products[producto] +  (x.movimiento.cantidad*x.movimiento.unidad.ratio)
            elif x.movimiento.tipo_movimiento.nombre == 'SALIDA':
                dicc_products[producto] = dicc_products[producto] -  (x.movimiento.cantidad*x.movimiento.unidad.ratio)

        return dicc_products



    def productos_csv(self):
        return ";".join(self.producto_exact_profile_positions_what())