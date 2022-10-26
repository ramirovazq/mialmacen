from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from general.render_to_XLS_util import generate_to_xls_productos
from general.models import Producto
from django.conf import settings
import datetime


EMAIL_SENDER =  'email@email.com'
SUBJECT = "Envio de reporte de almacen"
MESSAGE = "Hola el reporte de almacén viene en la liga siguiente "

class Command(BaseCommand):
    help = 'Send email with almacen report'

    def add_arguments(self, parser):
        parser.add_argument('emails', nargs='+', type=str)

    def handle(self, *args, **options):
        filename_single = "export_inventario_" + datetime.datetime.now().strftime("%Y%m%d%H%M") + ".xls"
        filename = settings.MEDIA_ROOT + filename_single
        self.stdout.write(self.style.SUCCESS('Filename "%s"' % filename))
        # this line generates file
        generate_to_xls_productos(
                queryset=Producto.objects.all(),
                filename=filename
        )
        BASE_URL = "http://127.0.0.1:8000"
        url_file  = BASE_URL + settings.MEDIA_URL + filename_single
        self.stdout.write(self.style.SUCCESS('URL "%s"' % url_file))

        options_emails = options['emails']
        options_emails = options_emails[1:]
        send_mail(SUBJECT, MESSAGE + url_file, EMAIL_SENDER, options_emails, fail_silently=False)
        self.stdout.write(self.style.SUCCESS('Successfully send email to "%s"' % options_emails))