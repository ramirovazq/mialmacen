from django.template import Variable, defaultfilters
from django.http import HttpResponse
from django.conf import settings
from llantas.models import Llanta

from datetime import datetime as datetime_datetime
from datetime import date as datetime_date

import csv
import xlwt
import datetime
from pytz import timezone

def render_to_xls(queryset, filename):

    ezxf = xlwt.easyxf
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("movimientos")

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    row_num = 0

    columns = [
            'Id',
            'Tipo de movimiento',
            'Fecha de movimiento',
            'Fecha de creación',
            'Fecha de edición',
            'No folio', 
            'Origen',
            'Destino',
            'Marca', 
            'Medida', 
            'Posicion', 
            'Cantidad',
            'Status',
            'Dot',
            'Precio unitario',
            'Creador'
            ]

    for col_num in range(len(columns)):
        sheet.write(row_num, col_num, columns[col_num], font_style)

    rows = queryset.values_list('id', 'tipo_movimiento__nombre', 'fecha_movimiento','date_created', 'date_edited', \
                'vale__no_folio', 'origen__user__username', 'destino__user__username', 'llanta__marca__nombre', 'llanta__medida__nombre', 'llanta__posicion__nombre', 'cantidad',\
                'llanta__status__nombre', 'llanta__dot', 'precio_unitario', 'creador__user__username'
        )

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime_datetime):
                fecha_row = row[col_num].astimezone(timezone(settings.TIME_ZONE)).strftime("%d-%m-%Y %H:%M")
                sheet.write(row_num, col_num, fecha_row)    
            elif isinstance(row[col_num], datetime_date):
                fecha_row = row[col_num].strftime("%d-%m-%Y")#.astimezone(timezone(settings.TIME_ZONE)).strftime("%d-%m-%Y %H:%M")
                sheet.write(row_num, col_num, fecha_row)    
            else:                
                sheet.write(row_num, col_num, row[col_num])
        
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    book.save(response)
    return response


def render_to_csv(queryset, filename):

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    writer = csv.writer(response, delimiter=";")
    writer.writerow([
            'Id',
            'SKU',
            'Tipo de movimiento',
            'Fecha de movimiento',
            'Fecha de creación',
            'Fecha de edición',
            'No folio', 
            'Origen',
            'Destino',
            'Marca', 
            'Medida', 
            'Posicion', 
            'Cantidad',
            'Status',
            'Dot',
            'Precio unitario',
            'Creador'
            ]
)
    for movimiento in queryset:
          renglon = []
          renglon.append(movimiento.id)
          renglon.append(movimiento.sku())
          renglon.append(movimiento.tipo_movimiento) 

          if movimiento.fecha_movimiento:
            renglon.append(movimiento.fecha_movimiento.strftime("%d-%m-%Y")) 
          else:
            renglon.append('sin fecha movimiento') 
          renglon.append(movimiento.date_created.astimezone(timezone(settings.TIME_ZONE)).strftime("%d-%m-%Y %H:%M"))
          renglon.append(movimiento.date_edited.astimezone(timezone(settings.TIME_ZONE)).strftime("%d-%m-%Y %H:%M"))
          renglon.append(movimiento.vale.no_folio)
          renglon.append(movimiento.origen.user.username)
          renglon.append(movimiento.destino.user.username)
          renglon.append(movimiento.llanta.marca.nombre)
          renglon.append(movimiento.llanta.medida.nombre)
          renglon.append(movimiento.llanta.posicion.nombre)
          renglon.append(movimiento.cantidad)
          renglon.append(movimiento.llanta.status)
          renglon.append(movimiento.llanta.dot)
          renglon.append(movimiento.precio_unitario)
          renglon.append(movimiento.creador.user.username)
          writer.writerow(renglon)
    return response    




def render_to_xls_inventario(queryset, filename):

    ezxf = xlwt.easyxf
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("movimientos")

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    row_num = 0

    columns = [
            'Id',
                  'Marca',
                  'Medida',
                  'Posición',
                  'Dot',
                  'Status',
                  'Cantidad',
                  'Ubicación',
                  'Permisionarios',
            ]

    for col_num in range(len(columns)):
        sheet.write(row_num, col_num, columns[col_num], font_style)

    '''
<td>{{llanta.marca.nombre}} </td>
                    <td>{{llanta.medida.nombre}} </td>
                    <td>{{llanta.posicion.nombre}} </td>
                    <td>{{llanta.dot}} </td>
                    <td>{{llanta.status.nombre}} </td>
                    <td>{{llanta.cantidad_actual_total}} </td>
                    <td>{% for ubicacion, cantidad in llanta.total_ubicaciones.items %} [ bodega: {{ubicacion}} ; cantidad {{cantidad}}]{% endfor %}</td>
                    <td>{{ llanta.total_ubicaciones_detail  }}</td>
    '''

    rows = queryset.values_list('id', 
        'marca__nombre',
        'medida__nombre',
        'posicion__nombre',
        'dot',
        'status__nombre',
        )

    new_rows = []
    for row in rows:
        llanta = Llanta.objects.get(id=row[0])
        for ubicacion in llanta.total_ubicaciones():
            uyc = ("ubicacion: "+ ubicacion, "  cantidad: {}".format(llanta.total_ubicaciones()[ubicacion]))

        for ubicacion in llanta.total_ubicaciones_detail():
            cadena = "ubicacion: "+ ubicacion
            cadena = cadena + "  {}".format(llanta.total_ubicaciones_detail()[ubicacion])

        new_rows.append(row + (llanta.cantidad_actual_total(), uyc, cadena))

    for row in new_rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime_datetime):
                fecha_row = row[col_num].astimezone(timezone(settings.TIME_ZONE)).strftime("%d-%m-%Y %H:%M")
                sheet.write(row_num, col_num, fecha_row)    
            elif isinstance(row[col_num], datetime_date):
                fecha_row = row[col_num].strftime("%d-%m-%Y")#.astimezone(timezone(settings.TIME_ZONE)).strftime("%d-%m-%Y %H:%M")
                sheet.write(row_num, col_num, fecha_row)    
            else:                
                sheet.write(row_num, col_num, row[col_num])
        
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    book.save(response)
    return response
